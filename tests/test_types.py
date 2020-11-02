from validator.dataclass import ValidatorOutput


def test_validator_output_get_errors_return_empty():
    expected_errors = []
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

    errors = output.get_errors()

    assert errors == expected_errors


def test_validator_output_get_errors_return_errors():
    expected_errors = ['is_node_in_europe']
    data = {
        'is_ip_public': True,
        'is_node_in_europe': False,
        'is_geth_version_valid': True,
        'is_constellation_valid': True,
        'is_validator_valid': True,
        'is_regular_valid': True,
        'is_enode_in_directory_valid': True
    }
    output = ValidatorOutput(**data)

    errors = output.get_errors()

    assert errors == expected_errors
