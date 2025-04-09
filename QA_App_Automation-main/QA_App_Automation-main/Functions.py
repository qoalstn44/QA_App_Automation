import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException


def click_element(driver, xpath, description):
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        print(f"{description} 클릭 완료")
    except Exception as e:
        print(f"Exception in click_element for {description}: {e}")  # 로그 추가
        raise


def click_latest_screen_element(driver, predicate_string, description):
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable(
        (AppiumBy.IOS_PREDICATE, predicate_string)))
    element.click()
    print(f"{description} 클릭 완료")


def click_element_with_retry(driver, xpath, description, max_attempts=3):
    """Attempt to click an element, retrying if a StaleElementReferenceException occurs."""
    attempts = 0
    while attempts < max_attempts:
        try:
            click_element(driver, xpath, description)
            return
        except StaleElementReferenceException:
            attempts += 1
            print(f"{description} 클릭 재시도 중... ({attempts}/{max_attempts})")
            time.sleep(1)  # Optional: Add a delay between retries
    raise Exception(f"{description} 클릭 실패. 스크롤 시도 후에도 실패.")


def send_keys(driver, xpath, keys, description):
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    element.send_keys(keys)
    print(f"{description} 입력 완료")


def find_elements(driver, xpath, description):
    wait = WebDriverWait(driver, 10)
    elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, xpath)))
    print(f"{description}")
    return elements


def country_data():  # 국가 데이터 및 대륙별 국가 코드 딕셔너리를 반환하는 함수
    all_countries = {
        "charge_continent_europe": [
            "charge_country_NOK_xpath",
            "charge_country_DKK_xpath",
            "charge_country_SEK_xpath",
            "charge_country_CHF_xpath",
            "charge_country_ISK_xpath",
            "charge_country_GBP_xpath",
            "charge_country_EUR_xpath",
            "charge_country_CZK_xpath",
            "charge_country_TRY_xpath",
            "charge_country_PLN_xpath",
            "charge_country_HUF_xpath"
        ],
        "charge_continent_asia": [
            "charge_country_NPR_xpath",
            "charge_country_TWD_xpath",
            "charge_country_KRW_xpath",
            "charge_country_LAK_xpath",
            "charge_country_MOP_xpath",
            "charge_country_MYR_xpath",
            "charge_country_MNT_xpath",
            "charge_country_VND_xpath",
            "charge_country_SAR_xpath",
            "charge_country_SGD_xpath",
            "charge_country_AED_xpath",
            "charge_country_UZS_xpath",
            "charge_country_INR_xpath",
            "charge_country_IDR_xpath",
            "charge_country_JPY_xpath",
            "charge_country_CNY_xpath",
            "charge_country_KZT_xpath",
            "charge_country_QAR_xpath",
            "charge_country_KHR_xpath",
            "charge_country_THB_xpath",
            "charge_country_PHP_xpath",
            "charge_country_HKD_xpath"
        ],
        "charge_continent_northamerica": [
            "charge_country_MXN_xpath",
            "charge_country_USD_xpath",
            "charge_country_CAD_xpath"
        ],
        "charge_continent_southamerica": [
            "charge_country_BRL_xpath",
            "charge_country_PEN_xpath"
        ],
        "charge_continent_oceania": [
            "charge_country_NZD_xpath",
            "charge_country_XPF_xpath",
            "charge_country_FJD_xpath",
            "charge_country_AUD_xpath"
        ],
        "charge_continent_africa": [
            "charge_country_ZAR_xpath",
            "charge_country_MUR_xpath",
            "charge_country_EGP_xpath",
            "charge_country_KES_xpath"
        ]
    }

    country_code_to_name = {
        "NOK": "노르웨이",
        "DKK": "덴마크",
        "SEK": "스웨덴",
        "CHF": "스위스",
        "ISK": "아이슬란드",
        "GBP": "영국",
        "EUR": "유럽",
        "CZK": "체코",
        "TRY": "튀르키예",
        "PLN": "폴란드",
        "HUF": "헝가리",
        "NPR": "네팔",
        "TWD": "대만",
        "KRW": "대한민국",
        "LAK": "라오스",
        "MOP": "마카오",
        "MYR": "말레이시아",
        "MNT": "몽골",
        "VND": "베트남",
        "SAR": "사우디아라비아",
        "SGD": "싱가포르",
        "AED": "아랍에미리트",
        "UZS": "우즈베키스탄",
        "INR": "인도",
        "IDR": "인도네시아",
        "JPY": "일본",
        "CNY": "중국",
        "KZT": "카자흐스탄",
        "QAR": "카타르",
        "KHR": "캄보디아",
        "THB": "태국",
        "PHP": "필리핀",
        "HKD": "홍콩",
        "MXN": "멕시코",
        "USD": "미국",
        "CAD": "캐나다",
        "BRL": "브라질",
        "PEN": "페루",
        "NZD": "뉴질랜드",
        "XPF": "프랑스령 폴리네시아(타히티)",
        "FJD": "피지",
        "AUD": "호주",
        "ZAR": "남아공",
        "MUR": "모리셔스",
        "EGP": "이집트",
        "KES": "케냐"
    }

    return all_countries, country_code_to_name


