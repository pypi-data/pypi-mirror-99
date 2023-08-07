# Remote hello

These tests run various hello operations remotely.

    >>> cd(example("hello-package-2"))

## `hello`

    >>> run("guild run hello -r guild-uat -y")
    Building package
    ...
    Installing package and its dependencies
    Processing ./gpkg.hello-0.1-py2.py3-none-any.whl
    Installing collected packages: gpkg.hello
    Successfully installed gpkg.hello-0.1
    Starting hello on guild-uat as ...
    Hello Guild!
    Run ... stopped with a status of 'completed'
    <exit 0>

## `hello-file`

    >>> run("guild run hello-file -r guild-uat -y")
    Building package
    ...
    Installing package and its dependencies
    Processing ./gpkg.hello-0.1-py2.py3-none-any.whl
    Installing collected packages: gpkg.hello
    Successfully installed gpkg.hello-0.1
    Starting hello-file on guild-uat as ...
    Resolving packaged-files dependency
    Reading message from hello.txt
    Hello, from a file!
    <BLANKLINE>
    Saving message to msg.out
    Run ... stopped with a status of 'completed'
    <exit 0>

## `hello-op`

    >>> run("guild run hello-op -r guild-uat -y")
    Getting run info on guild-uat
    Building package
    ...
    Installing package and its dependencies
    Processing ./gpkg.hello-0.1-py2.py3-none-any.whl
    Installing collected packages: gpkg.hello
    Successfully installed gpkg.hello-0.1
    Starting hello-op on guild-uat as ...
    Resolving op dependency
    Using run ... for op resource
    Reading message from msg.out
    Hello, from a file!
    <BLANKLINE>
    Run ... stopped with a status of 'completed'
    <exit 0>
