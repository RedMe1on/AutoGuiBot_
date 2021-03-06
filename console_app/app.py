import pyautogui as pag
import time
import random
import pandas as pd
from tqdm import tqdm
from loguru import logger
from console_app import parse_size
from console_app.GenerateAccount import DbInfoAccount
from console_app.backup import Backup
from console_app.exceptions import WrongDisplaySize, WrongSearchImage, WrongSize
from console_app.mixins import PagMixin
from console_app.settings import PATH_TO_IMAGE, PATH_TO_RESULT
from console_app.vpn_connect import TouchVPN


class AutoRegistration(PagMixin):
    """Autoregistr account on endclothing"""
    display_size = pag.size()
    db_class = DbInfoAccount()
    main_page = "https://www.endclothing.com/"

    def click_on_auth_button(self):
        return self.click_and_get_coordinate_button(PATH_TO_IMAGE + 'auth_button.png')

    def click_on_log_out_button(self):
        return self.click_and_get_coordinate_button(PATH_TO_IMAGE + 'log_out_button.png')

    def click_on_save_button(self):
        return self.click_and_get_coordinate_button(PATH_TO_IMAGE + 'save_button.png')

    def click_on_form_auth(self):
        return self.click_on_form_with_field(PATH_TO_IMAGE + 'form_auth.png')

    def click_on_address_form(self):
        return self.click_on_form_with_field(PATH_TO_IMAGE + 'address_form.png')

    def click_on_card_form(self):
        return self.click_on_form_with_field(PATH_TO_IMAGE + 'card_form.png')

    def click_on_add_card(self):
        return self.click_and_get_coordinate_button(PATH_TO_IMAGE + 'add_new_card.png')

    def click_on_account_button(self):
        return self.click_and_get_coordinate_button(PATH_TO_IMAGE + 'account_button.png')

    def click_on_left_menu_address(self):
        return self.click_and_get_coordinate_button(PATH_TO_IMAGE + 'left_menu_address.png')

    def click_on_left_menu_card(self):
        return self.click_and_get_coordinate_button(PATH_TO_IMAGE + 'left_menu_card.png')

    def click_on_add_address(self):
        return self.click_and_get_coordinate_button(PATH_TO_IMAGE + 'add_address.png')

    def sign_up(self, account: pd, repeat=2):
        """???????????? ?????? ?????????????????????? ???????????? ??????????????????????"""
        start_repeat = repeat
        if self.display_size.width == 1920:
            self.load_page(self.main_page)

            click = self.click_on_auth_button()
            if not click:
                self.close_browser_tab()
                repeat = self.decrement_repeat_counter(repeat)
                self.sign_up(account, repeat=repeat)
                return
            log_out_button = self.click_on_log_out_button()
            if log_out_button:
                self.close_browser_tab()
                self.sign_up(account, repeat=repeat)
                return
            form_click = self.click_on_form_auth()
            if not form_click:
                self.close_browser_tab()
                repeat = self.decrement_repeat_counter(repeat)
                self.sign_up(account, repeat=repeat)
                return

            pag.typewrite(str(account.email), interval=random.uniform(0.1, 0.2))
            pag.press('enter')
            time.sleep(1)
            first_name_field = self.custom_delay(image_path=PATH_TO_IMAGE + 'first_name.png', delay=10)
            if not first_name_field:
                self.close_browser_tab()
                raise WrongSearchImage('?????????????? ??????????????????????????????')
            pag.press('tab')
            # time.sleep(1)

            name = self.db_class.get_first_and_last_name()
            self.typewrite_and_tab(name.first_name)
            self.typewrite_and_tab(name.last_name)

            pag.typewrite(str(account.password), interval=random.uniform(0.1, 0.2))
            pag.press('enter')

            self.add_address_to_account(account, repeat=start_repeat)
        else:
            raise WrongDisplaySize('???????????? ???????????? ???? ?????????? 1920')

    def add_address_to_account(self, account: pd, repeat=5) -> None:
        """?????????????????? ???????????? ?? ?????????????? ????????????????"""
        # webbrowser.open("https://www.endclothing.com/ru/account")
        # time.sleep(random.randint(7, 10))
        start_repeat = repeat
        # click Account button to /account
        account_button = self.custom_delay(image_path=PATH_TO_IMAGE + 'account_button.png', delay=10)
        if not account_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.load_page(self.main_page)
            self.click_on_auth_button()
            self.add_address_to_account(account=account, repeat=repeat)
            return
        else:
            self.click_on_x_y(x=account_button.left + 3, y=account_button.top + 3)

        # click to address from left menu
        left_menu_address = self.click_on_left_menu_address()
        if not left_menu_address:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.load_page(self.main_page)
            self.click_on_auth_button()
            self.add_address_to_account(account=account, repeat=repeat)
            return

        # add address
        add_address = self.click_on_add_address()
        if not add_address:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.load_page(self.main_page)
            self.click_on_auth_button()
            self.add_address_to_account(account=account, repeat=repeat)
            return

        # click to field Firstname address
        address_form = self.click_on_address_form()
        if not address_form:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.load_page(self.main_page)
            self.click_on_auth_button()
            self.add_address_to_account(account=account, repeat=repeat)
            return

        pag.press('delete')
        self.typewrite_and_tab(str(account.first_name))
        pag.press('delete')

        self.typewrite_and_tab(str(account.last_name))
        self.typewrite_and_tab(str(account.contact_number))
        self.typewrite_and_tab(str(account.address_line), tab_presses=2)
        self.typewrite_and_tab(str(account.town), tab_presses=2)

        pag.typewrite(str(account.postcode), interval=random.uniform(0.1, 0.2))

        save_button = self.click_on_save_button()
        if not save_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.load_page(self.main_page)
            self.click_on_auth_button()
            self.add_address_to_account(account=account, repeat=repeat)
            return

        success_add_address = self.custom_delay(PATH_TO_IMAGE + 'success_add_address.png', delay=10)
        if not success_add_address:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.load_page('https://www.endclothing.com/ru/account/')
            self.click_on_auth_button()
            self.add_address_to_account(account=account, repeat=repeat)
            return

        self.add_card_to_account(account, repeat=start_repeat)

    def add_card_to_account(self, account: pd, repeat=2) -> None:
        """?????????????????? ?????????? ?? ?????????????? ????????????????"""

        start_repeat = repeat  # need for same repeat for all function

        card_left_menu_button = self.click_on_left_menu_card()
        if not card_left_menu_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.load_page('https://www.endclothing.com/ru/account/')
            self.add_card_to_account(account=account, repeat=repeat)
            return

        # click on Add New Card
        add_new_card_button = self.click_on_add_card()
        if not add_new_card_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.load_page('https://www.endclothing.com/ru/account/')
            self.add_card_to_account(account=account, repeat=repeat)
            return

        # click on field number card
        card_form = self.click_on_card_form()
        if not card_form:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.load_page('https://www.endclothing.com/ru/account/')
            self.add_card_to_account(account=account, repeat=repeat)
            return

        self.typewrite_and_tab(str(account.card_number)[1:])
        self.typewrite_and_tab(str(account.expires)[1:])
        self.typewrite_and_tab(str(account.security_code)[1:])

        save_button = self.click_on_save_button()
        if not save_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.load_page('https://www.endclothing.com/ru/account/')
            self.add_card_to_account(account=account, repeat=repeat)
            return

        success_add_card = self.custom_delay(image_path=PATH_TO_IMAGE + 'success_add_card.png')
        if not success_add_card:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.load_page('https://www.endclothing.com/ru/account/')
            self.add_card_to_account(account, repeat=repeat)
            return

        self.close_browser_tab()
        self.log_out(repeat=start_repeat)

    def log_out(self, repeat=3) -> None:
        self.load_page(self.main_page)
        time.sleep(2)
        auth_button = self.click_on_auth_button()
        if not auth_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.log_out(repeat=repeat)
            return
        form_auth = self.custom_delay(image_path=PATH_TO_IMAGE + 'form_auth.png', delay=3)
        if not form_auth:
            log_out_button = self.click_on_log_out_button()
            if not log_out_button:
                self.close_browser_tab()
                repeat = self.decrement_repeat_counter(repeat)
                self.log_out(repeat=repeat)
                return
        self.close_browser_tab()


