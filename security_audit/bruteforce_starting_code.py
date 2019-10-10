from encode_token import OPAYGOEncoder
from shared import OPAYGOShared
import codecs

# We know the key, and we know 3 tokens with count and value
known_value = 7
code_count_1 = int('016609796')
code_count_2 = int('395084796')
code_count_3 = int('682637796')
device_key_hex = 'a29ab82edc5fbbc41ec9530f6dac86b1'
device_key = codecs.decode(device_key_hex, 'hex')


if __name__ == '__main__':
    print('Trying to bruteforce the starting code...')

    token_base = OPAYGOShared.get_token_base(code_count_1) - known_value

    for i in range(999999):
        if i % 10000 == 0:
            print(str(int((i/999999)*100))+'%')

        starting_code = OPAYGOShared.put_base_in_token(i*1000, token_base)

        count, activation_code = OPAYGOEncoder.generate_standard_token(
            starting_code=starting_code,
            key=device_key,
            value=known_value,
            count=1,
            mode=OPAYGOShared.TOKEN_TYPE_ADD_TIME
        )

        if activation_code == code_count_1:

            count, activation_code_2 = OPAYGOEncoder.generate_standard_token(
                starting_code=starting_code,
                key=device_key,
                value=known_value,
                count=count,
                mode=OPAYGOShared.TOKEN_TYPE_ADD_TIME
            )

            if activation_code_2 == code_count_2:

                count, activation_code_3 = OPAYGOEncoder.generate_standard_token(
                    starting_code=starting_code,
                    key=device_key,
                    value=known_value,
                    count=count,
                    mode=OPAYGOShared.TOKEN_TYPE_ADD_TIME
                )

                if activation_code_3 == code_count_3:
                    print('Starting code found')
                    print(starting_code)
                    break
