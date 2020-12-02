from openpaygo import OPAYGOEncoder, OPAYGOShared, OPAYGODecoder
import codecs

device_key_hex = 'a29ab82edc5fbbc41ec9530f6dac86b1'
device_starting_code = 123456789
device_last_count = 4
days_to_activate = 7


if __name__ == '__main__':
    print('Generating code for device with key '+device_key_hex +
          ' and starting code '+str(device_starting_code)+'. ')
    print('The code will have the count (number of codes generated before) of ' +
          str(device_last_count)+'. ')
    print('The code will contain ' +
          str(days_to_activate) + ' days of activation. ')

    new_count, token = OPAYGOEncoder.generate_standard_token(
        starting_code=device_starting_code,
        key=codecs.decode(device_key_hex, 'hex'),
        value=days_to_activate,
        count=device_last_count,
        restricted_digit_set=False,
        mode=OPAYGOShared.TOKEN_TYPE_ADD_TIME
    )

    print(token)

    value, count, type = OPAYGODecoder.get_activation_value_count_and_type_from_token(
        starting_code=device_starting_code,
        key=codecs.decode(device_key_hex, 'hex'),
        token=token,
        last_count=device_last_count
    )
    print(value, count, type)
