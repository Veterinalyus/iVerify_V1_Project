import subprocess
import time
import webbrowser
import sys
import os


def main():

    base = os.path.dirname(os.path.abspath(__file__))

    app_file = os.path.join(base, "app_final.py")

    subprocess.Popen(
        [sys.executable, app_file],
        cwd=base
    )

    time.sleep(3)

    webbrowser.open(
        "http://127.0.0.1:5000"
    )


if __name__ == "__main__":
    main()