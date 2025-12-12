"""
YouTube Video Downloader Module

Dependencies:
    pip install yt-dlp

Usage:
    from youtube_downloader import YouTubeDownloader
    
    downloader = YouTubeDownloader()
    downloader.download('https://www.youtube.com/watch?v=VIDEO_ID')
"""

import yt_dlp
import os
from pathlib import Path


class YouTubeDownloader:
    def __init__(self, output_path='downloads'):
        """
        Initialize the YouTube downloader.
        
        Args:
            output_path: Directory where videos will be saved
        """
        self.output_path = Path(output_path)
        self.output_path.mkdir(exist_ok=True)
    
    def download(self, url, quality='best', audio_only=False, progress=True):
        """
        Download a YouTube video.
        
        Args:
            url: YouTube video URL
            quality: Video quality ('best', 'worst', or specific like '720p')
            audio_only: Download only audio (mp3)
            progress: Show download progress
            
        Returns:
            dict: Download information including file path
        """
        ydl_opts = {
            'outtmpl': str(self.output_path / '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook] if progress else [],
        }
        
        if audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            if quality == 'best':
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
            elif quality == 'worst':
                ydl_opts['format'] = 'worst'
            else:
                ydl_opts['format'] = f'bestvideo[height<={quality.replace("p", "")}]+bestaudio/best'
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return {
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader'),
                    'file_path': ydl.prepare_filename(info)
                }
        except Exception as e:
            raise Exception(f"Download failed: {str(e)}")
    
    def get_info(self, url):
        """
        Get video information without downloading.
        
        Args:
            url: YouTube video URL
            
        Returns:
            dict: Video metadata
        """
        ydl_opts = {'quiet': True}
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader'),
                    'description': info.get('description'),
                    'view_count': info.get('view_count'),
                    'thumbnail': info.get('thumbnail'),
                    'formats': [
                        {
                            'format_id': f.get('format_id'),
                            'ext': f.get('ext'),
                            'resolution': f.get('resolution'),
                            'filesize': f.get('filesize')
                        }
                        for f in info.get('formats', [])
                    ]
                }
        except Exception as e:
            raise Exception(f"Failed to get info: {str(e)}")
    
    def download_playlist(self, url, quality='best', audio_only=False):
        """
        Download an entire YouTube playlist.
        
        Args:
            url: YouTube playlist URL
            quality: Video quality
            audio_only: Download only audio
            
        Returns:
            list: List of downloaded video information
        """
        ydl_opts = {
            'outtmpl': str(self.output_path / '%(playlist)s/%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
        }
        
        if audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            ydl_opts['format'] = 'bestvideo+bestaudio/best' if quality == 'best' else quality
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                entries = info.get('entries', [])
                return [
                    {
                        'title': entry.get('title'),
                        'url': entry.get('webpage_url')
                    }
                    for entry in entries
                ]
        except Exception as e:
            raise Exception(f"Playlist download failed: {str(e)}")
    
    def _progress_hook(self, d):
        """Internal method to display download progress."""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            print(f"\rDownloading: {percent} at {speed} ETA: {eta}", end='')
        elif d['status'] == 'finished':
            print("\nDownload complete, processing...")


# Example usage
if __name__ == '__main__':
    # Initialize downloader
    downloader = YouTubeDownloader(output_path='my_videos')
    
    # Example 1: Download a single video
    video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    
    try:
        # Get video info first
        print("Fetching video info...")
        info = downloader.get_info(video_url)
        print(f"Title: {info['title']}")
        print(f"Duration: {info['duration']} seconds")
        print(f"Uploader: {info['uploader']}")
        
        # Download video
        print("\nDownloading video...")
        result = downloader.download(video_url, quality='720p')
        print(f"\nSaved to: {result['file_path']}")
        
        # Download audio only
        print("\nDownloading audio...")
        audio_result = downloader.download(video_url, audio_only=True)
        print(f"Audio saved to: {audio_result['file_path']}")
        
    except Exception as e:
        print(f"Error: {e}")