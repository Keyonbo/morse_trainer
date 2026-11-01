# Morse Trainer

**DIY Morse code trainer powered by Raspberry Pi Pico H and MicroPython.**

This repository captures the first stable prototype of Morse Trainer, **v1.3**. It was developed incrementally using Thonny and is now organized for further development with VS Code and Git.

## Current features

- Send Morse manually using a momentary push button.
- Hear the signal through a passive PS1240 piezo buzzer.
- Mirror key presses with a red LED (series 330 Ω resistor).
- Decode the international Morse alphabet (A–Z and 0–9).
- Detect letters and spaces using fixed timing thresholds.
- Accumulate decoded text on a 128×64 SSD1306 OLED screen.
- Clear the message using a dedicated RESET button.
- Print decoding events to the serial REPL.

**Status:** Keying, audio, display, and text decoding were tested successfully in earlier builds. The RESET button and LED are implemented in v1.3; final end-to-end testing of those latest additions has not yet been reported. This is a code snapshot, not a claim of verified new hardware behavior.

## Hardware

| Part | Device connection |
| --- | --- |
| Raspberry Pi Pico H (RP2040) | Main controller |
| MORSE push button | GP14 / physical pin 19 → button → GND |
| RESET push button | GP16 / physical pin 21 → button → GND |
| Passive PS1240 piezo buzzer | GP15 / physical pin 20 (+) and GND (−) |
| Red LED | GP17 / physical pin 22 → **330 Ω** → LED anode (+), LED cathode (−) → GND |
| OLED SSD1306 (I²C, 128×64) | GP0 / pin 1 → SDA; GP1 / pin 2 → SCL; 3V3(OUT) / pin 36 → VCC; GND → GND |

All GND pins are electrically common. See [`docs/wiring.md`](docs/wiring.md) for a complete pin table and notes.

## Repository layout

```text
morse-trainer/
├── device/
│   └── main.py           # Working MicroPython firmware v1.3
├── docs/
│   ├── wiring.md         # Physical wiring and electrical notes
│   ├── development.md    # VS Code + Pico development workflow
│   └── roadmap.md        # Planned features (not implemented)
├── tests/
│   └── test_source_contract.py  # Host-side checks, no hardware needed
├── .vscode/
│   ├── extensions.json
│   └── settings.json
├── .gitignore
├── CHANGELOG.md
└── README.md
```

## Getting started with VS Code

1. Install [Visual Studio Code](https://code.visualstudio.com/) and the [MicroPico extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go).
2. Open the **repository root** (not the `device` directory) in VS Code.
3. Connect your Raspberry Pi Pico H via USB. **Close Thonny** first so it does not hold the serial port.
4. Open `device/main.py`. Use **MicroPico: Run current file on Pico** to test without saving the script as a startup program.
5. Once you are ready to deploy, use **MicroPico: Upload project to Pico**. The repository specifies `micropico.syncFolder: "device"`, so README/docs/tests are not sent to the board. The file appears as `/main.py` on the Pico and starts at power-on.

For MicroPico IntelliSense, you may run **MicroPico: Initialize MicroPico project**. If you do, verify that `.vscode/settings.json` still retains `"micropico.syncFolder": "device"`.

**OLED driver prerequisite:** The existing board already has `ssd1306.py` in `/lib` and the code has worked with it. This repository intentionally does **not** replace that installed driver. For another Pico, install a compatible MicroPython SSD1306 driver (e.g. `micropython-ssd1306` using Thonny's package manager) before running `main.py`. See [`docs/development.md`](docs/development.md).

## Behavior and timing

| Setting | v1.3 value |
| --- | ---: |
| Dot/dash threshold | 200 ms |
| End-of-letter pause | 700 ms |
| Word separator (evaluated before next key press) | 1700 ms |
| Audio PWM frequency | 2000 Hz |
| OLED I²C frequency | 100 kHz |
| OLED I²C timeout | 500,000 µs |
| OLED address | `0x3C` |

The thresholds are fixed in this version and are not yet tied to WPM.

## Test the repository locally

From the repository root, with Python 3 installed:

```bash
python -m unittest discover -s tests -v
```

These are static source-level checks. To test real GPIO, OLED output and sound, run the firmware on the Pico.

## Next milestones

- Listening / reception trainer (automatic playback of random letters).
- Adjustable WPM using the existing 10 kΩ potentiometer.
- MENU / OK controls and multiple operating modes.
- Better debounce and configurable letter timing.
- Enclosure and safe battery-powered operation.

See [`docs/roadmap.md`](docs/roadmap.md).

## Publishing

This project contains **no secrets**. Choose your preferred repository visibility on GitHub, and do not enable generated README or `.gitignore` when creating the empty remote repository (those are already included locally).

No project-wide license has been selected. Choose a license before inviting external contributions or re-use.
