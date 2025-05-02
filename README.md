# 🎬 YTDownLodr

Ein robuster, konfigurierbarer YouTube-Playlist-Downloader für automatisierte Abläufe, inklusive Caching, Fortschrittsanzeige, zufälliger Wartezeiten und strukturierter Log-Führung.

## 🔧 Features

- Lädt komplette YouTube-Playlists (oder Kanalvideos) herunter
- Fortschrittsbalken für Downloads (Video & Audio getrennt oder kombiniert)
- Zufällige Pause zwischen Downloads mit animierter Uhranzeige
- Automatisches Zusammenfügen von Video & Audio mit `ffmpeg`
- Caching der Playlist mit Fortschrittsstatus (JSON)
- Fehlerbehandlung für gesperrte Videos / Login-Pflicht
- Logging bereits geladener Video-IDs in aufgeteilten `.log`-Dateien
- Konfigurierbar per [config.json](./config.json)
- Einfach erweiterbar, modular aufgebaut

## 📦 Setup

### Voraussetzungen

- Python 3.9+
- `ffmpeg` (muss im Systempfad verfügbar sein)
- Empfohlen: Nutzung in einer virtuellen Umgebung

### Installation

```bash
git clone https://github.com/HalloWelt42/YTDownLodr.git
cd YTDownLodr
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### Nutzung

```bash
python yt_playlist.py
```

📝 Logs
Geladene Video-IDs werden in logs/ abgelegt. Die Dateien sind nach den ersten zwei Zeichen der Video-ID benannt, z.B.:

```
logs/ab.log
logs/jx.log
```

Diese Log-Struktur erlaubt effiziente Speicherung selbst bei sehr großen Playlists mit hunderttausenden IDs.

🐞 Fehlerquellen
LoginRequired: Manche Videos erfordern Anmeldung – sie werden automatisch übersprungen
BotDetection: Falls YouTube Anti-Bot-Mechanismen erkennt, wird der Vorgang sicher abgebrochen
