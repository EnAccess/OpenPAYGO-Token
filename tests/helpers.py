import codecs

from importlib import import_module
openpaygo_token = import_module("openpaygo-token")


SET_TIME = 1
ADD_TIME = 2
DISABLE_VALUE = 998

START_RED = '\033[91m'
END_RED = '\033[0m'


def generate_from_device_data(device_data, token_type, value_raw=None, value_days=None, token_count=None):
    assert (value_days is not None) or (value_raw is not None)
    if value_raw is None:
        value_raw = value_days*device_data['time_divider']
    device_data['token_count'], token = openpaygo_token.OPAYGOEncoder.generate_standard_token(
        starting_code=device_data['starting_code'],
        key=codecs.decode(device_data['key'], 'hex'),
        value=value_raw,
        count=token_count or device_data['token_count'],
        restricted_digit_set=device_data['restricted_digit_set'],
        mode=token_type
    )
    token = str(token).rjust(9, '0')
    token = ' '.join([token[i:i + 3] for i in range(0, len(token), 3)])
    return device_data, token


def test_how_many_days(test_name, token, value_days=None, value_raw=None, device_data=None, description=''):
    if value_days is None:
        if value_raw is not None:
            value_days = value_raw/device_data['time_divider']
        else:
            value_days = 'infinite'
    print(test_name+','+token+','+str(value_days)+' days active'+',"'+description+'"')


def test_accepted(test_name, token, expected, description=''):
    expected_string = 'Token Accepted' if expected else 'Token Refused'
    print(test_name+','+token+','+expected_string+',"'+description+'"')


def test_how_many_days_validator(device_simulator, test_name, token, value_days=None, value_raw=None, device_data=None, description='', accepted_but_used=False):
    if value_days is None:
        if value_raw is not None:
            value_days = value_raw/device_data['time_divider']
        else:
            value_days = 'infinite'
    result = device_simulator.enter_token(token.replace(' ', ''), show_result=False)
    if result == 1 or (accepted_but_used and result == -2):
        if device_simulator.get_days_remaining() == value_days:
            print(test_name+': Passed')
            return
    print(START_RED+test_name+': Failed'+END_RED)


def test_accepted_validator(device_simulator, test_name, token, expected, description=''):
    if device_simulator.enter_token(token.replace(' ', ''), show_result=False) == expected:
        print(test_name+': Passed')
        return
    else:
        print(START_RED+test_name+': Failed'+END_RED)


def test_name(test_base_name, test_number):
    return test_base_name+chr(test_number+64)
