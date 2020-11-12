from periodic import Periodic
from rpi_ws281x import PixelStrip
import asyncio

class light:

    def __init__(self, num_pixels=150):
        self.num_pixels = num_pixels

        self.periodic = Periodic(period_sec=.025)
        self.strip = PixelStrip(150, 18)
        self.strip.begin()

    async def flash(self):
        while True:
            await self.periodic.wait_for_period_boundary()
            self.set_red()
            await self.periodic.wait_for_semi_period_boundary()
            self.set_off()

    def set_red(self):
        for pixel in range(self.num_pixels-1):
            self.strip.setPixelColorRGB(pixel, 100, 0, 0)
        self.strip.show()

    def set_off(self):
        for pixel in range(self.num_pixels-1):
            self.strip.setPixelColorRGB(pixel, 0, 0, 0)
        self.strip.show()


if __name__ == '__main__':
    light = light()
    asyncio.run(light.flash())
    pass

