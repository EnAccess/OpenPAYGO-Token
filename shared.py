import siphash
import struct


class OPAYGOShared:
    MAX_ACTIVATION_VALUE = 995
    PAYG_DISABLE_VALUE = 998
    COUNTER_SYNC_VALUE = 999
    TOKEN_VALUE_OFFSET = 1000
    TOKEN_TYPE_SET_TIME = 1
    TOKEN_TYPE_ADD_TIME = 2

    @classmethod
    def get_token_base(cls, code):
        return int(code % cls.TOKEN_VALUE_OFFSET)

    @classmethod
    def put_base_in_token(cls, token, token_base):
        return token - cls.get_token_base(token) + token_base

    @classmethod
    def generate_next_token(cls, last_code, key):
        conformed_token = struct.pack('>L', last_code) # We convert the token to bytes
        conformed_token += conformed_token # We duplicate it to fit the minimum length
        token_hash = siphash.SipHash_2_4(key, conformed_token).hash() # We hash it
        new_token = cls._convert_hash_to_token(token_hash) # We convert to token and return
        return new_token

    @classmethod
    def _convert_hash_to_token(cls, this_hash):
        hash_int = struct.pack('>Q', this_hash) # We convert the hash to bytes
        hi_hash = int.from_bytes(hash_int[0:4], byteorder='big', signed=False) # We split it in two 32bits INT
        lo_hash = int.from_bytes(hash_int[4:8], byteorder='big', signed=False)
        result_hash = hi_hash ^ lo_hash # We XOR the two together to get a single 32bits INT
        token = cls._convert_to_29_5_bits(result_hash) # We convert the 32bits value to an INT no greater than 9 digits
        return token

    @classmethod
    def _convert_to_29_5_bits(cls, source):
        mask = ((1 << (32 - 2 + 1)) - 1) << 2
        temp = (source & mask) >> 2
        if temp > 999999999:
            temp = temp - 73741825
        return temp


