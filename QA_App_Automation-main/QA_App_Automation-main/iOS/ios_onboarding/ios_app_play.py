import json
from selenium.webdriver.common.by import By
from ios_common.ios_slack import Slack_manager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from ios_common.ios_pass_word import pass_words
import time

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

C000 = "'[iOS]BETA Travel Wallet 진입 성공'"
C001 = "'[iOS]약관 동의 및 개인정보 입력 가능'"
C001_1 = "'[iOS]약관 동의 및 개인정보 입력 다음 버튼'"
C001_2 = "'[iOS]마케팅 푸시 동의 확인'"

C002 = "'[iOS]개인정보 이름 입력 가능 '"
C002_1 = "'[iOS]개인정보 주민등록번호 첫번째 부분 입력 가능'"
C002_2 = "'[iOS]개인정보 주민등록번호 두번째 부분 입력 가능'"
C002_3 = "'[iOS]개인정보 통신사 선택 가능'"
C002_4 = "'[iOS]개인정보 SKT 선택 가능'"
C002_5 = "'[iOS]개인정보 휴대폰 번호 입력 가능'"
C002_6 = "'[iOS]개인정보 다음 버튼'"

C003 = "'[iOS]SNS 인증'"
C004 = "'[iOS]송금하기'"
C005 = "'[iOS]1원 인증'"
C005_1 = "'[iOS]1원 인증 2원 입력'"
C005_2 = "'[iOS]1원 인증 3원 입력'"

C006 = "'[iOS]패스워드 작성 완료'"


def handle_step(step_func, error_message):
    try:
        step_func()
    except StaleElementReferenceException as e:
        Slack_manager.test_failed_message(f"{error_message}: {e}")
        raise
    except Exception as e:
        Slack_manager.test_failed_message(f"{error_message}: {e}")
        raise


class App:
    @classmethod
    def ios_app_play(cls, driver):
        wait = WebDriverWait(driver, 10)
        userid = "SETKHANOVA DIANA RASHID KIZI"
        userrrn_first = "010531"
        userrrn_second = "8"
        userphone = "01034973100"

        def click_element(xpath, description):
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            element.click()
            print(f"{description} 클릭 완료")

        def send_keys(xpath, keys, description):
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            element.send_keys(keys)
            print(f"{description} 입력 완료")

        try:
            try:
                time.sleep(2)
                handle_step(lambda: click_element(onboarding_data["onboarding_img_popup_xpath"], "온보딩 전면 팝업"),
                        f"{C001} - Failed at service_jeon_agree_xpath")
                
                print("온보딩 팝업 닫기 성공")
            except Exception as e:
                print(f"온보딩 팝업 닫기 실패: {e}")
                print("팝업 닫기 실패에도 다음 단계로 진행합니다.")

            handle_step(lambda: click_element(onboarding_data["service_jeon_agree_xpath"], "서비스 전체 동의"),
                        f"{C001} - Failed at service_jeon_agree_xpath")

            handle_step(lambda: click_element(onboarding_data["next_xpath"], "다음"),
                        f"{C001_1} - Failed at next_xpath")

            # handle_step(lambda: click_element(onboarding_data["receive_marketing_xpath"], "마케팅 푸시 동의 확인"),
            #             f"{C001_2} - Failed at receive_marketing_xpath")

            handle_step(lambda: send_keys(onboarding_data["name_xpath"], userid, "이름"),
                        f"{C002} - Failed at name_xpath")

            handle_step(lambda: send_keys(onboarding_data["rrn_first_xpath"], userrrn_first, "주민등록번호 첫번째 부분"),
                        f"{C002_1} - Failed at rrn_first_xpath")

            handle_step(lambda: send_keys(onboarding_data["rrn_second_xpath"], userrrn_second, "주민등록번호 두번째 부분"),
                        f"{C002_2} - Failed at rrn_second_xpath")

            handle_step(lambda: click_element(onboarding_data["carrier_xpath"], "통신사 선택"),
                        f"{C002_3} - Failed at carrier_xpath")

            handle_step(lambda: click_element(onboarding_data["carrier_skt_xpath"], "SKT 선택"),
                        f"{C002_4} - Failed at carrier_skt_xpath")

            handle_step(lambda: send_keys(onboarding_data["phone_xpath"], userphone, "휴대폰 번호"),
                        f"{C002_5} - Failed at phone_xpath")

            handle_step(lambda: click_element(onboarding_data["next_xpath"], "다음"),
                        f"{C002_6} - Failed at next_xpath")
            
            handle_step(lambda: click_element(onboarding_data["sms_re_request_xpath"], "재요청"),
                        f"{C002_6} - Failed at sms_re_request_xpath")

            handle_step(lambda: click_element(onboarding_data["sns_auth_xpath"], "SNS 인증"),
                        f"{C003} - Failed at sns_auth_xpath")

            handle_step(lambda: click_element(onboarding_data["send_money_xpath"], "송금하기"),
                        f"{C004} - Failed at send_money_xpath")

            handle_step(lambda: click_element(onboarding_data["penny1_xpath"], "1원 입력"),
                        f"{C005} - Failed at penny1_xpath")

            handle_step(lambda: click_element(onboarding_data["penny2_xpath"], "2원 입력"),
                        f"{C005_1} - Failed at penny2_xpath")

            handle_step(lambda: click_element(onboarding_data["penny3_xpath"], "3원 입력"),
                        f"{C005_2} - Failed at penny3_xpath")

            handle_step(lambda: pass_words.pass_word_infos(driver),
                        f"{C006} - Failed at pass_word_infos")
            
            handle_step(lambda: click_element(onboarding_data["today_xpath"], "전면 팝업 닫기"),
                        f"{C005_2} - Failed at penny3_xpath")
        except Exception as e:
            print(f"General Exception: {e}")
        else:
            Slack_manager.test_completed_message(C000)
