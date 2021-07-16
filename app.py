import pyautogui as pag
import webbrowser
import time
import random
from GenerateAccount import DbInfoAccount


class AutoRegistration:
    """Autoregistr account on endclothing"""
    display_size = pag.size()
    db_class = DbInfoAccount()

    def first_sign_up(self, index: int):
        """Скрипт для прохождения первой регистрации"""
        webbrowser.open("https://www.endclothing.com/")
        if self.display_size.width == 1920:
            time.sleep(7)
            pag.moveTo(367, 175, random.uniform(0.25, 0.5))
            pag.click()
            time.sleep(1)
            pag.moveTo(random.randint(720, 1187), random.randint(600, 625), random.uniform(0.25, 0.5))
            pag.click()
            auth_info = self.db_class.get_auth_info_with_card(index)
            pag.typewrite(auth_info.email, interval=random.uniform(0.1, 0.2))
            pag.press('enter')
            time.sleep(2)
            pag.press('tab')
            time.sleep(1)
            name = self.db_class.get_first_and_last_name()
            pag.typewrite(name.first_name, interval=random.uniform(0.1, 0.2))
            pag.press('tab')
            time.sleep(1)
            pag.typewrite(name.last_name, interval=random.uniform(0.1, 0.2))
            pag.press('tab')
            time.sleep(1)
            pag.typewrite(auth_info.password, interval=random.uniform(0.1, 0.2))
            pag.press('enter')
            time.sleep(10)
            self.add_address_to_account(0)

    def add_address_to_account(self, index: int) -> None:
        """Добавляет адресс в профиль аккаунта"""
        #click Account button to /addresses
        pag.moveTo(random.randint(296, 555), random.randint(219, 252), random.uniform(0.25, 0.5))
        pag.click()
        # webbrowser.open("https://www.endclothing.com/ru/account")
        time.sleep(random.randint(7, 10))

        #click to address from left menu
        pag.moveTo(random.randint(268, 455), random.randint(581, 595), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)
        #add address
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
        pag.typewrite(address.first_name, interval=random.uniform(0.1, 0.2))
        pag.press('tab')
        time.sleep(1)
        pag.hotkey('ctrl', 'a')
        pag.press('delete')
        pag.typewrite(address.last_name, interval=random.uniform(0.1, 0.2))
        pag.press('tab')
        time.sleep(1)
        pag.typewrite(address.contact_number, interval=random.uniform(0.1, 0.2))
        pag.press('tab')
        time.sleep(1)
        pag.typewrite(address.address_line, interval=random.uniform(0.1, 0.2))
        pag.press('tab', presses=2)
        time.sleep(1)
        pag.typewrite(address.town, interval=random.uniform(0.1, 0.2))
        pag.press('tab', presses=2)
        time.sleep(1)
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
        pag.typewrite(card_info.card_number, interval=random.uniform(0.1, 0.2))
        pag.press('tab')
        time.sleep(1)
        pag.typewrite(card_info.expires, interval=random.uniform(0.1, 0.2))
        pag.press('tab')
        time.sleep(1)
        pag.typewrite(card_info.security_code, interval=random.uniform(0.1, 0.2))
        pag.press('tab')
        time.sleep(1)
        pag.moveTo(random.randint(619, 805), random.randint(781, 831), random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)
        self.log_out()

    def log_out(self) -> None:
        webbrowser.open("https://www.endclothing.com/")
        time.sleep(7)
        pag.moveTo(367, 175, random.uniform(0.25, 0.5))
        pag.click()
        time.sleep(1)
        pag.moveTo(random.randint(286, 550), random.randint(274, 318), random.uniform(0.25, 0.5))
        pag.click()



if __name__ == '__main__':
    print(pag.size())
    c = AutoRegistration()
    c.log_out()

