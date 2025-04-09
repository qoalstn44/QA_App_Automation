from Functions import find_elements, click_element_with_retry, handle_step, click_element, click_element_with_scroll, click_latest_screen_element
from selenium.common.exceptions import TimeoutException
from ios_common.ios_pass_word import currency_exchange_pass_word, pass_word
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import os
import sys
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Functions import country_data

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
refund_data = json_data["refund"][0]["number1"][0]
refund_country_data = json_data["refund"][0]["number2"][0]
charge_completed_data = json_data["charge"][0]["number4"][0]
charge_data = json_data["charge"][0]["number1"][0]

charge_continent_data = json_data["charge"][0]["number2"][0]
foreign_currency_exchange_data = json_data["foreign_currency_exchange"][0]["number1"][0]


refund_xpath_mapping = {
    "노르웨이": refund_country_data["refund_country_NOK_xpath"],
    "덴마크": refund_country_data["refund_country_DKK_xpath"],
    "스웨덴": refund_country_data["refund_country_SEK_xpath"],
    "스위스": refund_country_data["refund_country_CHF_xpath"],
    "아이슬란드": refund_country_data["refund_country_ISK_xpath"],
    "영국": refund_country_data["refund_country_GBP_xpath"],
    "유럽": refund_country_data["refund_country_EUR_xpath"],
    "체코": refund_country_data["refund_country_CZK_xpath"],
    "튀르키예": refund_country_data["refund_country_TRY_xpath"],
    "폴란드": refund_country_data["refund_country_PLN_xpath"],
    "헝가리": refund_country_data["refund_country_HUF_xpath"],
    "멕시코": refund_country_data["refund_country_MXN_xpath"],
    "미국": refund_country_data["refund_country_USD_xpath"],
    "캐나다": refund_country_data["refund_country_CAD_xpath"],
    "브라질": refund_country_data["refund_country_BRL_xpath"],
    "페루": refund_country_data["refund_country_PEN_xpath"],
    "뉴질랜드": refund_country_data["refund_country_NZD_xpath"],
    "프랑스령 폴리네시아(타히티)": refund_country_data["refund_country_XPF_xpath"],
    "피지": refund_country_data["refund_country_FJD_xpath"],
    "호주": refund_country_data["refund_country_AUD_xpath"],
    "남아공": refund_country_data["refund_country_ZAR_xpath"],
    "모리셔스": refund_country_data["refund_country_MUR_xpath"],
    "이집트": refund_country_data["refund_country_EGP_xpath"],
    "케냐": refund_country_data["refund_country_KES_xpath"],
    "네팔": refund_country_data["refund_country_NPR_xpath"],
    "대만": refund_country_data["refund_country_TWD_xpath"],
    "대한민국": refund_country_data["refund_country_KRW_xpath"],
    "라오스": refund_country_data["refund_country_LAK_xpath"],
    "마카오": refund_country_data["refund_country_MOP_xpath"],
    "말레이시아": refund_country_data["refund_country_MYR_xpath"],
    "몽골": refund_country_data["refund_country_MNT_xpath"],
    "베트남": refund_country_data["refund_country_VND_xpath"],
    "사우디아라비아": refund_country_data["refund_country_SAR_xpath"],
    "싱가포르": refund_country_data["refund_country_SGD_xpath"],
    "아랍에미리트": refund_country_data["refund_country_AED_xpath"],
    "우즈베키스탄": refund_country_data["refund_country_UZS_xpath"],
    "인도": refund_country_data["refund_country_INR_xpath"],
    "인도네시아": refund_country_data["refund_country_IDR_xpath"],
    "일본": refund_country_data["refund_country_JPY_xpath"],
    "중국": refund_country_data["refund_country_CNY_xpath"],
    "카자흐스탄": refund_country_data["refund_country_KZT_xpath"],
    "카타르": refund_country_data["refund_country_QAR_xpath"],
    "캄보디아": refund_country_data["refund_country_KHR_xpath"],
    "태국": refund_country_data["refund_country_THB_xpath"],
    "필리핀": refund_country_data["refund_country_PHP_xpath"],
    "홍콩": refund_country_data["refund_country_HKD_xpath"]
}


