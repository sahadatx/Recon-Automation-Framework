from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from core.context import ExecutionContext


class BasePlugin(ABC):


    name: ClassVar[str] = ""

    version: ClassVar[str] = "1.0.0"

    author: ClassVar[str] = ""

    description: ClassVar[str] = ""


    enabled: ClassVar[bool] = True

    depends_on: ClassVar[tuple[str, ...]] = ()

    config: ClassVar[dict[str, Any]] = {}


    def initialize(self) -> None:


        pass

    def before_run(
        self,
        context: ExecutionContext,
    ) -> None:


        pass

    @abstractmethod
    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:


        raise NotImplementedError

    def after_run(
        self,
        context: ExecutionContext,
        result: dict[str, Any],
    ) -> None:


        pass

    def before_export(
        self,
        result: dict[str, Any],
    ) -> None:


        pass

    def after_export(
        self,
        result: dict[str, Any],
    ) -> None:


        pass

    def shutdown(self) -> None:


        pass


__all__ = [
    "BasePlugin",
]
