from datetime import datetime, timedelta
from shared import OPAYGOShared
from decode_token import OPAYGODecoder


class DeviceSimulator:

    def __init__(self, starting_code, key, starting_count=0):
        self.starting_code = starting_code
        self.key = key
        self.count = starting_count
        self.expiration_date = datetime.now()
        self.payg_enabled = True

    def print_status(self):
        print('-------------------------')
        print('Expiration Date: '+ str(self.expiration_date))
        print('Current count: '+str(self.count))
        print('PAYG Enabled: '+str(self.payg_enabled))
        print('Active: '+str(self.is_active()))
        print('-------------------------')

    def is_active(self):
        return self.expiration_date > datetime.now()

    def enter_token(self, token):
        token_int = int(token)
        self._update_device_status_from_token(token_int)

    def _update_device_status_from_token(self, token):
        token_value, token_count, token_type = OPAYGODecoder.get_activation_value_count_and_type_from_token(
            token=token,
            starting_code=self.starting_code,
            key=self.key,
            last_count=self.count
        )
        if token_value is None:
            print('TOKEN_INVALID')
        else:
            self.count = token_count
            self._update_device_status_from_token_value(token_value, token_type)

    def _update_device_status_from_token_value(self, token_value, token_type):
        if token_value <= OPAYGOShared.MAX_ACTIVATION_VALUE:
            self.payg_enabled = True
            self._update_expiration_date_from_days(token_value, token_type)
        elif token_value == OPAYGOShared.PAYG_DISABLE_VALUE:
            self.payg_enabled = False
        elif token_value != OPAYGOShared.COUNTER_SYNC_VALUE:
            # We do nothing if its the sync counter value, the counter has been synced already
            print('COUNTER_SYNCED')
        else:
            # If it's another value we also do nothing, as they are not defined
            print('UNKNOWN_COMMAND')

    def _update_expiration_date_from_days(self, number_of_days, token_type):
        if token_type == OPAYGOShared.TOKEN_TYPE_SET_TIME:
            print('Mode: Set Time')
            self.expiration_date = datetime.now() + timedelta(days=number_of_days)
        else:
            print('Mode: Add Time')
            self.expiration_date = self.expiration_date + timedelta(days=number_of_days)
