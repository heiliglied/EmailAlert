# EmailAlert
Python Email 알리미

홈 서버 구축 시, 유동IP를 사용할 때 IP가 변경되면 메일로 알려주는 스크립트.

## 사용법

1. setup.ini 와 setup.py
 - setup.ini는 일반적인 섹션, 변수로 설정되어 있으며, setup.py를 실행시켜 단답형 텍스트 입력으로 setup.ini 파일 설정을 변경하도록 함.
 
2. sendmail.py
 - setup.ini 파일을 configParser로 받아와 해당 내용을 메일로 발송하는 스크립트.
 - 파일 실행 시 setup.ini 파일에 기록된 IP주소와 현재 IP주소를 비교하며, 변경되었을 경우에만 발송함.
 
## 그 외

Python의 입 출력, 기본 동작을 익히기에 꽤 괜찮은 스크립트라 생각되어 올려 둠.
포함된 daemon.py에 ip 체크 로직을 심어둬도 됨.

deamon.py의 경우 c style로 작성하였으나, python 내장 패키지인 python_daemon을 이용하면 대부분의 로직이 구현되어있음.

is 키워드 대신 == 사용을 권장함.
