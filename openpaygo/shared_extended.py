import siphash
import struct


class OPAYGOSharedExtended(object):
    MAX_BASE = 999999
    MAX_ACTIVATION_VALUE = 999999
    TOKEN_VALUE_OFFSET_EXTENDED = 1000000

    @classmethod
    def get_token_base(cls, code):
        return int(code % cls.TOKEN_VALUE_OFFSET_EXTENDED)

    @classmethod
    def put_base_in_token(cls, token, token_base):
        if token_base > cls.MAX_BASE:
            Exception('INVALID_VALUE')
        return token - cls.get_token_base(token) + token_base

    @classmethod
    def generate_next_token(cls, last_code, key):
        conformed_token = struct.pack('>Q', last_code) # We convert the token to bytes
        token_hash = siphash.SipHash_2_4(key, conformed_token).hash() # We hash it
        new_token = cls._convert_hash_to_token(token_hash) # We convert to token and return
        return new_token

    @classmethod
    def _convert_hash_to_token(cls, this_hash):
        token = cls._convert_to_40_bits(this_hash) # We convert the 64bits value to an INT no greater than 12 digits
        return token

    @classmethod
    def _convert_to_40_bits(cls, source):
        mask = ((1 << (64 - 24 + 1)) - 1) << 24
        temp = (source & mask) >> 24
        if temp > 999999999999:
            temp = temp - 99511627777
        return temp

    @classmethod
    def convert_to_4_digit_token(cls, source):
        restricted_digit_token = ''
        bit_array = cls._bit_array_from_int(source, 40)
        for i in range(20):
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
