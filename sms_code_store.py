# -*- coding: utf-8 -*-
"""
短信验证码存储模块
供发布任务（如抖音）在需要验证码时轮询获取，供前端页面提交验证码写入
"""
import threading

_lock = threading.Lock()
_pending_codes = {}  # { "douyin": "123456" }


def submit(platform: str, code: str) -> None:
    """提交验证码"""
    with _lock:
        _pending_codes[platform] = code.strip()


def get_and_clear(platform: str) -> str | None:
    """获取并清除验证码，一次性消费"""
    with _lock:
        return _pending_codes.pop(platform, None)


def has_pending(platform: str) -> bool:
    """检查是否有待消费的验证码"""
    with _lock:
        return platform in _pending_codes
