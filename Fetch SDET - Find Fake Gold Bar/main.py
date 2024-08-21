from Testcase.FindFakeGoldBar import FindFakeGoldBar

"""
TODO 1: Install chrome
TODO 2: Install selenium webdriver based on chrome version.
TODO 3: assign a valid selenium webdriver path to "driver_path" variable inside config_data file
"""

if __name__ == '__main__':
    FindFakeGoldBar_object = FindFakeGoldBar()
    FindFakeGoldBar_object.find_gold_bar()
