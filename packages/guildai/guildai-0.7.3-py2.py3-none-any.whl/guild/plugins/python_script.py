# Copyright 2017-2021 TensorHub, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division

import hashlib
import json
import logging
import os
import subprocess
import sys

import six
from six.moves import shlex_quote

import yaml

from guild import cli
from guild import config
from guild import entry_point_util
from guild import guildfile
from guild import model as modellib
from guild import op_util
from guild import plugin as pluginlib
from guild import python_util
from guild import util
from guild import var
from guild import yaml_util

from . import flags_import_util

IMPLICIT_ALL_FLAGS = object()


_flag_importers = entry_point_util.EntryPointResources(
    "guild.python.flags", "Python flag importer"
)


class DataLoadError(Exception):
    pass


class PythonScriptOpdefSupport(object):
    """Interface for Python script opdef support.

    `python_script_opdef_loaded` is called to potentially update
    opdef.
    """

    def python_script_opdef_loaded(self, opdef):
        """Called by Python plugin when an opdef is loaded.

        Gives implementor an opportunity to modify the opdef.
        """
        pass


class PythonFlagsImporter(object):
    """Interface for Python flags importer."""

    def __init__(self, ep):
        self.ep = ep

    def flags_for_script(self, script, log):
        """Returns Guild flag config for a Python script."""
        pass


class PythonScriptModelProxy(object):

    name = ""
    fullname = ""
    output_scalars = None
    objective = "loss"
    plugins = []

    def __init__(self, script_path, op_name):
        assert script_path[-3:] == ".py", script_path
        assert script_path.endswith(op_name), (script_path, op_name)
        self.script_path = script_path
        if os.path.isabs(op_name) or op_name.startswith(".."):
            self.op_name = os.path.basename(op_name)
        else:
            self.op_name = op_name
        script_base = script_path[: -len(self.op_name)]
        self.modeldef = self._init_modeldef()
        self.reference = modellib.script_model_ref(self.name, script_base)

    def _init_modeldef(self):
        flags_data = self._flags_data()
        flags_dest = flags_data.pop("$dest", None)
        data = [
            {
                "model": self.name,
                "operations": {
                    self.op_name: {
                        "exec": self._exec_attr(),
                        "flags": flags_data,
                        "flags-dest": flags_dest,
                        "output-scalars": self.output_scalars,
                        "objective": self.objective,
                        "plugins": self.plugins,
                        "sourcecode": self._sourcecode(),
                    }
                },
            }
        ]
        gf = guildfile.Guildfile(data, dir=os.path.dirname(self.script_path))
        return gf.models[self.name]

    def _exec_attr(self):
        return "${python_exe} -um guild.op_main %s ${flag_args}" % shlex_quote(
            self._script_module()
        )

    def _script_module(self):
        return python_util.script_module(self.script_path, config.cwd())

    def _flags_data(self):
        flags_import_util.log_flags_info(
            "### Script flags for %s", os.path.normpath(self.script_path)
        )
        plugin = pluginlib.for_name("python_script")
        return plugin._flags_data_for_path(self.script_path, "", ".")

    @staticmethod
    def _sourcecode():
        return None


