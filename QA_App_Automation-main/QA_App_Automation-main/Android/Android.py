import json
from appium import webdriver
from android_common.android_slack import Slack_manager
from appium.options.common.base import AppiumOptions
from android_onboarding.android_app_play import App, Apps, Appss
from android_common.android_pass_word import pass_word
from android_charge.android_test_charge import My_Wallet_Charge
from android_card.android_test_my_wallet import Create_a_wallet
from android_refund.android_test_refund import ClickLaterButton
from android_charge.android_test_min_charge import My_Wallet_Minimum_Charge
from android_mypage.android_test_mypage import Mypage
from android_foreign_currency_exchange.android_foreign_currency_exchange import Foreign_Currency_Exchange
from android_foreign_currency_exchange.android_foreign_currency_exchange import Randem_Foreign_Currency_Exchange
import atexit
with open("Android/android_DB/android_DB.json", "r") as f:
    config = json.load(f)
juwan_data = config["users"][0]["juwan"]
# Appium options
options = AppiumOptions()
options.load_capabilities(juwan_data)
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
Slack_manager.test_started_message()
try:
    # Run your tests
    # Appss.android_app_plays(driver)
    # App.android_app_play(driver)
    # My_Wallet_Charge.charge_and_refund_all(driver)
    My_Wallet_Minimum_Charge.Minimum_charge_and_refund_all(driver)
    Foreign_Currency_Exchange.KRW_to_foreign_currency(driver)
    Randem_Foreign_Currency_Exchange.random_foreign_currency_to_foreign_currency_exchange(driver)
    Mypage.field_update(driver)
    # Create_a_wallet.mobile_card_a_wallet(driver)
finally:
    atexit.register(Slack_manager.final_summary_message)



                