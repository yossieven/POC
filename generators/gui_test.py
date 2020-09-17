import ctypes
import math
import os
from enum import Enum
from idlelib.pyshell import PROCESS_SYSTEM_DPI_AWARE
from time import sleep

import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from win32api import GetSystemMetrics

# Fixture for Firefox


class AttachmentTypeExtended(Enum):

    def __init__(self, mime_type, extension):
        self.mime_type = mime_type
        self.extension = extension

    AVI = ("video/avi", "avi")
    MP4 = ("video/avi", "mp4")

#
# @pytest.fixture(scope="class")
# def driver_init(request):
#     ff_driver = webdriver.Firefox()
#     request.cls.driver = ff_driver
#     yield
#     ff_driver.close()
#
#
# # Fixture for Chrome
# @pytest.fixture(scope="class")
# def chrome_driver_init(request):
#     options = webdriver.ChromeOptions()
#     options.add_argument('--lang=en-EN')
#     chrome_driver = webdriver.Chrome(options=options)
#     request.cls.driver = chrome_driver
#     yield chrome_driver
#
#     chrome_driver.close()


@pytest.fixture
def master(request):
    parameters = []
    for i in range(10):
        parameters.append((i, i + 1))
    return request.param


screen_w = GetSystemMetrics(0)
screen_y = GetSystemMetrics(1)
errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_SYSTEM_DPI_AWARE)
half_width = int(math.floor(screen_w/4))


