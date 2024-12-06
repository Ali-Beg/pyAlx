# main.py
import argparse
from src.core.shell import Shell
from src.gui.main_window import MainWindow

def main():
    parser = argparse.ArgumentParser(description='Python Shell')
    parser.add_argument('--gui', action='store_true', help='Start in GUI mode')
    args = parser.parse_args()
    
    if args.gui:
        window = MainWindow()
        window.run()
    else:
        shell = Shell()
        shell.run()

if __name__ == "__main__":
    main()