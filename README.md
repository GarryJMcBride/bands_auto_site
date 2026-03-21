# bands_auto_site

## Documentation

See `/docs`

<br>

## Prerequisites

### Node.js

You must have [Node.js](https://nodejs.org/) installed.

Check if Node and npm are available:

```bash
node -v
npm -v
```

If not installed, download from: https://nodejs.org/

---

<br>

## Setup Environment

### Python

```bash
# create Python Environment
python -m venv .venv
```

```bash
# activate .venv - Linux Terminal
source .venv/Scripts/activate # windows
source .venv/bin/activate # linux
```

```bash
# install 'uv' package manager into env
pip install uv
```

```bash
# initialize `uv`
uv init
```

```bash
# add packages with `uv`
uv add <package_name>
```

```bash
# install newly added packages from `uv.lock`
uv sync
```

# TODO: Fix packages so that there is `core` and `dev

```bash
# install only Core packages
uv add --dev <package_name>

uv sync --dev

# sync all development packages
uv sync --no-dev
```

### JavaScript

Install JavaScript Dependicies from `package.json`

```bash
npm init -y                     # Init project with defaults (creates package.json)
npm install                     # Install all dependencies from package.json
```
---

<br>