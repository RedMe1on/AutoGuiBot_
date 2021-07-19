import pyautogui as pag
import webbrowser
import time
import random
from GenerateAccount import DbInfoAccount
from exceptions import WrongDisplaySize


class AutoRegistration:
    """Autoregistr account on endclothing"""
    display_size = pag.size()
    db_class = DbInfoAccount()
    main_page = "https://www.endclothing.com/"

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

    def sign_up(self, index: int):
        """Скрипт для прохождения первой регистрации"""
        if self.display_size.width == 1920:
            self.load_page(self.main_page)
            self.click_on_login_button()
            self.click_on_email_field()
            auth_info = self.db_class.get_auth_info_with_card(index)
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
            raise WrongDisplaySize('Ширина экрана не равна 1920')

    def add_address_to_account(self, index: int) -> None:
        """Добавляет адресс в профиль аккаунта"""
        # click Account button to /addresses
        pag.moveTo(random.randint(296, 555), random.randint(219, 252), random.uniform(0.25, 0.5))
        pag.click()
        # webbrowser.open("https://www.endclothing.com/ru/account")
        time.sleep(random.randint(7, 10))

        # click to address from left menu
        pag.moveTo(random.randint(268, 455), random.randint(581, 595), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)
        # add address
        pag.moveTo(random.randint(1533, 1546), random.randint(435, 440), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(2)
        # click to field Firstname address
        pag.moveTo(random.randint(629, 1519), random.randint(612, 629), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)
        pag.hotkey('ctrl', 'a')
        pag.press('delete')
        address = self.db_class.get_address(index)
        self.typewrite_and_tab(address.first_name)
        pag.hotkey('ctrl', 'a')
        pag.press('delete')

        self.typewrite_and_tab(address.last_name)
        self.typewrite_and_tab(address.contact_number)
        self.typewrite_and_tab(address.address_line, tab_presses=2)
        self.typewrite_and_tab(address.town, tab_presses=2)

        pag.typewrite(address.postcode, interval=random.uniform(0.1, 0.2))
        pag.moveTo(random.randint(625, 776), random.randint(791, 817), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(3)
        self.add_card_to_account(index)

    def add_card_to_account(self, index: int) -> None:
        """Добавляет карту в профиль аккаунта"""
        # click on SavedCard on left menu
        pag.moveTo(random.randint(274, 340), random.randint(630, 635), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)
        # click on Add New Card
        pag.moveTo(random.randint(1026, 1115), random.randint(676, 677), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(2)
        # click on field number card
        pag.moveTo(random.randint(633, 1516), random.randint(625, 645), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)
        card_info = self.db_class.get_auth_info_with_card(index)
        self.typewrite_and_tab(card_info.card_number)
        self.typewrite_and_tab(card_info.expires)
        self.typewrite_and_tab(card_info.security_code)
        pag.moveTo(random.randint(619, 805), random.randint(781, 831), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)
        self.log_out()

    def log_out(self) -> None:
        self.load_page(self.main_page)
        self.click_on_login_button()
        pag.moveTo(random.randint(286, 550), random.randint(274, 318), random.uniform(0.25, 0.5))
        pag.click()


class AutoCompetition(AutoRegistration):
    """Autoregistr account on endclothing"""

    def log_in(self, index):
        """Login on site"""
        self.load_page(self.main_page)
        self.click_on_login_button()
        self.click_on_email_field()

        auth_info = self.db_class.get_auth_info_with_card(index)
        pag.typewrite(auth_info.email, interval=random.uniform(0.1, 0.2))
        pag.press('enter')
        time.sleep(2)
        pag.press('tab')
        time.sleep(1)
        pag.typewrite(auth_info.password, interval=random.uniform(0.1, 0.2))
        pag.press('enter')

    def request_to_competition(self, page: str) -> None:
        self.load_page(page)

        #click to EnterDraw button
        pag.moveTo(random.randint(831, 1073), random.randint(994, 1025), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)

        # click size field
        pag.moveTo(random.randint(343, 707), random.randint(465, 483), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)

        # click address field
        pag.moveTo(random.randint(770, 1135), random.randint(465, 483), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)

        # choose address field
        pag.moveTo(random.randint(747, 1136), random.randint(510, 546), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)

        # click payments field
        pag.moveTo(random.randint(1196, 1555), random.randint(465, 483), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)

        # choose payments field
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




if __name__ == '__main__':
    print(pag.size())
    c = AutoCompetition()
    c.request_to_competition('https://launches.endclothing.com/product/nike-dunk-low-og-w-dm9467-700')
