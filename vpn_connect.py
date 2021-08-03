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

    def connect_in_browser(self, repeat=5) -> bool:
        self.load_page('https://www.google.com/', delay=3)
        vpn_button = self.click_touch_vpn_button()
        if not vpn_button:
            repeat = self.decrement_repeat_counter(repeat)
            self.connect_in_browser(repeat=repeat)
        # click connect touch vpn
        self.click_on_x_y(x=1462, y=369)
        time_sleep = 4
        stop_vpn_button = False
        while time_sleep > 0 and not stop_vpn_button:
            stop_vpn_button = self.search_screen('image_to_check/stop_vpn.png')
            time_sleep -= 1
        if not stop_vpn_button:
            repeat = self.decrement_repeat_counter(repeat)
            self.connect_in_browser(repeat=repeat)
        return True

    def reconnect_in_browser(self, repeat=5):
        self.load_page('https://www.google.com/', delay=3)
        active_vpn_button = self.click_active_touch_vpn_button()
        if not active_vpn_button:
            repeat = self.decrement_repeat_counter(repeat)
            self.reconnect_in_browser(repeat=repeat)

        stop_vpn_button = self.click_and_get_coordinate_button('image_to_check/stop_vpn.png')
        if not stop_vpn_button:
            repeat = self.decrement_repeat_counter(repeat)
            self.reconnect_in_browser(repeat=repeat)

        counter_check = 4
        connect_vpn_button = False
        while counter_check > 0 and not connect_vpn_button:
            connect_vpn_button = self.click_and_get_coordinate_button('image_to_check/connect_touch_vpn.png')
            counter_check -= 1
        if not connect_vpn_button:
            repeat = self.decrement_repeat_counter(repeat)
            self.reconnect_in_browser(repeat=repeat)

        counter_check = 4
        while counter_check > 0 and not stop_vpn_button:
            stop_vpn_button = self.search_screen('image_to_check/stop_vpn.png')
            counter_check -= 1
        if not stop_vpn_button:
            repeat = self.decrement_repeat_counter(repeat)
            self.connect_in_browser(repeat=repeat)
        return True


if __name__ == '__main__':
    c = TouchVPN()
    c.reconnect_in_browser()

