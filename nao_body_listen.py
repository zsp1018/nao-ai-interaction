# -*- coding: utf-8 -*-
import socket
import json
import time
from naoqi import ALProxy, ALBroker

# === 修改 IP ===
ROBOT_IP = "192.168.31.97"  # 你的 Nao IP
ROBOT_PORT = 9559
BRAIN_HOST = '192.168.31.65'    # 你的电脑 IP (本机)
BRAIN_PORT = 6666
# =============

def execute_instruction(tts, motion, posture, animated_speech, animation_player, leds, data):
    print("DEBUG: 收到原始数据: " + repr(data))
    try:
        # 尝试去除可能存在的首尾单引号（虽然正常不应该有，但为了保险）
        data = data.strip().strip("'")
        response = json.loads(data)
        text_to_say = response.get('text', '')
        action = response.get('motion')
        voice_pitch = response.get('voice_pitch') # 新增：获取音调参数

        # 0. 设置音调 (如果有)
        if voice_pitch:
            try:
                pitch_value = float(voice_pitch)
                tts.setParameter("pitchShift", pitch_value)
                print("设置音调为: " + str(pitch_value))
            except Exception:
                pass
        else:
            # 默认恢复正常音调，防止一直变声
            tts.setParameter("pitchShift", 1.0)
        
        # 预处理文本编码
        encoded_text = ""
        if text_to_say:
            encoded_text = text_to_say.encode('utf-8')

        # 优先处理：如果只是说话或者挥手，使用 Animated Speech 增强表现力
        action_str = str(action) if action else None
        
        if encoded_text and (action_str == "wave" or action_str is None):
            print("使用 Animated Speech 说话: " + encoded_text)
            
            # 如果是挥手，强制加上挥手动画标签
            if action_str == "wave":
                # 格式: ^start(动画路径) 文本 ^wait(动画路径)
                sentence = "^start(animations/Stand/Gestures/Hey_1) " + encoded_text + " ^wait(animations/Stand/Gestures/Hey_1)"
                animated_speech.say(sentence)
            else:
                # 如果没有特定动作，直接用 animated_speech，它会自动加一些随机手势
                animated_speech.say(encoded_text)
            
            return # 处理完毕，直接返回

        # 其他情况 (如走路、坐下等复杂动作)，还是分开执行比较稳妥
        # 1. 说话
        if encoded_text:
            print("Nao说: " + encoded_text)
            tts.say(encoded_text)

        # 2. 动作
        if action_str:
            print("执行动作: " + action_str)
            if action_str == "forward":
                motion.moveTo(0.3, 0.0, 0.0) # 前进30厘米
            elif action_str == "turn_left":
                motion.moveTo(0.0, 0.0, 1.57) # 左转90度
            elif action_str == "turn_right":
                motion.moveTo(0.0, 0.0, -1.57)
            elif action_str == "crouch":
                motion.rest()
            elif action_str == "stand":
                motion.wakeUp()
                posture.goToPosture("Stand", 0.5)
            elif action_str == "sit":
                posture.goToPosture("Sit", 0.5)
            elif action_str == "happy":
                # 开心：举手抬头 + 绿色眼睛
                leds.fadeRGB("FaceLeds", 0x00FF00, 0.5)
                motion.setStiffnesses("Body", 1.0)
                names = ["RShoulderPitch", "LShoulderPitch", "HeadPitch"]
                angles = [[-0.5, 0.0], [-0.5, 0.0], [-0.3, 0.0]]
                times = [[0.5, 1.5], [0.5, 1.5], [0.5, 1.5]]
                motion.angleInterpolation(names, angles, times, True)
                time.sleep(1.0)
                leds.fadeRGB("FaceLeds", 0xFFFFFF, 0.5) # 恢复白色
            elif action_str == "sad":
                # 难过：低头垂手 + 蓝色眼睛
                leds.fadeRGB("FaceLeds", 0x0000FF, 0.5)
                motion.setStiffnesses("Body", 1.0)
                names = ["HeadPitch", "RShoulderPitch", "LShoulderPitch"]
                angles = [[0.4], [1.5], [1.5]]
                times = [[1.0], [1.0], [1.0]]
                motion.angleInterpolation(names, angles, times, True)
                time.sleep(1.0)
                leds.fadeRGB("FaceLeds", 0xFFFFFF, 0.5)
            elif action_str == "think":
                # 思考：手摸头 + 旋转眼睛
                leds.rotateEyes(0x0000FF, 1.0, 2.0)
                motion.setStiffnesses("Body", 1.0)
                names = ["RShoulderPitch", "RElbowYaw", "RElbowRoll", "RHand", "HeadYaw"]
                angles = [[-1.0], [1.5], [1.5], [1.0], [-0.3]]
                times = [[1.0], [1.0], [1.0], [1.0], [1.0]]
                motion.angleInterpolation(names, angles, times, True)
                time.sleep(1.0)
                # 复位
                motion.wakeUp()
                leds.fadeRGB("FaceLeds", 0xFFFFFF, 0.5)
            elif action_str == "guitar":
                # 空气吉他
                try:
                    animation_player.run("animations/Stand/Waiting/AirGuitar_1")
                except Exception:
                    print("动作库中未找到 AirGuitar_1")
            elif action_str == "taichi":
                # 太极
                try:
                    animation_player.run("animations/Stand/Waiting/TaiChi_1")
                except Exception:
                    try:
                        animation_player.run("animations/Stand/Gestures/TaiChi_1")
                    except Exception:
                        print("动作库中未找到 TaiChi_1")
            elif action_str == "fear":
                # 害怕
                leds.fadeRGB("FaceLeds", 0xFF0000, 0.1) # 红色闪烁
                try:
                    animation_player.run("animations/Stand/Emotions/Negative/Fear_1")
                except Exception:
                    pass
                leds.fadeRGB("FaceLeds", 0xFFFFFF, 0.5)
            elif action_str == "shy":
                # 害羞
                leds.fadeRGB("FaceLeds", 0xFF00FF, 0.5) # 粉色
                try:
                    animation_player.run("animations/Stand/Emotions/Neutral/Embarrassed_1")
                except Exception:
                    pass
                leds.fadeRGB("FaceLeds", 0xFFFFFF, 0.5)
            elif action_str == "winner":
                # 胜利
                leds.fadeRGB("FaceLeds", 0xFFFF00, 0.5) # 黄色
                try:
                    animation_player.run("animations/Stand/Emotions/Positive/Winner_1")
                except Exception:
                    pass
                leds.fadeRGB("FaceLeds", 0xFFFFFF, 0.5)

    except ValueError as e:
        print("收到无效数据: " + str(e))

