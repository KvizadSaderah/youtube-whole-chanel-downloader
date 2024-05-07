import os
import argparse
import googleapiclient.discovery
import subprocess
import sys
import questionary

API_KEY = 'youtube-api-key'
# https://developers.google.com/youtube/v3/getting-started

def get_playlists(youtube, channel_id):
    """ Fetches playlists for a given YouTube channel ID """
    request = youtube.playlists().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50
    )
    response = request.execute()
    return [{'id': item['id'], 'title': item['snippet']['title']} for item in response.get('items', [])]

def get_videos_from_playlist(youtube, playlist_id):
    videos = []
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    for item in response.get('items', []):
        video_id = item['snippet']['resourceId']['videoId']
        video_title = item['snippet']['title'].replace('/', '-')  # Replace problematic characters in filenames
        videos.append({'id': video_id, 'title': video_title, 'link': f'https://www.youtube.com/watch?v={video_id}'})
    return videos

def download_video(video_link, video_title, output_directory):
    video_path = f"{output_directory}/{video_title}.mp4"
    if not os.path.exists(video_path):  # Check if the file already exists
        command = ["yt-dlp", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                   "--limit-rate", "500K",  # Limit download speed
                   "--retries", "10",  # Increase retry attempts
                   "--fragment-retries", "10",  # Retries on fragment errors
                   "--sleep-interval", "3",  # Sleep between downloads (seconds)
                   "--max-sleep-interval", "20",  # Maximum sleep interval
                   "-o", video_path, video_link]
        subprocess.run(command)
    else:
        print(f"File already exists: {video_path} - Skipping download.")


def main(channel_id):
    """ Main function to execute the workflow """
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)
    playlists = get_playlists(youtube, channel_id)
    
    while True:
        choice = questionary.select(
            "Select a playlist to download:",
            choices=[playlist['title'] for playlist in playlists] + ["Exit"]
        ).ask()

        if choice == "Exit":
            print("Exiting program.")
            break

        selected_playlist = next((item for item in playlists if item['title'] == choice), None)

        if selected_playlist:
            playlist_folder = os.path.join('.', 'downloads', selected_playlist['title'].replace('/', '-'))
            os.makedirs(playlist_folder, exist_ok=True)
            videos = get_videos_from_playlist(youtube, selected_playlist['id'])
            all_exist = True
            for video in videos:
                download_video(video['link'], video['title'], playlist_folder)
                all_exist = False
            if all_exist:
                print("All videos in this playlist are already downloaded.")
        else:
            print("No playlist selected. Exiting...")

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Download videos from a selected YouTube playlist into organized folders.")
        parser.add_argument("channel_id", help="YouTube channel ID")
        args = parser.parse_args()
        main(args.channel_id)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. You can resume the operation later.")

