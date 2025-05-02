from pytubefix import YouTube
yt_id = "e6vPt_e9sRw"
video_url = f"https://www.youtube.com/watch?v={yt_id}"
download_path = "downloads"

yt = YouTube(video_url)
stream = yt.streams.get_highest_resolution()
stream.download(output_path=download_path)

print(f"Download abgeschlossen: {yt.title}")