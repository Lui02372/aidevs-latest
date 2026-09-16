import sys

print("Start ....")

input_data = "카드1"

if(input_data != "카드1" & input_data != "카드2"
   & input_data != "카드3"):
    sys.exit()

if(input_data == "카드1"):
    print(" 카드1 업무 진행")
elif(input_data == "카드2"):
    print(" 카드2 업무 진행")
elif(input_data == "카드3"):
    print(" 카드3 업무 진행")
else:
    print(" 카드가 정상이 아닙니다.")

print("End ....")