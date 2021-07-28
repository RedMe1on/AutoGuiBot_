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


class Backup:
    """Backup class"""

    def __init__(self):
        self._date = datetime.date.today()
        self._data = False

    def backup_create(self, data: pd, name_backup: str) -> None:
        data.to_pickle(f'backup/backup_{name_backup}_{self._date}.p')

    def backup_load(self, name_backup: str) -> pd:
        return pd.read_pickle(f'backup/backup_{name_backup}_{self._date}.p')

    def backup_check(self, name_backup: str) -> bool:
        try:
            self._data = self.backup_load(name_backup)
            backup = True
        except FileNotFoundError:
            backup = False
        return backup

    def _filter_data(self, data: pd, column_merge: str) -> pd:
        common = data.merge(self._data, on=column_merge)
        return data[~data[column_merge].isin(common[column_merge])]

    def merge_backup(self, column_merge: str, name_backup: str, data: pd) -> pd or False:
        if self.backup_check(name_backup=name_backup):
            data = self._filter_data(data, column_merge)
        else:
            data = False
        return data


class AutoRegistration:
    """Autoregistr account on endclothing"""
    display_size = pag.size()
    db_class = DbInfoAccount()
    main_page = "https://www.endclothing.com/"
    backup_data = pd.DataFrame(columns=['email'])

    @staticmethod
    def click_on_login_button() -> None:
        pag.moveTo(367, 175, random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)

    @staticmethod
    def click_on_email_field() -> None:
        pag.moveTo(random.randint(720, 1187), random.randint(600, 625), random.uniform(0.25, 0.5))
        pag.click()

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

    def sign_up(self, index_account: int, repeat=3):
        """Скрипт для прохождения первой регистрации"""
        if self.display_size.width == 1920:
            self.load_page(self.main_page)
            if self.search_screen('image_to_check/authbutton.png'):
                self.click_on_login_button()
                time.sleep(3)
                if self.search_screen('image_to_check/form_auth.png'):
                    self.click_on_email_field()
                    auth_info = self.db_class.get_auth_info_with_card(index_account)
                    pag.typewrite(auth_info.email, interval=random.uniform(0.1, 0.2))
                    pag.press('enter')
                    time.sleep(2)
                    pag.press('tab')
                    time.sleep(1)

                    name = self.db_class.get_first_and_last_name()
                    self.typewrite_and_tab(name.first_name)
                    self.typewrite_and_tab(name.last_name)

                    pag.typewrite(auth_info.password, interval=random.uniform(0.1, 0.2))
                    pag.press('enter')
                    time.sleep(10)
                    self.add_address_to_account(0)
                else:
                    repeat = self.decrement_repeat_counter(repeat)
                    self.sign_up(index_account, repeat=repeat)
            else:
                repeat = self.decrement_repeat_counter(repeat)
                self.sign_up(index_account, repeat=repeat)
        else:
            raise WrongDisplaySize('Ширина экрана не равна 1920')

    def add_address_to_account(self, index_account: int, repeat=3) -> None:
        """Добавляет адресс в профиль аккаунта"""
        # webbrowser.open("https://www.endclothing.com/ru/account")
        # time.sleep(random.randint(7, 10))

        # click Account button to /account
        pag.moveTo(random.randint(296, 555), random.randint(219, 252), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(3)

        # click to address from left menu
        pag.moveTo(random.randint(268, 455), random.randint(581, 595), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(3)
        # add address
        pag.moveTo(random.randint(1533, 1546), random.randint(435, 440), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(3)
        # click to field Firstname address
        pag.moveTo(random.randint(629, 1519), random.randint(612, 629), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)
        pag.hotkey('ctrl', 'a')
        pag.press('delete')
        address = self.db_class.get_address(index_account)
        self.typewrite_and_tab(address.first_name)
        pag.hotkey('ctrl', 'a')
        pag.press('delete')

        self.typewrite_and_tab(address.last_name)
        self.typewrite_and_tab(address.contact_number)
        self.typewrite_and_tab(address.address_line, tab_presses=2)
        self.typewrite_and_tab(address.town, tab_presses=2)

        pag.typewrite(address.postcode, interval=random.uniform(0.1, 0.2))
        pag.moveTo(random.randint(625, 776), random.randint(768, 798), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(3)

        if not self.search_screen('image_to_check/add_address.png'):
            repeat = self.decrement_repeat_counter(repeat)
            self.load_page('https://www.endclothing.com/ru/account/')
            self.add_address_to_account(index_account, repeat=repeat)

        self.add_card_to_account(index_account)

    def add_card_to_account(self, index_account: int, repeat=3) -> None:
        """Добавляет карту в профиль аккаунта"""
        # click on SavedCard on left menu
        pag.moveTo(random.randint(274, 340), random.randint(630, 635), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(3)
        # click on Add New Card
        add_new_card_button = self.search_screen('image_to_check/add_new_card.png')
        if add_new_card_button:
            pag.moveTo(random.randint(add_new_card_button.left, add_new_card_button.left + add_new_card_button.width),
                       random.randint(add_new_card_button.top, add_new_card_button.top + add_new_card_button.height),
                       random.uniform(0.25, 0.5))
            pag.click()
            time.sleep(3)
            # click on field number card
            pag.moveTo(random.randint(633, 1516), random.randint(625, 645), random.uniform(0.25, 0.5))
            pag.click()
            time.sleep(1)
            auth_card_info = self.db_class.get_auth_info_with_card(index_account)
            self.typewrite_and_tab(auth_card_info.card_number)
            self.typewrite_and_tab(auth_card_info.expires)
            self.typewrite_and_tab(auth_card_info.security_code)
            pag.moveTo(random.randint(619, 805), random.randint(781, 831), random.uniform(0.25, 0.5))
            pag.click()
            time.sleep(2)

            # backup save
            self.backup_data.append({"email": auth_card_info.email}, ignore_index=True)
            Backup().backup_create(data=self.backup_data, name_backup='registration')

            self.log_out()

        # if not self.search_screen('image_to_check/card_not_exist.png'):
        #     pass
        # else:
        #     repeat = self.decrement_repeat_counter(repeat)
        #     self.load_page('https://www.endclothing.com/ru/account')
        #     self.add_card_to_account(index_account, repeat=repeat)

    def log_out(self) -> None:
        self.load_page(self.main_page)
        self.click_on_login_button()
        pag.moveTo(random.randint(286, 550), random.randint(274, 318), random.uniform(0.25, 0.5))
        pag.click()


class AutoRequestCompetition(AutoRegistration):
    """Autoregistr account on endclothing"""

    def __init__(self, competition_index: int):
        self.competition_info = self.db_class.get_competition_info(competition_index)
        self.page_competition = self.competition_info.page
        self.available_sizes = parse_size.get_size_list(self.page_competition)

    def log_in(self, index_account):
        """Login on site"""
        self.load_page(self.main_page)
        self.click_on_login_button()
        self.click_on_email_field()

        auth_info = self.db_class.get_auth_info_with_card(index_account)
        pag.typewrite(auth_info.email, interval=random.uniform(0.1, 0.2))
        pag.press('enter')
        time.sleep(2)
        pag.press('tab')
        time.sleep(1)
        pag.typewrite(auth_info.password, interval=random.uniform(0.1, 0.2))
        pag.press('enter')

    def request_to_competition(self, index_account: int) -> None:
        # self.log_in(index_account)
        self.load_page(self.page_competition)

        # click to EnterDraw button
        pag.moveTo(random.randint(831, 1073), random.randint(994, 1025), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)

        # click size field
        pag.moveTo(random.randint(343, 707), random.randint(465, 483), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)
        required_size = self.competition_info.sizes[0]
        if required_size in self.available_sizes:
            index = self.available_sizes.index(required_size)
            scroll_size = 0
            if index % 2 == 0:
                # choose even size option
                coordinate_correction = 60 * index / 2
                width = random.randint(393, 458)
                if index > 17:
                    scroll_size = 60 * (index - 17)
            else:
                # choose odd size option
                coordinate_correction = 60 * (index - 1) / 2
                width = random.randint(579, 645)
                if index > 17:
                    scroll_size = 60 * (index - (17 + 1))

            pag.scroll(-scroll_size)
            pag.moveTo(width, random.randint(523 + coordinate_correction - scroll_size,
                                             543 + coordinate_correction - scroll_size),
                       random.uniform(0.25, 0.5))
            pag.click()
            time.sleep(1)
            pag.scroll(scroll_size)

        # click address field
        pag.moveTo(random.randint(770, 1135), random.randint(465, 483), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)

        # choose address option
        pag.moveTo(random.randint(747, 1136), random.randint(510, 546), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)

        # click payments field
        pag.moveTo(random.randint(1196, 1555), random.randint(465, 483), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)

        # choose payments option
        pag.moveTo(random.randint(741, 1143), random.randint(568, 582), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)

        # click accept checkbox
        pag.moveTo(random.randint(560, 1287), random.randint(572, 593), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)

        # click button EnterDraw
        pag.moveTo(random.randint(789, 1122), random.randint(644, 673), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)
        # backup save
        auth_card_info = self.db_class.get_auth_info_with_card(index_account)
        self.backup_data = self.backup_data.append({"email": auth_card_info.email}, ignore_index=True)
        Backup().backup_create(data=self.backup_data, name_backup='request_to_competition')

        self.log_out()


if __name__ == '__main__':
    c = AutoRequestCompetition(competition_index=0)
    c.add_card_to_account(index_account=0)

    data = Backup().backup_load(name_backup='request_to_competition')
    print(data)
