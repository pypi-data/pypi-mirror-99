# mls-model-registry (sktmls)

## Contents

- [Description](#description)
- [How to use](#how-to-use)
- [Development](#development)
  - [Requirements for development](#requirements-for-development)
  - [Local model registry](#local-model-registry)
  - [Python environment](#python-environment)
  - [Documents generation](#documents-generation)
- [Version](#version)

## Description

A Python package for MLS model registry.

This python package includes
- Customized prediction pipelines inheriting MLSModel
- Model uploader to AWS S3 for meta management and online prediction

## Installation

Installation is automatically done by training containers in YE. If you want to install manually for local machines,

```bash
# develop
pip install --index-url https://test.pypi.org/simple/ --no-deps sktmls

# production
pip install sktmls
```

## How to use

- MLS Docs: https://ab.sktmls.com/docs/model-registry
- sktmls Docs: https://sktaiflow.github.io/mls-sdk/sktmls

## Development

### Requirements for development
- Python 3.6
- requirements.txt
- requirements-dev.txt

### Local model registry

To enable all model related features in local environment, you need to create a directory `models` in your home directory.

```bash
$ cd ~/
$ mkdir models
```

### Python environment

First you need to do the followings

```bash
$ python -V # Check if the version is 3.6.
$ python -m venv env # Create a virtualenv.
$ . env/bin/activate # Activate the env.
$ pip install "numpy>=1.19.4,<1.20" # Install numpy to avoid a requirement error.
$ pip install -r requirements.txt # Install required packages.
$ pip install -r requirements-dev.txt # Install required dev packages.
```

### Documents generation

Before a commit, generate documents if any docstring has been changed

```bash
rm -rf docs
pdoc --html --config show_source_code=False -f -o ./docs sktmls
```

### Version
`sktmls` package version is automatically genereated followd by a production release on format `YY.MM.DD`  
We use [Calendar Versioning](https://calver.org). For version available, see the [tags on this repository](https://github.com/sktaiflow/mls-model-registry/releases).  
