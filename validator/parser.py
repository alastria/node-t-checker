import re

from validator.exceptions import EnodeNotFoundException
from validator.types import NodeInformation


class NodeInformationParser:
    ENODE_REGEX = r'ENODE:(?P<enode>(\s+)?enode:\/\/(?P<hash>\w+)@(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):21000\?discport=0)'

    @classmethod
    def extract_from_text(cls, body: str) -> NodeInformation:
        enode = re.search(cls.ENODE_REGEX, body)

        if not enode:
            raise EnodeNotFoundException()

        return NodeInformation(
            ip=enode.group('ip'),
            hostname=enode.group('ip'),
            enode=enode.group('enode'))
