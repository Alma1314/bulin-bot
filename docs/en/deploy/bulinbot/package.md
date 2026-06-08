# Package Manager Deployment (uv)

Use `uv` to install and run NovaBot quickly.

## Before You Start

If `uv` is not installed, install it first by following the official guide:
<https://docs.astral.sh/uv/>

`uv` supports Linux, Windows, and macOS.

## Important Notes

> [!WARNING]
> NovaBot deployed via `uv` **does not support upgrading through the WebUI**. To update, run `uv tool upgrade nova-bot --python 3.12` from the command line.

NovaBot requires Python 3.12 or later. Use `--python 3.12` to ensure that `uv` creates the tool environment with Python 3.12; if Python downloads are enabled, `uv` will download Python 3.12 automatically when it is missing.

## Install and Start

```bash
uv tool install nova-bot --python 3.12
nova-bot
```
