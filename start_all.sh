#!/bin/bash

# 启动 Ollama 服务 (终端 1)
gnome-terminal --title="Ollama Server" -- bash -c "ollama serve; exec bash"

# 启动 AI Brain (终端 2)
gnome-terminal --title="AI Brain (Python 3)" -- bash -c "
source ~/anaconda3/etc/profile.d/conda.sh
conda activate ai_env
echo '正在启动 AI Brain...'
env -u http_proxy -u https_proxy -u all_proxy -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY python ai_brain_voice.py
exec bash
"

# 启动 Nao Body (终端 3)
gnome-terminal --title="Nao Body (Python 2)" -- bash -c "
source ~/anaconda3/etc/profile.d/conda.sh
conda activate naoqi
export PYTHONPATH=\$PYTHONPATH:~/pynaoqi/lib/python2.7/site-packages
export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:~/pynaoqi/lib
echo '正在启动 Nao Body...'
python nao_body_listen.py
exec bash
"

echo "所有服务已在独立终端中启动！"