C000 = "'내 지갑 첫번째 레이블 선택 성공'"
C001 = "'환불하기 버튼 선택 성공'"
C002 = "'환불 가능 금액(전체) 선택 성공'"
C003 = "'다음 버튼 선택 성공'"
C004 = "'환불 하기 버튼 선택 성공'"
C005 = "'환불 완료 텍스트 확인 성공'"
C006 = "'확인 버튼 선택 성공'"
C007 = "'뒤로가기 버튼 선택 성공'"
C008 = "'환불 성공'"


def handle_exchange_rate_info(driver):
    try:
        handle_step(lambda: find_elements(
            driver, charge_completed_data["Change_exchange_rate_information"], "환율 정보가 변경되었습니다 텍스트 확인"), "Failed to find '환율 정보가 변경되었습니다' 텍스트")
        handle_step(lambda: click_element(
            driver, '//XCUIElementTypeButton[@name="확인"]', "확인 버튼 클릭"), "Failed to click '확인' 버튼")
        handle_step(lambda: click_element(
            driver, onboarding_data["next_xpath"], "다음 선택"), f"{C003} - Failed at next_xpath")
        time.sleep(0.5)
        handle_step(lambda: click_element(
            driver, refund_data["refund_next_xpath"], "환불하기"), f"{C004} - Failed at refund_next_xpath")

        pass_word.pass_word_info(driver)

        handle_step(lambda: click_element(
            driver, onboarding_data["receive_marketing_xpath"], "확인 선택"), f"{C000} - Failed at receive_marketing_xpath")
        handle_step(lambda: find_elements(
            driver, refund_data["refund_completed_text_xpath"], "환불 완료 텍스트 확인"), f"{C000} - Failed at refund_completed_text_xpath")
        handle_step(lambda: click_element(
            driver, onboarding_data["receive_marketing_xpath"], "확인"), f"{C006} - Failed at receive_marketing_xpath")
        handle_step(lambda: click_element_with_retry(
            driver, refund_data["refund_usage_details_back_button_xpath"], "뒤로가기"), f"{C007} - Failed at refund_usage_details_back_button_xpath")
    except Exception as e:
        print(f"Exception during handling exchange rate info: {e}")


class My_Wallet_Reset:
    @classmethod
    def reset(cls, driver, country_name):
        country_xpath = refund_xpath_mapping.get(country_name)
        if not country_xpath:
            raise ValueError(
                f"Refund XPATH for {country_name} not found in mapping")

        def execute_reset():
            handle_step(lambda: click_element(
                driver, country_xpath, f"{country_name} 선택"), f"{C000} - Failed at {country_xpath}")
            handle_step(lambda: click_element(
                driver, refund_data["refund_xpath"], "환불하기"), f"{C001} - Failed at refund_xpath")
            handle_step(lambda: click_element(
                driver, refund_data["refund_full_amount_xpath"], "환불 가능 금액(전체)"), f"{C002} - Failed at refund_full_amount_xpath")
            handle_step(lambda: click_element(
                driver, onboarding_data["next_xpath"], "다음"), f"{C003} - Failed at next_xpath")
            time.sleep(2)
            handle_step(lambda: click_element(
                driver, refund_data["refund_next_xpath"], "환불하기"), f"{C004} - Failed at refund_next_xpath")

            pass_word.pass_word_info(driver)

            lambda: find_elements(
                driver, refund_data["refund_completed_text_xpath"], "환불 완료 텍스트 확인"), f"{C005} - Failed at refund_completed_text_xpath"
            handle_step(lambda: click_element(
                driver, onboarding_data["receive_marketing_xpath"], "확인"), f"{C006} - Failed at receive_marketing_xpath")
            time.sleep(2)
            handle_step(lambda: click_element(
                driver, refund_data["refund_usage_details_back_button_xpath"], "뒤로가기"), f"{C007} - Failed at refund_usage_details_back_button_xpath")

        try:
            execute_reset()
        except Exception as e:
            handle_exchange_rate_info(driver)
            try:
                execute_reset()
            except Exception as inner_e:
                print(
                    f"Exception during retry after handling exchange rate info: {inner_e}")


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def charge_USD_currency(driver):
    all_countries, country_code_to_name = country_data()
    country_code = "USD"
    # 한국 통화에 해당하는 XPath 찾기
    for continent_key, countries in all_countries.items():
        for country_xpath in countries:
            # 한국 통화 (KRW)와 일치하는 경우만 실행
            if country_xpath.endswith(f"_{country_code}_xpath"):
                time.sleep(2)
                # 북미 선택
                handle_step(lambda: click_element_with_retry(
                    driver, charge_continent_data[continent_key]["charge_continent_" + continent_key.split('_')[
                        2] + "_xpath"],
                    f"{continent_key.split('_')[2]} 선택"), f"{continent_key} - Failed at charge_continent_" + continent_key.split('_')[2] + "_xpath")

                # 미국 선택
                handle_step(lambda: click_element_with_retry(
                    driver, charge_continent_data[continent_key][country_xpath], f"{country_code_to_name[country_code]} 선택"), f"{country_xpath} - Failed at {country_xpath}")
                

