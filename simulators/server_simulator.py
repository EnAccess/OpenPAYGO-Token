from datetime import datetime
from encode_code import OPAYGOEncoder
from shared import OPAYGOShared


class SingleDeviceServerSimulator:

    def __init__(self, starting_code, key, starting_count=0):
        self.starting_code = starting_code
        self.key = key
        self.count = starting_count
        self.expiration_date = datetime.now()
        self.payg_enabled = True

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
            count=self.count
        )

    def generate_token_from_date(self, new_expiration_date, force=False):
        self.expiration_date = new_expiration_date
        days_to_activate = self._get_number_of_days_to_activate()
        if days_to_activate > OPAYGOShared.MAX_VALUE:
            if not force:
                raise Exception('TOO_MANY_DAYS_TO_ACTIVATE')
            else:
                days_to_activate = OPAYGOShared.MAX_VALUE # Will need to be activated again after those days
        return self._generate_token_from_days(days_to_activate)

    def _generate_token_from_days(self, days_to_activate):
        self.count += 1
        return OPAYGOEncoder.generate_token_activation(
            starting_code=self.starting_code,
            key=self.key,
            value=days_to_activate,
            count=self.count
        )

    def _get_number_of_days_to_activate(self):
        if self.expiration_date <= datetime.now():
            return 0
        else:
            return self._timedelta_to_days(self.expiration_date - datetime.now())

    def _timedelta_to_days(self, this_timedelta):
        return this_timedelta.days + int(round(this_timedelta.seconds / 3600 / 24, 0))
