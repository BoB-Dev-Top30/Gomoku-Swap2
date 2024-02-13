import subprocess

# 외부 명령 실행 및 표준 입출력 캡처 설정
proc = subprocess.Popen(['./M5N.Slave', '127.0.0.1:5005', './app', 'my_client'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# 서버로부터의 출력을 읽고 출력하기
while True:
    output = proc.stdout.readline()
    if output == '' and proc.poll() is not None:
        break
    if output:
        print(output.strip())