import subprocess

folder = "imagesnew"

files = [()]

for file in files:
    subprocess.call(["magick", "convert", file[0], "-trim", "-background", "white", file[1]])