"""
Downloads lesson video from chess.com

Usage:

To use it as a library
```py
import from download_lesson_video import download_lesson_video
download_lesson_video(url, path_to_a_folder)
```

To use it from cli
```sh
python3 download_lesson_video.py [url to the video page]
```

Example url: https://www.chess.com/lessons/hou-yifan-my-career-so-far/the-world-youth-champion-hou-yifanship
"""

import requests
import sys
import re
import os


def get_lesson_name(url):
    """
    Extract lesson name from url
    """

    # Split the URL by the '?' character to separate the URL from the query parameters
    split_url = url.split('?')
    url_without_query = split_url[0]

    # Split the URL without query parameters by the '#' character to separate the URL from the fragment
    split_url = url_without_query.split('#')
    url_without_fragment = split_url[0]

    # Split the URL without query parameters or fragments by the '/' character to create a list of strings representing each part of the URL
    split_url = url_without_fragment.split('/')

    # Extract the last non-empty element of the list
    for i in range(len(split_url) - 1, -1, -1):
        if split_url[i]:
            ending_part = split_url[i]
            break

    return ending_part


def download_video(url, path):
    """Download the video and save it to the current directory"""
    file_name = get_video_file_name(url)
    print(f"Downloading video {file_name}")
    try:
        r = requests.get(url, allow_redirects=True)
    except:
        print("Failed to download the video. Might be a network problem",
              file=sys.stderr)

    # Create path if not exists
    if not os.path.exists(path):
        os.makedirs(path)

    # Save the file
    open(os.path.join(path, f"{file_name}"), 'wb').write(r.content)
    print(f"{file_name} downloaded")


def get_video_file_name(url):
    """
    Get video file name from url
    """
    split_url = url.split('/')

    # Find the index of the last element that ends with '.mp4'
    mp4_index = [i for i, s in enumerate(split_url) if s.endswith('.mp4')][-1]

    # Extract the file name from the URL
    return split_url[mp4_index]


def get_page_html(url):
    """
    Get the html of a page
    """
    print(f"Downloading page {url}")
    try:
        res = requests.get(url)
    except:
        print(f"Failed to fetch html from {url}", file=sys.stderr)
        return ""
    return res.text


def get_video_url(html):
    """Extract the video url from the lesson page"""
    print("Extracting video url from page...")
    url_pattern = re.compile(r'https://.*?\.mp4')
    url_match = url_pattern.search(html)

    # Check if a match was found and print the result
    if url_match:
        return url_match.group(0)
    else:
        print("Failed to extract video url from page. \nThis lesson doesn't have a video mostlikely.", file=sys.stderr)
        return ""


def download_lesson_video(video_lesson_url, path=os.getcwd()):
    html = get_page_html(video_lesson_url)
    video_lesson_url = get_video_url(html)
    if video_lesson_url:
        download_video(video_lesson_url, path)


if __name__ == "__main__":
    # Get url of the lesson from command line
    if len(sys.argv) > 1:
        first_arg = sys.argv[1]
        if "chess.com/lessons" in first_arg:
            download_lesson_video(first_arg)
        else:
            print("I need the url of the lesson page like this 👇 \n https://www.chess.com/lessons/hou-yifan-my-career-so-far/the-world-youth-champion-hou-yifanship", file=sys.stderr)
            exit(1)
    else:
        print("Error: Expected at least one command-line argument.", file=sys.stderr)
        exit(1)
