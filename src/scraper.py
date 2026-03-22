from yt_dlp import YoutubeDL

def search_youtube(query, max_results=10):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    search_url = f"ytsearch{max_results}:{query}"

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_url, download=False)

    return info.get('entries', [])