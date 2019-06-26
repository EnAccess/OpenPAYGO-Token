from shared import OPAYGOShared


class OPAYGOEncoder:

    @classmethod
    def generate_token_activation(cls, starting_code, key, value, count):
        # We get the first 3 digits with encoded value
        starting_code_base = OPAYGOShared.get_token_base(starting_code)
        token_base = cls._encode_base(starting_code_base, value)
        current_token = OPAYGOShared.put_base_in_token(starting_code, token_base)
        for xn in range(1, count + 1):
            current_token = OPAYGOShared.generate_next_token(current_token, key)
        final_token = OPAYGOShared.put_base_in_token(current_token, token_base)
        return final_token

    @classmethod
    def _encode_base(cls, base, number):
        if number + base > 999:
            return number + base - 1000
        else:
            return number + base
