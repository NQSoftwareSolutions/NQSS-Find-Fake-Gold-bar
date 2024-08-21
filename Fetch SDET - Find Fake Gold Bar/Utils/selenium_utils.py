import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Config.config_data import *

class selenium_utils():
    def __init__(self):
        """
        this will open url and provide driver for child classes
        :param driver: chrome driver
        """
        self.driver = None
        self.open_url()

    def open_chrome(self):
        """
        This is open driver with specified capabilities
        :return: this will return chrome driver
        """
        options = Options()
        options.add_argument('--window-size=1080x900')
        options.add_argument('--incognito')

        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(0.5)

        if 'browserVersion' in self.driver.capabilities:
            print("browserVersion: "+str(self.driver.capabilities['browserVersion']))
        else:
            print("browserVersion: "+str(self.driver.capabilities['version']))

        if 'chrome' in self.driver.capabilities:
            print(self.driver.capabilities['chrome'])
            if 'chromedriverVersion' in self.driver.capabilities['chrome']:
                print("chromedriverVersion: "+str(self.driver.capabilities['chrome']['chromedriverVersion']))

        print("Chrome Opened")
        return self.driver

    def open_url(self):
        """
        this will open specified url
        """
        print(f"Opening url: {web_url}")
        self.open_chrome()
        self.driver.get(web_url)

    def click_and_send_keys(self, keys, locator, local_type = By.XPATH):
        """
        This will click on element and send key
        :param keys: Keys which we want to send for input field
        :param locator: locator of elements in DOM
        :param local_type:
        """
        try:
            element = self.get_element(locator, local_type)
            if element != False:
                element.click()
                time.sleep(1)
                element.send_keys(keys)
        except Exception as Ex:
            print(f"click and send keys failed, keys are: {keys} error: {str({Ex})}")

    def get_element(self, locator, locator_type=By.XPATH):
        """
        This will help us to locate element
        :param locator: locator of elements in DOM
        :param locator_type:
        :return: element
        """
        # element = ""
        element = False
        get_by = self.get_by(locator_type)
        try:
            elements_list = self.get_elements(locator, locator_type)
            if elements_list is not None and len(elements_list)> 0:
                element = elements_list[0]
        except Exception as ex:
            print("Element not found with locator :: " + locator + "and locator type = " + get_by + ", error:"+str(ex))
            element = element
        return element

    def get_elements(self, locator, locator_type=By.XPATH):
        getBy = self.get_by(locator_type)
        elements_list = []
        try:
            elements_list = self.driver.find_elements(getBy, locator)
        except Exception as ex:
            print("getElements: Elements Not Found. locator:"+str(locator)+", Error:"+str(ex))
        return elements_list

    @staticmethod
    def get_by(locator_type):
        """
        This will return locator for elements to find by
        :param locator_type:
        :return: type of locator
        """
        if locator_type is not None:
            if locator_type == By.ID:
                return By.ID
            if locator_type == By.CLASS_NAME:
                return By.CLASS_NAME
            if locator_type == By.XPATH:
                return By.XPATH
            if locator_type == By.LINK_TEXT:
                return By.LINK_TEXT
            if locator_type == By.CSS_SELECTOR:
                return By.CSS_SELECTOR
            if locator_type == By.NAME:
                return By.NAME
        else:
            print("Locator Type ::" + str(locator_type) + " is not correct")

    def click_element(self, locator, locator_type=By.XPATH):
        """
        This will click on element
        :param locator:
        :param locator_type:
        """
        element = self.get_element(locator, locator_type)
        if element != False:
            element.click()
        else:
            print("Not clicked. Element object is false.  with locator :: " + locator + " and Locator type :: " + locator_type + "")

    def get_element_text(self, locator, locator_type=By.XPATH):
        element = self.get_element(locator, locator_type)
        return element.text if element != False else ""

    @staticmethod
    def wait_min():
        time.sleep(1)

    @staticmethod
    def wait_min2():
        time.sleep(3)

    @staticmethod
    def wait_med():
        time.sleep(5)

    @staticmethod
    def wait_max():
        time.sleep(8)

    @staticmethod
    def wait_custom(_size):
        time.sleep(_size)

    def confirm_box_accept(self, wait_after_accept = False, wait_time=1, is_retry = False):
        """
        This will accept confirm box and return its text.
        :rtype: confirm box text
        """

        box_text = "-"
        retried_attempted = 0
        max_attempts = 15

        while box_text != "" and retried_attempted < max_attempts:
            if retried_attempted != 0:
                print("box_text: " + str(box_text) + ", retried_attempted: " + str(retried_attempted))

            try:
                try:
                    confirm_box = self.driver.switch_to.alert
                    str_text = str(confirm_box.text)
                    confirm_box.accept()
                    print("confirm_box accepted")

                    # if wait_after_accept == True:
                    #     self.wait_for_loading_to_complete()

                except Exception as ex:
                    print("No confirm_box found. Error: "+str(ex))
                    str_text = self.prompt_box_accept(wait_after_accept=wait_after_accept, wait_time=wait_time)

                retried_attempted = retried_attempted + 1
                box_text = str_text

                if is_retry==False:
                    break

            except Exception as ex:
                print("ConfirmBox_accept Error: " + str(ex))
                print("ex:" + str(ex))
                retried_attempted = retried_attempted + 1
        return box_text

    def prompt_box_accept(self, wait_after_accept = False, wait_time=1):
        """
        This will accept prompt box and return its text.
        :rtype: prompt box text
        """
        try:
            prompt_box = Alert(self.driver)
            str_text = str(prompt_box.text)
            prompt_box.accept()
            print("prompt_box accepted")
            # if wait_after_accept == True:
            #     self.wait_for_loading_to_complete()
        except Exception as ex:
            print("PromptBox_accept Error: " + str(ex))
            str_text = self.alert_box_accept(wait_after_accept=wait_after_accept, wait_time=wait_time)
        return str_text

    # def alert_box_accept(self, wait_after_accept = False, wait_time=1):
    #     """
    #     This will accept alert box and return its text.
    #     :rtype: alert box text
    #     """
    #     str_text = ""
    #     try:
    #         alert = WebDriverWait(self.driver, wait_time).until(EC.alert_is_present(), 'Timed out waiting for alert ' + 'confirmation popup to appear.')
    #         str_text = str(alert.text)
    #         alert.accept()
    #         print("alert accepted")
    #         if wait_after_accept == True:
    #             self.wait_for_loading_to_complete()
    #
    #     except Exception as ex:
    #         print("AlertBox_accept: No alert found. Error: " + str(ex))
    #     return str_text

    # def wait_for_loading_to_complete(self, loading_path="", minimize_wait=False, locator_type=By.XPATH):
    #     """
    #     This will wait for loading to be complete
    #     :rtype: object
    #     """
    #     print("wait_for_loading_to_complete start")
    #     had_loading = False
    #     if minimize_wait == True:
    #         self.wait_custom(0.2)
    #     else:
    #         self.wait_med()
    #
    #     if loading_path == "":
    #         loading_path = "//div[contains(@class,'modalOverlay')]//div[contains(@class,'juicBusyIndicatorAnimation')]"
    #
    #     wait_time_sec = 60
    #     try :
    #         if self.isElementPresent(loading_path, locator_type, True) == True:
    #             had_loading = True
    #             element = WebDriverWait(self.driver, wait_time_sec).until(EC.invisibility_of_element_located((By.XPATH, loading_path)))
    #     except Exception as ex :
    #         print("wait_for_loading_to_complete: Error: " + str(ex))
    #         self.wait_min2()
    #
    #     self.wait_min()
    #     print("wait_for_loading_to_complete end")
    #     return had_loading

