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
    pull_request_id: int = os.environ.get('TRAVIS_PULL_REQUEST')
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

    if not pull_request_id:
        return

    enode_config = EnodeRequestConfig(
        url=os.environ.get('ENODE_URL'),
        username=os.environ.get('ENODE_USERNAME'),
        password=os.environ.get('ENODE_PASSWORD'),
        db=os.environ.get('ENODE_DB')
    )

    github_service = GithubService(GITHUB_TOKEN)
    github_service.use_pull_request_id(pull_request_id)
    pr_body = github_service.get_pr_body()

    try:
        node_info: NodeInformation = NodeInformationParser.extract_from_text(
            pr_body)
    except EnodeNotFoundException:
        return

    node_validator = NodeValidator(
        node_info
    ).use_enode_request_config(enode_config)
    output: ValidatorOutput = node_validator.get_validation()

    output_formatter = ValidatorOutputFormatter(github_service, output)
    message = output_formatter.get_message()

    if output.has_errors():
        output_formatter.publish_errors(message)
        return

    output_formatter.publish_success_message(message)


if __name__ == '__main__':
    validate()