def minimum_charge_all():
    minimum_charge_maping_data = {
        "NOK": ("노르웨이", 1),
        "DKK": ("덴마크", 1),
        "SEK": ("스웨덴", 1),
        "CHF": ("스위스", 1),
        "ISK": ("아이슬란드", 10),
        "GBP": ("영국", 1),
        "EUR": ("유럽", 1),
        "CZK": ("체코", 2),
        "TRY": ("튀르키예", 3),
        "PLN": ("폴란드", 1),
        "HUF": ("헝가리", 30),
        "NPR": ("네팔", 10),
        "TWD": ("대만", 3),
        "KRW": ("대한민국", 100),
        "LAK": ("라오스", 1500),
        "MOP": ("마카오", 1),
        "MYR": ("말레이시아", 1),
        "MNT": ("몽골", 300),
        "VND": ("베트남", 2000),
        "SAR": ("사우디아라비아", 1),
        "SGD": ("싱가포르", 1),
        "AED": ("아랍에미리트", 1),
        "UZS": ("우즈베키스탄", 1000),
        "INR": ("인도", 8),
        "IDR": ("인도네시아", 1),
        "JPY": ("일본", 20),
        "CNY": ("중국", 1),
        "KZT": ("카자흐스탄", 40),
        "QAR": ("카타르", 1),
        "KHR": ("캄보디아", 300),
        "THB": ("태국", 3),
        "PHP": ("필리핀", 5),
        "HKD": ("홍콩", 1),
        "MXN": ("멕시코", 2),
        "USD": ("미국", 1),
        "CAD": ("캐나다", 1),
        "BRL": ("브라질", 1),
        "PEN": ("페루", 1),
        "NZD": ("뉴질랜드", 1),
        "XPF": ("프랑스령 폴리네시아", 9),
        "FJD": ("피지", 1),
        "AUD": ("호주", 1),
        "ZAR": ("남아프리카 공화국", 2),
        "MUR": ("모리셔스", 4),
        "EGP": ("이집트", 3),
        "KES": ("케냐", 10)
    }
    return minimum_charge_maping_data


import logging
def handle_step(step_func, error_message, fail_message=None):
    try:
        return step_func()
    except (StaleElementReferenceException, NoSuchElementException) as e:
        from Android.android_common.android_slack import Slack_manager
        if fail_message:
            Slack_manager.test_failed_message(f"{fail_message}: {e}")
        else:
            Slack_manager.test_failed_message(f"{error_message}: {e}")
        logging.error(f"Exception caught in handle_step: {e}")
        print(f"Exception caught in handle_step: {e}")  # 콘솔에도 출력
        raise
    except Exception as e:
        from Android.android_common.android_slack import Slack_manager
        Slack_manager.test_failed_message(f"{error_message}: {e}")
        logging.error(f"Exception caught in handle_step: {e}")
        print(f"Exception caught in handle_step: {e}")  # 콘솔에도 출력
        raise


def extract_and_calculate_and_click(driver, elements, percentage=0.8):
    all_numbers = [int(''.join(re.findall(r'\d+', element.text)))
                   for element in elements]

    if all_numbers:
        total_value = all_numbers[0]
        print(f"추출된 100% 값: {total_value}")
        calculated_value = int(total_value * percentage)
        print(f"계산된 {int(percentage * 100)}% 값: {calculated_value}")

        for digit in str(calculated_value):
            button_xpath = f'//android.widget.Button[@resource-id="com.mobiletoong.travelwallet:id/btnKeyboard" and @text="{
                digit}"]'
            handle_step(lambda: click_element(driver, button_xpath,
                        f"{digit} 버튼 클릭"), f"Failed to click button {digit}")


def minimum_charge_click(driver, currency, minimum_charge_maping_data):
    # 최소 충전 금액을 매핑 데이터에서 찾음
    if currency in minimum_charge_maping_data:
        # (국가 이름, 최소 충전 금액)에서 금액 추출
        charge_number = minimum_charge_maping_data[currency][1]
        print(f"Charge number for {currency}: {charge_number}")
        print(f"{currency} 통화의 최소 충전 금액: {charge_number}")

        # 키패드로 숫자 입력
        for digit in str(charge_number):
            button_xpath = f'//android.widget.Button[@resource-id="com.mobiletoong.travelwallet:id/btnKeyboard" and @text="{
                digit}"]'
            handle_step(lambda: click_element(driver, button_xpath,
                        f"{digit} 버튼 클릭"), f"Failed to click button {digit}")
    else:
        print(f"Currency {currency} not found in the mapping data.")


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 스크롤

def swipe(driver, start_x, start_y, end_x, end_y, duration=1000):
    try:
        driver.swipe(start_x, start_y, end_x, end_y, duration)
        print(f"스크롤 수행: {start_x}, {start_y} -> {end_x}, {end_y}")
    except Exception as e:
        print(f"Exception during swipe: {e}")


def scroll(driver, direction="down"):
    try:
        screen_size = driver.get_window_size()
        width = screen_size['width']
        height = screen_size['height']

        if direction == "down":
            start_y = int(height * 0.6)
            end_y = int(height * 0.2)
        else:
            start_y = int(height * 0.4)
            end_y = int(height * 0.8)

        start_x = width // 2

        swipe(driver, start_x, start_y, start_x, end_y)
    except Exception as e:
        print(f"Exception during scroll: {e}")


def click_element_with_scroll(driver, xpath, description, max_attempts=4):
    attempts = 0
    while attempts < max_attempts:
        try:
            click_element(driver, xpath, description)
            return
        except (Exception, StaleElementReferenceException):
            attempts += 1
            print(
                f"{description} 요소를 찾을 수 없습니다. 스크롤 시도 중... ({attempts}/{max_attempts})")
            scroll(driver)
    raise Exception(f"{description} 요소를 찾을 수 없습니다. 스크롤 시도 후에도 실패")
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------


def check_element_exists(driver, xpath, timeout=0.5):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return True
    except TimeoutException:
        return False