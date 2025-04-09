import json
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from android_common.android_slack import Slack_manager
from android_common.android_pass_word import pass_words
from Functions import click_element_with_scroll
import time

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

C000 = "'[Android]BETA Travel Wallet 진입 성공'"
C001 = "'[Android]약관 동의 및 개인정보 입력 가능'"
C001_1 = "'[Android]약관 동의 및 개인정보 입력 다음 버튼'"
C001_2 = "'[Android]마케팅 푸시 동의 확인'"

C002 = "'[Android]개인정보 입력 가능'"
C002_1 = "'[Android]개인정보 주민등록번호 첫번째 부분 입력 가능'"
C002_2 = "'[Android]개인정보 주민등록번호 두번째 부분 입력 가능'"
C002_3 = "'[Android]개인정보 통신사 선택 가능'"
C002_4 = "'[Android]개인정보 SKT 선택 가능'"
C002_5 = "'[Android]개인정보 휴대폰 번호 입력 가능'"
C002_6 = "'[Android]개인정보 다음 버튼'"

C003 = "'[Android]1원 인증'"
C004 = "'[Android]SNS 인증'"
C005 = "'[Android]송금하기'"
C006 = "'[Android]1원 인증'"
C006_1 = "'[Android]1원 인증 2원 입력'"
C006_2 = "'[Android]1원 인증 3원 입력'"

C007 = "'[Android]패스워드 작성 완료'"
C008 = "'[Android]지문 인식 취소 버튼'"


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
    def android_app_play(cls, driver):
        wait = WebDriverWait(driver, 10)
        userid = "황주원"
        userrrn_first = "970927"
        userrrn_second = "1"
        userphone = "01042065008"

        def click_element(by, value, description):
            wait.until(EC.presence_of_element_located((by, value))).click()
            print(f"{description} 클릭 완료")

        def send_keys(by, value, keys, description):
            element = wait.until(EC.presence_of_element_located((by, value)))
            element.send_keys(keys)
            print(f"{description} 입력 완료")

        try:
            # Step 1: BETA Travel Wallet 진입
            handle_step(lambda: click_element(By.XPATH, '//android.widget.TextView[@content-desc="[BETA] travel Wallet"]', "[BETA] travel Wallet 진입"),
                        f"{C000} - Failed at BETA Travel Wallet")
            time.sleep(5)
            try:
                click_element(By.XPATH, onboarding_data["img_popup_close_xpath"], "온보딩 바텀 시트 팝업 닫기"), f"{C002} - Failed at img_popup_close_xpath"
                print("온보딩 팝업 닫기 성공")
            except Exception as e:
                print(f"온보딩 팝업 닫기 실패: {e}")
                print("팝업 닫기 실패에도 다음 단계로 진행합니다.")

            # Step 2: 약관 동의
            handle_step(lambda: click_element(By.ID, onboarding_data["service_jeon_agree_id"], "서비스 전체 동의"),
                        f"{C001} - Failed at service_jeon_agree_id")

            # Step 3: 개인정보 입력
            handle_step(lambda: click_element(By.ID, onboarding_data["next_id"], "다음"),
                        f"{C001_1} - Failed at next_id")

            # handle_step(lambda: click_element(By.ID, onboarding_data["receive_marketing_id"], "마케팅 푸시 동의 확인"),
            #             f"{C001_2} - Failed at receive_marketing_id")

            handle_step(lambda: send_keys(By.XPATH, onboarding_data["name_xpath"], userid, "이름"),
                        f"{C002} - Failed at name_xpath")

            handle_step(lambda: send_keys(By.ID, onboarding_data["rrn_first_id"], userrrn_first, "주민등록번호 첫번째 부분"),
                        f"{C002_1} - Failed at rrn_first_id")

            handle_step(lambda: send_keys(By.ID, onboarding_data["rrn_second_id"], userrrn_second, "주민등록번호 두번째 부분"),
                        f"{C002_2} - Failed at rrn_second_id")

            handle_step(lambda: click_element(By.XPATH, onboarding_data["carrier_xpath"], "통신사 선택"),
                        f"{C002_3} - Failed at carrier_xpath")

            handle_step(lambda: send_keys(By.XPATH, onboarding_data["phone_xpath"], userphone, "휴대폰 번호"),
                        f"{C002_5} - Failed at phone_xpath")

            
            handle_step(lambda: click_element(By.ID, onboarding_data["next_button_id"], "다음"),
                        f"{C002_6} - Failed at next_button_id")
            
            handle_step(lambda: click_element(By.XPATH, onboarding_data["sms_re_request_xpath"], "재요청"),
                        f"{C002_6} - Failed at next_button_id")

            handle_step(lambda: click_element(By.ID, onboarding_data["sns_auth_id"], "SNS 인증을 할 수 없나요?"),
                        f"{C004} - Failed at sns_auth_id")

            handle_step(lambda: click_element(By.ID, onboarding_data["send_money_id"], "송금하기"),
                        f"{C005} - Failed at send_money_id")

            handle_step(lambda: send_keys(By.ID, onboarding_data["penny1_id"], "1", "1원 클릭"),
                        f"{C006} - Failed at penny1_id")

            handle_step(lambda: send_keys(By.ID, onboarding_data["penny2_id"], "2", "2원 클릭"),
                        f"{C006_1} - Failed at penny2_id")

            handle_step(lambda: send_keys(By.ID, onboarding_data["penny3_id"], "3", "3원 클릭"),
                        f"{C006_2} - Failed at penny3_id")

            handle_step(lambda: pass_words.pass_word_infos(driver),
                        f"{C007} - Failed at pass_word_infos")

            handle_step(lambda: click_element(By.ID, onboarding_data["cancel_fingerprint_recognition_id"], "지문 인식 취소"),
                        f"{C008} - Failed at cancel_fingerprint_recognition_id")
            try:
                # 엘리먼트 존재 여부 확인
                wait.until(EC.presence_of_element_located((By.XPATH, onboarding_data["today_xpath"])))
                click_element(By.XPATH, onboarding_data["today_xpath"], "전면 팝업 닫기 선택")
            except TimeoutException:
                # 엘리먼트가 없을 경우 종료
                print("Today_xpath 요소가 존재하지 않아 클릭하지 않고 종료합니다.")
                return
            

        except Exception as e:
            print(f"General Exception: {e}")
        else:
            Slack_manager.test_completed_message(C000)