class KRW_to_foreign_exchange:
    @classmethod
    def KRW_exchange_reset(cls, driver, country):
        country_xpath = refund_xpath_mapping.get(country)
        if not country_xpath:
            raise ValueError(f"Refund XPATH for {country} not found in mapping")

        try:
            handle_step(lambda: click_element_with_retry(
                driver, country_xpath, f"{country} 선택"), f"{C000} - Failed at {country_xpath}")

            handle_step(lambda: click_element(
                driver, foreign_currency_exchange_data["foreign_currency_exchange_xpath"], "외화간 환전 선택"), f"{C005} - Failed at foreign_currency_exchange")

            # Predicate String을 사용하여 최신 화면의 버튼 클릭
            handle_step(lambda: click_element(
                driver, foreign_currency_exchange_data["total_amount_of_foreign_currency_exchange_xpath"], "외화간 환전 전체 통화 선택"), f"{C005} - Failed at total_amount_of_foreign_currency_exchange_xpath")
            
            handle_step(lambda: click_element(
                driver, foreign_currency_exchange_data["foreign_currency_exchange_country_xpath"], "외화간 환전할 국가 선택"), f"{C005} - Failed at foreign_currency_exchange_country")

            charge_USD_currency(driver)  # 미국 통화 선택

            handle_step(lambda: click_element_with_retry(
                driver, foreign_currency_exchange_data["exchange_next_button_xpath"], "환전하기 버튼 선택"), f"{C003} - Failed at next_button_xpath")
            handle_step(lambda: click_element(
                driver, foreign_currency_exchange_data["exchange_button_xpath"], "환전 버튼 선택"), f"{C005} - Failed at exchange_button_xpath")

            currency_exchange_pass_word.currency_exchange_pass_word_info(driver)

        except Exception as e:
            print(e)



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def random_handle_rexchange_rate_info(driver):
    try:
        # 환전 실패 시 다시 시도 (최대 3회 재시도)
        retry_count = 0
        max_retries = 3
        while exchange_status is False and retry_count < max_retries:
            print(f"환전 실패, 프로세스를 다시 시도합니다. 재시도 횟수: {retry_count + 1}/{max_retries}")
            retry_count += 1
            handle_step(lambda: click_element_with_retry(
                driver, foreign_currency_exchange_data["final_confirmation_button_for_foreign_currency_exchange_xpath"], "환전 최종 확인 선택"), f"{C003} - Failed at final_confirmation_button_for_foreign_currency_exchange_xpath")
            handle_step(lambda: click_element_with_retry(
                driver, onboarding_data["next_button_xpath"], "다음"), f"{C003} - Failed at next_button_xpath")
            handle_step(lambda: click_element(  # 환전 버튼 선택
                driver, foreign_currency_exchange_data["exchange_button_xpath"], "환전 버튼 선택"), f"{C005} - Failed at exchange_button_xpath")
            currency_exchange_pass_word.currency_exchange_pass_word_info(driver)
            
            # 다시 환전 상태 확인
            exchange_status = exchange_status_checker.check_exchange_status(driver)
    except Exception as e:
        print(e)


