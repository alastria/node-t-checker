import pytest  # type: ignore

from validator.parser import NodeInformationParser
from validator.types import NodeInformation
from validator.exceptions import EnodeNotFoundException


def test_extract_from_text_raise_exception():
    body = '''
    ENODE: **invalid enode**
    '''

    with pytest.raises(EnodeNotFoundException):
        NodeInformationParser.extract_from_text(body)


def test_extract_from_text_with_spaces_return_valid_information():
    expected_ip = '5.57.225.79'
    body = f'''
    ENODE:   enode://8064fc030d09cff5690efbd7bd07dcb4ababbb1f04ae0a0b02776c6c60b86a78cda4baff33d44a681b3a76d36988232877f0ed9bb8c47ec95c5158b6409016ae@{expected_ip}:21000?discport=0
    '''

    enode = NodeInformationParser.extract_from_text(body)

    assert enode.ip == expected_ip


def test_extract_from_text_no_spaces_return_valid_information():
    expected_ip = '5.57.225.79'
    body = f'''
    ENODE:enode://8064fc030d09cff5690efbd7bd07dcb4ababbb1f04ae0a0b02776c6c60b86a78cda4baff33d44a681b3a76d36988232877f0ed9bb8c47ec95c5158b6409016ae@{expected_ip}:21000?discport=0
    '''

    enode = NodeInformationParser.extract_from_text(body)

    assert enode.ip == expected_ip
