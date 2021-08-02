import datetime

import pyautogui as pag
import webbrowser
import time
import random
import pandas as pd
from pyscreeze import Box
from tqdm import tqdm

import parse_size
from GenerateAccount import DbInfoAccount
from backup import Backup
from exceptions import WrongDisplaySize, WrongSearchImage, WrongSize
from mixins import PagMixin


class AutoRegistration(PagMixin):
    """Autoregistr account on endclothing"""
    display_size = pag.size()
    db_class = DbInfoAccount()
    main_page = "https://www.endclothing.com/"

    def click_on_auth_button(self):
        return self.click_on_button('image_to_check/authbutton.png')

    def click_on_log_out_button(self):
        return self.click_on_button('image_to_check/log_out_button.png')

    def click_on_save_button(self):
        return self.click_on_button('image_to_check/save_button.png')

    def click_on_form_auth(self):
        return self.click_on_form_with_field('image_to_check/form_auth.png')

    def click_on_add_card(self):
        return self.click_on_form_with_field('image_to_check/add_new_card.png')

    def click_on_account_button(self):
        return self.click_on_form_with_field('image_to_check/account_button.png')

    def sign_up(self, account: pd, repeat=3):
        """Скрипт для прохождения первой регистрации"""
        if self.display_size.width == 1920:
            self.load_page(self.main_page)
            click = self.click_on_auth_button()
            if click:
                form_click = self.click_on_form_auth()
                if form_click:
                    pag.typewrite(account.email, interval=random.uniform(0.1, 0.2))
                    pag.press('enter')
                    time.sleep(2)
                    pag.press('tab')
                    time.sleep(1)

                    name = self.db_class.get_first_and_last_name()
                    self.typewrite_and_tab(name.first_name)
                    self.typewrite_and_tab(name.last_name)

                    pag.typewrite(account.password, interval=random.uniform(0.1, 0.2))
                    pag.press('enter')
                    time.sleep(10)
                    self.add_address_to_account(0)
                else:
                    repeat = self.decrement_repeat_counter(repeat)
                    self.sign_up(account, repeat=repeat)
            else:
                repeat = self.decrement_repeat_counter(repeat)
                self.sign_up(account, repeat=repeat)
        else:
            raise WrongDisplaySize('Ширина экрана не равна 1920')

    def add_address_to_account(self, account: pd, repeat=3) -> None:
        """Добавляет адресс в профиль аккаунта"""
        # webbrowser.open("https://www.endclothing.com/ru/account")
        # time.sleep(random.randint(7, 10))

        # click Account button to /account
        account_button = self.click_on_account_button()
        if account_button:
            # click to address from left menu
            self.click_on_x_y(random.randint(268, 455), random.randint(581, 595), time_sleep=2)
            # add address
            self.click_on_x_y(random.randint(1533, 1546), random.randint(435, 440), time_sleep=3)
            # click to field Firstname address
            self.click_on_x_y(random.randint(629, 1519), random.randint(612, 629))

            pag.hotkey('ctrl', 'a')
            pag.press('delete')
            self.typewrite_and_tab(account.first_name)
            pag.hotkey('ctrl', 'a')
            pag.press('delete')

            self.typewrite_and_tab(account.last_name)
            self.typewrite_and_tab(account.contact_number)
            self.typewrite_and_tab(account.address_line, tab_presses=2)
            self.typewrite_and_tab(account.town, tab_presses=2)

            pag.typewrite(account.postcode, interval=random.uniform(0.1, 0.2))
            self.click_on_x_y(random.randint(625, 776), random.randint(768, 798), time_sleep=3)

            if not self.search_screen('image_to_check/add_address.png'):
                repeat = self.decrement_repeat_counter(repeat)
                self.load_page('https://www.endclothing.com/ru/account/')
                self.add_address_to_account(account, repeat=repeat)

            self.add_card_to_account(account)
        else:
            repeat = self.decrement_repeat_counter(repeat)
            self.click_on_auth_button()
            self.add_address_to_account(account, repeat=repeat)

    def add_card_to_account(self, account: pd, repeat=3) -> None:
        """Добавляет карту в профиль аккаунта"""
        # click on SavedCard on left menu
        self.click_on_x_y(random.randint(274, 340), random.randint(630, 635), time_sleep=3)
        # click on Add New Card
        add_new_card_button = self.click_on_add_card()
        if add_new_card_button:
            # click on field number card
            self.click_on_x_y(random.randint(633, 1516), random.randint(625, 645))

            self.typewrite_and_tab(account.card_number)
            self.typewrite_and_tab(account.expires)
            self.typewrite_and_tab(account.security_code)

            self.click_on_x_y(random.randint(619, 805), random.randint(781, 831), time_sleep=2)
            self.log_out()

    def log_out(self, repeat=3) -> None:
        self.load_page(self.main_page)
        auth_button = self.click_on_auth_button()
        if auth_button:
            log_out_button = self.click_on_log_out_button()
            if not log_out_button:
                repeat = self.decrement_repeat_counter(repeat)
                self.load_page('https://www.endclothing.com/ru/')
                self.log_out(repeat=repeat)
        else:
            repeat = self.decrement_repeat_counter(repeat)
            self.load_page('https://www.endclothing.com/ru/')
            self.log_out(repeat=repeat)


