import subprocess


def test_encode():
    echo_args = ['echo', 'lol']
    args = ['encryptor', 'encode', '-c', 'caesar', '-k', '2']
    echo = subprocess.Popen(echo_args, stdout=subprocess.PIPE)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=echo.stdout)
    echo.stdout.close()
    res, reserr = proc.communicate()
    assert res == b'nqn\n'


def test_decode():
    echo_args = ['echo', 'nqn']
    args = ['encryptor', 'decode', '-c', 'caesar', '-k', '2']
    echo = subprocess.Popen(echo_args, stdout=subprocess.PIPE)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=echo.stdout)
    echo.stdout.close()
    res, reserr = proc.communicate()
    assert res == b'lol\n'
