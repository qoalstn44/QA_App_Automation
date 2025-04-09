import json
import re
import time
# from Functions import click_element, click_element_with_retry, find_elements
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from android_common.android_slack import Slack_manager
from android_common.android_pass_word import pass_word
from android_refund.android_test_refund import My_Wallet_Reset


# JSON 파일 경로
json_file_path = 'Android/android_DB/android_DB.json'

# JSON 파일 읽기 함수


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# JSON 파일 읽기
json_data = load_json(json_file_path)
onboarding_data = json_data["onboarding"][0]["number1"][0]
charge_data = json_data["charge"][0]["number1"][0]
charge_continent_data = json_data["charge"][0]["number2"][0]
charge_continent_100_data = json_data["charge"][0]["number3"][0]
charge_completed_data = json_data["charge"][0]["number4"][0]
refund_data = json_data["refund"][0]["number1"][0]


# class Currency_Exchange:
#     def Cross_Charge(cls, driver):
