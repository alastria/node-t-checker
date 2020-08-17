from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import List


@dataclass(frozen=True)
class ValidatorOutput:
    is_ip_public: bool
    is_node_in_europe: bool
    is_geth_version_valid: bool
    is_constellation_valid: bool
    is_validator_valid: bool
    is_regular_valid: bool
    is_enode_in_directory_valid: bool

    def get_errors(self) -> List[str]:
        return [
            key
            for key, value in asdict(self).items()
            if not value
        ]


@dataclass(frozen=True)
class NodeInformation:
    ip: str = ''
    enode: str = ''
    hostname: str = ''


@dataclass(frozen=True)
class EnodeRequestConfig:
    url: str = ''
    username: str = ''
    password: str = ''
    db: str = ''


class PublishableOutput(ABC):
    @abstractmethod
    def publish(self, body: str) -> None: pass
