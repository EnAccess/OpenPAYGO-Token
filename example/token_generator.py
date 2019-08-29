from encode_token import OPAYGOEncoder
import codecs


# Input for the code to be generated
device_key_hex = 'a29ab82edc5fbbc41ec9530f6dac86b1'
device_starting_code = 123456789
device_last_count = 1
days_to_activate = 7


if __name__ == '__main__':
    print('Generating code for device with key '+device_key_hex+' and starting code '+str(device_starting_code)+'. ')
    print('The code will have the count (number of codes generated before) of '+str(device_last_count)+'. ')
    print('The code will contain ' + str(days_to_activate) + ' days of activation. ')

    activation_code = OPAYGOEncoder.generate_token_activation(
        starting_code=device_starting_code,
        key=codecs.decode(device_key_hex, 'hex'),
        value=days_to_activate,
        count=device_last_count+1,
        restricted_digit_set=False
    )

    print(str(activation_code))
