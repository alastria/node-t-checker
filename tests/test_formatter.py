from validator.formatter import ValidatorOutputFormatter
from validator.dataclass import ValidatorOutput


def test_get_message_return_success(mocker):
    expected_message = ValidatorOutputFormatter.SUCCESS_MESSAGE
    data = {
        'is_ip_public': True,
        'is_node_in_europe': True,
        'is_geth_version_valid': True,
        'is_constellation_valid': True,
        'is_validator_valid': True,
        'is_regular_valid': True,
        'is_enode_in_directory_valid': True
    }
    output = ValidatorOutput(**data)
    formatter = ValidatorOutputFormatter(
        mocker.patch('validator.github.GithubService'),
        output
    )

    message = formatter.get_message()

    assert message == expected_message

def test_get_message_return_errors_formatted(mocker):
    expected_message = '\n'.join([
        ValidatorOutputFormatter.ERROR_MESSAGES['is_ip_public'],
        ValidatorOutputFormatter.ERROR_MESSAGES['is_node_in_europe']
    ])
    data = {
        'is_ip_public': False,
        'is_node_in_europe': False,
        'is_geth_version_valid': True,
        'is_constellation_valid': True,
        'is_validator_valid': True,
        'is_regular_valid': True,
        'is_enode_in_directory_valid': True
    }
    output = ValidatorOutput(**data)
    formatter = ValidatorOutputFormatter(
        mocker.patch('validator.github.GithubService'),
        output
    )

    message = formatter.get_message()

    assert message == expected_message


def test_get_format_errors_empty_errors(mocker):
    expected_message = ''
    data = {
        'is_ip_public': False,
        'is_node_in_europe': False,
        'is_geth_version_valid': True,
        'is_constellation_valid': True,
        'is_validator_valid': True,
        'is_regular_valid': True,
        'is_enode_in_directory_valid': True
    }
    output = ValidatorOutput(**data)
    formatter = ValidatorOutputFormatter(
        mocker.patch('validator.github.GithubService'),
        output
    )

    message = formatter.format_errors([])

    assert message == expected_message


def test_get_format_errors_with_errors(mocker):
    expected_message = '\n'.join([
        ValidatorOutputFormatter.ERROR_MESSAGES['is_ip_public'],
        ValidatorOutputFormatter.ERROR_MESSAGES['is_node_in_europe']
    ])
    data = {
        'is_ip_public': False,
        'is_node_in_europe': False,
        'is_geth_version_valid': True,
        'is_constellation_valid': True,
        'is_validator_valid': True,
        'is_regular_valid': True,
        'is_enode_in_directory_valid': True
    }
    output = ValidatorOutput(**data)
    formatter = ValidatorOutputFormatter(
        mocker.patch('validator.github.GithubService'),
        output
    )

    message = formatter.format_errors(['is_ip_public', 'is_node_in_europe'])

    assert message == expected_message