class AutoRequestCompetition(AutoRegistration):
    """Autoregistr account on endclothing"""

    def click_and_get_coord_on_size_button(self):
        return self.click_and_get_coordinate_button('image_to_check/size_button.png')

    def click_and_get_coord_on_address_button(self):
        return self.click_and_get_coordinate_button('image_to_check/choose_address.png')

    def click_and_get_coord_on_payment_button(self):
        return self.click_and_get_coordinate_button('image_to_check/choose_payment.png')

    def log_in(self, account: pd):
        """Login on site"""
        self.load_page(self.main_page)
        self.click_on_account_button()
        self.click_on_form_auth()

        pag.typewrite(account.email, interval=random.uniform(0.1, 0.2))
        pag.press('enter')
        time.sleep(2)
        pag.press('tab')
        time.sleep(1)
        pag.typewrite(account.password, interval=random.uniform(0.1, 0.2))
        pag.press('enter')

    def request_to_competition(self, competition: pd, repeat=3) -> None:
        # self.log_in(index_account)
        self.load_page(competition.page)

        # click to EnterDraw button TODO сделать скрол до того места, куда и кнопка прокручивает
        pag.moveTo(random.randint(831, 1073), random.randint(994, 1025), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)

        # click size field
        size_button = self.click_and_get_coord_on_size_button()
        if size_button:
            required_size = competition.sizes[0]
            available_sizes = parse_size.get_size_list(competition.page)
            if required_size in available_sizes:
                index = available_sizes.index(required_size)
                scroll_size = 0
                start_y_coordinate = size_button.top + size_button.height + 35
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
                self.click_on_x_y(width, random.randint(start_y_coordinate + coordinate_correction - scroll_size,
                                                        start_y_coordinate + 20 + coordinate_correction - scroll_size))
                pag.scroll(scroll_size)
            else:
                raise WrongSize(f'Размер не найден. Доступные размеры: {available_sizes}')
            # click address field
            address_button = self.click_and_get_coord_on_address_button()
            if address_button:
                # choose address option
                start_y_coordinate = address_button.top + address_button.height + 15
                self.click_on_x_y(
                    random.randint(address_button.left + 5, address_button.left + address_button.width - 5),
                    random.randint(start_y_coordinate, start_y_coordinate + 25))
            # else:
            #     repeat = self.decrement_repeat_counter(repeat)
            #     self.request_to_competition(index_account=index_account, repeat=repeat)

            # click payments field
            payment_button = self.click_and_get_coord_on_payment_button()
            if payment_button:
                pag.moveTo(random.randint(1196, 1555), random.randint(465, 483), random.uniform(0.25, 0.5))
                pag.click()
                time.sleep(1)

                # choose payments option
                pag.moveTo(random.randint(741, 1143), random.randint(568, 582), random.uniform(0.25, 0.5))
                pag.click()
                time.sleep(1)
            else:
                repeat = self.decrement_repeat_counter(repeat)
                self.request_to_competition(competition=competition, repeat=repeat)

            # click accept checkbox
            pag.moveTo(random.randint(560, 1287), random.randint(572, 593), random.uniform(0.25, 0.5))
            pag.click()
            time.sleep(1)

            # click button EnterDraw
            pag.moveTo(random.randint(789, 1122), random.randint(644, 673), random.uniform(0.25, 0.5))
            pag.click()
            time.sleep(1)

            # # backup save
            # auth_card_info = self.db_class.get_auth_info_with_card(index_account)
            # self.backup_data = self.backup_data.append({"email": auth_card_info.email}, ignore_index=True)
            # Backup().backup_create(data=self.backup_data, name_backup='request_to_competition')

            self.log_out()

        else:
            repeat = self.decrement_repeat_counter(repeat)
            self.request_to_competition(competition=competition, repeat=repeat)


class AutoRegistrationArrayAccount(AutoRegistration, Backup):
    backup_data = pd.DataFrame(columns=['email'])
    _file_output = 'registered_accounts.csv'

    def _to_csv(self) -> None:
        self._data.to_csv(self._file_output, encoding='utf-8-sig', sep=';', index=False)

    def registration_many_accounts(self):
        data = self.db_class.read_file(self.db_class.db_auth)

        name_backup = 'request_to_competition'
        backup_data = self.backup_check(name_backup=name_backup)
        if backup_data:
            data = self.merge_data_with_backup(column_merge='email', name_backup=name_backup, data=data)
        else:
            backup_data = self.backup_data
        with tqdm(total=len(data)) as progress_bar:
            for account in self.db_class.read_file(self.db_class.db_auth).itertuples():
                try:
                    self.sign_up(account)

                    # backup save
                    self.backup_data.append({"email": account.email},
                                            ignore_index=True)
                    Backup().backup_create(data=backup_data, name_backup='registration')
                except Exception as e:
                    print(f'Не зарегистрировал {account.email}', e)
                progress_bar.update(1)
        self._to_csv()


class AutoRequestArrayCompetition(AutoRequestCompetition, Backup):
    backup_data = pd.DataFrame(columns=['email'])
    _file_output = 'requests_competition_accounts.csv'

    def _to_csv(self) -> None:
        self._data.to_csv(self._file_output, encoding='utf-8-sig', sep=';', index=False)

    def request_many_competition(self):
        data = self.db_class.read_file(self.db_class.db_auth)

        name_backup = 'request_to_competition'
        backup_data = self.backup_check(name_backup=name_backup)
        if backup_data:
            data = self.merge_data_with_backup(column_merge='email', name_backup=name_backup, data=data)
        else:
            backup_data = self.backup_data
        with tqdm(total=len(data)) as progress_bar:
            for account in data.itertuples():
                self.log_in(account=account)
                for competition in self.db_class.read_file(self.db_class.db_competition).itertuples():

                    self.request_to_competition(account)

                    # backup save
                    self.backup_data.append({"email": account.email},
                                            ignore_index=True)
                    Backup().backup_create(data=backup_data, name_backup='registration')
                    progress_bar.update(1)
        self._to_csv()


if __name__ == '__main__':
    reg = AutoRegistration()
    c = AutoRequestCompetition(competition_index=0)
    c.sign_up(index_account=0)

    data = Backup().backup_load(name_backup='request_to_competition')
    print(data)
