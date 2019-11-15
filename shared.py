import siphash
import struct


class OPAYGOShared(object):
    MAX_BASE = 999
    MAX_ACTIVATION_VALUE = 995
    PAYG_DISABLE_VALUE = 998
    COUNTER_SYNC_VALUE = 999
    TOKEN_VALUE_OFFSET = 1000
    TOKEN_TYPE_SET_TIME = 1
    TOKEN_TYPE_ADD_TIME = 2

    @classmethod
    def get_token_base(cls, code):
        return int(code) % cls.TOKEN_VALUE_OFFSET

    @classmethod
    def put_base_in_token(cls, token, token_base):
        if token_base > cls.MAX_BASE:
            Exception('INVALID_VALUE')
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
        hi_hash = struct.unpack('>L', hash_int[0:4])[0]  # We split it in two 32bits INT
        lo_hash = struct.unpack('>L', hash_int[4:8])[0]
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

    @classmethod
    def convert_to_4_digit_token(cls, source):
        restricted_digit_token = ''
        bit_array = cls._bit_array_from_int(source, 30)
        for i in range(15):
            this_array = bit_array[i*2:(i*2)+2]
            restricted_digit_token += str(cls._bit_array_to_int(this_array)+1)
        return int(restricted_digit_token)

    @classmethod
    def convert_from_4_digit_token(cls, source):
        bit_array = []
        for digit in str(source):
            digit = int(digit) - 1
            this_array = cls._bit_array_from_int(digit, 2)
            bit_array += this_array
        return cls._bit_array_to_int(bit_array)

    @classmethod
    def _bit_array_to_int(cls, bit_array):
        integer = 0
        for bit in bit_array:
            integer = (integer << 1) | bit
        return integer

    @classmethod
    def _bit_array_from_int(cls, source, bits):
        bit_array = []
        for i in range(bits):
            bit_array += [bool(source & (1 << (bits - 1 - i)))]
        return bit_array