class PythonScriptPlugin(pluginlib.Plugin):

    resolve_model_op_priority = 60

    def resolve_model_op(self, opspec):
        path = os.path.join(config.cwd(), opspec)
        if python_util.is_python_script(path):
            model = PythonScriptModelProxy(path, opspec)
            return model, model.op_name
        return None

    def guildfile_loaded(self, gf):
        local_cache = {}
        for m in gf.models.values():
            for opdef in m.operations:
                self._maybe_apply_main(opdef)
                if not opdef.main or _is_explicit_guild_plugin(opdef.main):
                    continue
                self._apply_script_flags(opdef, local_cache)
                self._notify_plugins_python_script_opdef_loaded(opdef)

    @staticmethod
    def _maybe_apply_main(op):
        if not (op.main is not None or op.exec_ is not None or op.steps is not None):
            op.main = python_util.safe_module_name(op.name)

    def _apply_script_flags(self, opdef, local_cache):
        flags_import_util.apply_flags(
            opdef,
            lambda: self._flags_data(opdef, local_cache),
            lambda flags_data: self._apply_flags_dest(flags_data, opdef),
        )

    def _flags_data(self, opdef, local_cache):
        main_mod = op_util.split_cmd(opdef.main)[0]
        flags_dest = opdef.flags_dest
        try:
            flags_data = local_cache[(main_mod, flags_dest)]
        except KeyError:
            flags_import_util.log_flags_info("reading flags for main spec %r", main_mod)
            model_paths = op_util.opdef_model_paths(opdef)
            flags_data = self._flags_data_(main_mod, model_paths, opdef.flags_dest)
        else:
            flags_import_util.log_flags_info(
                "using cached flags for main spec %r", main_mod
            )
        return flags_data

    def _flags_data_(self, main_mod, model_paths, flags_dest):
        try:
            sys_path, mod_path = python_util.find_module(main_mod, model_paths)
        except ImportError as e:
            if os.getenv("NO_WARN_FLAGS_IMPORT") != "1":
                self.log.warning("cannot import flags from %s: %s", main_mod, e)
            return {}
        else:
            package = self._main_spec_package(main_mod)
            return self._flags_data_for_path(mod_path, package, sys_path, flags_dest)

    @staticmethod
    def _main_spec_package(main_spec):
        parts = main_spec.rsplit("/", 1)
        return python_util.split_mod_name(parts[-1])[0]

    def _flags_data_for_path(self, mod_path, mod_package, sys_path, flags_dest=None):
        data, cached_data_path = self._cached_data(mod_path)
        if data is not None:
            return data
        return self._load_and_cache_flags_data(
            mod_path, mod_package, sys_path, flags_dest, cached_data_path
        )

    def _cached_data(self, mod_path):
        cached_path = self._cached_data_path(mod_path)
        if self._cache_valid(cached_path, mod_path):
            with open(cached_path, "r") as f:
                # Use yaml to avoid json's insistence on treating
                # strings as unicode.
                return yaml.safe_load(f), cached_path
        return None, cached_path

    @staticmethod
    def _cached_data_path(mod_path):
        cache_dir = var.cache_dir("import-flags")
        abs_path = os.path.abspath(mod_path)
        path_hash = hashlib.md5(abs_path.encode()).hexdigest()
        return os.path.join(cache_dir, path_hash)

    @staticmethod
    def _cache_valid(cache_path, mod_path):
        if os.getenv("NO_IMPORT_FLAGS_CACHE") == "1" or not os.path.exists(cache_path):
            return False
        return os.path.getmtime(mod_path) <= os.path.getmtime(cache_path)

    def _load_and_cache_flags_data(
        self, mod_path, mod_package, sys_path, flags_dest, cached_data_path
    ):
        if (
            os.getenv("NO_IMPORT_FLAGS_PROGRESS") != "1"
            and os.getenv("FLAGS_TEST") != "1"
            and not os.getenv("_GUILD_COMPLETE")
        ):
            cli.note_once("Refreshing flags...")
        try:
            script = python_util.Script(mod_path, mod_package, sys_path)
        except SyntaxError as e:
            if os.getenv("NO_WARN_FLAGS_IMPORT") != "1":
                self.log.warning(
                    "cannot import flags from %s: invalid syntax on line %i\n"
                    "  %s\n"
                    "  %s^",
                    mod_path,
                    e.lineno,
                    e.text.rstrip(),
                    " " * (e.offset - 1),
                )
            return {}
        else:
            try:
                data = self._flags_data_for_script(script, flags_dest)
            except DataLoadError:
                return {}
            else:
                self._apply_abs_paths(data, os.path.dirname(script.src))
                self._cache_data(data, cached_data_path)
                return data

    @staticmethod
    def _cache_data(data, path):
        util.ensure_dir(os.path.dirname(path))
        with open(path, "w") as f:
            json.dump(data, f)

    def _flags_data_for_script(self, script, flags_dest):
        flags_dest = flags_dest or self._script_flags_dest(script)
        if flags_dest == "args":
            data = self._argparse_flags_data(script)
        elif flags_dest == "globals":
            data = self._global_assigns_flags_data(script)
        elif flags_dest.startswith("global:"):
            data = self._global_param_flags_data(script, flags_dest[7:])
        elif flags_dest.startswith("args:"):
            data = self._entry_point_args_flags_data(flags_dest, script)
        else:
            self.log.debug(
                "ingoring flags dest '%s' for Python script %s", flags_dest, script
            )
            data = {}
        if flags_dest:
            flags_import_util.log_flags_info(
                "%s flags imported for dest %r:\n%s",
                (_script_desc, script),
                flags_dest,
                (_assigns_flag_data_desc, data),
            )
        data["$dest"] = flags_dest
        return data

    def _script_flags_dest(self, script):
        if self._imports_argparse(script):
            flags_import_util.log_flags_info(
                "%s imports argparse - assuming args", (_script_desc, script)
            )
            return "args"
        else:
            flags_import_util.log_flags_info(
                "%s does not import argparse - assuming globals", (_script_desc, script)
            )
            return "globals"

    @staticmethod
    def _imports_argparse(script):
        return "argparse" in script.imports

    def _argparse_flags_data(self, script):
        env = dict(os.environ)
        env.update(
            {
                "PYTHONPATH": os.path.pathsep.join([script.sys_path or ''] + sys.path),
                "LOG_LEVEL": str(self.log.getEffectiveLevel()),
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )
        with util.TempFile() as tmp:
            cmd = [
                sys.executable,
                "-m",
                "guild.plugins.import_argparse_flags_main",
                script.src,
                script.mod_package or '',
                tmp.path,
            ]
            self.log.debug("import_argparse_flags_main env: %s", env)
            self.log.debug("import_argparse_flags_main cmd: %s", cmd)
            try:
                out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, env=env)
            except subprocess.CalledProcessError as e:
                error, details = _split_argparse_flags_error(e.output.decode().strip())
                if details and self.log.getEffectiveLevel() > logging.DEBUG:
                    error += " (run with guild --debug for details)"
                if os.getenv("NO_WARN_FLAGS_IMPORT") != "1":
                    self.log.warning(
                        "cannot import flags from %s: %s", script.src, error
                    )
                if details and self.log.getEffectiveLevel() <= logging.DEBUG:
                    self.log.error(details)
                raise DataLoadError()
            else:
                out = out.decode()
                self.log.debug("import_argparse_flags_main output: %s", out)
                _log_warnings(out, self.log)
                return _load_data(tmp.path)

    def _global_assigns_flags_data(self, script):
        params = script.params
        return {
            str(name): flags_import_util.flag_data_for_val(val)
            for name, val in params.items()
            if self._is_global_assign_flag(name) and self._is_assignable_flag_val(val)
        }

    @staticmethod
    def _is_global_assign_flag(name):
        return name[:1] != "_"

    @staticmethod
    def _is_assignable_flag_val(val):
        # Don't support dict value assignments as flags.
        return not isinstance(val, dict)

    def _global_param_flags_data(self, script, param_name):
        param_val = script.params.get(param_name)
        if not isinstance(param_val, dict):
            self.log.warning(
                "cannot import flags for param '%s' in '%s': param must be a dict",
                param_name,
                _script_desc(script),
            )
            return {}
        config_vals = util.encode_nested_config(param_val)
        return {
            str(name): flags_import_util.flag_data_for_val(val)
            for name, val in config_vals.items()
            if self._is_global_assign_flag(name) and self._is_assignable_flag_val(val)
        }

    def _entry_point_args_flags_data(self, flags_dest, script):
        assert flags_dest.startswith("args:")
        ep_name = flags_dest[5:]
        try:
            importer = _flag_importers.one_for_name(ep_name)
        except LookupError:
            self.log.warning(
                "cannot find flag import support for flag-dest %r - unable "
                "to import flags",
                ep_name,
            )
            return {}
        else:
            return importer.flags_for_script(script, self.log)

    @staticmethod
    def _apply_abs_paths(data, script_dir):
        for flag_data in data.values():
            if not isinstance(flag_data, dict):
                continue
            default = flag_data.get("default")
            if (
                not default
                or not isinstance(default, six.string_types)
                or os.path.sep not in default
            ):
                continue
            abs_path = os.path.join(script_dir, default)
            if os.path.exists(abs_path):
                flag_data["default"] = abs_path

    @staticmethod
    def _apply_flags_dest(flags_data, opdef):
        """Applies '$dest' in flags_data to opdef.

        The process of applying always removes '$dest' from
        flags_data if it exists.

        The process of applying will never modify a non-None value of
        opdef.flags_dest.
        """
        try:
            flags_dest = flags_data.pop("$dest")
        except KeyError:
            pass
        else:
            if opdef.flags_dest is None:
                opdef.flags_dest = flags_dest

    @staticmethod
    def _notify_plugins_python_script_opdef_loaded(opdef):
        for _name, plugin in pluginlib.iter_plugins():
            if isinstance(plugin, PythonScriptOpdefSupport):
                plugin.python_script_opdef_loaded(opdef)


def _is_explicit_guild_plugin(main_spec):
    """Returns true if main_spec specifies a Guild plugin.

    Used to avoid performing implicit logic on top of another
    plugin that's explicitly defined in main.
    """
    return main_spec.rstrip().startswith("guild.plugins.")


def _log_warnings(out, log):
    for line in out.split("\n"):
        if line.startswith("WARNING:"):
            log.warning(line[9:])


def _script_desc(script):
    return os.path.relpath(script.src)


def _assigns_flag_data_desc(data, indent=2):
    desc = yaml_util.encode_yaml(data)
    return _indent(desc, indent)


def _indent(s, indent):
    lines = s.split("\n")
    prefix = " " * indent
    return "\n".join([prefix + line for line in lines])


def _load_data(path):
    out = open(path, "r").read().strip()
    if not out:
        return {}
    return yaml.safe_load(out)


def _split_argparse_flags_error(e_str):
    if "Traceback" in e_str:
        lines = e_str.split("\n")
        return lines[-1], _strip_debug_tag(e_str)
    else:
        return e_str, None


def _strip_debug_tag(s):
    if s.startswith("DEBUG: "):
        return s[7:]
    return s
