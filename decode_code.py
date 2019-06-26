from shared import OPAYGOShared


class OPAYGODecoder:
    MAX_TOKEN_JUMP = 50

    @classmethod
    def get_activation_value_and_count_from_token(cls, token, starting_code, key, last_count):
        token_base = OPAYGOShared.get_token_base(token) # We get the base of the token
        current_code = OPAYGOShared.put_base_in_token(starting_code, token_base) # We put it into the starting code
        starting_code_base = OPAYGOShared.get_token_base(starting_code) # We get the base of the starting code
        for count in range(0, last_count + cls.MAX_TOKEN_JUMP + 1): # We try all combination up until last_count + CODE_JUMP
            masked_token = OPAYGOShared.put_base_in_token(current_code, token_base)
            if masked_token == token and count > last_count:
                value = cls._decode_base(starting_code_base, token_base) # If there is a match we get the value from the token
                return value, count
            current_code = OPAYGOShared.generate_next_token(current_code, key) # If not we go to the next token
        return None, None

    @classmethod
    def _decode_base(cls, starting_code_base, token_base):
        decoded_value = token_base - starting_code_base
        if decoded_value < 0:
            return decoded_value + 1000
        else:
            return decoded_value
