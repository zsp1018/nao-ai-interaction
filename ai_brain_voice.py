import socket
import json
import ollama
import sys
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# === 配置 ===
HOST = '0.0.0.0'
PORT = 6666

# 提示词
SYSTEM_PROMPT = """
You are Nao, a robot assistant.
You are receiving VOICE TRANSCRIPTS from the user.
Respond in JSON format only.
Keys:
1. "text": Short spoken response (Chinese or English).
2. "motion": "wave", "forward", "turn_left", "turn_right", "crouch", "stand", "sit", "happy", "sad", "think", "guitar", "taichi", "fear", "shy", "winner", or null.
3. "voice_pitch": 1.0 (normal), 1.5 (child/chipmunk), 0.6 (monster/deep), 1.2 (female/sweet).

Example: {"text": "我是可爱的小朋友", "motion": "happy", "voice_pitch": 1.5}
"""

# 语音识别队列
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    """麦克风回调函数"""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def start_server():
    # 1. 加载离线语音模型
    print("⏳ [系统] 正在加载 Vosk 语音模型，请稍候...")
    if not os.path.exists("model"):
        print("❌ [错误] 找不到 'model' 文件夹！请确保你下载并解压了模型。")
        sys.exit(1)
    
    try:
        model = Model("model")
    except Exception as e:
        print(f"❌ [错误] 模型加载失败: {e}")
        sys.exit(1)

    # 2. 启动 Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    
    print(f"🧠 [AI Voice Brain] 启动成功！监听端口 {PORT}")
    print("🎧 麦克风已就绪，等待 Nao 连接...")

    conn, addr = server_socket.accept()
    print(f"🔗 Nao 已连接: {addr}")

    # 3. 开始监听循环
    # 采样率 16000 是 Vosk 小模型的标准
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        rec = KaldiRecognizer(model, 16000)
        
        with conn:
            print("\n" + "="*40)
            print("🎤 请说话！(比如: '你好', '挥挥手', '向前走')")
            print("="*40 + "\n")

            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    # 识别出了一句完整的话
                    result = json.loads(rec.Result())
                    text = result.get("text", "").replace(" ", "") # 去掉空格
                    
                    if not text:
                        continue # 没听到说话，继续听
                    
                    print(f"👂 [听到]: {text}")

                    # === 发送给 AI 思考 ===
                    print(f"🤔 [思考中]...")
                    try:
                        response = ollama.chat(model='llama3', format='json', messages=[
                            {'role': 'system', 'content': SYSTEM_PROMPT},
                            {'role': 'user', 'content': text},
                        ])
                        
                        raw_json = response['message']['content']
                        
                        # === JSON 清洗 (你验证过有效的逻辑) ===
                        parsed_data = None
                        try:
                            parsed_data = json.loads(raw_json)
                        except json.JSONDecodeError:
                            start = raw_json.find('{')
                            end = raw_json.rfind('}') + 1
                            if start != -1 and end != -1:
                                try:
                                    parsed_data = json.loads(raw_json[start:end])
                                except: pass
                        
                        if parsed_data is None:
                            print("❌ JSON 解析失败，跳过")
                            continue

                        # 补全字段
                        if "motion" not in parsed_data: parsed_data["motion"] = None
                        if "text" not in parsed_data: parsed_data["text"] = ""
                        if "voice_pitch" not in parsed_data: parsed_data["voice_pitch"] = 1.0
                        
                        final_json = json.dumps(parsed_data)
                        print(f"✨ [指令]: {final_json}")
                        
                        # 发送给 Nao
                        conn.sendall(final_json.encode('utf-8'))
                        print("📡 已发送")

                    except Exception as e:
                        print(f"❌ 处理错误: {e}")

import os # 补上这个 import

if __name__ == '__main__':
    start_server()