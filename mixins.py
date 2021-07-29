import datetime

import pyautogui as pag
import webbrowser
import time
import random
import pandas as pd
from pyscreeze import Box

import parse_size
from GenerateAccount import DbInfoAccount
from exceptions import WrongDisplaySize, WrongSearchImage


class PagMixin:
    """Миксин для работы с автоматическим gui для сайта"""

    @staticmethod
    def click_on_x_y(x: int, y: int) -> None:
        pag.moveTo(x, y, random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)

    @staticmethod
    def typewrite_and_tab(field: str, range_random_start=0.1, range_random_end=0.2, tab_presses=1) -> None:
        pag.typewrite(field, interval=random.uniform(range_random_start, range_random_end))
        pag.press('tab', presses=tab_presses)
        time.sleep(1)

    @staticmethod
    def load_page(site: str, delay=7) -> None:
        webbrowser.open(site)
        time.sleep(delay)

    @staticmethod
    def search_screen(image_path: str) -> Box:
        point = pag.locateOnScreen(image_path)
        return point

    @staticmethod
    def decrement_repeat_counter(repeat):
        if repeat == 0:
            raise WrongSearchImage('Неудалось найти нужную кнопку на экране, возможно, какая-то ошибка')
        else:
            repeat = repeat - 1
            return repeat

    def click_on_button(self, image_path: str, time_sleep=2) -> bool:
        location = self.search_screen(image_path)
        if location:
            self.click_on_x_y(random.randint(location.left + 1, location.left + (location.width - 1)),
                              random.randint(location.top + 1, location.top + (location.height - 1)))
            time.sleep(time_sleep)
            return True
        else:
            return False

    def click_on_form_with_field(self, from_image_path: str) -> bool:
        form = self.search_screen(from_image_path)
        if form:
            # click on form and tab to email field
            self.click_on_x_y(form.left + 5, form.top + 5)
            pag.press('tab')
            return True
        else:
            return False