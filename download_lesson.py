"""
Downloads all the videos form a lesson from chess.com

Usage:

To use it as a library
```py
import from download_lesson import download_lesson
download_lesson(url, path_to_a_folder)
```

To use it from cli
```sh
python3 download_lesson.py [url to the lesson page]
```

Example url: https://www.chess.com/lessons/hou-yifan-my-career-so-far
"""

from download_lesson_video import *


def get_video_lessons_links(url):
    html = get_page_html(url)
    lesson_name = get_lesson_name(url)
    pattern = re.compile(
        fr'https://www\.chess\.com/lessons/{lesson_name}/[^"]+')
    links = re.findall(pattern, html)
    return list(set(links))


def download_lesson(url, path=os.getcwd()):
    """
    Download all videos of a lesson inside a folder
    """
    links = get_video_lessons_links(url)
    lesson_name = get_lesson_name(url)

    for link in links:
        download_lesson_video(
            link, os.path.join(path, lesson_name))


if __name__ == "__main__":
    # Get url of the lesson from command line
    if len(sys.argv) > 1:
        first_arg = sys.argv[1]
        if "chess.com/lessons" in first_arg:
            download_lesson(first_arg)
        else:
            print("I need the url of the lesson page like this 👇 \n https://www.chess.com/lessons/hou-yifan-my-career-so-far", file=sys.stderr)
            exit(2)
    else:
        print("Error: Expected at least one command-line argument.", file=sys.stderr)
        exit(1)
