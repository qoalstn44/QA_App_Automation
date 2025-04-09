import os
import sys
import json
import re
import time
from Functions import country_data, check_element_exists
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from ios_common.ios_slack import Slack_manager
from ios_common.ios_pass_word import pass_word
from ios_refund.ios_test_refund import My_Wallet_Reset
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# JSON 파일 경로
json_file_path = 'iOS/ios_DB/ios_DB.json'

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
C005 = "'충전 완료 텍스트 확인'"


# def handle_step(step_func, error_message):
#     try:
#         return step_func(StaleElementReferenceException, NoSuchElementException, TimeoutException, Exception)
#     except () as e:
#         Slack_manager.test_failed_message(f"{error_message}: {e}")
# raise


def handle_step(step_func, error_message, fail_message=None):
    try:
        return step_func()
    except (StaleElementReferenceException, NoSuchElementException, TimeoutException) as e:
        if fail_message:
            Slack_manager.test_failed_message(f"{fail_message}: {e}")
        else:
            Slack_manager.test_failed_message(f"{error_message}: {e}")
        raise
    except Exception as e:
        Slack_manager.test_failed_message(f"{error_message}: {e}")
        raise


def click_element(driver, xpath, description):
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()
    print(f"{description} 클릭 완료")


def send_keys(driver, xpath, keys, description):
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    element.send_keys(keys)
    print(f"{description} 입력 완료")


def find_elements(driver, xpath, description):
    wait = WebDriverWait(driver, 20)
    elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, xpath)))
    print(f"{description} 요소들 찾기 완료")
    return elements


def extract_and_calculate_and_click(driver, elements, percentage=0.8):
    all_numbers = [int(''.join(re.findall(r'\d+', element.text)))
                   for element in elements]

    if all_numbers:
        total_value = all_numbers[0]
        print(f"추출된 100% 값: {total_value}")
        calculated_value = int(total_value * percentage)
        print(f"계산된 {int(percentage * 100)}% 값: {calculated_value}")

        for digit in str(calculated_value):
            button_xpath = f'//XCUIElementTypeButton[@name="{digit}"]'
            handle_step(lambda: click_element(driver, button_xpath,
                        f"{digit} 버튼 클릭"), f"Failed to click button {digit}")


def handle_exchange_rate_info(driver):
    try:
        handle_step(lambda: find_elements(
            driver, charge_completed_data["Change_exchange_rate_information"], "환율 정보가 변경되었습니다 텍스트 확인"), "Failed to find '환율 정보가 변경되었습니다' 텍스트")
        handle_step(lambda: click_element(
            driver, '//XCUIElementTypeButton[@name="확인"]', "확인 버튼 클릭"), "Failed to click '확인' 버튼")
        handle_step(lambda: click_element(
            driver, onboarding_data["next_xpath"], "다음 선택"), f"{C002} - Failed at next_xpath")
        handle_step(lambda: click_element(
            driver, charge_data["charge_xpath"], "충전하기 버튼 선택"), f"{C000} - Failed at charge_xpath")

        pass_word.pass_word_info(driver)

        handle_step(lambda: find_elements(
            driver, charge_completed_data["charge_completed"], "충전 완료 텍스트 확인"), "Failed at charge_completed")
        handle_step(lambda: click_element(
            driver, charge_completed_data["charge_close"], "닫기 선택"), f"{C005} - Failed at charge_close")
    except Exception as e:
        print(f"Exception during handling exchange rate info: {e}")


def scroll(driver, distance=0.5):
    try:
        driver.execute_script(
            "mobile: scroll", {"direction": "down", "distance": distance})
        print(f"스크롤 다운 방향으로 {distance} 만큼 이동")
    except Exception as e:
        print(f"스크롤 중 예외 발생: {e}")


def click_element_until_visible(driver, xpath, description, max_attempts=5, scroll_distance=0.5):
    attempts = 0
    while attempts < max_attempts:
        try:
            click_element(driver, xpath, description)
            return
        except (StaleElementReferenceException, TimeoutException):
            scroll(driver, distance=scroll_distance)
            attempts += 1
    raise (
        f"Failed to click element {description} after {max_attempts} attempts")


class My_Wallet_Charge:
    @classmethod
    def charge_and_refund_all(cls, driver):
        all_countries, country_code_to_name = country_data()

        for continent_key, countries in all_countries.items():
            for country_xpath in countries:
                def execute_charge_steps():
                    handle_step(lambda: click_element(
                        driver, charge_data["charge_xpath"], "충전하기 버튼 선택"), f"{C000} - Failed at charge_xpath")
                    
                    handle_step(lambda: click_element(
                        driver, charge_continent_data[continent_key]["charge_continent_" + continent_key.split('_')[
                            2] + "_xpath"],
                        f"{continent_key.split('_')[2]} 선택"), f"{continent_key} - Failed at charge_continent_" + continent_key.split('_')[2] + "_xpath")
                    
                    click_element_until_visible(driver, charge_continent_data[continent_key][country_xpath], country_xpath.split(
                        "_")[2] + " 선택"), f"{country_xpath} - Failed at {country_xpath}"
                    
                    specific_area_xpath = charge_continent_100_data["charge_country_100%_xpath"] + '//*'

                    elements = handle_step(lambda: find_elements(
                        driver, specific_area_xpath, "해당 영역 내 모든 요소"), f"{C001} - Failed at specific_area_xpath")
                    
                    extract_and_calculate_and_click(driver, elements)
                    
                    handle_step(lambda: click_element(
                        driver, onboarding_data["next_xpath"], "다음 선택"), f"{C002} - Failed at next_xpath")
                    time.sleep(0.5)
                    handle_step(lambda: click_element(
                        driver, charge_data["charge_xpath"], "충전하기 버튼 선택"), f"{C002} - Failed at charge_xpath")
                    time.sleep(0.5)
                    pass_word.pass_word_info(driver)
                    handle_step(lambda: find_elements(
                        driver, charge_completed_data["charge_completed"], "충전 완료 텍스트 확인"), "Failed at charge_completed")
                    
                    handle_step(lambda: click_element(
                        driver, charge_completed_data["charge_close"], "닫기 선택"), f"{C005} - Failed at charge_close")
                    
                    # ✅ 충전 성공 후 바텀시트 감지 및 자동 닫기 처리
                    if check_element_exists(driver, charge_completed_data["charge_meeting_post_bottom_sheet_close_xpath"]):
                        print("바텀시트 감지됨, 닫기 진행")
                        handle_step(lambda: click_element(
                            driver, charge_completed_data["charge_meeting_post_bottom_sheet_close_xpath"], "바텀시트 닫기"), 
                            "Failed at charge_meeting_post_bottom_sheet_close_xpath")
                        time.sleep(1)  # ✅ 바텀시트 닫힘 반영 대기

                    # 환불 단계 추가
                    country_code = country_xpath.split('_')[2]
                    country_name = country_code_to_name.get(country_code)
                    if not country_name:
                        raise ValueError(
                            f"Country name for code {country_code} not found in mapping")

                    My_Wallet_Reset.reset(driver, country_name)

                try:
                    execute_charge_steps()
                    Slack_manager.test_completed_message(
                        f"{country_xpath} 충전, 환불 완료")
                except Exception as e:
                    handle_exchange_rate_info(driver)
                    try:
                        execute_charge_steps()
                        Slack_manager.test_completed_message(
                            f"{country_xpath} 충전, 환불 완료")
                    except Exception as inner_e:
                        print(
                            f"Exception during retry after handling exchange rate info: {inner_e}")
                        Slack_manager.test_failed_message(
                            f"{country_xpath} 충전 실패")
