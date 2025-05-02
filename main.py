import os
import re
import json
import time
import random
import subprocess
from pytubefix import Playlist, YouTube
from pytubefix.exceptions import BotDetection


class FileUtils:
    @staticmethod
    def sanitize(name: str, max_length=100) -> str:
        name = re.sub(r'[\\/*?:"<>|]', '_', name)
        name = re.sub(r'\s+', ' ', name).strip()
        return name[:max_length]

    @staticmethod
    def exists(path: str) -> bool:
        return os.path.exists(path)


class ProgressBar:
    @staticmethod
    def callback(stream, chunk, bytes_remaining):
        total = stream.filesize or 1
        downloaded = total - bytes_remaining
        percent = int(downloaded / total * 100)
        bar_length = 50
        filled = int(bar_length * percent / 100)
        bar = '█' * filled + '-' * (bar_length - filled)
        print(f'\r  📥 [{bar}] {percent:3d}%', end='', flush=True)


class CacheManager:
    def __init__(self, path: str):
        self.path = path
        self.data = self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def save(self):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=2, ensure_ascii=False)


class YTDownloader:
    def __init__(self, ytdl_config: dict):
        self.config = ytdl_config
        self.cache = CacheManager(ytdl_config["cache_file"])
        self.ignore = ytdl_config["ignore_list"]
        self.downloaded = 0
        self._init_playlist()
        self._prepare_paths()

    def _init_playlist(self):
        if not self.cache.data:
            print("🔁 Lade Playlist von YouTube ...")
            pl = Playlist(self.config["playlist_url"])
            self.cache.data = {
                "channel_name": FileUtils.sanitize(pl.owner or "Kanal"),
                "video_ids": [v.video_id for v in pl.videos],
                "last_index": 0
            }
            self.cache.save()
        self.video_ids = self.cache.data["video_ids"]
        self.index = self.cache.data["last_index"]
        self.channel_name = self.cache.data["channel_name"]

    def _prepare_paths(self):
        self.channel_path = os.path.join(self.config["download_dir"], self.channel_name)
        os.makedirs(self.channel_path, exist_ok=True)

    def wait_animation(self, minutes: int):
        total_seconds = minutes * 60
        print(f"\n⏳ Wartezeit: {minutes} Minute(n)")
        for remaining in range(total_seconds, 0, -1):
            mins, secs = divmod(remaining, 60)
            print(f"\r🕒  Nächstes Video in {mins:02}:{secs:02} min", end='', flush=True)
            time.sleep(1)
        print("\r🟢 Fortsetzung...                      ")

    def _get_log_filename(self, video_id: str):
        return os.path.join(self.config["log_dir"], f"{video_id[:2]}.log")

    def _log_video_id(self, video_id: str, title: str):
        log_filename = self._get_log_filename(video_id)
        os.makedirs(self.config["log_dir"], exist_ok=True)
        with open(log_filename, "a", encoding="utf-8") as log_file:
            log_file.write(f"{video_id} | {title}\n")

    def download_video(self, yt: YouTube, filename: str) -> bool:
        safe_title = FileUtils.sanitize(yt.title)
        filepath = os.path.join(self.channel_path, filename)

        print(f"\n📹 Video-ID: {yt.video_id} | Titel: {yt.title}")  # Ausgabe der ID und des Titels

        for res in self.config["resolutions"]:
            prog = yt.streams.filter(progressive=True, file_extension="mp4", res=res).first()
            if prog:
                print(f"🎞️  {res} → {yt.title}")
                print("   ▶ Lade Video (Progressive)...")
                prog.download(output_path=self.channel_path, filename=filename)
                print("   ✅ Fertig.\n")
                self._log_video_id(yt.video_id, yt.title)  # Loggen der ID und des Titels
                return True

            vid = yt.streams.filter(adaptive=True, only_video=True, file_extension="mp4", res=res).first()
            aud = yt.streams.filter(adaptive=True, only_audio=True, file_extension="mp4").order_by("abr").desc().first()

            if vid and aud:
                print(f"\n🎞️  {res} (Muxed) → {yt.title}")
                tmp_v = os.path.join(self.channel_path, f"{safe_title}_v.mp4")
                tmp_a = os.path.join(self.channel_path, f"{safe_title}_a.mp4")

                print("   ▶ Lade Video...")
                vid.download(output_path=self.channel_path, filename=os.path.basename(tmp_v))

                print("   ▶ Lade Audio...")
                aud.download(output_path=self.channel_path, filename=os.path.basename(tmp_a))

                print("   🛠️  Baue Video zusammen...")
                subprocess.run([
                    "ffmpeg", "-y", "-i", tmp_v, "-i", tmp_a,
                    "-c:v", "copy", "-c:a", "aac", filepath
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                os.remove(tmp_v)
                os.remove(tmp_a)
                print("   ✅ Fertig.\n")
                self._log_video_id(yt.video_id, yt.title)  # Loggen der ID und des Titels
                return True

        return False

    def run(self):
        total = len(self.video_ids)

        for i in range(self.index, total):
            vid_id = self.video_ids[i]
            try:
                yt = YouTube(
                    url=f"https://www.youtube.com/watch?v={vid_id}",
                    on_progress_callback=ProgressBar.callback
                )

            except Exception as e:
                print(f"\n⚠️ Fehler: {vid_id} → {e}")
                continue

            safe_title = FileUtils.sanitize(yt.title)
            filename = f"{safe_title}.mp4"
            filepath = os.path.join(self.channel_path, filename)

            if yt.title in self.ignore or yt.video_id in self.ignore:
                print(f"\n⏭️ Übersprungen (Ignore): {yt.title}")
                continue
            if FileUtils.exists(filepath):
                print(f"\n⏭️ Übersprungen (vorhanden): {yt.title}")
                continue
            if self.downloaded >= self.config["max_downloads"]:
                print(f"\n🛑 Max. Anzahl ({self.config['max_downloads']}) erreicht.")
                break

            try:
                success = self.download_video(yt, filename)
                if success:
                    self.downloaded += 1
                else:
                    print(f"\n⚠️ Keine Streams für {yt.title}")
                    continue
            except BotDetection as e:
                print(f"\n🚫 Bot erkannt: {yt.title} → {e}")
                break
            except Exception as e:
                print(f"\n❌ Fehler bei {yt.title}: {e}")
                continue

            self.cache.data["last_index"] = i + 1
            self.cache.save()

            if self.downloaded < self.config["max_downloads"]:
                pause = random.randint(*self.config["wait_range"])
                self.wait_animation(pause)

        print("\n🏁 Fertig oder Limit erreicht.")


# === Startkonfiguration ===
if __name__ == "__main__":
    config = {
        "playlist_url": "https://www.youtube.com/@ct3003/videos",  # Beispiel Playlist-URL
        "download_dir": "downloads",
        "log_dir": "logs",  # Ordner für Log-Dateien
        "cache_file": "playlist_cache.json",
        "max_downloads": 50,
        "wait_range": (0, 0),  # in Minuten
        "resolutions": ["1080p", "720p", "480p", "360p", "240p", "144p"],
        "ignore_list": []
    }

    downloader = YTDownloader(config)
    downloader.run()
