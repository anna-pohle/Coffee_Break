"""
Setup script für py2app - erstellt die CoffeeBreak.app
"""
from setuptools import setup

APP = ['coffee_break.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': None,
    'plist': {
        'CFBundleName': 'CoffeeBreak',
        'CFBundleDisplayName': 'CoffeeBreak',
        'CFBundleIdentifier': 'com.coffeebreak.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': True,  # Keine Dock-Icon, nur Menüleiste
        'NSHighResolutionCapable': True,
    },
    'packages': ['rumps'],
    'includes': ['objc', 'Foundation', 'AppKit', "ctypes"],
    'excludes': ['tkinter', 'matplotlib', 'numpy', 'scipy', 'pandas'],
    'site_packages': True,
    "frameworks": [
        "/opt/homebrew/opt/libffi/lib/libffi.8.dylib",
    ],
}

setup(
    name='CoffeeBreak',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)