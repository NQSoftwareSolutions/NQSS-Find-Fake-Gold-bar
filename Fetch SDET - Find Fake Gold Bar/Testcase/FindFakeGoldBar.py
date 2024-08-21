import math

from Utils.selenium_utils import selenium_utils


class FindFakeGoldBar(selenium_utils):
    def __init__(self):
        super().__init__()

    def find_gold_bar(self):
        box_xpath = "//div[@class='game-board']//div[@class='board-row']"
        weight_btn_xpath = "//button[@id='weigh']"
        reset_btn_xpath = "//button[@id='reset' and .='Reset']"
        result_operator_xpath = "//div[@class='result']/button[@id='reset']"

        coins_list = [0,1,2,3,4,5,6,7,8]
        message = 'Oops! Try Again!'
        max_retries = 8
        count = 0
        fake_coin = ''
        while message != "Yay! You find it!" and count != max_retries:
            count += 1
            print(f"Retries count: {str(count)}")

            list_index = int(len(coins_list) / 3)
            coins_temp_list_a = coins_list[:list_index]
            coins_temp_list_b = coins_list[list_index:list_index + list_index]
            coins_temp_list_c = coins_list[list_index + list_index:]

            # filling left box
            for i in coins_temp_list_a:
                left_box_input_xpath = box_xpath + f"//input[@id='left_{i}']"
                self.click_and_send_keys(i, left_box_input_xpath)
                self.wait_min2()

            # filling right box
            for i in coins_temp_list_b:
                right_box_input_xpath = box_xpath + f"//input[@id='right_{i}']"
                self.click_and_send_keys(i, right_box_input_xpath)
                self.wait_min2()

            self.click_element(weight_btn_xpath)
            self.wait_min2()

            result_operator = self.get_element_text(result_operator_xpath)
            if result_operator == '=':
                coins_list = coins_temp_list_c
            elif result_operator == '<':
                coins_list = coins_temp_list_a
            else:
                coins_list = coins_temp_list_b

            fake_coin = coins_list[-1]
            self.click_element(reset_btn_xpath)
            self.wait_min2()

            # clicking on fake coin button
            coin_btn_xpath = f"//div[@class='coins']//button[@id='coin_{fake_coin}']"
            self.click_element(coin_btn_xpath)
            self.wait_min2()

            message = self.confirm_box_accept(wait_after_accept=True)
            print(f"Message: {message}")
            self.wait_min2()





