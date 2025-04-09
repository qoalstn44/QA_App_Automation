import json
import random
import string
import time
from ios_common.ios_slack import Slack_manager
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from ios_charge.ios_test_charge import click_element

# JSON 파일 경로
json_file_path = 'iOS/ios_DB/ios_DB.json'

# JSON 파일 읽기 함수


def load_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# XPath 데이터 초기화 함수
json_data = load_json(json_file_path)
mypage_button_data = json_data["mypage"][0]["number1"]
mypage_before_data = json_data["mypage"][0]["number2"]
textfield_xpath = json_data['mypage'][0]['number3']

C001 = "'마이탭 진입 완료'"
C002 = "'내 정보 관리 진입 완료'"
C003 = "'영문 이름 수정 완료'"
C004 = "'직업 수정 완료'"
C005 = "'국문주소 수정 완료'"
C006 = "'영문주소 수정 완료'"


# 주어진 길이만큼 랜덤 알파벳 문자열을 생성하는 함수
def generate_random_string(length):
    letters = string.ascii_letters  # 대소문자 알파벳 포함
    return ''.join(random.choice(letters) for _ in range(length))

# 특정 필드에 랜덤 문자열을 입력하고, 해당 필드의 업데이트 결과를 출력하는 함수


def update_textfield_with_random_value(driver, field_xpath, field_name, length=8):
    wait = WebDriverWait(driver, 10)

    try:
        # XPath를 사용해 필드 찾기
        field_element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, field_xpath)))

        # 필드 내용 삭제
        field_element.clear()

        # 랜덤 값 생성
        random_value = generate_random_string(length)
        time.sleep(1)

        # 랜덤 값 입력
        field_element.send_keys(random_value)

        print(f"{field_name} 수정 완료: {random_value}")
        return random_value

    except Exception as e:
        print(f"{field_name} 업데이트 중 오류 발생: {e}")
        return None

# 주어진 요소에 대한 정보를 가져와 출력하는 함수


def get_element(driver, get_type, message_type="변경 전"):
    wait = WebDriverWait(driver, 10)
    if get_type in mypage_before_data:
        button_xpath = mypage_before_data[get_type]

        text_xpath = mypage_before_data["text_xpath"]
        # message_type에 따라 메시지 변경
        element_message = f"{message_type} {get_type}"
    else:
        print("알 수 없는 요소 유형입니다.")
        return None

    try:
        # 버튼을 찾기
        button = wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, button_xpath)))

        # 버튼 내부에서 모든 텍스트 요소 찾기
        text_elements = button.find_elements(AppiumBy.XPATH, text_xpath)

        # 두 번째 텍스트 요소가 있는지 확인
        if len(text_elements) >= 2:
            # 두 번째 텍스트 값 가져오기
            value = text_elements[1].text
            print(f"{element_message}: {value}")
            return value
        else:
            print("Not enough text elements found.")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

# 영문 이름/국문주소/영문주소 정보 수정 함수


def update_information(driver, before_type, update_button, textfields):
    get_element(driver, before_type)  # 변경 전 값 출력
    click_element(driver, update_button, "수정")  # 수정 클릭
    for field_name, xpath in textfields.items():
        update_textfield_with_random_value(driver, xpath, field_name, length=6)
    click_element(driver, mypage_button_data["complete_xpath"], "완료")  # 완료 클릭
    click_element(driver, mypage_button_data["confirm_xpath"], "확인")  # 확인 클릭
    get_element(driver, before_type, message_type="변경 후")  # 변경 후 값 출력

# 마이페이지에서 정보를 업데이트하는 클래스


class Mypage:
    def field_update(driver):
        try:
            click_element(
                driver, mypage_button_data["my_tab_xpath"], "마이 탭")  # 마이탭 클릭
            # 내 정보 관리 클릭
            click_element(
                driver, mypage_button_data["my_info_manage_xpath"], "내 정보 관리")

            # 영문 이름 수정
            update_information(driver, "EnglishName_xpath", mypage_button_data["update_EnglishName_xpath"], {
                "textfield_1": textfield_xpath["textfield_1_xpath"],
                "textfield_2": textfield_xpath["textfield_2_xpath"],
            })

            # 국문주소 수정
            update_information(driver, "Korean_Address_xpath", mypage_button_data["update_Korean_Address_xpath"], {
                "textfield_2": textfield_xpath["textfield_2_xpath"],
            })

            # 영문주소 수정
            update_information(driver, "English_Address_xpath", mypage_button_data["update_English_Address_xpath"], {
                "textfield_1": textfield_xpath["textfield_1_xpath"],
                "textfield_2": textfield_xpath["textfield_2_xpath"],
                "textfield_3": textfield_xpath["textfield_3_xpath"],
                "textfield_4": textfield_xpath["textfield_4_xpath"],
            })
            Slack_manager.test_completed_message("내 정보 관리 테스트 성공")
        except Exception as e:
            print(f"오류 발생: {e}")
