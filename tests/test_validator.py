import subprocess
import tempfile

from .mocks import SubprocessOutputMock
from validator.validator import NodeValidator
from validator.dataclass import NodeInformation, EnodeRequestConfig


def test_is_ip_public_returncode_invalid_return_false(mocker):
    subprocess_output = b''
    subprocess_mock = SubprocessOutputMock(returncode=1, stdout=subprocess_output)
    mocker.patch.object(subprocess, 'run', return_value=subprocess_mock)
    node_info = NodeInformation('1.2.3.4', 'myenode')
    validator = NodeValidator(node_info)

    is_valid = validator.is_ip_public()

    assert not is_valid


def test_is_ip_public_return_true(mocker):
    subprocess_output = b'''
        Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-29 12:40 CEST
        Nmap scan report for XXXX (2.1.4.5)
        Host is up (0.045s latency).

        PORT      STATE SERVICE
        21000/tcp open  irtrans

        Nmap done: 1 IP address (1 host up) scanned in 0.25 seconds
    '''
    subprocess_mock = SubprocessOutputMock(returncode=0, stdout=subprocess_output)
    mocker.patch.object(subprocess, 'run', return_value=subprocess_mock)
    node_info = NodeInformation('1.2.3.4', 'myenode')
    validator = NodeValidator(node_info)

    is_valid = validator.is_ip_public()

    assert is_valid


def test_is_ip_public_return_false(mocker):
    subprocess_output = b'''
        Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-29 12:40 CEST
        Nmap scan report for XXXX (2.1.4.5)
        Host is up (0.045s latency).

        PORT      STATE SERVICE
        21000/tcp closed  irtrans

        Nmap done: 1 IP address (1 host up) scanned in 0.25 seconds
    '''
    subprocess_mock = SubprocessOutputMock(returncode=0, stdout=subprocess_output)
    mocker.patch.object(subprocess, 'run', return_value=subprocess_mock)
    node_info = NodeInformation('1.2.3.4', 'myenode')
    validator = NodeValidator(node_info)

    is_valid = validator.is_ip_public()

    assert not is_valid

def test_is_node_in_europe_returncode_invalid_return_false(mocker):
    subprocess_output = b''
    subprocess_mock = SubprocessOutputMock(returncode=1, stdout=subprocess_output)
    mocker.patch.object(subprocess, 'run', return_value=subprocess_mock)
    node_info = NodeInformation('1.2.3.4', 'myenode')
    validator = NodeValidator(node_info)

    is_valid = validator.is_node_in_europe()

    assert not is_valid


def test_is_node_in_europe_return_false(mocker):
    subprocess_output = b'''
        ...
        remarks:
        remarks:        ------------------------------------------------------
        country:        US
    '''
    subprocess_mock = SubprocessOutputMock(returncode=0, stdout=subprocess_output)
    mocker.patch.object(subprocess, 'run', return_value=subprocess_mock)
    node_info = NodeInformation('1.2.3.4', 'myenode')
    validator = NodeValidator(node_info)

    is_valid = validator.is_node_in_europe()

    assert not is_valid


def test_is_node_in_europe_return_true(mocker):
    subprocess_output = b'''
        ...
        remarks:
        remarks:        ------------------------------------------------------
        country:        EU
    '''
    subprocess_mock = SubprocessOutputMock(returncode=0, stdout=subprocess_output)
    mocker.patch.object(subprocess, 'run', return_value=subprocess_mock)
    node_info = NodeInformation('1.2.3.4', 'myenode')
    validator = NodeValidator(node_info)

    is_valid = validator.is_node_in_europe()

    assert is_valid


def test_is_valid_json_file_invalid_json_return_false(mocker):
    file_output = '''
        [ "https://137.117.233.65:9000/",
          "https://15.161.123.199:9000/",
          "https://195.55.232.91:9000/",
        ]
    '''
    node_info = NodeInformation('1.2.3.4', 'myenode')
    validator = NodeValidator(node_info)

    is_valid = validator.is_valid_json_file(file_output)

    assert not is_valid


def test_is_valid_json_file_valid_json_return_true():
    file_output = '''
        [ "https://137.117.233.65:9000/",
          "https://15.161.123.199:9000/",
          "https://195.55.232.91:9000/"
        ]
    '''
    node_info = NodeInformation('1.2.3.4', 'myenode')
    validator = NodeValidator(node_info)

    is_valid = validator.is_valid_json_file(file_output)

    assert is_valid


