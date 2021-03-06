def command_res(cmd):
    import subprocess
    if type(cmd) is not str:
        raise TypeError("cmd type is str, not '%s'" % type(cmd).__name__)
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()


if __name__ == '__main__':
    print(command_res(input('Введите комманду: ')))
