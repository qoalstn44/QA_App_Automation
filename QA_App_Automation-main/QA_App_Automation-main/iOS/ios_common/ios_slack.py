from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient
import logging
import json
import os

# 로거 설정
logger = logging.getLogger(__name__)


class Slack_manager:
    channel_id = "C06L95ZCZQS"  # 메시지를 보낼 채널 ID
    success_count = 0
    failure_count = 0
    started_count = 0
    error_messages = []
    thread_ts = None  # 스레드 타임스탬프 저장 변수
    count_file = "iOS/ios_DB/ios_started_count.json"  # 카운트를 저장할 파일 경로

    # Slack WebClient 인스턴스
    client = WebClient(
        token="xoxb-495605985203-7813895056743-tOhYkoayhXF57AnNTqyqNcUk")  # 슬랙 봇 토큰

    @classmethod
    def load_count(cls):
        """파일에서 카운트 정보를 불러오는 함수"""
        if os.path.exists(cls.count_file):
            try:
                with open(cls.count_file, "r") as f:
                    data = json.load(f)
                    cls.started_count = data.get(
                        "started_count", cls.started_count)  # 값이 없으면 기존 값 유지
                    logger.info(f"Loaded started_count: {cls.started_count}")
            except (json.JSONDecodeError, KeyError):
                logger.error("카운트 파일에서 오류가 발생했습니다. started_count 계속 증가합니다.")
        else:
            logger.info("카운트 파일이 존재하지 않음. started_count 계속 증가합니다.")

    @classmethod
    def save_count(cls):
        """카운트 정보를 파일에 저장하는 함수"""
        with open(cls.count_file, "w") as f:
            json.dump({
                "started_count": cls.started_count,
            }, f)

    @classmethod
    def test_started_message(cls):
        cls.load_count()
        cls.started_count += 1
        message = f"🤖 [TravelWallet_WebPage] iOS_자동화 테스트 [시작]합니다!\n\n 실행횟수 : {cls.started_count}"
        cls.send_slack_message(message)
        cls.save_count()  # 카운트 업데이트 후 저장

    @classmethod
    def send_slack_message(cls, message, thread_ts=None):
        try:
            response = cls.client.chat_postMessage(
                channel=cls.channel_id,
                text=message,
                thread_ts=thread_ts  # 스레드 타임스탬프를 추가하여 스레드에 메시지 전송
            )
            # 첫 메시지 전송 시 스레드 타임스탬프 저장
            if cls.thread_ts is None:
                cls.thread_ts = response['ts']
            logger.info(f"Slack 메시지가 성공적으로 전송되었습니다: {response}")
        except SlackApiError as e:
            logger.error(f"Slack 메시지 전송 중 오류발생: {e.response['error']}")

    @classmethod
    def test_failed_message(cls, additional_message=None):
        cls.failure_count += 1
        if additional_message:
            cls.error_messages.append(additional_message)
        cls.send_update_message(
            success=False, additional_message=additional_message)

    @classmethod
    def test_completed_message(cls, additional_message=None):
        cls.success_count += 1
        cls.send_update_message(
            success=True, additional_message=additional_message)

    @classmethod
    def send_update_message(cls, success, additional_message=None):
        pass_message = f"PASS👍 : {cls.success_count}"
        fail_message = f"FAIL🚨 : {cls.failure_count}"

        if success and additional_message:
            pass_message += f", {additional_message}"
        elif not success and additional_message:
            fail_message += f", {additional_message}"

        message = (f"🤖 [TravelWallet_WebPage] iOS_자동화 테스트 [업데이트]\n\n"
                   f"{pass_message}\n{fail_message}")
        cls.send_slack_message(message, cls.thread_ts)

    @classmethod
    def final_summary_message(cls):
        error_details = "\n".join([msg.split("-", 1)[0]
                                  for msg in cls.error_messages])
        message = (f"📝 [TravelWallet_WebPage] iOS_자동화 테스트 [종료] 최종 결과:\n\n"
                   f"PASS👍 : {cls.success_count}\n"
                   f"FAIL🚨 : {cls.failure_count}\n\n"
                   f"에러 메시지:\n{error_details}")
        cls.send_slack_message(message, cls.thread_ts)
        cls.save_count()  # 최종 메시지 후 카운트 저장


# 테스트 코드 실행 예시
if __name__ == "__main__":
    # Slack_manager.load_count()  # 카운트 불러오기
    Slack_manager.test_started_message()  # 첫 메시지 전송
    # Slack_manager.test_completed_message("테스트 케이스 1 완료")
    # Slack_manager.test_failed_message("테스트 케이스 2 실패 - 네트워크 오류")
    # Slack_manager.final_summary_message()
