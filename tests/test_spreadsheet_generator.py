from helpers import ADD_TIME, SET_TIME, DISABLE_VALUE, generate_from_device_data, test_accepted, test_how_many_days, test_name


def run_core_token_tests(device_data):

    test = 'We enter an invalid token'
    token_g1 = '123 456 789'
    test_accepted('G1', token_g1, False, description=test)

    test = 'We enter a valid token for setting one day'
    device_data, token_g2 = generate_from_device_data(device_data, token_type=SET_TIME, value_days=1)
    test_how_many_days('G2', token_g2, 1, description=test)

    test = 'We enter a valid token for adding one day'
    device_data, token_g3 = generate_from_device_data(device_data, token_type=ADD_TIME, value_days=1)
    test_how_many_days('G3', token_g3, 2, description=test)

    test = 'We enter the same Add Time token for 1 day, the days should not be added and the device should signal that the token was already used'
    test_how_many_days('G4A', token_g3, 2, description=test)
    test = 'We enter the older Set Time token for 1 day, the days should not change and the device should signal that the token was already used'
    test_how_many_days('G4B', token_g2, 2, description=test)

    test = 'We enter a valid token for setting 30 days and ensures it sets and does not add to the existing'
    device_data, token_g5 = generate_from_device_data(device_data, token_type=SET_TIME, value_days=30)
    test_how_many_days('G5', token_g5, 30, description=test)

    test = 'We enter a valid token for setting 0 days and ensures the device is inactive with the outputs disabled immediately'
    device_data, token_g6 = generate_from_device_data(device_data, token_type=SET_TIME, value_days=0)
    test_how_many_days('G6', token_g6, 0, description=test)

    test = 'We enter 3 consecutive Add Time tokens with the maximum amount of days and ensure that they cumulate properly'
    for i in range(1,3+1):
        device_data, token_g7 = generate_from_device_data(device_data, token_type=ADD_TIME, value_raw=995)
        test_how_many_days(test_name('G7', i), token_g7, value_raw=995*i, device_data=device_data, description=test)
        test = ''

    test = 'We enter 21 consecutive Set Time tokens for 1, 2, 3, … 21 days each with a count 30 higher than the other. The validation of the token should not take more than 5 seconds'
    for i in range(1,21+1):
        device_data, token_g8 = generate_from_device_data(device_data, token_type=SET_TIME, value_days=i, token_count=device_data['token_count']+29)
        test_how_many_days(test_name('G8', i), token_g8, value_days=i, device_data=device_data, description=test)
        test = ''

    test = 'We enter a PAYG Disable token into the device'
    device_data, token_g9 = generate_from_device_data(device_data, token_type=SET_TIME, value_raw=DISABLE_VALUE)
    test_how_many_days('G9', token_g9, None, description=test)

    test = 'We enter a Set Time token for 0 day, it should relock the device'
    device_data, token_g10 = generate_from_device_data(device_data, token_type=SET_TIME, value_days=0)
    test_how_many_days('G10', token_g10, 0, description=test)

    test = 'We enter a PAYG Disable token to relock the device, then enter a Add Time token with 0 day, it should NOT relock the device (Optional)'
    device_data, token_g11a = generate_from_device_data(device_data, token_type=SET_TIME, value_raw=DISABLE_VALUE)
    test_how_many_days('G11A', token_g11a, None, description=test)
    device_data, token_g11b = generate_from_device_data(device_data, token_type=ADD_TIME, value_days=0)
    test_how_many_days('G11B', token_g11b, None)

    test = 'We deactivate the device with a Set Time of 0 days. We then wait 48 hours before entering a Add Time of 1 day and ensuring that the days late are not considered in the activation time'
    device_data, token_g12a = generate_from_device_data(device_data, token_type=SET_TIME, value_days=0)
    test_how_many_days('G12A', token_g12a, 0, description=test)
    device_data, token_g12b = generate_from_device_data(device_data, token_type=ADD_TIME, value_days=1)
    test_how_many_days('G12B', token_g12b, 1)

    return device_data


def run_unordered_entry_tests(device_data):

    test = 'We generate 3 Add Time tokens, then enter the 3rd, then first, then second and ensure the days are added properly'
    device_data, token_u1a = generate_from_device_data(device_data, token_type=SET_TIME, value_days=60)
    test_how_many_days('U1A', token_u1a, 60, description=test)
    device_data, token_u1b = generate_from_device_data(device_data, token_type=ADD_TIME, value_days=10)
    device_data, token_u1c = generate_from_device_data(device_data, token_type=ADD_TIME, value_days=5)
    device_data, token_u1d = generate_from_device_data(device_data, token_type=ADD_TIME, value_days=1)
    test_how_many_days('U1B', token_u1d, 61)
    test_how_many_days('U1C', token_u1b, 71)
    test_how_many_days('U1D', token_u1c, 76)

    test = 'We generate an Add Time, a Set Time and another Add Time token. We enter the set time and ensure that the older Add Time does not work but the newer does'
    device_data, token_u2a = generate_from_device_data(device_data, token_type=ADD_TIME, value_days=5)
    device_data, token_u2b = generate_from_device_data(device_data, token_type=SET_TIME, value_days=10)
    device_data, token_u2c = generate_from_device_data(device_data, token_type=ADD_TIME, value_days=3)
    test_how_many_days('U2A', token_u2b, 10, description=test)
    test_accepted('U2B', token_u2a, False)
    test_how_many_days('U2C', token_u2c, 13)

    test = 'We generate an Add Time token and a Disable PAYG token, we enter the Disable PAYG token and then the Add Time token should be refused'
    device_data, token_u3a = generate_from_device_data(device_data, token_type=ADD_TIME, value_days=1)
    device_data, token_u3b = generate_from_device_data(device_data, token_type=SET_TIME, value_raw=DISABLE_VALUE)
    test_how_many_days('U3A', token_u3b, None, description=test)
    test_accepted('U3B', token_u3a, False)

    return device_data




if __name__ == '__main__':
    device_data = {
        'serial_number': 'changeme',
        'starting_code': 123456789,
        'key': 'a29ab82edc5fbbc41ec9530f6dac86b1',
        'restricted_digit_set': False,
        'time_divider': 1,
        'token_count': 1
    }
    print('Test Name,Token Used,Expected Result,Test Details,Result')
    device_data = run_core_token_tests(device_data)
    device_data = run_unordered_entry_tests(device_data)
