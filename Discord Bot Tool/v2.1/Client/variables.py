from ntpath import join
import os
from pathlib import Path
from sys import platform

def create_folders(path):
    if not os.path.exists(path):
        os.makedirs(path)

def joinpath(path="", *args):
    return os.path.join(PROJECT_DIR, path, *args)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TRASH_ICON = joinpath("assets", "img", "trash_icon.png")

