![GitHub license](https://img.shields.io/github/license/jupyter-naas/drivers)
![Bump version](https://github.com/jupyter-naas/naas/workflows/Bump%20version/badge.svg)
![Upload Python Package](https://github.com/jupyter-naas/naas/workflows/Upload%20Python%20Package/badge.svg)
![codecov](https://codecov.io/gh/jupyter-naas/naas/branch/main/graph/badge.svg?token=UC3SAL8S0U)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=jupyter-naas_naas&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=jupyter-naas_naas)
<a href="#badge">
  <img alt="semantic-release" src="https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg">
</a>
<a href="http://commitizen.github.io/cz-cli/"><img alt="Commitizen friendly" src="https://img.shields.io/badge/commitizen-friendly-brightgreen.svg"></a>
![PyPI](https://img.shields.io/pypi/v/naas)

# Naas (Notebooks As Automated Services)

Schedule notebooks, to automate all your tasks.

Use the power of scripting in the cloud.
Whenever you need it (even when you sleep).

* Schedule your scripts
* Use Notebooks as API
* Share assets securely
* Send emails

# Documentation 

<p>
  <a href="https://naas.gitbook.io/naas/" title="Redirect to Documentation">
    <img width="200px" src="https://raw.githubusercontent.com/jupyter-naas/naas/main/images/gitbook.svg" alt="Gitbooks naas" />
  </a>
 </p>

# Issue

If you found a bug or need a new feature go there :
https://naas.canny.io/

## Try Naas
Using Binder
You can try out some of Naas features using the My Binder service.

Click on a link below to try Naas, on a sandbox environment, without having to install anything.
Test it in binder (WIP)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jupyter-naas/naas/main)

## Install

`pip3 install naas`

### Install with drivers

`pip3 install 'naas[full]'`

---

# DEVELOPMENT

## Install

it will create and install all dependency in docker machine

`./install.sh`

## Test local server

`./install.sh -ro`
it will run your docker machine only.

if you want to rebuild docker too `./install.sh -r`


Then open your browser at the url:
`http://localhost:8888`

enter `test` as password

if you want other password `./install.sh -t=mypassword`

### Api documentation

We have a WIP documentation in swagger.

`http://127.0.0.1:5000/swagger/`

### Livereload 

If you do change in naas code, the server will live reload.

If you use naas in a notebook restart the kernel to get the changes.

### isolated Manager
open manager outsite of jupyter context :

`http://localhost:5000/naas`

## Run test 

run it in the shell of jupyter
`pytest -x`  

## Check lint

`python -m black naas` format better
`python -m flake8 naas` check if any left error

## Publish

You can commit from jupyter or from your local IDE, code of Naas is sync between docker machine and your computer

this auto publish by github action on main branch

# Supporters: 
<p>
  <a href="http://sentry.com" title="Redirect to Sentry">
    <img width="200px" src="https://raw.githubusercontent.com/jupyter-naas/naas/main/images/sentry.svg" alt="Sentry" />
  </a>
  <a href="https://gitbook.com" title="Redirect to Gitbook">
    <img width="200px" src="https://raw.githubusercontent.com/jupyter-naas/naas/main/images/gitbook.svg" alt="Gitbooks" />
  </a>
  <a href="https://canny.io" title="Redirect to Canny">
    <img width="200px" src="https://raw.githubusercontent.com/jupyter-naas/naas/main/images/canny.svg" alt="Canny" />
  </a>
</p>

### Authors:
* [Martin donadieu](https://github.com/riderx)
