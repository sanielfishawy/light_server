import logging

class StateHelper:
    NUM_PIXELS_KEY = 'num_pixels'
    POWER_KEY = 'power'
    BLINK_KEY = 'blink'

    MIN_FREQUENCY_KEY = 'min_frequency'
    MAX_FREQUENCY_KEY = 'max_frequency'
    DEFAULT_FREQUENCY_KEY = 'default_frequency'
    FREQUENCY_KEY = 'frequency'

    MIN_DUTY_CYCLE_KEY = 'min_duty_cycle'
    MAX_DUTY_CYCLE_KEY = 'max_duty_cycle'
    DUTY_CYCLE_KEY = 'duty_cycle'

    BRIGHTNESS_KEY = 'brightness'
    RED_KEY = 'red'
    GREEN_KEY = 'green'
    BLUE_KEY = 'blue'

    @classmethod
    def get_default_state(cls):
        return {
            cls.NUM_PIXELS_KEY: 136,
            cls.POWER_KEY: True,
            cls.BLINK_KEY: False,
            cls.MIN_FREQUENCY_KEY: 1,
            cls.MAX_FREQUENCY_KEY: 80,
            cls.DEFAULT_FREQUENCY_KEY: 40,
            cls.FREQUENCY_KEY: 2,
            cls.MIN_DUTY_CYCLE_KEY: 10,
            cls.MAX_DUTY_CYCLE_KEY: 80,
            cls.DUTY_CYCLE_KEY: 50,
            cls.BRIGHTNESS_KEY: 255,
            cls.RED_KEY: 127,
            cls.GREEN_KEY: 0,
            cls.BLUE_KEY: 0,
        }

class Limits:
    @classmethod
    def get_frequency_in_limits(cls, frequency) -> int:
        frequency = int(frequency)
        frequency = max(frequency, cls.get_min_frequency())
        frequency = min(frequency, cls.get_max_frequency())
        return frequency

    @classmethod
    def get_duty_cycle_in_limits(cls, duty_cycle) -> int:
        duty_cycle = int(duty_cycle)
        duty_cycle = max(duty_cycle, cls.get_min_duty_cycle())
        duty_cycle = min(duty_cycle, cls.get_max_duty_cycle())
        return duty_cycle

    @classmethod
    def get_color_bright_in_limits(cls, value) -> int:
        value = int(value)
        value = max(0, value)
        value = min(255, value)
        return value

    @classmethod
    def get_min_frequency(cls):
        return StateHelper.get_default_state()[StateHelper.MIN_FREQUENCY_KEY]

    @classmethod
    def get_max_frequency(cls):
        return StateHelper.get_default_state()[StateHelper.MAX_FREQUENCY_KEY]

    @classmethod
    def get_min_duty_cycle(cls):
        return StateHelper.get_default_state()[StateHelper.MIN_DUTY_CYCLE_KEY]

    @classmethod
    def get_max_duty_cycle(cls):
        return StateHelper.get_default_state()[StateHelper.MAX_DUTY_CYCLE_KEY]


class LightState:
    def __init__(self):
        self.state = StateHelper.get_default_state()

    def get_state(self):
        return self.state

    def get_num_pixels(self):
        return self.get_state()[StateHelper.NUM_PIXELS_KEY]

    def set_num_pixels(self, num_pixels: int):
        self.state[StateHelper.NUM_PIXELS_KEY] = num_pixels
        return self

    def get_power(self):
        return self.get_state()[StateHelper.POWER_KEY]

    def set_power(self, power: bool):
        self.state[StateHelper.POWER_KEY] = power
        return self

    def get_blink(self):
        return self.get_state()[StateHelper.BLINK_KEY]

    def set_blink(self, blink: bool):
        self.state[StateHelper.BLINK_KEY] = bool(blink)
        return self

    def get_frequency(self):
        return self.get_state()[StateHelper.FREQUENCY_KEY]

    def get_period(self):
        return 1.0 / self.get_frequency()

    def set_frequency(self, frequency: int):
        self.state[StateHelper.FREQUENCY_KEY] = Limits.get_frequency_in_limits(frequency)
        return self

    def get_duty_cycle(self):
        return self.get_state()[StateHelper.DUTY_CYCLE_KEY]

    def set_duty_cycle(self, duty_cycle: int):
        self.state[StateHelper.DUTY_CYCLE_KEY] = Limits.get_duty_cycle_in_limits(duty_cycle)

    def get_brightness(self):
        return self.get_state()[StateHelper.BRIGHTNESS_KEY]

    def set_brightness(self, brightness: int):
        self.state[StateHelper.BRIGHTNESS_KEY] = Limits.get_color_bright_in_limits(brightness)

    def get_red(self):
        return self.get_state()[StateHelper.RED_KEY]

    def set_red(self, red):
        self.state[StateHelper.RED_KEY] = Limits.get_color_bright_in_limits(red)
        return self

    def get_green(self):
        return self.get_state()[StateHelper.GREEN_KEY]

    def set_green(self, green):
        self.state[StateHelper.GREEN_KEY] = Limits.get_color_bright_in_limits(green)
        return self

    def get_blue(self):
        return self.get_state()[StateHelper.BLUE_KEY]

    def set_blue(self, blue):
        self.state[StateHelper.BLUE_KEY] = Limits.get_color_bright_in_limits(blue)
        return self