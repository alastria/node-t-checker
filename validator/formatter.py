from typing import List

from dataclass import ValidatorOutput, PublishableOutput


class ValidatorOutputFormatter:
    SUCCESS_MESSAGE = '✅ Node Validated technically'
    ERROR_MESSAGES = {
        'is_ip_public': 'IP has to be public, please check it out!',
        'is_node_in_europe': 'The Node has to be in Europe, please check it out!',
        'is_geth_version_valid': 'The geth version has to be v1.8.x',
        'is_constellation_valid': 'The JSON in the data/constellation-nodes.json is not valid, please paste it on https://jsonlint.com',
        'is_validator_valid': 'The JSON in the data/validator-nodes.json is not valid, please paste it on https://jsonlint.com',
        'is_regular_valid': 'The JSON in the data/validator-nodes.json is not valid, please paste it on https://jsonlint.com',
        'is_enode_in_directory_valid': 'The enode in the DIRECTORY_REGULAR.md file is not the same as in the nodes.json files',
    }

    def __init__(
        self, service: PublishableOutput, output: ValidatorOutput
    ):
        self.publish_service = service
        self.output = output

    def get_message(self):
        errors = self.output.get_errors()

        if errors:
            return self.format_errors(errors)

        return self.SUCCESS_MESSAGE

    def format_errors(self, errors: List[str]) -> str:
        error_messages = map(
            lambda error: self.ERROR_MESSAGES[error],
            errors)
        return '\n'.join(error_messages)

    def publish_errors(self, body: str) -> None:
        self.publish_service.publish(body)

    def publish_success_message(self, body: str) -> None:
        self.publish_service.publish(body)
