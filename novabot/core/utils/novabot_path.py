"""Centralized NovaBot path helpers.

Project path:
- Fixed to the source tree location.

Root path:
- Defaults to the current working directory.
- Can be overridden with the ``NOVABOT_ROOT`` environment variable.

Data subdirectories:
- Most runtime data lives under ``<root>/data``.
- A few tool-runtime files intentionally live under the system temporary
  directory as ``.novabot``.
"""

import os
import tempfile

from novabot.core.utils.runtime_env import is_packaged_desktop_runtime


def get_novabot_path() -> str:
    """Return the NovaBot project source path."""
    return os.path.realpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"),
    )


def get_novabot_root() -> str:
    """Return the NovaBot root directory."""
    if path := os.environ.get("NOVABOT_ROOT"):
        return os.path.realpath(path)
    if is_packaged_desktop_runtime():
        return os.path.realpath(os.path.join(os.path.expanduser("~"), ".novabot"))
    return os.path.realpath(os.getcwd())


def get_novabot_data_path() -> str:
    """Return the NovaBot data directory path."""
    return os.path.realpath(os.path.join(get_novabot_root(), "data"))


def get_novabot_config_path() -> str:
    """Return the NovaBot config directory path."""
    return os.path.realpath(os.path.join(get_novabot_data_path(), "config"))


def get_novabot_plugin_path() -> str:
    """Return the NovaBot plugin directory path."""
    return os.path.realpath(os.path.join(get_novabot_data_path(), "plugins"))


def get_novabot_plugin_data_path() -> str:
    """Return the NovaBot plugin data directory path."""
    return os.path.realpath(os.path.join(get_novabot_data_path(), "plugin_data"))


def get_novabot_t2i_templates_path() -> str:
    """Return the NovaBot T2I templates directory path."""
    return os.path.realpath(os.path.join(get_novabot_data_path(), "t2i_templates"))


def get_novabot_webchat_path() -> str:
    """Return the NovaBot WebChat data directory path."""
    return os.path.realpath(os.path.join(get_novabot_data_path(), "webchat"))


def get_novabot_temp_path() -> str:
    """Return the NovaBot temporary data directory path."""
    return os.path.realpath(os.path.join(get_novabot_data_path(), "temp"))


def get_novabot_skills_path() -> str:
    """Return the NovaBot skills directory path."""
    return os.path.realpath(os.path.join(get_novabot_data_path(), "skills"))


def get_novabot_workspaces_path() -> str:
    """Return the NovaBot workspaces directory path."""
    return os.path.realpath(os.path.join(get_novabot_data_path(), "workspaces"))


def get_novabot_system_tmp_path() -> str:
    """Return the shared system temporary directory used by local tools."""
    return os.path.realpath(os.path.join(tempfile.gettempdir(), ".novabot"))


def get_novabot_site_packages_path() -> str:
    """Return the NovaBot third-party site-packages directory path."""
    return os.path.realpath(os.path.join(get_novabot_data_path(), "site-packages"))


def get_novabot_knowledge_base_path() -> str:
    """Return the NovaBot knowledge base root path."""
    return os.path.realpath(os.path.join(get_novabot_data_path(), "knowledge_base"))


def get_novabot_backups_path() -> str:
    """Return the NovaBot backups directory path."""
    return os.path.realpath(os.path.join(get_novabot_data_path(), "backups"))
