from selenium.webdriver.common.by import By
from android_common.android_slack import Slack_manager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
C001 = "'패스워드 작성 완료'"
C002 = "'패스워드 작성 실패'"


class pass_words:
    def pass_word_infos(driver):
        try:
            wait = WebDriverWait(driver, 10)
            button_texts = ["0", "1"]
            for _ in range(6):  # Repeat 12 times
                for text in button_texts:
                    xpath = f'//android.widget.Button[@resource-id="com.mobiletoong.travelwallet:id/btnKeyboard" and @text="{text}"]'
                    wait.until(EC.presence_of_element_located(
                        (By.XPATH, xpath))).click()
        except Exception:
            print(f"Test failed: {C002}")
        else:
            print(f"Test completed: {C001}")


class pass_word:
    def pass_word_info(driver):
        try:
            wait = WebDriverWait(driver, 20)
            button_texts = ["0", "1"]
            for _ in range(3):  # Repeat 12 times
                for text in button_texts:
                    xpath = f'//android.widget.Button[@resource-id="com.mobiletoong.travelwallet:id/btnKeyboard" and @text="{text}"]'
                    wait.until(EC.presence_of_element_located(
                        (By.XPATH, xpath))).click()
        except Exception:
            print(f"Test failed: {C002}")
        else:
            print(f"Test completed: {C001}")