class AutoRequestCompetition(AutoRegistration):
    """Autoregistr account on endclothing"""

    def click_and_get_coord_on_size_button(self):
        return self.click_and_get_coordinate_button(PATH_TO_IMAGE + 'size_button.png')

    def click_and_get_coord_on_address_button(self):
        return self.click_and_get_coordinate_button(PATH_TO_IMAGE + 'choose_address.png')

    def click_and_get_coord_on_payment_button(self):
        return self.click_and_get_coordinate_button(PATH_TO_IMAGE + 'choose_payment.png')

    def click_and_get_coord_on_checkbox_competition(self):
        return self.click_and_get_coordinate_button(PATH_TO_IMAGE + 'checkbox_competition.png', confidence=0.92)

    def click_and_get_coord_on_enter_draw(self, time_sleep=5):
        return self.click_and_get_coordinate_button(PATH_TO_IMAGE + 'enter_draw_button.png', time_sleep=time_sleep)

    def click_and_get_check_auto_choose_field(self):
        return self.click_and_get_coordinate_button(PATH_TO_IMAGE + 'check_auto_choose_field.png')

    def log_in(self, account: pd, repeat=3):
        """Login on site"""
        self.load_page(self.main_page)

        auth_button = self.click_on_auth_button()
        if not auth_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.log_in(account=account, repeat=repeat)
            return

        log_out_button = self.click_on_log_out_button()
        if log_out_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.log_in(account=account, repeat=repeat)
            return

        auth_form_button = self.click_on_form_auth()
        if not auth_form_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.log_in(account=account, repeat=repeat)
            return

        pag.typewrite(str(account.email), interval=random.uniform(0.1, 0.2))
        pag.press('enter')
        check_not_registr_account = self.custom_delay(PATH_TO_IMAGE + 'first_name.png', delay=5)
        if check_not_registr_account:
            # ?????????? ????????????????, ?????????? ?????????? ?????????????????????????? ?????????? ?????????????? ????????
            self.close_browser_tab()
            raise WrongSearchImage('?????????????? ???? ??????????????????????????????')

        auth_form_button = self.click_on_form_auth()
        if not auth_form_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.log_in(account=account, repeat=repeat)
            return
        pag.press('tab')
        pag.typewrite(str(account.password), interval=random.uniform(0.1, 0.2))
        pag.press('enter')

        account_button = self.custom_delay(image_path=PATH_TO_IMAGE + 'account_button.png')
        if not account_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.log_in(repeat=repeat, account=account)

    def choose_address(self):
        # click address field
        address_button = self.click_and_get_coord_on_address_button()
        if address_button:
            # choose address option
            start_y_coordinate = address_button.top + address_button.height + 15
            self.click_on_x_y(
                random.randint(address_button.left + 5, address_button.left + address_button.width - 5),
                random.randint(start_y_coordinate, start_y_coordinate + 25))

    def choose_payment(self):
        # click payments field
        payment_button = self.click_and_get_coord_on_payment_button()
        if payment_button:
            start_y_coordinate = payment_button.top + payment_button.height + 15
            self.click_on_x_y(
                random.randint(payment_button.left + 5, payment_button.left + payment_button.width - 5),
                random.randint(start_y_coordinate, start_y_coordinate + 25))

    def request_to_competition(self, competition: pd, repeat=3) -> None:
        self.load_page(competition.page)

        # click to EnterDraw button on centre screen
        chat_widjet = self.custom_delay(PATH_TO_IMAGE + 'chat_widjet.png', delay=10)
        if not chat_widjet:
            chat_widjet = self.custom_delay(PATH_TO_IMAGE + 'open_chat.png', delay=10)
            if not chat_widjet:
                self.close_browser_tab()
                repeat = self.decrement_repeat_counter(repeat)
                self.request_to_competition(competition=competition, repeat=repeat)
                return
        self.click_on_x_y(x=chat_widjet.left / 2, y=chat_widjet.top + 3)

        # click size field
        size_button = self.click_and_get_coord_on_size_button()
        if not size_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.request_to_competition(competition=competition, repeat=repeat)
            return

        required_size = competition.size
        available_sizes = parse_size.get_size_list(str(competition.page))
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
            raise WrongSize(f'???????????? ???? ????????????. ?????????????????? ??????????????: {available_sizes}')

        accept_checkbox = self.click_and_get_coord_on_checkbox_competition()
        if not accept_checkbox:
            self.choose_address()
            accept_checkbox = self.click_and_get_coord_on_checkbox_competition()
            if not accept_checkbox:
                self.choose_payment()
                # click accept checkbox
                accept_checkbox = self.click_and_get_coord_on_checkbox_competition()
                if not accept_checkbox:
                    self.close_browser_tab()
                    repeat = self.decrement_repeat_counter(repeat)
                    self.request_to_competition(competition=competition, repeat=repeat)
                    return

        # click button EnterDraw
        enter_draw_button = self.click_and_get_coord_on_enter_draw(time_sleep=5)
        if not enter_draw_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.request_to_competition(competition=competition, repeat=repeat)
            return

        self.close_browser_tab()


