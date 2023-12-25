class ColorAnimation:
    def __init__(self,
                 led_strip,
                 color,
                 num_leds = 50):
        self.__led_strip = led_strip
        self.__num_leds = num_leds
        self.__color = color

    def __hex_to_rgb(self, hex):
        # converts a hex colour code into RGB
        if '#' in hex:
            hex = hex.lstrip('#')
        r, g, b = (int(hex[i:i + 2], 16) for i in (0, 2, 4))
        return r, g, b

    def next_step(self):
        for i in range(self.__num_leds):
            r, g, b = self.__hex_to_rgb(self.__color)
            self.__led_strip.set_rgb(i, r, g, b)
