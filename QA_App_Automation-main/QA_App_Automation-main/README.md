### onboarding파일에 상대 경로를 지정 후 사용 하셔야 합니다.
_android_app_play.py, ios_app_play.py_

_JSON 파일 경로_
```
json_file_path = 'ios_DB.json, android_DB.json에 상대 경로 지정'
```

_테스트 계정 유저 정보_
```
class App:
@classmethod
def ios_app_play(cls, driver):
userid = "테스트 계정 이름"
userrrn_first = "주민등록 앞 번호 6자리"
userrrn_second = "주민 등록 뒷 번호 1자리"
userphone = "테스트 게정 전화 번호"
```

### Automation.py에 상대 경로를 지정 후 사용 하셔야 합니다.

_Automation.py_

```if name == 'main':
scripts = [
'Android.py의 상대 경로 저정',
'iOS.py의 상대 경로 지정'
]
```

### slack.py에 상대 경로 지정 후 사용 하셔야 합니다.

_ios_slack.py, android_slack.py_

```class Slack_manager:
webhook_url = "본인이 만든 테스트 슬렉 채널 URL 지정"
channel = "#테스트 슬렉 채널 명 기입 "
```
