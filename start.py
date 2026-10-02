# =====================================================
# iVerify V2 - Launcher
# Sosyal Medya Veri Analiz Motoru
# =====================================================

import subprocess
import sys


def start_iverify():
    print("iVerify V2 başlatılıyor...")
    
    subprocess.run(
        [sys.executable, "app.py"]
    )


if __name__ == "__main__":
    start_iverify()