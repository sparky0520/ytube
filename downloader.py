import yt_dlp

def download(url, path="."):
    ydl_opts = {
        "format": "bv*+ba/best",   # best video + best audio
        "merge_output_format": "mp4",   # force final output to mp4
        "outtmpl": f"{path}/%(title)s.%(ext)s",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download complete!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    link = input("Enter YouTube link: ")
    download(link)
