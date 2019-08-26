from shared import OPAYGOShared


class OPAYGOEncoder:

    @classmethod
    def generate_token_activation(cls, starting_code, key, value, count,
                                  mode=OPAYGOShared.TOKEN_TYPE_SET_TIME, restricted_digit_set=False):
        # We get the first 3 digits with encoded value
        starting_code_base = OPAYGOShared.get_token_base(starting_code)
        token_base = cls._encode_base(starting_code_base, value)
        current_token = OPAYGOShared.put_base_in_token(starting_code, token_base)
        current_count_odd = count % 2
        if mode == OPAYGOShared.TOKEN_TYPE_SET_TIME:
            if current_count_odd: # Odd numbers are for Set Time
                new_count = count+2
            else:
                new_count = count+1
        else:
            if current_count_odd: # Even numbers are for Add Time
                new_count = count+1
            else:
                new_count = count+2
        for xn in range(1, new_count):
            current_token = OPAYGOShared.generate_next_token(current_token, key)
        final_token = OPAYGOShared.put_base_in_token(current_token, token_base)
        if restricted_digit_set:
            final_token = OPAYGOShared.convert_to_4_digit_token(final_token)
        return final_token

    @classmethod
    def _encode_base(cls, base, number):
        if number + base > 999:
            return number + base - 1000
        else:
            return number + base
