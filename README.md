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

## Setup/Configure Environment

When working between branches, or pulling updates from git, the language environments will need to be updated per branch. Not all of the following commands will need to be run when development is on going. Just need to update the packages for `python` and `npm`.

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

TODO: Fix packages so that there is `core` and `dev`

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
# Init project with defaults (creates package.json)
npm init -y
```

```bash
# Install all dependencies from package.json
npm install

# or

npm ci  # Clean install (faster, uses package-lock.json)
```

```bash
# Install/Uninstall specific package
npm install <package>           # Install a package (adds to dependencies)
npm install <package> --save-dev  # Install as dev dependency
npm install -g <package>        # Install globally
npm uninstall <package>         # Remove a package
```

```bash
# Typically builds for production
npm run build                   
```
---

<br>

### Uvicorn - Server gateway

```bash
# Install dependencies
pip install fastapi uvicorn
```
```bash
# Run directly from the terminal (simplest way)
uvicorn main:app
# or Enable auto-reload
uvicorn main:app --reload
```
```bash
# Run on a specific port
uvicorn main:app --reload --port 8080
```
```bash
# Run on all network interfaces (accessible on your local network)
uvicorn main:app --host 0.0.0.0 --port 8080
```