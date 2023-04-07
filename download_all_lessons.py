"""
Downloads all lessons from chess.com

Usage:

To use it as a library
```py
import from download_all_lessons import download_all_lessons
download_all_lessons(path_to_a_folder)
```

To use it from cli
```sh
python3 download_all_lessons.py
```
"""

import sys
from download_lesson import *
import os
from bs4 import BeautifulSoup


def get_number_of_pages(category):
    """
    Get how many pages are there for a category
    """
    html = get_page_html(f"https://www.chess.com/lessons/{category}")
    soup = BeautifulSoup(html, 'html.parser')
    last_page_button = soup.select_one('div[id="pagination-bottom"]')
    selected_page = last_page_button['data-total-pages']
    return int(selected_page)


def get_lessons_of_page_number(category, page_number):
    """
    Get lessons link of a given page number
    """
    html = get_page_html(
        f"https://www.chess.com/lessons/{category}?page={page_number}")
    soup = BeautifulSoup(html, 'html.parser')
    course_wrapper = soup.find('div', class_="course-wrapper")
    links = [a['href'] for a in course_wrapper.find_all('a')]
    return links


def download_all_lessons(path=os.getcwd()):
    """
    Download all lessons that are available on the website
    """
    categories = ['openings', 'strategy', 'tactics', 'endgames', 'games']

    for category in categories:
        print(f'Downloading from category {category}')
        num_of_pages = get_number_of_pages(category)
        for i in range(1, num_of_pages+1):
            lessons = get_lessons_of_page_number(category, i)
            for lesson in lessons:
                download_lesson(lesson, os.path.join(path, category))


if __name__ == "__main__":
    download_all_lessons(path=os.path.join(os.getcwd(), 'all'))