class Apps:
    @classmethod
    def android_app_plays(cls, driver):
        wait = WebDriverWait(driver, 10)

        def click_element(by, value, description):
            wait.until(EC.presence_of_element_located((by, value))).click()
            print(f"{description} 클릭 완료")

        try:
            # Step 1: BETA Travel Wallet 진입
            handle_step(lambda: click_element(By.XPATH, '//android.widget.TextView[@content-desc="[BETA] travel Wallet"]', "[BETA] travel Wallet 진입"),
                        f"{C000} - Failed at BETA Travel Wallet")
            pass_words.pass_word_infos
        
            # Step 2: 전면 팝업 '오늘 하루 보기 않기' 버튼 클릭 여부 확인
            try:
                # 엘리먼트 존재 여부 확인
                
                wait.until(EC.presence_of_element_located((By.XPATH, onboarding_data["Today_xpath"])))
                click_element(By.XPATH, onboarding_data["Today_xpath"], "전면 팝업 오늘 하루 보기 않기 선택")
            except TimeoutException:
                # 엘리먼트가 없을 경우 종료
                print("Today_xpath 요소가 존재하지 않아 클릭하지 않고 종료합니다.")
                return

        except Exception as e:
            print(f"General Exception: {e}")
        else:
            Slack_manager.test_completed_message(C000)





class Appss:
    @classmethod
    def android_app_plays(cls, driver):
        wait = WebDriverWait(driver, 10)

        def click_element(by, value, description):
            wait.until(EC.presence_of_element_located((by, value))).click()
            print(f"{description} 클릭 완료")

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
    

        try:
            click_element_with_scroll(By.XPATH, '//android.widget.Spinner[@text="이전 버전 보기"]', "성공"), f"{C000} - Failed at BETA Travel Wallet"        
        except Exception as e:
            print(f"General Exception: {e}")
        else:
            Slack_manager.test_completed_message(C000)