from encode_token import OPAYGOEncoder, OPAYGOShared
from decode_token import OPAYGODecoder
import codecs

# Set this up for the device you want to verify
device_key_hex = 'a29ab82edc5fbbc41ec9530f6dac86b1'
device_starting_code = 123456789
device_count = 1


if __name__ == '__main__':
    device_count, token = OPAYGOEncoder.generate_standard_token(
        starting_code=device_starting_code,
        key=codecs.decode(device_key_hex, 'hex'),
        value=1,
        count=device_count,
        restricted_digit_set=False,
        mode=OPAYGOShared.TOKEN_TYPE_ADD_TIME
    )
    print(device_count, token)

    new_count, token = OPAYGOEncoder.generate_standard_token(
        starting_code=device_starting_code,
        key=codecs.decode(device_key_hex, 'hex'),
        value=5,
        count=device_count+16,
        restricted_digit_set=False,
        mode=OPAYGOShared.TOKEN_TYPE_ADD_TIME
    )
    print(new_count, token)

    device_count, token = OPAYGOEncoder.generate_standard_token(
        starting_code=device_starting_code,
        key=codecs.decode(device_key_hex, 'hex'),
        value=5,
        count=device_count,
        restricted_digit_set=False,
        mode=OPAYGOShared.TOKEN_TYPE_ADD_TIME
    )
    print(device_count, token)

    device_count, token = OPAYGOEncoder.generate_standard_token(
        starting_code=device_starting_code,
        key=codecs.decode(device_key_hex, 'hex'),
        value=5,
        count=device_count,
        restricted_digit_set=False,
        mode=OPAYGOShared.TOKEN_TYPE_ADD_TIME
    )
    print(device_count, token)

