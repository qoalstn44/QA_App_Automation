from selenium.webdriver.common.by import By
from ios_common.ios_slack import Slack_manager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import json

C001 = "'모마일 카드 생성 완료'"
C001_1 = "'직업 선택 레이블(급여소득자)'"
C002 = "'이미 모바일카드 생성 되어있음.'"
C003 = "'실물카드 신청 완료.'"
C003_1 = "'실물카드 신청 취소 완료'"
C004 = "'실물카드 신청 실패.'"
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
card_data = json_data["card"][0]["number1"][0]
charge_data = json_data["charge"][0]["number4"][0]
my_data = json_data["my"][0]["number1"][0]
pay_data = json_data["pay"][0]["number1"][0]


def handle_step(step_func, error_message):
    try:
        return step_func()
    except (StaleElementReferenceException, NoSuchElementException, TimeoutException, Exception) as e:
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


def enter_password(driver, password_xpaths, repeat=4):
    for _ in range(repeat):
        for xpath in password_xpaths:
            handle_step(lambda: click_element(
                driver, xpath, "비밀번호 입력"), f"비밀번호 입력 - Failed at {xpath}")


def scroll(driver, distance=0.5):
    try:
        driver.execute_script(
            "mobile: scroll", {"direction": "down", "distance": distance})
        print(f"스크롤 다운 방향으로 {distance} 만큼 이동")
    except Exception as e:
        print(f"스크롤 중 예외 발생: {e}")


class Create_a_wallet:
    @classmethod
    def mobile_card_a_wallet(cls, driver):
        try:
            handle_step(lambda: click_element(
                driver, card_data["create_a_wallet_xpath"], "월렛 만들기"), f"{C001} - Failed at create_a_wallet_xpath")
            handle_step(lambda: click_element(
                driver, card_data["create_a_wallet_xpath"], "월렛 만들기"), f"{C001} - Failed at create_a_wallet_xpath")
        except Exception:
            print(f"월렛 만들기 버튼을 찾지 못해 함수 실행 중단")
            return  # 함수 실행 중단

        try:
            steps = [
                (card_data["career_choice_text_xpath"], "직업을 선택해주세요."),
                (card_data["salary_earner_xpath"], "직업 선택 레이블(급여소득자)"),
                (card_data["card_password_xpath"], "비밀번호")
            ]
            for xpath, description in steps:
                handle_step(lambda: click_element(driver, xpath,
                            description), f"{description} - Failed at {xpath}")

            password_xpaths = [
                card_data["card_password_number_0_xpath"],
                card_data["card_password_number_1_xpath"]
            ]

            enter_password(driver, password_xpaths)

            handle_step(lambda: click_element(
                driver, card_data["card_full_agreement_xpath"], "전체동의"), f"전체동의 - Failed at {card_data['card_full_agreement_xpath']}")
            handle_step(lambda: click_element(
                driver, card_data["card_complete_xpath"], "완료"), f"완료 - Failed at {card_data['card_complete_xpath']}")
            Slack_manager.test_completed_message(C001)
            handle_step(lambda: click_element(
                driver, card_data["card_application_xpath"], "카드 신청"), f"카드 신청 - Failed at {card_data['card_application_xpath']}")
            handle_step(lambda: click_element(
                driver, card_data["card_application_xpath"], "카드 신청"), f"카드 신청 - Failed at {card_data['card_application_xpath']}")
            steps = [
                (card_data["card_password_xpath"], "비밀번호")
            ]
            for xpath, description in steps:
                handle_step(lambda: click_element(driver, xpath,
                            description), f"{description} - Failed at {xpath}")

            password_xpaths = [
                card_data["card_password_number_0_xpath"],
                card_data["card_password_number_1_xpath"]
            ]
            # 카드 신청 후 비밀번호 다시 입력
            enter_password(driver, password_xpaths)

            scroll(driver)

            handle_step(lambda: click_element(
                driver, card_data["card_full_agreement_xpath"], "전체동의"), f"전체동의 - Failed at {card_data['card_full_agreement_xpath']}")

            handle_step(lambda: click_element(
                driver, onboarding_data["next_xpath"], "다음"), f"다음 - Failed at {onboarding_data['next_xpath']}")
            handle_step(lambda: click_element(
                driver, onboarding_data["next_xpath"], "다음"), f"다음 - Failed at {onboarding_data['next_xpath']}")

            handle_step(lambda: click_element(
                driver, card_data["card_application_completed_xpath"], "신청 완료"), f"신청 완료 - Failed at {card_data['card_application_completed_xpath']}")
            handle_step(lambda: click_element(
                driver, card_data["card_close_button_xpath"], "닫기"), f"닫기 - Failed at {card_data['card_close_button_xpath']}")
            Slack_manager.test_completed_message(C003)
            handle_step(lambda: click_element(
                driver, my_data["my_tab_xpath"], "마이 탭 선택"), f"마이 탭 선택 - Failed at {my_data['my_tab_xpath']}")
            handle_step(lambda: click_element(
                driver, my_data["my_card_management_xpath"], "카드 관리 선택"), f"카드 관리 선택 - Failed at {my_data['my_card_management_xpath']}")

            handle_step(lambda: click_element(
                driver, card_data["card_cancel_application_xpath"], "실물 카드 신청 취소 선택"), f"실물 카드 신청 취소 선택 - Failed at {card_data['card_cancel_application_xpath']}")
            handle_step(lambda: click_element(
                driver, card_data["card_cancel_application_popup_xpath"], "팝업 신청 취소 선택"), f"팝업 신청 취소 선택 - Failed at {card_data['card_cancel_application_popup_xpath']}")

            handle_step(lambda: find_elements(
                driver, card_data["card_empty_view_text_xpath"], "보유중인 카드가 없습니다. 확인"), f"보유중인 카드가 없습니다. 확인 - Failed at {card_data['card_empty_view_text_xpath']}")

            handle_step(lambda: click_element(
                driver, card_data["card_back_button_xpath"], "카드 관리 뒤로가기 버튼 선택"), f"카드 관리 뒤로가기 버튼 선택 - Failed at {card_data['card_back_button_xpath']}")
            handle_step(lambda: click_element(
                driver, pay_data["pay_tab_xpath"], "홈 탭 선택"), f"페이 탭 선택 - Failed at {pay_data['pay_tab_xpath']}")

            Slack_manager.test_completed_message(C003_1)
        except Exception as e:
            Slack_manager.test_failed_message(f"{C002}: {e}")
