
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
- Node.js (für den YouTube-Token-Generator)
- Empfohlen: Nutzung in einer virtuellen Umgebung

### Installation

#### 1. Klonen des Repositories

```bash
git clone https://github.com/HalloWelt42/YTDownLodr.git
cd YTDownLodr
```

#### 2. Python-Virtualenv einrichten

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

#### 3. Node.js und den YouTube-Token-Generator installieren

Für den Token-Generator benötigen wir Node.js und den `youtube-po-token-generator`. Führe die folgenden Befehle aus, um Node.js zu installieren und den Token-Generator zu installieren:

1. **Installiere Node.js** (falls nicht bereits installiert):

   - macOS/Linux: Besuche [nodejs.org](https://nodejs.org/) und folge den Anweisungen.
   - Windows: Lade den Installer von [nodejs.org](https://nodejs.org/) herunter und installiere ihn.

2. **Installiere den Token-Generator:**

   ```bash
   npm install -g youtube-po-token-generator
   ```

#### 4. Token-Generierung sicherstellen

Stelle sicher, dass der `youtube-po-token-generator` ordnungsgemäß funktioniert, indem du folgenden Befehl ausführst:

```bash
youtube-po-token-generator
```

Dieser Befehl gibt ein Token zurück, das im Projekt automatisch verwendet wird.

## ▶️ Nutzung

Um den Downloader zu starten, führe folgenden Befehl aus:

```bash
python main.py

# oder
.venv/bin/python main.py 
```

📝 **Logs:**  
Geladene Video-IDs werden in `logs/` abgelegt. Die Dateien sind nach den ersten zwei Zeichen der Video-ID benannt, z.B.:

```
logs/ab.log
logs/jx.log
```

Diese Log-Struktur ermöglicht eine effiziente Speicherung, selbst bei sehr großen Playlists mit hunderttausenden IDs.

## 🔉 Audio-Only-Modus

Mit der Option `audio_only` in der `config.json` kannst du den Downloader in einen reinen Audio-Modus versetzen. In diesem Modus wird ausschließlich der beste Audiostream eines Videos heruntergeladen und automatisch in das MP3-Format konvertiert. Die Videospur wird vollständig ignoriert.

### Beispiel: `config.json`

```json
{
  "audio_only": true
}
```

### Verhalten:

- ✅ Wenn `audio_only: true`:  
  - Nur Audio wird heruntergeladen (`.webm`)
  - Automatische Umwandlung in `.mp3` mit `ffmpeg`
  - Ideal für Musik- oder Podcast-Playlists

- ✅ Wenn `audio_only: false`:  
  - Audio **und** Video werden separat geladen
  - Zusammenbau zu `.mp4` mit `ffmpeg`
  - Audiostream wird auch hier benötigt, aber **nicht konvertiert**

📌 Diese Einstellung spart Bandbreite und Speicherplatz, wenn nur der Ton benötigt wird, und erlaubt bei Bedarf trotzdem den vollständigen Video-Download.

## 🐞 Fehlerquellen

- **LoginRequired**: Manche Videos erfordern Anmeldung – sie werden automatisch übersprungen.
- **BotDetection**: Falls YouTube Anti-Bot-Mechanismen erkennt, wird der Vorgang sicher abgebrochen.

PS: der Token-Generator ist aktuell kurios : ) der scheint nicht genutzt zu werden oder ist outdated.