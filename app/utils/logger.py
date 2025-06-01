"""
结构化日志系统配置
包含敏感信息过滤和环境相关配置
"""
import logging
import logging.config
import sys
import os
import json
import re
from typing import Dict, Any, Optional
from datetime import datetime
from app.config import settings

class SensitiveDataFilter(logging.Filter):
    """敏感信息过滤器"""
    
    # 敏感字段模式
    SENSITIVE_PATTERNS = [
        re.compile(r'(password|passwd|pwd)[\'"]?\s*[:=]\s*[\'"]?([^\'"\s]+)', re.IGNORECASE),
        re.compile(r'(api[_-]?key|apikey|token|secret)[\'"]?\s*[:=]\s*[\'"]?([^\'"\s]+)', re.IGNORECASE),
        re.compile(r'(bearer\s+)([a-zA-Z0-9\-._~+/]+=*)', re.IGNORECASE),
        re.compile(r'(authorization[\'"]?\s*[:=]\s*[\'"]?)([^\'"\s]+)', re.IGNORECASE),
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """过滤敏感信息"""
        if hasattr(record, 'msg'):
            record.msg = self._mask_sensitive_data(str(record.msg))
        
        # 过滤参数中的敏感信息
        if hasattr(record, 'args') and record.args:
            record.args = tuple(
                self._mask_sensitive_data(str(arg)) if isinstance(arg, str) else arg 
                for arg in record.args
            )
        
        return True
    
    def _mask_sensitive_data(self, text: str) -> str:
        """屏蔽敏感数据"""
        for pattern in self.SENSITIVE_PATTERNS:
            text = pattern.sub(r'\1***MASKED***', text)
        return text

class StructuredFormatter(logging.Formatter):
    """结构化日志格式化器"""
    
    def format(self, record: logging.LogRecord) -> str:
        # 创建结构化日志数据
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        
        # 添加额外的上下文信息
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        if hasattr(record, 'operation'):
            log_data['operation'] = record.operation
        if hasattr(record, 'duration'):
            log_data['duration_ms'] = record.duration
        
        # 添加异常信息
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # 根据环境决定输出格式
        if settings.debug:
            # 开发环境：可读性更好的格式
            return f"[{log_data['timestamp']}] [{log_data['level']}] [{log_data['logger']}] {log_data['message']}"
        else:
            # 生产环境：JSON格式便于日志收集
            return json.dumps(log_data, ensure_ascii=False)

def get_log_level() -> int:
    """根据环境获取日志级别"""
    env_level = getattr(settings, 'log_level', 'INFO').upper()
    
    # 开发环境和生产环境的不同配置
    if settings.debug:
        return getattr(logging, env_level, logging.DEBUG)
    else:
        return getattr(logging, env_level, logging.INFO)

def setup_logger():
    """配置应用日志系统"""
    log_level = get_log_level()
    
    # 创建根日志配置
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'structured': {
                '()': StructuredFormatter,
            },
            'simple': {
                'format': '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'filters': {
            'sensitive_data': {
                '()': SensitiveDataFilter,
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'structured' if not settings.debug else 'simple',
                'filters': ['sensitive_data'],
                'stream': sys.stdout
            }
        },
        'loggers': {
            'app': {
                'level': log_level,
                'handlers': ['console'],
                'propagate': False
            },
            'uvicorn': {
                'level': logging.WARNING if not settings.debug else logging.INFO,
                'handlers': ['console'],
                'propagate': False
            },
            'uvicorn.error': {
                'level': logging.WARNING,
                'handlers': ['console'],
                'propagate': False
            },
            'uvicorn.access': {
                'level': logging.INFO if settings.debug else logging.WARNING,
                'handlers': ['console'],
                'propagate': False
            }
        },
        'root': {
            'level': log_level,
            'handlers': ['console']
        }
    }
    
    # 如果是生产环境，可以添加文件日志
    if not settings.debug:
        logging_config['handlers']['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'level': log_level,
            'formatter': 'structured',
            'filters': ['sensitive_data']
        }
        logging_config['loggers']['app']['handlers'].append('file')
    
    # 应用配置
    logging.config.dictConfig(logging_config)

def get_logger(name: str) -> logging.Logger:
    """获取指定名称的日志器"""
    return logging.getLogger(f"app.{name}")

def log_api_call(logger: logging.Logger, operation: str, user_id: Optional[str] = None, 
                 duration: Optional[float] = None, **kwargs):
    """记录API调用日志"""
    extra = {
        'operation': operation,
        'user_id': user_id,
        'duration': duration
    }
    extra.update(kwargs)
    
    message = f"API call: {operation}"
    if user_id:
        message += f" (user: {user_id})"
    if duration:
        message += f" (duration: {duration:.2f}ms)"
    
    logger.info(message, extra=extra)

def log_error(logger: logging.Logger, error: Exception, context: Optional[Dict[str, Any]] = None):
    """记录错误日志"""
    extra = context or {}
    logger.error(f"Error occurred: {type(error).__name__}: {str(error)}", 
                exc_info=True, extra=extra)

# 在模块导入时自动初始化日志
setup_logger()
