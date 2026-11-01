# Changelog

## [1.3] — 2026-10-29 (code snapshot)

- Added GP17 LED indicator synchronized to the MORSE button.
- LED turns off during RESET.
- Kept existing audio, OLED, and Morse decoding behavior.
- Latest LED change has not yet been confirmed by a subsequent hardware test in the recorded development history.

## [1.2] — 2026-10-29

- Added a dedicated GP16 RESET button to clear the message and current sequence.

## [1.1] — 2026-10-27

- Added full international Morse alphabet (A–Z) and digits (0–9).
- Added accumulated message and automatic spacing between words.
- Displays up to 32 recent characters on the OLED; prints message in REPL.

## [1.0] — 2026-10-27

- Validated Pico H, MicroPython, key, PS1240 buzzer, and SSD1306 OLED.
- Recognized initial sample of Morse characters.
- Stable OLED configuration: `I2C(0, freq=100000, timeout=500000)` with address `0x3C`.
