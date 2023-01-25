import os
import subprocess


def compilar_directorio(f):

    if os.path.isfile(f):

        if os.path.basename(f).endswith(".ui"):

            arg = f'{os.path.basename(f)} -o {os.path.basename(f).replace(".ui", "")}.py'
            print("Archivo encontrado: " + os.path.basename(f))

            if os.sep != "/":

                comando = "C:\\Users\\a21mariogb\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\pyuic6.exe"

                subprocess.run([comando, os.path.basename(f), "-o",
                                os.path.basename(f).replace(".ui", "") + ".py"], cwd=os.path.abspath(os.getcwd()))

            else:

                subprocess.run(["python3", "-m", "PyQt6.uic.pyuic", "-x", os.path.basename(f), "-o",
                                os.path.basename(f).replace(".ui", "") + ".py"], cwd=os.path.abspath(os.getcwd()))


def main():

    for f in os.listdir(os.path.abspath(os.getcwd())):

        compilar_directorio(f)


if __name__ == '__main__':
    main()
