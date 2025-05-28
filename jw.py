import time
from rpi_ws281x import *

# LED strip configuration:
LED_COUNT = 300         # Number of LED pixels.
LED_PIN = 18            # GPIO pin connected to the pixels (18 uses PWM).
LED_FREQ_HZ = 800000    # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10            # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255    # Overall strip brightness (0 to 255)
LED_INVERT = False      # True to invert the signal (use only if needed)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

def setStaticWhite(strip, brightness=255):
    """Set all LEDs to static white with a given brightness."""
    color = Color(brightness, brightness, brightness)  # Simulate brightness via RGB values
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def turnOffLEDs(strip):
    """Turn off all LEDs."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def setRangeColor(strip, start, end, color):
    """Set a range of pixels to the same color."""
    for i in range(start, end):
        strip.setPixelColor(i, color)
    strip.show()

def set_all_pixels(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def wheel(pos):
    """Generate rainbow colors across 0–255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def color_wave(strip, duration=10):
    """Rainbow shimmer wave animation."""
    for j in range(256):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(duration / 256.0)

def color_pulse(strip, color, pulse_count=3, interval=1):
    """Pulse a solid color on and off."""
    for _ in range(pulse_count):
        set_all_pixels(strip, color)
        time.sleep(interval / 2)
        turnOffLEDs(strip)
        time.sleep(interval / 2)

def chase(strip, color, delay=0.05, loops=2):
    """Chase effect: one bright pixel moving down the strip."""
    for _ in range(loops):
        for i in range(strip.numPixels()):
            turnOffLEDs(strip)
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(delay)

def alternate_flash(strip, color1, color2, flashes=3, interval=1):
    """Alternate two full-strip colors."""
    for _ in range(flashes):
        set_all_pixels(strip, color1)
        time.sleep(interval / 2)
        set_all_pixels(strip, color2)
        time.sleep(interval / 2)

def fade_out_white(strip, steps=20, duration=2):
    """Fade from white to black."""
    for i in range(steps, -1, -1):
        brightness = int(255 * i / steps)
        set_all_pixels(strip, Color(brightness, brightness, brightness))
        time.sleep(duration / steps)


try:
    color_wave(strip, duration=10)  # 10s
    color_pulse(strip, Color(255, 0, 0), pulse_count=3, interval=2)  # 6s
    chase(strip, Color(0, 255, 0), delay=0.03, loops=2)  # 6s
    alternate_flash(strip, Color(0, 0, 255), Color(255, 255, 0), flashes=3, interval=2)  # 6s
    fade_out_white(strip, steps=20, duration=2)  # 2s
    turnOffLEDs(strip)



    while True:
        pass
except KeyboardInterrupt:
    turnOffLEDs(strip)
