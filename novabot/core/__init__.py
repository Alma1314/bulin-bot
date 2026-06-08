import os

from novabot.core.config import NovaBotConfig
from novabot.core.config.default import DB_PATH
from novabot.core.db.sqlite import SQLiteDatabase
from novabot.core.file_token_service import FileTokenService
from novabot.core.utils.pip_installer import (
    DependencyConflictError as DependencyConflictError,
)
from novabot.core.utils.pip_installer import (
    PipInstaller,
)
from novabot.core.utils.requirements_utils import (
    RequirementsPrecheckFailed as RequirementsPrecheckFailed,
)
from novabot.core.utils.requirements_utils import (
    find_missing_requirements as find_missing_requirements,
)
from novabot.core.utils.requirements_utils import (
    find_missing_requirements_or_raise as find_missing_requirements_or_raise,
)
from novabot.core.utils.shared_preferences import SharedPreferences
from novabot.core.utils.t2i.renderer import HtmlRenderer

from .log import LogBroker, LogManager  # noqa
from .utils.novabot_path import get_novabot_data_path

# 初始化数据存储文件夹
os.makedirs(get_novabot_data_path(), exist_ok=True)

DEMO_MODE = os.getenv("DEMO_MODE", "False").strip().lower() in ("true", "1", "t")

novabot_config = NovaBotConfig()
t2i_base_url = novabot_config.get("t2i_endpoint", "https://t2i.soulter.top/text2img")
html_renderer = HtmlRenderer(t2i_base_url)
logger = LogManager.GetLogger(log_name="novabot")
LogManager.configure_logger(logger, novabot_config)
LogManager.configure_trace_logger(novabot_config)
db_helper = SQLiteDatabase(DB_PATH)
# 简单的偏好设置存储, 这里后续应该存储到数据库中, 一些部分可以存储到配置中
sp = SharedPreferences(db_helper=db_helper)
# 文件令牌服务
file_token_service = FileTokenService()
pip_installer = PipInstaller(
    novabot_config.get("pip_install_arg", ""),
    novabot_config.get("pypi_index_url", None),
)
