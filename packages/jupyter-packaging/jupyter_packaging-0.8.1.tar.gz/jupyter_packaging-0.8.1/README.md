# Jupyter Packaging

Tools to help build and install Jupyter Python packages that require a pre-build step that may include JavaScript build steps.

## Install

`pip install jupyter-packaging`

## Usage

There are three ways to use `jupyter-packaging` in another package.

### As a Build Requirement

Use a `pyproject.toml` file as outlined in [pep-518](https://www.python.org/dev/peps/pep-0518/).
An example:

```toml
[build-system]
requires = ["jupyter_packaging~=0.8.0"]
build-backend = "setuptools.build_meta"
```

Below is an example `setup.py` using the above config.
It assumes the rest of your metadata is in [`setup.cfg`](https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html).
We wrap the import in a try/catch to allow the file to be run without `jupyter_packaging`
so that `python setup.py` can be run directly when not building.

```py
from setuptools import setup

try:
    from jupyter_packaging import wrap_installers, npm_builder
    builder = npm_builder()
    cmdclass = wrap_installers(pre_develop=builder, pre_dist=builder)
except ImportError:
    cmdclass = {}

setup(cmdclass=cmdclass))
```

### As a Build Backend

Use the `jupyter_packaging` build backend.
The pre-build command is specified as metadata in `pyproject.toml`:

```toml
[build-system]
requires = ["jupyter_packaging~=0.8.0"]
build-backend = "jupyter_packaging.build_api"

[tool.jupyter-packaging.builder]
func = "jupyter_packaging.npm_builder"

[tool.jupyter-packaging.build-args]
build_cmd = "build:src"
```

The corresponding `setup.py` would be greatly simplified:

```py
from setuptools import setup
setup()
```

The `tool.jupyter-packaging.builder` section expects a `func` value that points to an importable
module and a function with dot separators.  If not given, no pre-build function will run.

The optional `tool.jupyter-packaging.build-args` sections accepts a dict of keyword arguments to
give to the pre-build command.

The build backend does not handle the `develop` command (`pip install -e .`).
If desired, you can wrap just that command:

```py
import setuptools

try:
    from jupyter_packaging import wrap_installers, npm_builder
    builder = npm_builder(build_cmd="build:dev")
    cmdclass = wrap_installers(pre_develop=builder)
except ImportError:
    cmdclass = {}

setup(cmdclass=cmdclass))
```

### As a Vendored File

Vendor `setupbase.py` locally alongside `setup.py` and import the module directly.

```py
import setuptools
from setupbase import wrap_installers, npm_builder
builder = npm_builder
cmdclass = wrap_installers(post_develop=builder, pre_dist=builder)
setup(cmdclass=cmdclass)
```

## Usage Notes

- We recommend using `include_package_data=True` and `MANIFEST.in` to control the assets included in the [package](https://setuptools.readthedocs.io/en/latest/userguide/datafiles.html).
- Tools like [`check-manifest`](https://github.com/mgedmin/check-manifest) or [`manifix`](https://github.com/vidartf/manifix) can be used to ensure the desired assets are included.
- Simple uses of `data_files` can be handled in `setup.cfg` or in `setup.py`.  If recursive directories are needed use `get_data_files()` from this package.
- Unfortunately `data_files` are not supported in `develop` mode (a limitation of `setuptools`).  You can work around it by doing a full install (`pip install .`) before the develop install (`pip install -e .`), or by adding a script to push the data files to `sys.base_prefix`.


## Development Install

```bash
git clone https://github.com/jupyter/jupyter-packaging.git
cd jupyter-packaging
pip install -e .
```

You can test changes locally by creating a `pyproject.toml` with the following, replacing the local path to the git checkout:

```toml
[build-system]
requires = ["jupyter_packaging@file://<path-to-git-checkout>"]
build-backend = "setuptools.build_meta"
```

Note: you need to run `pip cache remove jupyter_packaging` any time changes are made to prevent `pip` from using a cached version of the source.
