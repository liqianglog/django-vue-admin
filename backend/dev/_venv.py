import os
import sys
from pathlib import Path

# #################### start #######################
# AREPL for python调试，导入项目依赖    (可禁用)
BASE_DIR = Path(__file__).parent.parent
VENV_DIR = Path.joinpath(BASE_DIR, "__pypackages__", "3.8", "lib")  # PDM
# print(f"{BASE_DIR=}")
# 确认BASE_DIR无误后添加如下路径至系统路径
for dir in [str(BASE_DIR), str(VENV_DIR)]:
    if dir not in sys.path:
        sys.path.insert(1, dir)
# #################### end #########################

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings")
django.setup()
