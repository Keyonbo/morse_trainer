# Development workflow

## Current toolchain

- Raspberry Pi Pico H with **MicroPython already installed**.
- Thonny was used to prototype and validate earlier versions.
- VS Code + MicroPico is the planned development environment.
- A compatible `ssd1306.py` driver is already installed at `/lib/ssd1306.py` on the user's current Pico.

## Working in VS Code

1. Install VS Code and the **MicroPico** extension (`paulober.pico-w-go`).
2. Close Thonny (the serial port cannot usually be used by both simultaneously).
3. Open the `morse-trainer` **root** folder in VS Code.
4. Connect the Pico by USB. MicroPython is already on the board; do not reflash it just to change editors.
5. Open `device/main.py`.
6. Use `Ctrl+Shift+P` → **MicroPico: Run current file on Pico** to execute and test it.
7. After confirming it works, use **MicroPico: Upload project to Pico** to make `device/main.py` available as `/main.py` for automatic startup.

The `.vscode/settings.json` file sets:

```json
{
  "micropico.syncFolder": "device",
  "micropico.autoConnect": true
}
```

**Important:** Do not upload the repository root. Only `device/` is meant to be copied to the Pico. This prevents unnecessary files such as README and tests from occupying its flash storage.

Running a file remotely and installing it as `/main.py` are separate actions: the former tests the firmware, the latter makes it run at power-on.

## SSD1306 dependency

The `ssd1306` driver is **not included** in the repo because the exact copy currently on the board is working, and replacing it would risk changing the working hardware setup. The current Pico should keep `/lib/ssd1306.py` intact.

To set up a *new* Pico, install a compatible `micropython-ssd1306` module to `/lib` using Thonny's **Tools → Manage packages**, or follow upstream MicroPython package instructions. Confirm this import works:

```python
from ssd1306 import SSD1306_I2C
```

If the display initially returns `OSError: [Errno 110] ETIMEDOUT`, verify wiring and the I²C timeout. The proven settings for the present hardware are:

```python
I2C(0, sda=Pin(0), scl=Pin(1), freq=100000, timeout=500000)
```

## Static tests

Run on the **computer**, not Pico:

```bash
python -m unittest discover -s tests -v
```

These tests inspect the frozen firmware and verify alphabet/timing/pin assignments. They cannot replace device testing.

## Releasing later versions

1. Keep `device/main.py` on a working revision.
2. Make one functional change at a time.
3. Test on Pico.
4. Update CHANGELOG and documentation.
5. Commit and tag a release once hardware testing is confirmed.
