
print("start ...")

while True:
    print("Menu Start ")
    cmd = input("Input cmd..")
    print(f"입력하신 정보는 {cmd}")
    if (cmd == "1"):
        print("1번 메뉴를 선택하셨습니다.")
    elif (cmd == "2"):
        print("2번 메뉴를 선택하셨습니다.")
    elif (cmd == "q"):
        print("Bye ...")
        break  
    else: 
        print("잘못된 메뉴를 선택하셨습니다.")
print("end ....")
