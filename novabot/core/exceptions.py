from __future__ import annotations


class NovaBotError(Exception):
    """Base exception for all NovaBot errors.
    错误的基类"""


class ProviderNotFoundError(NovaBotError):
    """Raised when a specified provider is not found.
    查不到指定的 LLM Provider 时抛出"""


class EmptyModelOutputError(NovaBotError):
    """Raised when the model response contains no usable assistant output.
    LLM 返回空响应时抛出"""


class KnowledgeBaseUploadError(NovaBotError):
    """Raised when knowledge base upload fails with a user-facing message.
    知识库上传失败时抛出"""

    def __init__(
        self,
        *,
        stage: str,
        user_message: str,
        details: dict | None = None,
    ) -> None:
        super().__init__(user_message)
        self.stage = stage
        self.user_message = user_message
        self.details = details or {}

    def __str__(self) -> str:
        return self.user_message
