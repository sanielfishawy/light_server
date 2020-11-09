class StateHelper:
    POWER_KEY = 'power'

    @classmethod
    def get_default_state(cls):
        return {
            cls.POWER_KEY: False,
        }


class LightState:

    def __init__(self):
        self.state = StateHelper.get_default_state()

    def getState(self):
        return self.state

    def getPower(self):
        return self.getState()[StateHelper.POWER_KEY]

    def setPower(self, power):
        self.state[StateHelper.POWER_KEY] = power
        return self




