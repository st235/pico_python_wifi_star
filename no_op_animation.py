class NoOpAnimation:
    def __init__(self,
                 led_strip,
                 num_leds = 50):
        self.__led_strip = led_strip
        self.__num_leds = num_leds

    def next_step(self):
        for i in range(self.__num_leds):
            self.__led_strip.set_rgb(i, 0, 0, 0)
