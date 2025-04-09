import time
import json
import random
from android_refund.android_test_refund import KRW_to_foreign_exchange, random_to_foreign_exchange
from selenium.common.exceptions import StaleElementReferenceException
from android_common.android_slack import Slack_manager
from android_refund.android_test_refund import exchange_status_checker
from android_common.android_pass_word import pass_word
from Functions import country_data, click_element, find_elements, click_element_with_retry, handle_step, extract_and_calculate_and_click, click_element_with_scroll
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
foreign_currency_exchange = json_data["foreign_currency_exchange"][0]["number1"][0]

C000 = "'충전하기 선택 성공'"
C001 = "'100% 외화 조회 선택 성공'"
C002 = "'다음 선택 성공'"
C003 = "'충전하기 버튼 선택'"
C004 = "'80% 외화 충전 선택 성공'"
C004_1 = "'환율변동 충전 실패'"
C005 = "'충전 완료 텍스트 확인'"
C006 = "'환불 완료 텍스트 확인'"
C007 = "'환불 실패'"


def random_perform_reset(driver, country_xpath, country_code_to_name):
    country_name = get_country_name(country_xpath, country_code_to_name)
    random_to_foreign_exchange.random_exchange_reset(driver, country_name)

def perform_reset(driver, country_xpath, country_code_to_name):
    country_name = get_country_name(country_xpath, country_code_to_name)
    KRW_to_foreign_exchange.KRW_exchange_reset(driver, country_name)


def get_country_name(country_xpath, country_code_to_name):
    country_code = country_xpath.split('_')[2]
    country_name = country_code_to_name.get(country_code)
    if not country_name:
        raise ValueError(
            f"Country name for code {country_code} not found in mapping")
    return country_name


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
        time.sleep(1)
        handle_step(lambda: click_element_with_retry(
            driver, onboarding_data["next_button_xpath"], "다음 선택"), f"{C002} - Failed at next_button_xpath")
        time.sleep(0.5)
        handle_step(lambda: click_element_with_retry(
            driver, charge_data["charge_xpath"], "충전하기 버튼 선택"), f"{C000} - Failed at charge_xpath")
        pass_word.pass_word_info(driver)
        handle_step(lambda: click_element_with_retry(
            driver, charge_completed_data["charge_close_xpath"], "닫기 선택"), f"{C005} - Failed at charge_close_xpath")
    except Exception as e:
        print(f"Exception during handling exchange rate info: {e}")


class Foreign_Currency_Exchange:
    country_code = "KRW"
    @classmethod
    def KRW_to_foreign_currency(cls, driver):
        all_countries, country_code_to_name = country_data()


        # 한국 통화에 해당하는 XPath 찾기
        for continent_key, countries in all_countries.items():
            for country_xpath in countries:
                # 한국 통화 (KRW)와 일치하는 경우만 실행
                if country_xpath.endswith(f"_{cls.country_code}_xpath"):
                    def KRW_execute_charge_steps():
                        time.sleep(2)
                        # "충전하기 버튼 선택"
                        handle_step(lambda: click_element_with_retry(
                            driver, charge_data["charge_xpath"], "충전하기 버튼 선택"), f"{C000} - Failed at charge_xpath")

                        # 대륙 선택 (Asia 선택)
                        handle_step(lambda: click_element_with_retry(
                            driver, charge_continent_data[continent_key]["charge_continent_" + continent_key.split('_')[
                                2] + "_xpath"],
                            f"{continent_key.split('_')[2]} 선택"), f"{continent_key} - Failed at charge_continent_" + continent_key.split('_')[2] + "_xpath")

                        # 한국 선택
                        handle_step(lambda: click_element_with_retry(
                            driver, charge_continent_data[continent_key][country_xpath], f"{country_code_to_name[cls.country_code]} 선택"), f"{country_xpath} - Failed at {country_xpath}")

                        # 이후 충전 절차
                        time.sleep(3)
                        specific_area_xpath = charge_continent_100_data["charge_country_100%_xpath"]
                        elements = handle_step(lambda: find_elements(
                            driver, specific_area_xpath, "해당 영역 내 모든 요소"), f"{C001} - Failed at specific_area_xpath")
                        extract_and_calculate_and_click(driver, elements)
                        handle_step(lambda: click_element_with_retry(
                            driver, onboarding_data["next_button_xpath"], "다음 선택"), f"{C002} - Failed at next_button_xpath")
                        time.sleep(0.5)
                        handle_step(lambda: click_element_with_retry(
                            driver, charge_data["charge_xpath"], "충전하기 버튼 선택"), f"{C002} - Failed at charge_xpath")
                        time.sleep(0.5)
                        pass_word.pass_word_info(driver)
                        time.sleep(2)
                        completion_status = handle_step(lambda: check_completion_status # pass_word 실행 후 check_completion_status가 충전 성공/실패 확인 check_completion_status가 성공/실패 찾는거에 따라 분기처리
                                                        (driver), f"{C004} - Failed at charge_completed_xpath", fail_message=C004_1)

                        if completion_status is None: # 만약 성공/실패 둘의 텍스트를 찾을수 없으면 해당 에러 메세지 노출
                            raise Exception("충전 성공 또는 환불 실패 텍스트를 찾을 수 없습니다.")

                        if not completion_status: # 환불 실패 텍스트가 발견되면 handle_exchange_rate_info 함수 실행
                            handle_exchange_rate_info(driver)
                            perform_reset(driver, country_xpath,
                                          country_code_to_name)
                        else:

                            handle_step(lambda: click_element_with_retry # 충전 성공 시 닫기 후 환불 진행 
                                        (driver, charge_completed_data["charge_close_xpath"], "닫기 선택"), f"{C005} - Failed at charge_close_xpath")

                            perform_reset(driver, country_xpath,
                                          country_code_to_name)

                    try:
                        KRW_execute_charge_steps()
                        status, reason_text = exchange_status_checker.check_exchange_status(driver)

                        if status is True:
                            try:
                                Slack_manager.test_completed_message(f"{country_code_to_name[cls.country_code]} -> {reason_text} 환전 성공")
                            except Exception as slack_e:
                                print(f"Slack 메시지 전송 중 오류 발생: {slack_e}")
                            return cls.country_code
                        elif status is False:
                            Slack_manager.test_failed_message(f"{country_code_to_name[cls.country_code]} 환전 실패")
                            return None
                        else:
                            print("환전 상태 확인 실패")
                    except Exception as e:
                        print(f"오류 발생: {e}")
                        handle_exchange_rate_info(driver)
                        try:
                            KRW_execute_charge_steps()
                            status, reason_text = exchange_status_checker.check_exchange_status(driver)

                            if status is True:
                                try:
                                    Slack_manager.test_completed_message(f"{country_code_to_name[cls.country_code]} -> {reason_text} 환전 성공")
                                except Exception as slack_e:
                                    print(f"재시도 후 Slack 메시지 전송 중 오류 발생: {slack_e}")
                                return cls.country_code
                            elif status is False:
                                Slack_manager.test_failed_message(f"{country_code_to_name[cls.country_code]} -> {reason_text} 환전 실패")
                                return None
                        except Exception as inner_e:
                            print(f"재시도 중 예외 발생: {inner_e}")
                            Slack_manager.test_failed_message(f"{country_code_to_name[cls.country_code]} -> {reason_text} 충전 실패")
                            return None

                            
    
