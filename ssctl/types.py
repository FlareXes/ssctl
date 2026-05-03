from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Action(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"


@dataclass
class Rule:
    action: Action
    domain: str
    path: Optional[str] = None


@dataclass
class GlobalConfig:
    default: Action = Action.ALLOW


@dataclass
class Config:
    global_config: GlobalConfig
    rules: List[Rule]
