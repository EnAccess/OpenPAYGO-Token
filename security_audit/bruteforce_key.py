from encode_token import OPAYGOEncoder
from shared import OPAYGOShared
import codecs

# We know the starting code, and we know 3 tokens with count and value

known_value = 7
code_count_1 = int('16609796')
code_count_2 = int('395084796')
code_count_3 = int('682637796')
starting_code = 123456789


if __name__ == '__main__':
    print('Trying to bruteforce the key...')

    token_base = OPAYGOShared.get_token_base(code_count_1) - known_value

    for i in range(2**64):
        if i % 10000 == 0:
            print(str(round((i/(2**64))*100, 10))+'%')

        device_key = i.to_bytes(16, 'big')
        #print(device_key)

        count, activation_code = OPAYGOEncoder.generate_standard_token(
            starting_code=starting_code,
            key=device_key,
            value=known_value,
            count=1
        )

        if activation_code == code_count_1:
            print('Level 1 Match found!')
            print(device_key)

            count, activation_code_2 = OPAYGOEncoder.generate_standard_token(
                starting_code=starting_code,
                key=device_key,
                value=known_value,
                count=count
            )

            if activation_code_2 == code_count_2:
                print('Level 2 Match found!')
                print(device_key)

                count, activation_code_3 = OPAYGOEncoder.generate_standard_token(
                    starting_code=starting_code,
                    key=device_key,
                    value=known_value,
                    count=count
                )

                if activation_code_3 == code_count_3:
                    print('Level 3 Match found')
                    print(device_key)
                    break
