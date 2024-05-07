# youtube-whole-chanel-downloader


## Description
This script allows you to download videos from YouTube into organized folders using the YouTube Data API and yt-dlp. It's designed to handle multiple videos, ensuring they are neatly sorted into directories based on playlist titles.

## Installation
Ensure you have Python 3 installed on your system. Clone this repository and install the required dependencies:

```
git clone https://github.com/yourusername/youtube-playlist-downloader.git
cd youtube-playlist-downloader
pip install -r requirements.txt
```

## Usage
Run the script by passing a YouTube channel ID as an argument:

```
python downloader.py YOUR_CHANNEL_ID
```
Where channel ID is something like "UCaDZLsDEEBBJESXmm" string, can be found on each channel in 'share channel' section with button "Copy channel ID"

Follow the prompts to select a playlist for downloading. The script will handle the rest, downloading all videos into the appropriate directory.

## Dependencies
This project relies on several external libraries listed in the `requirements.txt` file, ensuring all functionalities are supported.

## License
This project is distributed under the MIT License. See the LICENSE file for more details.
