import argparse
from .new import NewPackage
from .upload import UploadPackage

# TERMINAL ARGUMENTS
parser = argparse.ArgumentParser(prog='UploadHub', description='Manages package uploads')
parser.add_argument('mode')
args = parser.parse_args()
mode = args.mode

if __name__ == '__main__':
    if mode.lower().startswith('n'): window = NewPackage
    elif mode.lower().startswith('u'): window = UploadPackage
    else: exit('Invalid command')

    window = window(
        themename='darkly',
        title='UploadHub By Armando Chaparro 18/07/23',
        resizable=(None, None)
    )

    window.attributes('-topmost', True)
    window.place_window_center()
    window.mainloop()