def random_exchange_click(driver, exclude_country_code=None):
    # 대륙별 국가 중에서 무작위로 선택
    all_countries, country_code_to_name = country_data()
    
    # 충전 통화를 제외한 모든 국가 필터링
    if exclude_country_code:
        filtered_countries = {
            continent: [xpath for xpath in countries if exclude_country_code not in xpath]
            for continent, countries in all_countries.items()
        }
    else:
        filtered_countries = all_countries

    # 필터링된 국가 목록에서 무작위로 대륙과 국가 선택
    continent_key = random.choice(list(filtered_countries.keys()))
    country_xpath = random.choice(filtered_countries[continent_key])
    country_code = country_xpath.split('_')[-2]  # 국가 코드 추출

    # 대륙 선택
    handle_step(lambda: click_element_with_retry(
        driver, charge_continent_data[continent_key]["charge_continent_" + continent_key.split('_')[2] + "_xpath"],
        f"{continent_key.split('_')[2]} 선택"), f"{continent_key} - Failed at charge_continent_" + continent_key.split('_')[2] + "_xpath")
    
    # 선택한 국가 클릭
    handle_step(lambda: click_element_with_scroll(
        driver, charge_continent_data[continent_key][country_xpath], f"{country_code_to_name[country_code]} 선택"), f"{country_xpath} - Failed at {country_xpath}")


class exchange_status_checker:
    exchange_status = None
    reason_text = "결과 없음"
    
    @classmethod
    def check_exchange_status(cls, driver, timeout=20):
        # 이미 저장된 상태가 있으면 해당 상태를 반환
        if cls.exchange_status is not None:
            print("DEBUG: 저장된 상태 반환")
            return cls.exchange_status, cls.reason_text

        try:
            print("DEBUG: 환전 성공/실패 여부 확인 대기 중...")
            elements = WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, foreign_currency_exchange_data["exchange_pass_fail_xpath"]))
            )
            for element in elements:
                text = element.text
                if "환전완료" in text:
                    reason_elements = WebDriverWait(driver, timeout).until(
                        EC.presence_of_all_elements_located((By.XPATH, foreign_currency_exchange_data["exchange_pass_fail_xpath"]))
                    )
                    cls.reason_text = reason_elements[0].text if reason_elements else "결과 없음"
                    print(f"[환전완료] 확인됨. 결과: {cls.reason_text}")
                    cls.exchange_status = True  # 환전 성공 상태 저장
                    return cls.exchange_status, cls.reason_text
                elif "환전실패" in text:
                    reason_elements = WebDriverWait(driver, timeout).until(
                        EC.presence_of_all_elements_located((By.XPATH, foreign_currency_exchange_data["exchange_pass_fail_xpath"]))
                    )
                    cls.reason_text = reason_elements[0].text if reason_elements else "결과 없음"
                    print(f"[환전실패] 확인됨. 결과: {cls.reason_text}")
                    cls.exchange_status = False  # 환전 실패 상태 저장
                    return cls.exchange_status, cls.reason_text

            print("환전 상태 확인되지 않음.")
            return None, cls.reason_text

        except TimeoutException:
            print("환전 상태 요소 로딩 실패로 TimeoutException 발생.")
            return None, cls.reason_text

    @classmethod
    def reset_status(cls):
        # 상태를 초기화하여 이후에 다시 상태를 확인할 수 있게 함
        cls.exchange_status = None
        cls.reason_text = "결과 없음"


