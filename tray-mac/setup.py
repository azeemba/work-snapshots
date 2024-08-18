from setuptools import setup

APP = ['tray.py']
DATA_FILES = ["book_x.png", "book_open.png", "nice-camera-click-106269.mp3"]
OPTIONS = {
    'argv_emulation': False,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps'],
}

setup(
    name="Work Snapshots",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

# rm -rf build
# rm -rf dist
# python setup.py py2app -A