def test_is_valid_json_file_invalid_fake_json_return_false():
    file_output = '''
        "enode://d4328d9a744b2770b4c46f5594c59f03e9c936538758cf53c119e1ff05c7cdb86e7ecfb107aa121d24c3342f2cb68090cea9e40d82f43f18c517215ae576b8ed@195.55.232.91:21000?discport=0",
        "enode://be6a6eef8c5ea5e64414126e0bdc10481543416ed3baf9bb10e66842f011404035291d6f93b2a770ce232a687bdaf5c2602d3cd8f696a835456d693f7947b3d3@51.138.52.113:21000?discport=0",
        "enode://0752557351410a2b31bb91a008c25510dccbbba53241937c77a061fe128c9e2102bbf3b7ee55cb85c37d980a85f5cf20ccde1f92bf10a12d68db8be78d3de705@52.50.15.212:21000?discport=0",
    '''
    node_info = NodeInformation('1.2.3.4', 'myenode')
    validator = NodeValidator(node_info)
    is_valid = validator.is_valid_json_file(file_output, fake_json=True)

    assert not is_valid


def test_is_valid_json_file_valid_fake_json_return_true():
    file_output = '''
        "enode://d4328d9a744b2770b4c46f5594c59f03e9c936538758cf53c119e1ff05c7cdb86e7ecfb107aa121d24c3342f2cb68090cea9e40d82f43f18c517215ae576b8ed@195.55.232.91:21000?discport=0",
        "enode://be6a6eef8c5ea5e64414126e0bdc10481543416ed3baf9bb10e66842f011404035291d6f93b2a770ce232a687bdaf5c2602d3cd8f696a835456d693f7947b3d3@51.138.52.113:21000?discport=0",
        "enode://0752557351410a2b31bb91a008c25510dccbbba53241937c77a061fe128c9e2102bbf3b7ee55cb85c37d980a85f5cf20ccde1f92bf10a12d68db8be78d3de705@52.50.15.212:21000?discport=0"
    '''
    node_info = NodeInformation('1.2.3.4', 'myenode')
    validator = NodeValidator(node_info)

    is_valid = validator.is_valid_json_file(file_output, fake_json=True)

    assert is_valid


def test_has_valid_enode_in_regular_directory_return_false():
    file_output = '''
        # Directorio de nodos regulares
        | Entidad | Hosting info (Cores/Mem/HDD) | Clave private for * | enode |
        | ------- | ---------------------------------- | ------------- | ----- |
        | Alisys | Self hosted (1C/4GB/70GB) | AvVbQrGRfvMHHw+MO9KlW9g3NVY1ETTTRUGtAa07BS8= | enode://ee1cebf3111df175a5cd079c606cea7cc0a82e64c5900731d88cd79e00e8458068edeb2914167408856245a8731456205ef6bd6dfe6a63e112c5ee4e8a2d273c@154.62.228.24:21000?discport=0 |
        | Docuten | Stackscale (4C/8GB/100GB) | O+nm2OnJMsR76JIZYreRjpaD4SrcXgCq7MAaE/snpyA= | enode://8064fc030d09cff5690efbd7bd07dcb4ababbb1f04ae0a0b02776c6c60b86a78cda4baff33d44a681b3a76d36988232877f0ed9bb8c47ec95c5158b6409016ae@5.57.225.79:21000?discport=0 |
        | IoBuilders | Amazon (2C/4GB/100GB) | | enode://6dcccbad7a4e75701fef6fd0f578c7d3873a853c905a911c416c896914b7cbd46320c363659c46ea32abedd397cb592c001c274dd282c46ed0c63e95c242453c@34.241.169.145:21000?discport=0 |
        | DiplomE | Virtion (4C/8GB/256GB) | hCzwYkHamL2HMmzAUjg13pXFN2pEEvYLF/wYf5VCcEQ= | enode://3efb067df8150ae2473b57ca418200b90b91bc7740c79642346f36fe68bc34f5639f7e4c04cf6947f1a39dd5c25e699e2742a37cc7673d4890ac945d36a950de@5.28.41.68:21000?discport=0 |
        | Hippo Technologies | Amazon (2C/8GB/100GB) | | enode://42a00600c4c090edfda6a8797204dbb0362459468db953f89f9c507f8e544af7260fbd0e5af976cc5c2b21aa31e1964529a45aa1fc77b01044636c0f1574864f@18.213.143.8:21000?discport=0 |
        | Seres |  OVH (2C/8Gb/80Gb)| Cyj6f4xMTbch4m2UqUlrDY8Xw1Yo+d7MSitUOYfDuXs= | enode://5ab3f3c0aecbf042017d90aac930cf10f2e971e86f7314ab13d526c126b3b629d6051b0546971e220708de269e530452bde0990be5d6bcaa918a3a9772d73847@51.68.123.73:21000?discport=0 |
    '''

    node_info = NodeInformation('1.2.3.4', 'myenode')
    validator = NodeValidator(node_info)

    is_valid = validator.has_valid_enode_and_ip_in_regular_directory(file_output)

    assert not is_valid