class AutoRegistrationArrayAccount(AutoRegistration, Backup):
    """Class for registration on site many accounts with address and card"""
    backup_data = pd.DataFrame(
        columns=['email', 'password', 'card_number', 'expires', 'security_code', 'first_name', 'last_name',
                 'contact_number', 'address_line', 'town', 'postcode'])
    file_output = PATH_TO_RESULT + 'registered_accounts.csv'

    def registration_many_accounts(self, path_to_file_accounts: str, change_vpn=5, repeat=2):
        data = self.db_class.read_file(path_to_file_accounts)

        name_backup = 'registration'
        backup_data = self.backup_check(name_backup=name_backup, backup_empty_default=self.backup_data)
        if not backup_data.empty:
            data = self.filter_data(column_merge='email', data=data, backup_data=backup_data)

        with tqdm(total=len(data)) as progress_bar:
            vpn = TouchVPN()
            vpn.connect_in_browser()

            index = 0
            for account in data.itertuples():
                index += 1
                if index % change_vpn == 0:
                    vpn.reconnect_in_browser()
                try:
                    self.sign_up(account, repeat=repeat)

                    # backup save
                    backup_data = backup_data.append(
                        {"email": account.email, 'password': account.password, 'card_number': account.card_number,
                         'expires': account.expires, 'security_code': account.security_code,
                         'first_name': account.first_name, 'last_name': account.last_name,
                         'contact_number': account.contact_number, 'address_line': account.address_line,
                         'town': account.town, 'postcode': account.postcode},
                        ignore_index=True)
                    Backup().backup_create(data=backup_data, name_backup='registration')
                except Exception as e:
                    logger.error(f'???? ?????????????????????????????? {account.email}:{e}')
                    print(f'???? ?????????????????????????????? {account.email}:', e)
                progress_bar.update(1)

            vpn.disconnect()
        self.db_class.to_csv(backup_data, file_output=self.file_output)


