PiFace Control and Display Diagram
==================================
PiFace Control and Display is connected to the Raspberry Pi through an SPI
port expander (MCP23S17, chip select = 1). Here is a diagram of pin locations::

                   | PortA0 |
                   | PortA1 |
                   | PortA2 |
    Input Switches | PortA3 |
                   | PortA4 |
                   | PortA5 |
                   | PortA6 |
                   | PortA7 | -- MCP23S17 -- SPI -- Raspberry Pi
    HD44780 Data 4 | PortB0 |        |                  |
    HD44780 Data 5 | PortB1 |        |             GPIO Pin 23 -- IR
    HD44780 Data 6 | PortB2 |   Interrupts ------- GPIO Pin 25
    HD44780 Data 7 | PortB3 |
    HD44780 Enable | PortB4 |
    HD44780 RW     | PortB5 |
    HD44780 RS     | PortB6 |
    Backlight      | PortB7 |

The HD44780 LCD must be configured to be in 4-bit mode since we only have
4 data connections.

MCP23S17 datasheet: http://ww1.microchip.com/downloads/en/devicedoc/21952b.pdf
HD44780 datasheet: https://www.sparkfun.com/datasheets/LCD/HD44780.pdf
