from typing import Union

import pyautogui as pag
import webbrowser
import time

from mixins import PagMixin


class TouchVPN(PagMixin):
    """class for plagin Touch VPN into browser"""

    def click_touch_vpn_button(self):
        return self.click_and_get_coordinate_button('image_to_check/touch_vpn.png')

    def click_active_touch_vpn_button(self):
        return self.click_and_get_coordinate_button('image_to_check/active_touch_vpn.png')

    def open_google_page(self):
        self.load_page('https://www.google.com/', logo='image_to_check/logo_google.png')

    def connect_in_browser(self, repeat=5) -> None:
        self.open_google_page()

        vpn_button = self.click_touch_vpn_button()
        if not vpn_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.connect_in_browser(repeat=repeat)
            return
        # click connect touch vpn
        connect_vpn_button = self.click_and_get_coordinate_button('image_to_check/connect_touch_vpn.png')
        if not connect_vpn_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.connect_in_browser(repeat=repeat)
            return
        stop_vpn_button = self.custom_delay(image_path='image_to_check/stop_vpn.png')
        if not stop_vpn_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.connect_in_browser(repeat=repeat)
            return

    def reconnect_in_browser(self, repeat=5):
        self.open_google_page()

        active_vpn_button = self.click_active_touch_vpn_button()
        if not active_vpn_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.reconnect_in_browser(repeat=repeat)
            return

        stop_vpn_button = self.click_and_get_coordinate_button('image_to_check/stop_vpn.png')
        if not stop_vpn_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.reconnect_in_browser(repeat=repeat)
            return

        connect_vpn_button = self.custom_delay(image_path='image_to_check/connect_touch_vpn.png')
        if not connect_vpn_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.reconnect_in_browser(repeat=repeat)
            return

        self.click_on_x_y(x=connect_vpn_button.left + 10, y=connect_vpn_button.top + 5)

        stop_vpn_button = self.custom_delay(image_path='image_to_check/stop_vpn.png')
        if not stop_vpn_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.reconnect_in_browser(repeat=repeat)
            return
        self.close_browser_tab()

    def disconnect(self, repeat=3):
        self.open_google_page()

        active_vpn_button = self.click_active_touch_vpn_button()
        if not active_vpn_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.disconnect(repeat=repeat)
            return

        stop_vpn_button = self.click_and_get_coordinate_button('image_to_check/stop_vpn.png')
        if not stop_vpn_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.disconnect(repeat=repeat)
            return

        connect_vpn_button = self.custom_delay(image_path='image_to_check/connect_touch_vpn.png')
        if not connect_vpn_button:
            self.close_browser_tab()
            repeat = self.decrement_repeat_counter(repeat)
            self.disconnect(repeat=repeat)
            return
        self.close_browser_tab()


if __name__ == '__main__':
    c = TouchVPN()

    c.reconnect_in_browser()
    c.disconnect()
