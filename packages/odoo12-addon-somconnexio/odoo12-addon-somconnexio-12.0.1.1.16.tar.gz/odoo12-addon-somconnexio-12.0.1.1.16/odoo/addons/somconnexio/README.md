[![codecov](https://codecov.io/gl/coopdevs/odoo-somconnexio/branch/master/graph/badge.svg?token=ZfxYjFpQBz)](https://codecov.io/gl/coopdevs/odoo-somconnexio)
[![License: AGPL-3](https://img.shields.io/badge/licence-AGPL--3-blue.png)](http://www.gnu.org/licenses/agpl-3.0-standalone.html)
[![Beta](https://img.shields.io/badge/maturity-Beta-yellow.png)](https://odoo-community.org/page/development-status)

This project provides an ERP system for [Som Connexio](https://somosconexion.coop/) telecommunication users cooperative.

### Installation

This package requires Odoo v12.0 installed.

You can install this module using `pip`:

```sh
$ pip install odoo12-addon-somconnexio
```

More info in: https://pypi.org/project/odoo12-addon-somconnexio/

### DEVELOPMENT

#### Create development enviornment

Create the `devenv` container with the `somconnexio` module mounted and provision it. Follow the [instructions](https://gitlab.com/coopdevs/odoo-somconnexio-inventory#requirements) in [odoo-somconnexio-inventory](https://gitlab.com/coopdevs/odoo-somconnexio-inventory).

Once created, we can stop or start our `odoo-sc` lxc container as indicated here:
```sh
$ sudo systemctl start lxc@odoo-sc
$ sudo systemctl stop lxc@odoo-sc
```

To check our local lxc containers and their status, run:
```sh
$ sudo lxc-ls -f
```

#### Start the ODOO application

Enter to your local machine as the user `odoo`, activate the python enviornment first and run the odoo bin:
```sh
$ ssh odoo@odoo-sc.local
$ pyenv activate odoo
$ cd /opt/odoo
$ set -a && source /etc/default/odoo && set +a
$ ./odoo-bin -c /etc/odoo/odoo.conf -u somconnexio -d odoo
```

To use the local somconnexio module (development version) instead of the PyPI published one, you need to upgrade the [version in the manifest](https://gitlab.com/coopdevs/odoo-somconnexio/-/blob/master/somconnexio/__manifest__.py#L3) and then update the module with `-u` in the Odoo CLI.


#### Restart ODOO database from scratch

Enter to your local machine as the user `odoo`, activate the python enviornment first, drop the DB, and run the odoo bin to create it again:
```sh
$ ssh odoo@odoo-sc.local
$ pyenv activate odoo
$ dropdb odoo
$ cd /opt/odoo
$ ./odoo-bin -c /etc/odoo/odoo.conf -i somconnexio -d odoo --stop-after-init
```

#### Deploy branch

For tests purposes, we might want to deploy a given branch (`BRANCH`) into a server (staging), instead of publishing a new package release just to test some fix or new feature.

To do so, we need to enter into the server with an authorized user (<USER>), and then switch to `odoo` user to install with pip the package version found in the git branch.

```sh
$ ssh <USER>@staging-odoo.somconnexio.coop
$ sudo su - odoo
$ cd /opt/odoo
$ pyenv activate odoo
$ pip install -e git+https://gitlab.com/coopdevs/odoo-somconnexio@<BRANCH>#egg=odoo12-addon-somconnexio\&subdirectory=setup/somconnexio
```

At this point we need to restart Odoo to load the new installed module version.

```
$ sudo systemctl stop odoo
$ ./odoo-bin -c /etc/odoo/odoo.conf -u somconnexio -d odoo --stop-after-init
$ sudo systemctl start odoo
```

To restart the odoo service it is better to stop it, execute odoo with the upgrade (`-u`) option and start it again, rather that just `restart` it, in case there are changes in views within the deployed branch.

#### Run tests

You can run the tests with this command:
```sh
$ ./odoo-bin -c /etc/odoo/odoo.conf -u somconnexio -d odoo --stop-after-init --test-enable --workers 0
```

The company data is rewritten every module upgrade

#### Update CHANGELOG without running pipeline

If you need to update the CHANGELOG but you don't need to wait for the pipeline to end, you can put `[skip ci]` in your commit message and the pipeline will be skiped.
More info in https://docs.gitlab.com/ee/ci/yaml/#skip-pipeline

Credits
=======

###### Authors

* Coopdevs Treball SCCL

###### Contributors

* Coopdevs Treball SCCL
