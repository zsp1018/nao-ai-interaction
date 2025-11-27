# Nao 机器人 AI 交互 Demo

本项目利用本地大语言模型 (Llama 3) 为 Nao 机器人赋予智能语音交互和动作控制能力。

> **⚠️ 重要说明**
>
> *   **完全本地部署，无需联网**：所有计算（包括语音识别、大模型推理）均在本地电脑完成，保护隐私，低延迟，无需互联网连接。
> *   **Demo 性质**：本项目仅作为一个演示 Demo，旨在展示 Nao 机器人结合现代 AI 技术的能力。
> *   **模型扩展性**：当前默认配置使用的是 Llama 3 **8B** 模型。如果你拥有更强大的硬件资源（例如使用 **Thor** 等高性能推理框架），完全可以部署 **70B** 或更大参数的模型，以获得更深度的理解能力和更惊艳的交互体验.
<p align="center">
  <a href="https://www.bilibili.com/video/BV12NSMBREwr/?spm_id_from=333.337.search-card.all.click&vd_source=e624924603cde403f14272de3d1eea6f" target="_blank">
    <img src="https://github.com/zsp1018/nao-ai-interaction/raw/main/talk.gif" width="300" alt="点击查看B站演示视频">
  </a>
</p>
## 功能特性

*   **语音交互**：直接与 Nao 对话，使用本地语音识别 (Vosk) 听懂你的指令。
*   **AI 大脑**：由 Llama 3 (通过 Ollama 运行) 驱动，理解上下文并生成自然的回复。
*   **动作控制**：根据对话内容自动执行动作（如挥手、走路、坐下、打太极、弹吉他等）。
*   **情感表达**：通过眼睛灯光颜色和肢体语言表达情感（开心、难过、害怕、害羞）。
*   **变声功能**：通过语音指令改变 Nao 的音调（变成小黄人、怪兽、甜美女生等）。

## 环境要求

1.  **硬件**：Nao 机器人（需与电脑连接在同一 Wi-Fi 下）。
2.  **软件**：
    *   **Ollama**：已安装并运行 `llama3` 模型 (`ollama pull llama3`)。
    *   **Conda**：用于管理 Python 环境。
    *   **Naoqi SDK**：Nao 机器人的 Python 2.7 SDK。

## 安装步骤

1.  **环境配置**：
    *   创建 Python 3 环境 (`ai_env`) 用于运行 AI 大脑：
        ```bash
        conda create -n ai_env python=3.10
        conda activate ai_env
        pip install ollama sounddevice vosk
        ```
    *   创建 Python 2.7 环境 (`naoqi`) 用于控制 Nao：
        ```bash
        conda create -n naoqi python=2.7
        # 请手动安装 Naoqi SDK 并配置 PYTHONPATH
        ```

2.  **下载模型**：
    *   下载 Vosk 语音识别模型（推荐 `vosk-model-small-cn-0.22`），解压并重命名为 `model/` 文件夹，放在项目根目录下。

3.  **修改配置**：
    *   修改 `nao_body_listen.py`：将 `ROBOT_IP` 改为你 Nao 的实际 IP 地址。
    *   修改 `ai_brain_voice.py`：确保 `HOST` 和 `PORT` 配置正确。

## 使用方法

运行启动脚本，将在不同终端中自动启动所有服务：

```bash
./start_all.sh
```

或者手动分步运行：

1.  **终端 1 (Ollama 服务)**: `ollama serve`
2.  **终端 2 (AI 大脑)**: `python ai_brain_voice.py` (需在 `ai_env` 环境下)
3.  **终端 3 (Nao 身体)**: `python nao_body_listen.py` (需在 `naoqi` 环境下)

## 指令示例

试着对 Nao 说：
*   “你好”
*   “挥挥手”
*   “向前走”
*   “坐下”
*   “做一个开心的表情”
*   “弹个吉他”
*   “打太极”
*   “变成小黄人的声音”
