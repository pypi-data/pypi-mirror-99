dev-env
=======

|Maintained| |MIT license| |PythonVersions| |status| |PyPI|
|Requirements| |CodeFactor| |CircleCI| |codecov|
|docker-simonsdave/bionic-dev-env|

This repo was originally created as a way to centralize and document the
process of provisioning development environments (dev env). As time went
on it became clear that it would be helpful to centralize other common
development tools and utilities. This repo now contains tools, scripts
and utilities which:

-  provision dev and CI environments using
   `Docker <https://www.docker.com/>`__ with confidence that both the
   development and CI environments are the same
-  automate cutting releases
-  simplify integration testing

The tools, scripts and utilities in this repo assume the user follows a
pre-defined set of patterns and practices.

Key Concepts
------------

-  a project is hosted in either public or private github repo
-  at the project’s root is a text file called ``cfg4dev`` which
   configures the project’s dev env
-  after git cloning the repo, a developer configures the dev env by
   executing ``source cfg4dev``
-  ``dev-env`` publishes dev env docker images to `Docker
   Hub <https://hub.docker.com/>`__
-  the docker images are docker pulled to a developer’s machine by
   ``cfg4dev``
-  `CircleCI <https://www.circleci.com>`__ can use a ``dev-env`` docker
   image as a `docker
   executor <https://circleci.com/docs/2.0/executor-types/#using-docker>`__
-  `shell and python scripts <bin>`__ are run on a developer’s machine
   to access the dev env packaged in the docker image
-  the scripts are installed on a developer’s machine by ``cfg4dev``
-  at the project’s root is a text file called ``CHANGELOG.md`` which is
   manually curated by developers to record key changes to the project

Assumptions
-----------

-  developers use `macOS <https://www.apple.com/ca/macos/>`__
-  ``dev-env`` targets projects which are shell and Python centric
-  if a project’s repo is called ``abc-def-ghi`` and the project builds
   a Python package, the package is called ``abc_def_ghi`` and the
   source code for the package is in a sub-directory of the project’s
   root directory called ``abc_def_ghi`` - in addition, the
   ``abc_def_ghi`` directory contains a file called ``__init__.py`` that
   contains at least a single line that looks like
   ``__version__ = '1.2.0'`` which declares the Python package version
-  scripts and Dockerfiles to build a project’s development environment
   are in a sub-directory of the project’s root directory called
   ``dev_env``
-  projects use a branching strategy something like

   -  all development is done on the ``master`` branch (optionally using
      `feature
      branches <https://guides.github.com/introduction/flow/>`__)
   -  use `Semantic Versioning <http://semver.org/>`__
   -  for each release a new branch is created from master called
      ``release-<version>``

-  ``CHANGELOG.md`` follows a predefined format / structure

What Next
---------

-  take a look at the `shell and python scripts <bin>`__ to assess
   ``dev-env`` capability
-  `here’s <docs/using.md>`__ a description of how to start using
   ``dev-env``
-  take a look at
   `this <https://github.com/simonsdave/dev-env-testing>`__ github repo
   which illustrates how to use ``dev-env``
-  if you’d like to help contribute to ``dev-env`` see
   `this <docs/contributing.md>`__

References/Inspirations
-----------------------

-  `21 Nov ’18 - How to fully utilise Docker during
   development <https://medium.com/tsftech/how-to-fully-utilise-docker-during-development-42bb3cdc3017>`__
-  `semantic-release - fully automated version management and package
   publishing <https://github.com/semantic-release/semantic-release>`__

.. |Maintained| image:: https://img.shields.io/maintenance/yes/2021.svg?style=flat
.. |MIT license| image:: http://img.shields.io/badge/license-MIT-brightgreen.svg
   :target: http://opensource.org/licenses/MIT
.. |PythonVersions| image:: https://img.shields.io/pypi/pyversions/dev-env.svg?style=flat
.. |status| image:: https://img.shields.io/pypi/status/dev-env.svg?style=flat
.. |PyPI| image:: https://img.shields.io/pypi/v/dev-env.svg?style=flat
   :target: https://pypi.python.org/pypi/dev-env
.. |Requirements| image:: https://requires.io/github/simonsdave/dev-env/requirements.svg?branch=release-0.6.14
   :target: https://requires.io/github/simonsdave/dev-env/requirements/?branch=release-0.6.14
.. |CodeFactor| image:: https://www.codefactor.io/repository/github/simonsdave/dev-env/badge/release-0.6.14
   :target: https://www.codefactor.io/repository/github/simonsdave/dev-env/overview/release-0.6.14
.. |CircleCI| image:: https://circleci.com/gh/simonsdave/dev-env/tree/release-0.6.14.svg?style=shield
   :target: https://circleci.com/gh/simonsdave/dev-env/tree/release-0.6.14
.. |codecov| image:: https://codecov.io/gh/simonsdave/dev-env/branch/release-0.6.14/graph/badge.svg
   :target: https://codecov.io/gh/simonsdave/dev-env/branch/release-0.6.14
.. |docker-simonsdave/bionic-dev-env| image:: https://img.shields.io/badge/docker-simonsdave%2Fbionic--dev--env-blue.svg
   :target: https://hub.docker.com/r/simonsdave/bionic-dev-env/