class AutoRequestArrayCompetition(AutoRequestCompetition, Backup):
    """Class for request many account yo many competition"""
    backup_data = pd.DataFrame(
        columns=['email', 'password', 'card_number', 'expires', 'security_code', 'first_name', 'last_name',
                 'contact_number', 'address_line', 'town', 'postcode', 'number_competition',
                 'not_request_to_competition'])
    file_output = PATH_TO_RESULT + 'requests_competition_accounts.csv'

    def request_many_competition(self, path_to_file_accounts: str, path_to_file_competition: str, change_vpn=5,
                                 repeat=2):
        data = self.db_class.read_file(path_to_file_accounts)
        name_backup = 'request_to_competition'
        backup_data = self.backup_check(name_backup=name_backup, backup_empty_default=self.backup_data)
        if not backup_data.empty:
            data = self.filter_data(column_merge='email', data=data, backup_data=backup_data)

        with tqdm(total=len(data)) as progress_bar:
            vpn = TouchVPN()
            vpn.connect_in_browser(repeat=repeat)

            index = 0
            for account in data.itertuples():
                index += 1
                if index % change_vpn == 0:
                    vpn.reconnect_in_browser()
                try:
                    self.log_in(account=account, repeat=repeat)

                    number_competition = 0
                    not_request_to_competition = []
                    for competition in self.db_class.read_file(path_to_file_competition).itertuples():
                        try:
                            self.request_to_competition(competition, repeat=repeat)
                            self.close_browser_tab()
                            number_competition += 1
                        except Exception as e:
                            not_request_to_competition.append(competition.page)
                            logger.info(f'???? ?????????????????????????????? {account.email} ???? ?????????????? {competition.page}: {e}')
                            print(f'???? ?????????????????????????????? {account.email} ???? ?????????????? {competition.page}: {e}')
                        backup_data = backup_data.append(
                            {"email": account.email, 'password': account.password,
                             'card_number': account.card_number,
                             'expires': account.expires, 'security_code': account.security_code,
                             'first_name': account.first_name, 'last_name': account.last_name,
                             'contact_number': account.contact_number, 'address_line': account.address_line,
                             'town': account.town, 'postcode': account.postcode,
                             'number_competition': number_competition,
                             'not_request_to_competition': not_request_to_competition},
                            ignore_index=True)
                        Backup().backup_create(data=backup_data, name_backup='request_to_competition')

                    self.log_out(repeat=repeat)
                    progress_bar.update(1)
                except Exception as e:
                    logger.error(f'???? ?????????????????????????????? {account.email}:{e}')
                    print(f'???? ?????????????????????????????? {account.email}', e)
            vpn.disconnect()
        self.db_class.to_csv(backup_data, file_output=self.file_output)


if __name__ == '__main__':
    c = AutoRegistrationArrayAccount()
    c.log_out()