def main():
    # 连接 Nao
    try:
        myBroker = ALBroker("myBroker", "0.0.0.0", 0, ROBOT_IP, ROBOT_PORT)
        tts = ALProxy("ALTextToSpeech")
        motion = ALProxy("ALMotion")
        posture = ALProxy("ALRobotPosture")
        animated_speech = ALProxy("ALAnimatedSpeech")
        animation_player = ALProxy("ALAnimationPlayer") # 新增动画播放器
        leds = ALProxy("ALLeds") # 新增 LED 控制
        try:
            tts.setLanguage("Chinese") 
            print ("[Info] Language set to Chinese")
        except Exception:
            print("[Warning] Chinese language not found! Fallback to English.")
            tts.setLanguage("English")
        
        motion.wakeUp()
        # 开启呼吸模式，让机器人看起来像活的 (可爱一点)
        motion.setBreathEnabled("Body", True)
        
        tts.say("Voice control ready")
        print("Nao 连接成功，等待 AI 指令...")
    except Exception as e:
        print("连接 Nao 失败: " + str(e))
        return

    # 连接 AI Brain
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((BRAIN_HOST, BRAIN_PORT))
    except Exception as e:
        print("连接 AI Brain 失败: " + str(e))
        return

    try:
        while True:
            # 阻塞接收数据
            data = sock.recv(4096)
            if not data:
                print("Brain disconnected")
                break
            
            # === 修改：打印收到的原始数据，方便调试 ===
            print("[Debug] Received raw data: " + repr(data))
            
            # 尝试处理多条 JSON 粘在一起的情况 (简单处理: 只取第一条)
            if data.count('}{') > 0:
                data = data.replace('}{', '}|{') # 强行分割
                data_list = data.split('|')
                for d in data_list:
                    execute_instruction(tts, motion, posture, animated_speech, animation_player, leds, d)
            else:
                execute_instruction(tts, motion, posture, animated_speech, animation_player, leds, data)
            
    finally:
        motion.rest()
        sock.close()
        myBroker.shutdown()

if __name__ == "__main__":
    main()