def test_has_valid_enode_in_regular_directory_return_true():
    file_output = '''
        # Directorio de nodos regulares
        | Entidad | Hosting info (Cores/Mem/HDD) | Clave private for * | enode |
        | ------- | ---------------------------------- | ------------- | ----- |
        | Alisys | Self hosted (1C/4GB/70GB) | AvVbQrGRfvMHHw+MO9KlW9g3NVY1ETTTRUGtAa07BS8= | enode://ee1cebf3111df175a5cd079c606cea7cc0a82e64c5900731d88cd79e00e8458068edeb2914167408856245a8731456205ef6bd6dfe6a63e112c5ee4e8a2d273c@154.62.228.24:21000?discport=0 |
        | Docuten | Stackscale (4C/8GB/100GB) | O+nm2OnJMsR76JIZYreRjpaD4SrcXgCq7MAaE/snpyA= | enode://8064fc030d09cff5690efbd7bd07dcb4ababbb1f04ae0a0b02776c6c60b86a78cda4baff33d44a681b3a76d36988232877f0ed9bb8c47ec95c5158b6409016ae@5.57.225.79:21000?discport=0 |
        | IoBuilders | Amazon (2C/4GB/100GB) | | enode://6dcccbad7a4e75701fef6fd0f578c7d3873a853c905a911c416c896914b7cbd46320c363659c46ea32abedd397cb592c001c274dd282c46ed0c63e95c242453c@34.241.169.145:21000?discport=0 |
        | DiplomE | Virtion (4C/8GB/256GB) | hCzwYkHamL2HMmzAUjg13pXFN2pEEvYLF/wYf5VCcEQ= | enode://3efb067df8150ae2473b57ca418200b90b91bc7740c79642346f36fe68bc34f5639f7e4c04cf6947f1a39dd5c25e699e2742a37cc7673d4890ac945d36a950de@5.28.41.68:21000?discport=0 |
        | Hippo Technologies | Amazon (2C/8GB/100GB) | | enode://42a00600c4c090edfda6a8797204dbb0362459468db953f89f9c507f8e544af7260fbd0e5af976cc5c2b21aa31e1964529a45aa1fc77b01044636c0f1574864f@18.213.143.8:21000?discport=0 |
        | Seres |  OVH (2C/8Gb/80Gb)| Cyj6f4xMTbch4m2UqUlrDY8Xw1Yo+d7MSitUOYfDuXs= | enode://5ab3f3c0aecbf042017d90aac930cf10f2e971e86f7314ab13d526c126b3b629d6051b0546971e220708de269e530452bde0990be5d6bcaa918a3a9772d73847@51.68.123.73:21000?discport=0 |
    '''

    node_info = NodeInformation('1.2.3.4', '42a00600c4c090edfda6a8797204dbb0362459468db953f89f9c507f8e544af7260fbd0e5af976cc5c2b21aa31e1964529a45aa1fc77b01044636c0f1574864f')
    validator = NodeValidator(node_info)

    is_valid = validator.has_valid_enode_and_ip_in_regular_directory(file_output)

    assert is_valid


def test_is_enode_online_empty_hosts_false(mocker):
    valid_hosts = []
    mocker.patch.object(
        NodeValidator,
        'get_valid_hosts_from_external_source',
        return_value=valid_hosts)
    node_info = NodeInformation(
        '1.2.3.4', 'myenode', 'myhostname')
    validator = NodeValidator(node_info)
    validator.use_enode_request_config(EnodeRequestConfig())

    is_valid = validator.is_enode_online()

    assert not is_valid


def test_is_enode_online_false(mocker):
    valid_hosts = ['REG_SA_Telsius_2_4_00', 'REG_SEAT_T_2_16_01']
    mocker.patch.object(
        NodeValidator,
        'get_valid_hosts_from_external_source',
        return_value=valid_hosts)
    mocker.patch
    node_info = NodeInformation(
        '1.2.3.4', 'myenode', 'myhostname')
    validator = NodeValidator(node_info)
    validator.use_enode_request_config(EnodeRequestConfig())

    is_valid = validator.is_enode_online()

    assert not is_valid


def test_is_enode_online_return(mocker):
    valid_hosts = ['REG_SA_Telsius_2_4_00', 'REG_SEAT_T_2_16_01']
    mocker.patch.object(
        NodeValidator,
        'get_valid_hosts_from_external_source',
        return_value=valid_hosts)
    node_info = NodeInformation(
        '1.2.3.4', 'myenode', 'REG_SA_Telsius_2_4_00')
    validator = NodeValidator(node_info)
    validator.use_enode_request_config(EnodeRequestConfig())

    is_valid = validator.is_enode_online()

    assert is_valid