def test_open_search_not_found(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--lang=en-EN')
    options.add_argument('--window-size=1900x1080')
    chrome_driver = webdriver.Chrome(options=options)
    chrome_driver.set_window_position(0, 0)
    window_size = chrome_driver.get_window_size()
    # chrome_driver.set_window_size(half_width, screen_y)
    options2 = webdriver.ChromeOptions()
    options2.add_argument('--lang=en-EN')
    options2.add_argument('--window-size=1900x1080')
    chrome_driver2 = webdriver.Chrome(options=options2)
    chrome_driver2.set_window_position(window_size['width'] + 10, 0)
    # chrome_driver.set_window_size(half_width-10, screen_y)

    chrome_driver.get("https://www.google.com/")
    elem = chrome_driver.find_element_by_name("q")

    try:
        assert "Google" in chrome_driver.title
        print("assertion on title passed")
    except Exception as e:
        print("assertion on title failed! " + str(e))
        chrome_driver.close()

    elem.send_keys("something")
    elem.send_keys(Keys.RETURN)
    try:
        # self.driver.find_element_by_xpath("/html/body[@id='gsr']/div[@id='main']/div[@id='cnt']/div[@class='mw'][2]/div[@id='rcnt']/div[@class='col']/div[@id='center_col']/div[@id='res']/div[@id='topstuff']/div[@class='mnr-c']/div[@class='med card-section']")
        result = chrome_driver.find_element_by_xpath(
            "/html/body[@id='gsr']/div[@id='main']/div[@id='cnt']/div[@class='mw'][2]/div[@id='rcnt']/div[@class='col']/div[@id='center_col']/div[@id='res']/div[@id='search']/div/div[@id='rso']")
    except NoSuchElementException as e:
        chrome_driver.close()
        assert 0

    chrome_driver.close()

# @pytest.mark.usefixtures("driver_init")
# class BasicTest:
#     pass
#
#
# @pytest.mark.skip("some reason")
# class Test_URL_Firefox(BasicTest):
#     def test_open_url(self, rp_logger):
#         rp_logger.info("Firefox test")
#         self.driver.get("https://www.lambdatest.com/")
#         rp_logger.info("launching https://www.lambdatest.com/")
#         print(self.driver.title)
#
#         sleep(5)
#
#
# @pytest.fixture(scope="function", autouse=True)
# def test_failed_check(request):
#     yield
#     if request.node.rep_setup.failed:
#         print("setting up a test failed!", request.node.nodeid)
#     elif request.node.rep_setup.passed:
#         # attach_video(driver, filename)
#         if request.node.rep_call.failed:
#             driver = request.node.funcargs['chrome_driver_init']
#             take_screenshot(driver, request.node.name)
#             print("executing test failed", request.node.nodeid)
#
#
# def take_screenshot(driver, name):
#     sleep(1)
#     print("taking screenshot now!")
#     screenshot_file_path = "./{}.png".format(name)
#     print("file name == " + screenshot_file_path)
#     driver.save_screenshot(screenshot_file_path)
#
#     allure.attach(driver.get_screenshot_as_png(),
#                   name="this is a screenshot",
#                   attachment_type=allure.attachment_type.PNG)
    # allure.attach(screenshot_file_path, name='PNG attachment', attachment_type=allure.attachment_type.PNG)


# @pytest.mark.usefixtures("chrome_driver_init")
# class Test_URL_Chrome():
#
#     def test_open_search_not_found(self, db):
#         self.driver.get("https://www.google.com/")
#         elem = self.driver.find_element_by_name("q")
#
#         try:
#             assert "Google" in self.driver.title
#             print("assertion on title passed")
#         except Exception as e:
#             print("assertion on title failed! " + str(e))
#
#         elem.send_keys(str(db[0]) + " " + str(db[1]))
#         elem.send_keys(Keys.RETURN)
#         try:
#             # self.driver.find_element_by_xpath("/html/body[@id='gsr']/div[@id='main']/div[@id='cnt']/div[@class='mw'][2]/div[@id='rcnt']/div[@class='col']/div[@id='center_col']/div[@id='res']/div[@id='topstuff']/div[@class='mnr-c']/div[@class='med card-section']")
#             result = self.driver.find_element_by_xpath(
#                 "/html/body[@id='gsr']/div[@id='main']/div[@id='cnt']/div[@class='mw'][2]/div[@id='rcnt']/div[@class='col']/div[@id='center_col']/div[@id='res']/div[@id='search']/div/div[@id='rso']")
#         except NoSuchElementException as e:
#             assert 0
#
#     def test_open_search_dog_url(self, test_failed_check):
#         self.driver.get("https://www.google.com/")
#         elem = self.driver.find_element_by_name("q")
#
#         try:
#             assert "Google" in self.driver.title
#             print("assertion on title passed")
#         except Exception as e:
#             print("assertion on title failed! " + str(e))
#
#         elem.send_keys("dog")
#         elem.send_keys(Keys.RETURN)
#         try:
#             self.driver.find_element_by_xpath(
#                 "/html/body[@id='gsr']/div[@id='main']/div[@id='cnt']/div[@class='mw'][2]/div[@id='rcnt']/div[@class='col']/div[@id='center_col']/div[@id='res']/div[@id='search']/div/div[@id='rso']")
#         except Exception as e:
#             pytest.fail(e)
#         sleep(1)
#
#     def test_go_back_to_google(self, test_failed_check):
#         self.driver.get("https://www.google.com/")
#         elem = self.driver.find_element_by_name("q")
#         elem.send_keys("dog")
#         elem.send_keys(Keys.RETURN)
#         self.driver.execute_script("window.history.go(-1)")
#         self.driver.find_element_by_xpath(
#             "/html/body[@id='gsr']/div[@id='viewport']/div[@id='searchform']/form[@id='tsf']/div[2]/div[@class='A8SBwf']/div[@class='FPdoLc tfB0Bf']/center/input[@class='gNO89b']").click()
#
#         sleep(1)
#
#     def test_voice_search_no_mic(self, test_failed_check):
#         self.driver.get("https://www.google.com/")
#         self.driver.find_element_by_xpath(
#             "/html/body[@id='gsr']/div[@id='viewport']/div[@id='searchform']/form[@id='tsf']/div[2]/div[@class='A8SBwf']/div[@class='RNNXgb']/div[@class='SDkEP']/div[@class='dRYYxd']/div[@class='hpuQDe']").click()
#         try:
#             elem = self.driver.find_element_by_id("spch")
#             assert elem.value_of_css_property('display') == 'block'
#         except Exception as e:
#             print("couldn't find element")
#         sleep(10)
#
#         assert elem.value_of_css_property('display') == 'none'
