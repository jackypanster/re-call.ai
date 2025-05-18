import logging
import sys
from app.config import settings

def setup_logger():
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    log_format = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    logging.basicConfig(
        level=log_level,
        format=log_format,
        stream=sys.stdout
    )
    # 可选：抑制第三方库的冗余日志
    logging.getLogger("uvicorn").setLevel(log_level)
    logging.getLogger("uvicorn.error").setLevel(log_level)
    logging.getLogger("uvicorn.access").setLevel(log_level)

# 在模块导入时自动初始化日志
setup_logger()
