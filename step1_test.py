# -*- coding: utf-8 -*-
from naoqi import ALProxy

ROBOT_IP = "192.168.31.97"
PORT = 9559

# === 新增：填入你电脑在这个网段的 IP ===
MY_COMPUTER_IP = "192.168.31.255"  # <--- 请填入你电脑刚才查到的 IP
# ====================================

def main():
    print ("尝试从 " + MY_COMPUTER_IP + " 连接到 " + ROBOT_IP)
    try:
        # 这里的 0, 0, 0 是超时等参数，最后两个参数强制绑定本地 IP
        # 注意：不同版本的 ALProxy 构造函数略有不同，
        # 但最稳妥的方式是直接创建 broker
        
        from naoqi import ALBroker
        # 创建一个本地代理（Broker），绑定到电脑 IP，端口设为 0（自动分配）
        myBroker = ALBroker("myBroker", "0.0.0.0", 0, ROBOT_IP, PORT)
        
        # 现在通过 Broker 调用服务
        tts = ALProxy("ALTextToSpeech") # 不需要再传 IP 了，因为 Broker 连上了
        
        # 设置语言为中文
        tts.setLanguage("Chinese")
        
        msg = "北科大的钢魂熔炉里，我是一具被烙上“自动化”编号的合金骨骼,程序的风，吹得我关节沙沙作响，却吹不动胸腔里那枚,总想叛逃的齿轮。"
        print("机器人说: " + msg)
        tts.say(msg)
        print ("成功连接！")
        
        myBroker.shutdown()

    except Exception as e:
        print ("依然失败:"), e

if __name__ == "__main__":
    main()