from types import MappingProxyType
from typing import Dict, List


class Command:
    def __init__(self, tool: str, name: str, url: str, supports_special: bool, params: Dict[str, str]):
        self._tool: str = tool
        self._name: str = name
        self._url: str = url
        self._supports_special: bool = supports_special
        self._params: Dict[str, str] = dict(params)

    @property
    def tool(self) -> str:
        return self._tool

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    @property
    def supports_special(self) -> bool:
        return self._supports_special

    @property
    def params(self) -> Dict[str, str]:
        return self._params.copy()

    def has_param(self, param: str) -> bool:
        return param in self._params

    def has_params(self) -> bool:
        return len(self._params) > 0

    def list_params(self) -> List[str]:
        return list(self._params.keys())

    def get_default_param_value(self, param: str) -> str:
        return self._params[param]