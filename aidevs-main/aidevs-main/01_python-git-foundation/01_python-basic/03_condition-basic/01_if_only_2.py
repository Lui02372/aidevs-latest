# 숫자를 입력 받는다(1 ~ 10)
# 숫자가 아니면 프로그램 종료
# 숫자이면 출력 
import sys

print("Start ..")

input_str = input("숫자 입력(1~10):")
if (input_str.isdigit() != True):
    sys.exit()

input_number = int(input_str)
if(input_number < 1 == True | input_number > 10 == True):
    sys.exit()
# if(input_number > 10):
#     sys.exit()

print(f"입력 숫자는 {input_number}")
print("End ..")