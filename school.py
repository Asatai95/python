"""
辞書の値を取得
"""

person = {
    "first_name": "太郎",
    "last_name": "スタートアップ",
    "address": {
        "post_code": '904-0004',
        "prefecture": "沖縄県",
        "city": "沖縄市",
        "street": "中央１丁目７−８"},
    "phone": "080-3963-3355",
}

print("お名前: " + person["first_name"] + person["last_name"])
print("郵便番号: " + person["address"]["post_code"])
print("住所: " + person["address"]["prefecture"] + " " +person["address"]["city"]+ " " +person["address"]["street"])
print("電話番号: " + person["phone"])


print("-------------------------------------------------------")


"""
じゃんけんゲーム
"""

import random
from time import sleep


print("--じゃんけんゲーム--")
while True:
    print(" --------------------------------- ")
    print("  ")
    print("最初はグー,,,")
    sleep(1)
    print("じゃんけん,,,")
    sleep(2)
    print("-----------------------------------")
    print("0: グー")
    print("1: チョキ")
    print("2: パー")
    me = input("数字を入力してください: ")
    if not me in "0,1,2":
        print("上記以外の数字を入力しないで下さい")
    else:
        print("ポンッ!!")
        sleep(1)
        you = int(random.randrange(3))
        me = int(me)

        if me == 0 and you == 2:
            print("CPU: パー, You: グー")
            sleep(1)
            print("あなたの負けです")
        elif me == 1 and you == 0:
            print("CPU: チョキ, You: パー")
            sleep(1)
            print("あなたの負けです")
        elif me == 2 and you == 1:
            print("CPU: グー, You: チョキ")
            sleep(1)
            print("あなたの負けです")
        elif me == 0 and you == 1:
            print("CPU: チョキ, You: グー")
            sleep(1)
            print("あなたの勝ちです!!")
        elif me == 1 and you == 2:
            print("CPU: パー, You: チョキ")
            sleep(1)
            print("あなたの勝ちです!!")
        elif me == 2 and you == 0:
            print("CPU: グー, You: パー")
            sleep(1)
            print("あなたの勝ちです!!")
        else:
            sleep(1)
            print("あいこです")

    
