from rpi_ws281x import *
import numpy as np

# LED strip configuration:
LED_COUNT      = 100      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
strip = None

'''
    Given:
        - frame: an iterable with n triplets of RGB (0-255 (int)) colors
    Lights the leds based on this colors
'''
def frame_to_leds(frame):
    if not strip:
        return 
    for i, value in enumerate(frame):
        r,g,b = value
        strip.setPixelColor(i, Color(int(r),int(g),int(b)))
    strip.show()

'''
    On start initialize strip
'''
# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()
# Set all pixels to 0 at start
frame_to_leds(np.zeros((LED_COUNT, 3)))
    