class Randem_Foreign_Currency_Exchange:
    @staticmethod
    def random_foreign_currency_to_foreign_currency_exchange(driver):
        all_countries, country_code_to_name = country_data()

        # 대륙별 국가 중에서 무작위로 선택
        continent_key = random.choice(list(all_countries.keys()))
        country_xpath = random.choice(all_countries[continent_key])
        country_code = country_xpath.split('_')[-2]

        def randem_execute_charge_steps():
            time.sleep(2)
            handle_step(lambda: click_element_with_retry(driver, charge_data["charge_xpath"], "충전하기 버튼 선택"), f"{C000} - Failed at charge_xpath")
            handle_step(lambda: click_element_with_retry(driver, charge_continent_data[continent_key]["charge_continent_" + continent_key.split('_')[2] + "_xpath"], f"{continent_key.split('_')[2]} 선택"), f"{continent_key} - Failed at charge_continent_" + continent_key.split('_')[2] + "_xpath")
            handle_step(lambda: click_element_with_scroll(driver, charge_continent_data[continent_key][country_xpath], f"{country_code_to_name[country_code]} 선택"), f"{country_xpath} - Failed at {country_xpath}")

            time.sleep(3)
            specific_area_xpath = charge_continent_100_data["charge_country_100%_xpath"]
            elements = handle_step(lambda: find_elements(driver, specific_area_xpath, "해당 영역 내 모든 요소"), f"{C001} - Failed at specific_area_xpath")
            extract_and_calculate_and_click(driver, elements)
            handle_step(lambda: click_element_with_retry(driver, onboarding_data["next_button_xpath"], "다음 선택"), f"{C002} - Failed at next_button_xpath")
            time.sleep(0.5)
            handle_step(lambda: click_element_with_retry(driver, charge_data["charge_xpath"], "충전하기 버튼 선택"), f"{C002} - Failed at charge_xpath")
            time.sleep(0.5)
            pass_word.pass_word_info(driver)
            time.sleep(2)

            completion_status = handle_step(lambda: check_completion_status(driver), f"{C004} - Failed at charge_completed_xpath", fail_message=C004_1)

            if completion_status is None:
                raise Exception("충전 성공 또는 실패 텍스트를 찾을 수 없습니다.")

            if not completion_status:
                handle_exchange_rate_info(driver)
                random_perform_reset(driver, country_xpath, country_code_to_name)
            else:
                handle_step(lambda: click_element_with_retry(driver, charge_completed_data["charge_close_xpath"], "닫기 선택"), f"{C005} - Failed at charge_close_xpath")
                random_perform_reset(driver, country_xpath, country_code_to_name)

        try:
            randem_execute_charge_steps()
            status, reason_text = exchange_status_checker.check_exchange_status(driver)

            if status is True:
                try:
                    Slack_manager.test_completed_message(f"{country_code_to_name[country_code]} -> {reason_text} 환전 성공")
                except Exception as slack_e:
                    print(f"Slack 메시지 전송 중 오류 발생: {slack_e}")
                return country_code
            elif status is False:
                Slack_manager.test_failed_message(f"{country_code_to_name[country_code]} 환전 실패")
                return None
            else:
                print("환전 상태 확인 실패")
        except Exception as e:
            print(f"오류 발생: {e}")
            handle_exchange_rate_info(driver)
            try:
                randem_execute_charge_steps()
                status, reason_text = exchange_status_checker.check_exchange_status(driver)

                if status is True:
                    try:
                        Slack_manager.test_completed_message(f"{country_code_to_name[country_code]} -> {reason_text} 환전 성공")
                    except Exception as slack_e:
                        print(f"재시도 후 Slack 메시지 전송 중 오류 발생: {slack_e}")
                    return country_code
                elif status is False:
                    Slack_manager.test_failed_message(f"{country_code_to_name[country_code]} -> {reason_text} 환전 실패")
                    return None
            except Exception as inner_e:
                print(f"재시도 중 예외 발생: {inner_e}")
                Slack_manager.test_failed_message(f"{country_code_to_name[country_code]} -> {reason_text} 충전 실패")
                return None
