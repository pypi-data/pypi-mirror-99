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

import os

from guild import cli
from guild import cmd_impl_support
from guild import config
from guild import guildfile
from guild import model
from guild import util


def main(args):
    cmd_impl_support.init_model_path()
    dirs = models_iter_dirs(args)
    formatted = [_format_model(m) for m in iter_models(dirs)]
    filtered = [m for m in formatted if _filter_model(m, args)]
    cli.table(
        sorted(filtered, key=_model_sort_key),
        cols=["fullname", "description"],
        detail=(["source", "operations", "details"] if args.verbose else []),
    )


def models_iter_dirs(args):
    cwd = config.cwd()
    if not args.installed and guildfile.is_guildfile_dir(cwd):
        return [cwd]
    return []


def iter_models(dirs=None, include_anonymous=False):
    dirs = dirs or []
    abs_dirs = [os.path.abspath(d) for d in dirs]
    for m in model.iter_models():
        if (m.modeldef.name or include_anonymous) and _match_dirs(m, abs_dirs):
            yield m


def _match_dirs(model, abs_dirs):
    if not abs_dirs:
        return True
    return any(
        (
            os.path.abspath(model.modeldef.guildfile.dir) == abs_dir
            for abs_dir in abs_dirs
        )
    )


def _format_model(model):
    modeldef = model.modeldef
    description, details = util.split_description(modeldef.description)
    return {
        "fullname": model.fullname,
        "name": modeldef.name,
        "source": modeldef.guildfile.src,
        "description": description,
        "details": details,
        "operations": ", ".join([op.name for op in modeldef.operations]),
        "_model": model,
    }


def _filter_model(model, args):
    filter_vals = [
        model["fullname"],
        model["description"],
    ]
    return (model["name"][:1] != "_" or args.all) and util.match_filters(
        args.filters, filter_vals
    )


def _model_sort_key(m):
    return (_model_type_key(m), m["fullname"])


def _model_type_key(m):
    if isinstance(m["_model"], model.GuildfileModel):
        return 999
    return 0
