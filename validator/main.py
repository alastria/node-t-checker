#!/usr/bin/env python
import os

import click

from validator import NodeValidator
from formatter import ValidatorOutputFormatter
from dataclass import ValidatorOutput, EnodeRequestConfig, NodeInformation
from parser import NodeInformationParser
from github_service import GithubService
from exceptions import EnodeNotFoundException


@click.command()
def validate():
    pull_request_id = os.environ.get('TRAVIS_PULL_REQUEST')
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

    print(f"pull_request_id-> {pull_request_id}")
    print(f"GITHUB_TOKEN-> {GITHUB_TOKEN}")

    if not pull_request_id:
        return

    print(f"ENODE_URL-> {os.environ.get('ENODE_URL')}")
    print(f"ENODE_USERNAME-> {os.environ.get('ENODE_USERNAME')}")
    print(f"ENODE_PASSWORD-> {os.environ.get('ENODE_PASSWORD')}")
    print(f"ENODE_DB-> {os.environ.get('ENODE_DB')}")

    enode_config = EnodeRequestConfig(
        url=os.environ.get('ENODE_URL'),
        username=os.environ.get('ENODE_USERNAME'),
        password=os.environ.get('ENODE_PASSWORD'),
        db=os.environ.get('ENODE_DB')
    )

    github_service = GithubService(GITHUB_TOKEN)
    github_service.use_pull_request_id(int(pull_request_id))
    pr_body = github_service.get_pr_body()

    print(f"PR BODY-> {pr_body}")

    try:
        node_info: NodeInformation = NodeInformationParser.extract_from_text(
            pr_body)
    except EnodeNotFoundException as e:
        print(f"EnodeNotFoundException-> {e}")
        return

    print(f"NODE INFO-> {node_info}")

    node_validator = NodeValidator(node_info)
    node_validator.use_enode_request_config(enode_config)
    output: ValidatorOutput = node_validator.get_validation()

    print(f"OUTPUT-> {output}")

    output_formatter = ValidatorOutputFormatter(github_service, output)
    message = output_formatter.get_message()
    print(f"MESSAGE-> {message}")
    if output.has_errors():
        output_formatter.publish_errors(message)
        return

    output_formatter.publish_success_message(message)


if __name__ == '__main__':
    validate()
