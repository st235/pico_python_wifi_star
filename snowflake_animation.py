from random import uniform


class SnowflakeAnimation:
    def __init__(self,
                 led_strip,
                 num_leds = 50,
                 intensity = 0.0002,
                 background_colour = [30, 50, 50],
                 snow_colour = [240, 255, 255],
                 fade_up_speed = 255,
                 fade_down_speed = 1):
        self.__led_strip = led_strip
        self.__num_leds = num_leds
        self.__intensity = intensity
        self.__background_colour = background_colour
        self.__snow_colour = snow_colour
        self.__fade_up_speed = fade_up_speed
        self.__fade_down_speed = fade_down_speed

        self.__current_leds = [[0] * 3 for i in range(self.__num_leds)]
        self.__target_leds = [[0] * 3 for i in range(self.__num_leds)]

    def __display_current(self):
        for i in range(self.__num_leds):
            self.__led_strip.set_rgb(i, self.__current_leds[i][0], self.__current_leds[i][1], self.__current_leds[i][2])

    def __move_to_target(self):
        # nudge our current colours closer to the target colours
        for i in range(self.__num_leds):
            for c in range(3):  # 3 times, for R, G & B channels
                if self.__current_leds[i][c] < self.__target_leds[i][c]:
                    self.__current_leds[i][c] = min(self.__current_leds[i][c] + self.__fade_up_speed, self.__target_leds[i][c])  # increase current, up to a maximum of target
                elif self.__current_leds[i][c] > self.__target_leds[i][c]:
                    self.__current_leds[i][c] = max(self.__current_leds[i][c] - self.__fade_down_speed, self.__target_leds[i][c])  # reduce current, down to a minimum of target

    def next_step(self):
        for i in range(self.__num_leds):
            # randomly add snow
            if self.__intensity > uniform(0, 1):
                # set a target to start a snowflake
                self.__target_leds[i] = self.__snow_colour
            # slowly reset snowflake to background
            if self.__current_leds[i] == self.__target_leds[i]:
                self.__target_leds[i] = self.__background_colour
        self.__move_to_target() # nudge our current colours closer to the target colours
        self.__display_current() # display current colours to strip
