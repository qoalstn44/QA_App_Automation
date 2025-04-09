from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

C001 = "'패스워드 작성 완료'"


class pass_words:
    def pass_word_infos(driver):
        try:
            wait = WebDriverWait(driver, 10)
            button_texts = ["0", "1"]
            for _ in range(6):  # Repeat 12 times
                for text in button_texts:
                    xpath = f'//XCUIElementTypeButton[@name="{text}"]'
                    wait.until(EC.presence_of_element_located(
                        (By.XPATH, xpath))).click()
        except Exception:
            print(f"Test failed: {C001}")
        else:
            print(f"Test completed: {C001}")


class pass_word:
    def pass_word_info(driver):
        try:
            wait = WebDriverWait(driver, 20)
            button_texts = ["0", "1"]
            for _ in range(3):  # Repeat 12 times
                for text in button_texts:
                    xpath = f'//XCUIElementTypeButton[@name="{text}"]'
                    wait.until(EC.presence_of_element_located(
                        (By.XPATH, xpath))).click()
        except Exception:
            print(f"Test failed: {C001}")
        else:
            print(f"Test completed: {C001}")

class currency_exchange_pass_word:
    def currency_exchange_pass_word_info(driver):
        try:
            wait = WebDriverWait(driver, 20)
            button_texts = ["0", "1"]
            for _ in range(3):  # Repeat 12 times
                for text in button_texts:
                    xpath = f'(//XCUIElementTypeButton[@name="{text}"])[2]'
                    wait.until(EC.presence_of_element_located(
                        (By.XPATH, xpath))).click()
        except Exception:
            print(f"Test failed: {C001}")
        else:
            print(f"Test completed: {C001}")