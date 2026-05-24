from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Action(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"


class Status(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


@dataclass
class Rule:
    action: Action
    domain: str
    path: Optional[str] = None


@dataclass
class BypassRule:
    status: Status
    host: str


@dataclass
class GlobalConfig:
    default: Action = Action.ALLOW


@dataclass
class Config:
    global_config: GlobalConfig
    rules: List[Rule]
    bypass_rules: List[BypassRule]
