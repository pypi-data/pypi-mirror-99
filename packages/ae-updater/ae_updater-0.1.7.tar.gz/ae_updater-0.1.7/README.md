<!--
  THIS FILE IS EXCLUSIVELY MAINTAINED IN THE NAMESPACE ROOT PACKAGE. CHANGES HAVE TO BE DONE THERE.
  All changes will be deployed automatically to all the portions of this namespace package.
-->
# updater portion of ae namespace package

[![GitLabPipeline](https://img.shields.io/gitlab/pipeline/ae-group/ae_updater/master?logo=python)](
    https://gitlab.com/ae-group/ae_updater)
[![PyPIVersion](https://img.shields.io/pypi/v/ae_updater)](
    https://pypi.org/project/ae-updater/#history)

>The portions (modules and sub-packages) of the Application Environment for Python are within
the `ae` namespace and are providing helper methods and classes for to develop
full-featured applications with Python.

[![Coverage](https://ae-group.gitlab.io/ae_updater/coverage.svg)](
    https://ae-group.gitlab.io/ae_updater/coverage/ae_updater_py.html)
[![MyPyPrecision](https://ae-group.gitlab.io/ae_updater/mypy.svg)](
    https://ae-group.gitlab.io/ae_updater/lineprecision.txt)
[![PyLintScore](https://ae-group.gitlab.io/ae_updater/pylint.svg)](
    https://ae-group.gitlab.io/ae_updater/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/ae_updater)](
    https://pypi.org/project/ae-updater/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/ae_updater)](
    https://pypi.org/project/ae-updater/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/ae_updater)](
    https://pypi.org/project/ae-updater/)
[![PyPIFormat](https://img.shields.io/pypi/format/ae_updater)](
    https://pypi.org/project/ae-updater/)
[![PyPIStatus](https://img.shields.io/pypi/status/ae_updater)](
    https://libraries.io/pypi/ae-updater)
[![PyPIDownloads](https://img.shields.io/pypi/dm/ae_updater)](
    https://pypi.org/project/ae-updater/#files)


## installation


Execute the following command for to use the ae.updater module in your
application. It will install ae.updater into your python (virtual) environment:
 
```shell script
pip install ae-updater
```

If you instead want to contribute to this portion then first fork
[the ae_updater repository at GitLab](https://gitlab.com/ae-group/ae_updater "ae.updater code repository"),
then pull it to your machine and finally execute the following command in the root folder
of this repository (ae_updater):

```shell script
pip install -e .[dev]
```

The last command will install this module portion into your virtual environment, along with
the tools you need to develop and run tests or for to extend the portion documentation.
For to contribute only to the unit tests or the documentation of this portion replace
the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## namespace portion documentation

More info on the features and usage of this portion are available at
[ReadTheDocs](https://ae.readthedocs.io/en/latest/_autosummary/ae.updater.html#module-ae.updater
"ae_updater documentation").

<!-- Common files version 0.0.60 deployed version 0.1.2 (with 0.0.60)
     to https://gitlab.com/ae-group as ae_updater module as well as
     to https://ae-group.gitlab.io with CI check results as well as
     to https://pypi.org/project/ae-updater as namespace portion ae-updater.
-->
