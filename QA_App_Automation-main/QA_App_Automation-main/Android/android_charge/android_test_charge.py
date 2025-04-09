import time
import json
from android_refund.android_test_refund import My_Wallet_Reset
from selenium.common.exceptions import StaleElementReferenceException
from android_common.android_slack import Slack_manager
from android_common.android_pass_word import pass_word
from android_refund.android_test_refund import ClickLaterButton
from appium.options.android import UiAutomator2Options

from Functions import country_data, click_element, find_elements, click_element_with_retry, handle_step, extract_and_calculate_and_click, check_element_exists
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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


C000 = "'충전하기 선택 성공'"
C001 = "'100% 외화 조회 선택 성공'"
C002 = "'다음 선택 성공'"
C003 = "'충전하기 버튼 선택'"
C004 = "'80% 외화 충전 선택 성공'"
C004_1 = "'환율변동 충전 실패'"
C005 = "'충전 완료 텍스트 확인'"
C006 = "'환불 완료 텍스트 확인'"
C007 = "'환불 실패'"


def check_completion_status(driver):
    elements = find_elements(
        driver, charge_completed_data["charge_completed_xpath"], "충전 검증 중...")
    for element in elements:
        text = element.text
        if "충전 완료" in text:
            print("[충전 완료] 확인됨.")
            return True  # 성공 시 그대로 진행
        elif "충전 실패" in text:
            print("[충전 실패] 확인됨.")
            return False  # 실패 시 다시 충전 시도
    return None  # 해당 텍스트가 없는 경우


def handle_exchange_rate_info(driver):
    try:
        handle_step(lambda: click_element_with_retry(
            driver, charge_completed_data['change_exchange_rate_information_completed_xpath'], "'충전 환율 변동 [확인] 버튼 클릭'"), "Failed to click '확인' 버튼")
        time.sleep(2)
        handle_step(lambda: click_element_with_retry(
            driver, onboarding_data["next_button_xpath"], "다음 선택"), f"{C002} - Failed at next_button_xpath")
        time.sleep(2)
        handle_step(lambda: click_element_with_retry(
            driver, charge_data["charge_xpath"], "충전하기 버튼 선택"), f"{C000} - Failed at charge_xpath")
        pass_word.pass_word_info(driver)
        handle_step(lambda: click_element_with_retry(
            driver, charge_completed_data["charge_close_xpath"], "닫기 선택"), f"{C005} - Failed at charge_close_xpath")
        time.sleep(2)
    except Exception as e:
        print(f"Exception during handling exchange rate info: {e}")


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


def perform_reset(driver, country_xpath, country_code_to_name):
    country_name = get_country_name(country_xpath, country_code_to_name)
    My_Wallet_Reset.reset(driver, country_name)


def get_country_name(country_xpath, country_code_to_name):
    country_code = country_xpath.split('_')[2]
    country_name = country_code_to_name.get(country_code)
    if not country_name:
        raise ValueError(
            f"Country name for code {country_code} not found in mapping")
    return country_name



class My_Wallet_Charge:
    @classmethod
    def charge_and_refund_all(cls, driver):
        all_countries, country_code_to_name = country_data()

        for continent_key, countries in all_countries.items():
            for country_xpath in countries:
                success = False  # 성공 여부 플래그
                while not success:  # 특정 국가 충전 재시도 루프
                    try:
                        def execute_charge_steps():
                            time.sleep(3)
                            handle_step(lambda: click_element_with_retry(
                                driver, charge_data["charge_xpath"], "충전하기 버튼 선택"), f"{C000} - Failed at charge_xpath")
                            handle_step(lambda: click_element_with_retry(
                                driver, charge_continent_data[continent_key]["charge_continent_" + continent_key.split('_')[
                                    2] + "_xpath"],
                                f"{continent_key.split('_')[2]} 선택"), f"{continent_key} - Failed at charge_continent_" + continent_key.split('_')[2] + "_xpath")
                            time.sleep(3)

                            handle_step(lambda: click_element_with_scroll(driver, charge_continent_data[continent_key][country_xpath], country_xpath.split(
                                "_")[2] + " 선택"), f"{country_xpath} - Failed at {country_xpath}")

                            time.sleep(3)
                            specific_area_xpath = charge_continent_100_data["charge_country_100%_xpath"]
                            elements = handle_step(lambda: find_elements(
                                driver, specific_area_xpath, "해당 영역 내 모든 요소"), f"{C001} - Failed at specific_area_xpath")
                            extract_and_calculate_and_click(driver, elements)
                            handle_step(lambda: click_element_with_retry(
                                driver, onboarding_data["next_button_xpath"], "다음 선택"), f"{C002} - Failed at next_button_xpath")
                            time.sleep(3)
                            handle_step(lambda: click_element_with_retry(
                                driver, charge_data["charge_xpath"], "충전하기 버튼 선택"), f"{C002} - Failed at charge_xpath")
                            time.sleep(3)
                            pass_word.pass_word_info(driver)
                            time.sleep(3)
                            completion_status = handle_step(lambda: check_completion_status(
                                driver), f"{C004} - Failed at charge_completed_xpath", fail_message=C004_1)

                            if completion_status is None:
                                raise Exception("충전 성공 또는 환불 실패 텍스트를 찾을 수 없습니다.")

                            if not completion_status:
                                # 환불 실패 텍스트가 발견되면 handle_exchange_rate_info 함수 실행
                                handle_exchange_rate_info(driver)
                            else:
                                # 충전 성공 시 계속 진행
                                time.sleep(3)
                                handle_step(lambda: click_element_with_retry(driver, charge_completed_data["charge_close_xpath"], "닫기 선택"), f"{C005} - Failed at charge_close_xpath")
                                time.sleep(3)

                                if check_element_exists(driver, charge_completed_data["charge_meeting_post_bottom_sheet_close_xpath"]):
                                    print("바텀시트 감지됨, 닫기 진행")
                                    handle_step(lambda: click_element_with_retry(
                                        driver, charge_completed_data["charge_meeting_post_bottom_sheet_close_xpath"], "바텀시트 닫기"), "Failed at charge_meeting_post_bottom_sheet_close_xpath")
                                    time.sleep(3)  # 바텀시트 닫힘 반영 대기

                        execute_charge_steps()
                        My_Wallet_Reset.reset(driver, get_country_name(country_xpath, country_code_to_name))  # 환불은 독립적으로 실행
                        Slack_manager.test_completed_message(f"{country_xpath} 충전, 환불 완료")
                        success = True

                    except Exception:
                        print(f"Failed to charge {country_xpath}. Retrying...")








