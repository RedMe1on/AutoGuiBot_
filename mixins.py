import datetime
from typing import Union

import pyautogui as pag
import webbrowser
import time
import random
import pandas as pd
from pyscreeze import Box

import parse_size
from GenerateAccount import DbInfoAccount
from exceptions import WrongDisplaySize, WrongSearchImage
from settings import PATH_TO_IMAGE


class PagMixin:
    """Миксин для работы с автоматическим gui для сайта"""

    @staticmethod
    def click_on_x_y(x: int, y: int, time_sleep=1, speed=0.25) -> None:
        pag.moveTo(x, y, speed)
        pag.click()
        time.sleep(time_sleep)

    @staticmethod
    def typewrite_and_tab(field: str, range_random_start=0.1, range_random_end=0.2, tab_presses=1) -> None:
        pag.typewrite(field, interval=random.uniform(range_random_start, range_random_end))
        pag.press('tab', presses=tab_presses)
        time.sleep(1)

    @staticmethod
    def search_screen(image_path: str, confidence=0.8) -> Box:
        point = pag.locateOnScreen(image_path, confidence=confidence)
        return point

    @staticmethod
    def decrement_repeat_counter(repeat):
        if repeat == 0:
            raise WrongSearchImage('Неудалось найти нужную кнопку на экране, возможно, какая-то ошибка')
        else:
            repeat = repeat - 1
            return repeat

    @staticmethod
    def close_browser_tab() -> None:
        pag.hotkey('ctrl', 'w')

    def load_page(self, page: str, logo=PATH_TO_IMAGE + 'logo_site.png') -> None:
        webbrowser.open(page)
        self.custom_delay(logo)

    def custom_delay(self, image_path: str, delay=30):
        """Optimized delay for image"""
        button = None
        while delay > 0 and not button:
            button = self.search_screen(image_path)
            time.sleep(1)
            delay -= 1
        return button

    def click_and_get_coordinate_button(self, image_path: str, time_sleep=2, confidence=0.8) -> Union[Box, None]:
        location = self.search_screen(image_path, confidence=confidence)
        if location:
            self.click_on_x_y(random.randint(location.left + 1, location.left + (location.width - 1)),
                              random.randint(location.top + 1, location.top + (location.height - 1)))
            time.sleep(time_sleep)
        return location

    def click_on_form_with_field(self, from_image_path: str, speed=0.25) -> Union[Box, None]:
        form = self.search_screen(from_image_path)
        if form:
            # click on form and tab to email field
            self.click_on_x_y(form.left + 5, form.top + 5, speed=speed)
            pag.press('tab')
        return form
