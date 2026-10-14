"""Case-mounted 2.8-inch ILI9341 status display; touch and SD unused."""
from kmk.extensions import Extension

class KeyboardStatusDisplay(Extension):
    def __init__(self):
        self.previous_layer = None

    def during_bootup(self, sandbox):
        import board, busio, displayio, terminalio
        from fourwire import FourWire
        import adafruit_ili9341
        from adafruit_display_text import label
        displayio.release_displays()
        self.spi = busio.SPI(clock=board.GP26, MOSI=board.GP27)
        self.bus = FourWire(self.spi, command=board.GP22, chip_select=board.GP28,
                            baudrate=12_000_000)
        self.display = adafruit_ili9341.ILI9341(self.bus, width=240, height=320,
                                              rotation=0, auto_refresh=False)
        group = displayio.Group()
        group.append(label.Label(terminalio.FONT, text='Keyboard61', scale=2,
                                 color=0xE1E8EE, x=18, y=35))
        self.layer_label = label.Label(terminalio.FONT, text='Base layer', scale=2,
                                      color=0x72D5B1, x=18, y=105)
        group.append(self.layer_label)
        group.append(label.Label(terminalio.FONT, text='Turn: volume', color=0xE1E8EE,
                                 x=18, y=180))
        group.append(label.Label(terminalio.FONT, text='Press: mute', color=0xE1E8EE,
                                 x=18, y=205))
        self.display.root_group = group
        self.display.refresh()

    def after_matrix_scan(self, sandbox):
        current = sandbox.active_layers[0]
        if current != self.previous_layer:
            self.layer_label.text = 'Fn layer' if current == 1 else 'Base layer'
            self.display.refresh()
            self.previous_layer = current

