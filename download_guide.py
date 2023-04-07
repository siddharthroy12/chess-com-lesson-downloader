"""
Downloads all lessons from the guide from chess.com

Usage:

To use it as a library
```py
import from download_guide import download_guide
download_guide(path_to_a_folder)
```

To use it from cli
```sh
python3 download_guide.py
```
"""


import sys
from download_lesson import *
import os
from bs4 import BeautifulSoup


def get_guide_lessons():
    """
    Get all lessons links from guide with levels
    """
    html = get_page_html("https://www.chess.com/lessons/guide")
    soup = BeautifulSoup(html, 'html.parser')

    lessons_with_levels = {}

    levels = soup.find_all('div', class_='level-component')
    for level in levels:
        title = level.find('h2', class_='level-title').get_text(strip=True)
        lessons = [a['href'] for a in level.find_all('a')]
        lessons_with_levels[title] = lessons
    return lessons_with_levels


def download_guide(path=os.getcwd()):
    "Download all guide lessons and store it inside guide folder"
    lessons_level_url = get_guide_lessons()
    for level in lessons_level_url:
        download_lesson(lessons_level_url[level],
                        os.path.join(path, level))
    pass


if __name__ == "__main__":
    download_guide(path=os.path.join(os.getcwd(), 'guide'))
