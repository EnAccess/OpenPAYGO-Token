from datetime import datetime
from encode_token import OPAYGOEncoder
from shared import OPAYGOShared


class SingleDeviceServerSimulator:

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
        self.count += 1
        return OPAYGOEncoder.generate_token_activation(
            starting_code=self.starting_code,
            key=self.key,
            value=OPAYGOShared.PAYG_DISABLE_VALUE,
            count=self.count,
            restricted_digit_set=self.restricted_digit_set
        )

    def generate_counter_sync_token(self):
        return OPAYGOEncoder.generate_token_activation(
            starting_code=self.starting_code,
            key=self.key,
            value=OPAYGOShared.COUNTER_SYNC_VALUE,
            count=self.count,
            restricted_digit_set=self.restricted_digit_set
        )

    def generate_token_from_date(self, new_expiration_date, force=False):
        self.expiration_date = new_expiration_date
        furthest_expiration_date = self.furthest_expiration_date
        if new_expiration_date > self.furthest_expiration_date:
            self.furthest_expiration_date = new_expiration_date
        value = self._get_value_to_activate()

        if value > OPAYGOShared.MAX_ACTIVATION_VALUE:
            if not force:
                raise Exception('TOO_MANY_DAYS_TO_ACTIVATE')
            else:
                value = OPAYGOShared.MAX_ACTIVATION_VALUE # Will need to be activated again after those days

        if new_expiration_date > furthest_expiration_date:
            # If the date is strictly above the furthest date activated, use ADD
            return self._generate_token_from_value(value, mode=OPAYGOShared.TOKEN_TYPE_ADD_TIME)
        else:
            # If the date is below or equal to the furthest date activated, use SET
            return self._generate_token_from_value(value, mode=OPAYGOShared.TOKEN_TYPE_SET_TIME)

    def _generate_token_from_value(self, value, mode):
        self.count += 1
        return OPAYGOEncoder.generate_token_activation(
            starting_code=self.starting_code,
            key=self.key,
            value=value,
            count=self.count,
            mode=mode,
            restricted_digit_set=self.restricted_digit_set
        )

    def _get_value_to_activate(self):
        if self.expiration_date <= datetime.now():
            return 0
        else:
            days = self._timedelta_to_days(self.expiration_date - datetime.now())
            return int(round(days*self.time_divider, 0))

    @staticmethod
    def _timedelta_to_days(this_timedelta):
        return this_timedelta.days + (this_timedelta.seconds / 3600 / 24)
