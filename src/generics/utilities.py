import subprocess


def get_git_commit():
    return subprocess.check_output(["git", "describe", "--always"]).strip().decode()