class random_to_foreign_exchange:  # 내 지갑안에 통화 환전
    @classmethod
    def random_exchange_reset(cls, driver, country_code):
        # 충전된 통화의 Xpath를 얻기 위해 country_code를 사용
        country_xpath = refund_xpath_mapping.get(country_code)
        if not country_xpath:
            raise ValueError(f"Refund XPATH for {country_code} not found in mapping")

        def execute_reset():
            # 환전 절차 수행
            handle_step(lambda: click_element_with_retry(driver, country_xpath, f"{country_code} 선택"), f"{C000} - Failed at {country_xpath}")

            handle_step(lambda: click_element(driver, foreign_currency_exchange_data["foreign_currency_exchange_xpath"], "외화간 환전 선택"), f"{C005} - Failed at foreign_currency_exchange")
        
            handle_step(lambda: click_element(driver, foreign_currency_exchange_data["total_amount_of_foreign_currency_exchange_xpath"], "외화간 환전 전체 금액 선택"), f"{C005} - Failed at total_amount_of_foreign_currency_exchange")
            handle_step(lambda: click_element(driver, foreign_currency_exchange_data["foreign_currency_exchange_country_xpath"], "외화간 환전할 국가 선택"), f"{C005} - Failed at foreign_currency_exchange_country")

            random_exchange_click(driver, exclude_country_code=country_code)
            handle_step(lambda: click_element_with_retry(driver, foreign_currency_exchange_data["exchange_next_button_xpath"], "다음"), f"{C003} - Failed at next_button_xpath")
            handle_step(lambda: click_element(driver, foreign_currency_exchange_data["exchange_button_xpath"], "환전 버튼 선택"), f"{C005} - Failed at exchange_button_xpath")

            currency_exchange_pass_word.currency_exchange_pass_word_info(driver)

            exchange_status, reason_text = False, "결과 없음"
            try:
                # 환전 상태 확인
                exchange_status, reason_text = exchange_status_checker.check_exchange_status(driver)
                if exchange_status is None:
                    raise Exception("환전 상태 확인 실패")  # 상태가 None이면 예외 발생
            except Exception as e:
                print(f"환전 상태 확인 중 예외 발생: {e}")
                random_handle_rexchange_rate_info(driver)  # 환율 정보 재설정
                exchange_status, reason_text = exchange_status_checker.check_exchange_status(driver)  # 상태 재확인

            # 환전 성공/실패에 따른 처리
            if exchange_status is False:
                print("최대 재시도 횟수에 도달하여 환전을 완료할 수 없습니다.")
                return False
            elif exchange_status is True:
                print(f"환전 성공: {reason_text}")
                # 환전 성공 시 최종 확인 버튼 클릭
                handle_step(lambda: click_element_with_retry(
                    driver, foreign_currency_exchange_data["final_confirmation_button_for_foreign_currency_exchange_xpath"],
                    "환전 최종 확인 선택"), f"{C005} - Failed at final_confirmation_button_for_foreign_currency_exchange_xpath")
                
                # 뒤로 가기 버튼 클릭 시도
                try:
                    handle_step(lambda: click_element_with_retry(
                        driver, refund_data["refund_usage_details_back_button_xpath"], "뒤로가기"), f"{C007} - Failed at refund_usage_details_back_button_xpath")
                except Exception:
                    handle_step(lambda: click_element_with_retry(driver, refund_data["refund_review_xpath"], "나중에"), f"{C001} - Failed at refund_review_xpath")
                return True  # 성공적으로 완료 시 True 반환

        # execute_reset 호출 및 예외 처리
        try:
            # execute_reset을 한 번만 호출하여 결과 저장
            success = execute_reset()
            # 호출 결과에 따라 메시지 출력
            if success:
                print("환전이 성공적으로 완료되었습니다.")
            else:
                print("환전 실패: 환전 절차 완료되지 않음")

        except Exception as e:
            print(f"최초 실행 중 오류 발생: {e}")
            handle_exchange_rate_info(driver)  # 오류 발생 시 환율 정보 처리
            try:
                # 재시도 실행
                if execute_reset():
                    print("재시도 후 환전이 성공적으로 완료되었습니다.")
                else:
                    print("재시도 후에도 환전 절차가 완료되지 않았습니다.")
            except Exception as inner_e:
                print(f"재시도 중 오류 발생: {inner_e}")
