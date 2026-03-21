# bands_auto_site

## 


### Create Python Environment

```bash
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
