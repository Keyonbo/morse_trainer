# Wiring — Morse Trainer v1.3

Board: **Raspberry Pi Pico H (RP2040)**. Physical pin numbers refer to the 40-pin board header, viewed with USB at the top and component side facing up.

| Signal | GPIO | Physical pin | Connected part / connection |
| --- | --- | ---: | --- |
| OLED SDA | GP0 | 1 | SSD1306 SDA |
| OLED SCL | GP1 | 2 | SSD1306 SCL |
| OLED GND | GND | 3 or another GND | SSD1306 GND |
| MORSE input | GP14 | 19 | One side of momentary switch; other side to GND |
| Piezo output | GP15 | 20 | PS1240 positive (+); negative (−) to GND |
| RESET input | GP16 | 21 | One side of momentary switch; other side to GND |
| LED output | GP17 | 22 | Series 330 Ω resistor then LED anode (+) |
| GND | GND | 23 / 28 / 38 etc. | LED cathode (−) and common return |
| OLED power | 3V3(OUT) | 36 | SSD1306 VCC |

## Wiring notes

- The firmware enables the Pico's internal pull-ups for MORSE and RESET; no external pull-up resistors are required for these switches.
- For the four-leg tactile push buttons, use two terminals from opposite electrically separate sides. Check with a multimeter if in doubt.
- Put the **330 Ω resistor in series** with the ordinary LED, not parallel. The resistor can be before or after the LED.
- All Pico GND header pins are common; use a breadboard ground rail if you run out of header connectors.
- Power the SSD1306 from **3.3 V**, not 5 V, unless the module's own documentation specifically supports a higher input.
- The PS1240 piezo is driven at 2 kHz, matching the version already tested.
- **Disconnect USB power when rewiring or soldering.** Check for shorts between adjacent contacts.

## Battery operation — not implemented yet

A battery holder, power switch, and a verified power wiring arrangement will be added later. The Pico's VSYS input supports a regulated or appropriately rated supply, but **never connect a raw 9 V battery directly to VSYS or a GPIO**. Avoid simultaneously connecting an external supply and USB until the power path is designed and checked.

## Future expansion (not connected in v1.3)

- MENU button: proposed GP18.
- OK button: proposed GP19.
- 10 kΩ potentiometer wiper: proposed GP26 / ADC0 (physical pin 31), outer legs to 3V3(OUT) and GND.

These are **proposed assignments**, not v1.3 connections.

Official pinout: https://datasheets.raspberrypi.com/pico/Pico-2-Pinout.pdf
