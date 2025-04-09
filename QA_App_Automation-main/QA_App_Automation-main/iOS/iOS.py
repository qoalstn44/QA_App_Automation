import json
from appium import webdriver
from appium.options.common.base import AppiumOptions
from ios_onboarding.ios_app_play import App
from ios_common.ios_slack import Slack_manager
from ios_charge.ios_test_charge import My_Wallet_Charge
from ios_common.ios_pass_word import pass_word
from ios_card.ios_test_my_wallet import Create_a_wallet
from ios_mypage.ios_test_mypage import Mypage
from ios_foreign_currency_exchange.ios_foreign_currency_exchange import Foreign_Currency_Exchange
from ios_foreign_currency_exchange.ios_foreign_currency_exchange import Randem_Foreign_Currency_Exchange
import atexit

with open("iOS/ios_DB/ios_DB.json", "r") as f:
    config = json.load(f)
juwan_data = config["users"][0]["juwan"]
# Appium options
options = AppiumOptions()
options.load_capabilities(juwan_data)
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
Slack_manager.test_started_message()
try:
    # Run your tests
    # App.ios_app_play(driver)
    pass_word.pass_word_info(driver)
    My_Wallet_Charge.charge_and_refund_all(driver)
    Mypage.field_update(driver)
    # Foreign_Currency_Exchange.KRW_to_foreign_currency(driver)
    # Randem_Foreign_Currency_Exchange.random_foreign_currency_to_foreign_currency_exchange(driver)
    # Uncomment the following as needed for more tests
    # Create_a_wallet.mobile_card_a_wallet(driver)


finally:
    atexit.register(Slack_manager.final_summary_message)
