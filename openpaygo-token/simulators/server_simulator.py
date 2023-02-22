from datetime import datetime
from ..encode_token import OPAYGOEncoder
from ..shared import OPAYGOShared


class SingleDeviceServerSimulator(object):

    def __init__(self, starting_code, key, starting_count=1, restricted_digit_set=False, time_divider=1):
        self.starting_code = starting_code
        self.key = key
        self.count = starting_count
        self.expiration_date = datetime.now()
        self.furthest_expiration_date = datetime.now()
        self.payg_enabled = True
        self.time_divider = time_divider
        self.restricted_digit_set = restricted_digit_set

    def print_status(self):
        print('Expiration Date: '+ str(self.expiration_date))
        print('Current count: '+str(self.count))
        print('PAYG Enabled: '+str(self.payg_enabled))

    def generate_payg_disable_token(self):
        self.count, token = OPAYGOEncoder.generate_standard_token(
            starting_code=self.starting_code,
            key=self.key,
            value=OPAYGOShared.PAYG_DISABLE_VALUE,
            count=self.count,
            restricted_digit_set=self.restricted_digit_set
        )
        return SingleDeviceServerSimulator._format_token(token)

    def generate_counter_sync_token(self):
        self.count, token = OPAYGOEncoder.generate_standard_token(
            starting_code=self.starting_code,
            key=self.key,
            value=OPAYGOShared.COUNTER_SYNC_VALUE,
            count=self.count,
            restricted_digit_set=self.restricted_digit_set
        )
        return SingleDeviceServerSimulator._format_token(token)

    def generate_token_from_date(self, new_expiration_date, force=False):
        furthest_expiration_date = self.furthest_expiration_date
        if new_expiration_date > self.furthest_expiration_date:
            self.furthest_expiration_date = new_expiration_date

        if new_expiration_date > furthest_expiration_date:
            # If the date is strictly above the furthest date activated, use ADD
            value = self._get_value_to_activate(new_expiration_date, self.expiration_date, force)
            self.expiration_date = new_expiration_date
            return self._generate_token_from_value(value, mode=OPAYGOShared.TOKEN_TYPE_ADD_TIME)
        else:
            # If the date is below or equal to the furthest date activated, use SET
            value = self._get_value_to_activate(new_expiration_date, datetime.now(), force)
            self.expiration_date = new_expiration_date
            return self._generate_token_from_value(value, mode=OPAYGOShared.TOKEN_TYPE_SET_TIME)

    def _generate_token_from_value(self, value, mode):
        self.count, token = OPAYGOEncoder.generate_standard_token(
            starting_code=self.starting_code,
            key=self.key,
            value=value,
            count=self.count,
            mode=mode,
            restricted_digit_set=self.restricted_digit_set
        )
        return SingleDeviceServerSimulator._format_token(token)

    def _generate_extended_value_token(self, value):
        pass

    def _get_value_to_activate(self, new_time, reference_time, force_maximum=False):
        if new_time <= reference_time:
            return 0
        else:
            days = self._timedelta_to_days(new_time - reference_time)
            value = int(round(days*self.time_divider, 0))
            if value > OPAYGOShared.MAX_ACTIVATION_VALUE:
                if not force_maximum:
                    raise Exception('TOO_MANY_DAYS_TO_ACTIVATE')
                else:
                    return OPAYGOShared.MAX_ACTIVATION_VALUE  # Will need to be activated again after those days
            return value

    @staticmethod
    def _timedelta_to_days(this_timedelta):
        return this_timedelta.days + (this_timedelta.seconds / 3600 / 24)

    @staticmethod
    def _format_token(token):
        token = str(token)
        if len(token) < 9:
            token = '0' * (9 - len(token)) + token
        return token
