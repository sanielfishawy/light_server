from rpi_ws281x import PixelStrip
import asyncio
from threading import Thread

from periodic import Periodic
from light_state import LightState

class Light(Thread):

    def __init__(self, light_state:LightState):
        super().__init__()
        self.state = light_state
        self.periodic = None
        self.refresh_period_or_duty_cycle()

        self.strip = PixelStrip(150, 18)

    async def loop(self):
        while True:
            await self.periodic.wait_for_period_boundary()
            self.set_first_half_of_period()
            await self.periodic.wait_for_semi_period_boundary()
            self.set_second_half_of_period()

    def set_first_half_of_period(self):
        if not self.state.get_power():
            self.set_off()
        else:
            self.set_on()

    def set_second_half_of_period(self):
        if not self.state.get_power() or self.state.get_blink():
            self.set_off()
        else:
            self.set_on()

    def set_on(self):
        self.strip.setBrightness(self.state.get_brightness())
        for pixel in range(self.state.get_num_pixels()):
            self.strip.setPixelColorRGB(pixel, self.state.get_red(), self.state.get_green(), self.state.get_blue())
        self.strip.show()

    def set_off(self):
        for pixel in range(self.state.get_num_pixels()):
            self.strip.setPixelColorRGB(pixel, 0, 0, 0)
        self.strip.show()

    def refresh_period_or_duty_cycle(self):
        self.periodic = Periodic(
            period_sec=self.state.get_period(),
            semi_period_percent=self.state.get_duty_cycle()
        )

    def run(self):
        self.strip.begin()
        asyncio.run(self.loop())


if __name__ == '__main__':
    Light().start()

