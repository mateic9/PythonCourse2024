import subprocess
import os
import platform

def launch_in_terminal(command, args):
    try:
        if platform.system() == "Windows":

            subprocess.Popen(["start", "cmd", "/k"] + [command] + args, shell=True)
        elif platform.system() == "Darwin":
            script = f"""tell application "Terminal"
                do script "{command} {' '.join(args)}"
            end tell"""
            subprocess.run(["osascript", "-e", script])
        else:
            subprocess.Popen(["x-terminal-emulator", "-e", command] + args)
    except Exception as e:
        print(f"Error launching client: {e}")

command = r".\thread_client.py"
args = ["--mode=singleplayer", "--height=6", "--width=6" ,"--difficulty=medium" ,"--first=yes"]


if "--mode=singleplayer" in args:
    launch_in_terminal(command, args)
else:
    launch_in_terminal(command, args)
    launch_in_terminal(command, args)