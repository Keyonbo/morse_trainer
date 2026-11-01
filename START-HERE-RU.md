# Начало работы (русский)

## Открываем проект в VS Code

1. Распакуй `morse-trainer.zip` в удобное место.
2. В VS Code выбери **File → Open Folder** и открой `morse-trainer`.
3. Установи расширение **MicroPico** (оно предлагается в `extensions.json`).
4. Закрой Thonny, подключи Pico по USB.
5. Открой `device/main.py` и запускай через **MicroPico: Run current file on Pico**.

Не перепрошивай MicroPython заново: он уже установлен. Не перезаписывай `/lib/ssd1306.py` на Pico: он уже работает. VS Code нужен для дальнейшей разработки и Git, а не для смены прошивки.

Если захочешь автономный запуск, отдельно загрузи **только папку `device`** командой **MicroPico: Upload project to Pico**. Для этого в `.vscode/settings.json` установлен параметр `micropico.syncFolder = "device"`.

## Создаём Git-репозиторий

Открой VS Code Terminal в корне проекта и выполни:

```powershell
git init -b main
git add .
git commit -m "Initial Morse Trainer v1.3"
```

Если `git` не найден, установи [Git for Windows](https://git-scm.com/downloads/win). При первой настройке Git может попросить `user.name` и `user.email` — используй свои данные.

## Публикуем на GitHub

Создай на https://github.com/new **пустой** репозиторий `morse-trainer` (НЕ выбирай auto-create README/.gitignore/license). Затем в терминале:

```powershell
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/morse-trainer.git
git push -u origin main
```

Заменить `YOUR_GITHUB_USERNAME` на собственный GitHub username. Если Git попросит авторизацию — пройди стандартный вход через браузер/credential manager.

Подробности на английском: `README.md` и `docs/development.md`.
