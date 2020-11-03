import os
import re
import logging
import json
import subprocess
from typing import Optional, List
import requests
from requests.exceptions import HTTPError

from dataclass import NodeInformation, ValidatorOutput, EnodeRequestConfig


class NodeValidator():
    REGULAR_DIRECTORY_PATH = 'DIRECTORY_REGULAR.md'

    PUBLIC_IP_REGEX = r'21000/tcp\s+(open|filtered)'
    NODE_EUROPE_REGEX = r'country:\s+EU'

    def __init__(self, node_info: NodeInformation):
        self.node_info = node_info

    def use_enode_request_config(self, config: EnodeRequestConfig) -> None:
        self.enode_request_config = config

    def get_validation(self) -> ValidatorOutput:
        with open('data/validator-nodes', 'r') as file:
            is_validator_valid=self.is_valid_json_file(file.read())
        with open('data/constellation-nodes.json', 'r') as file:
            is_constellation_valid=self.is_valid_json_file(file.read())
        with open('data/regular-nodes.json', 'r') as file:
            is_regular_valid=self.is_valid_json_file(file.read())
        with open(self.REGULAR_DIRECTORY_PATH, 'r') as file:
            has_valid_enode = self.has_valid_enode_and_ip_in_regular_directory(file.read())

        return ValidatorOutput(
            is_ip_public=self.is_ip_public(),
            is_node_in_europe=self.is_node_in_europe(),
            is_geth_version_valid=self.is_geth_version_valid(),
            is_validator_valid=is_validator_valid,
            is_constellation_valid=is_constellation_valid,
            is_regular_valid=is_regular_valid,
            is_enode_in_directory_valid=has_valid_enode
        )

    def is_geth_version_valid(self) -> bool:
        # TODO
        return True

    def is_ip_public(self) -> bool:
        output = subprocess.run(
            f'nmap {self.node_info.ip} -p 21000',
            shell=True,
            capture_output=True
        )

        if output.returncode != 0:
            return False

        return bool(
            re.search(
                self.PUBLIC_IP_REGEX,
                output.stdout.decode('utf-8')
            )
        )

    def is_node_in_europe(self) -> bool:
        output = subprocess.run(
            f'whois -h whois.ripe.net {self.node_info.ip}',
            shell=True,
            capture_output=True
        )

        if output.returncode != 0:
            return False

        return bool(
            re.search(
                self.NODE_EUROPE_REGEX,
                output.stdout.decode('utf-8')
            )
        )

    def is_valid_json_file(self, file_output: str, fake_json: bool = False) -> bool:
        '''
            fake_json: It seems there are some files with a json extension
            and aren\'t JSON :scream:
        '''

        if fake_json:
            file_output = f'[ {file_output} ]'

        try:
            json.loads(file_output)
        except ValueError:
            return False
        return True

    def has_valid_enode_and_ip_in_regular_directory(
        self, directory_enodes: str
    ) -> bool:
        return self.node_info.enode in directory_enodes

    def is_enode_online(self) -> bool:
        valid_hosts = self.get_valid_hosts_from_external_source()
        return self.node_info.hostname in valid_hosts

    def get_valid_hosts_from_external_source(self) -> List[str]:
        results = requests.post(
            self.enode_request_config.url,
            data={
                'user': self.enode_request_config.username,
                'password': self.enode_request_config.password,
                'db': self.enode_request_config.db,
                'q': 'SHOW TAG VALUES FROM "geth.txpool/underpriced.count" with key="host"'
            }
        )

        try:
            results.raise_for_status()
        except HTTPError:
            return []

        try:
            hosts = results.json()[0]['series'][0]['values']
            return list(map(lambda item: item[1], hosts))
        except (KeyError, IndexError):
            return []
