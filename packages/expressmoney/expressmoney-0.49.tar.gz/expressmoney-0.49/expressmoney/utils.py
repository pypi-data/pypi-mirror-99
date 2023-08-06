import os


def environ():
    """ lists environment variables, and splits elements in path variable """

    for k, v in sorted(os.environ.items()):
        print(k+':', v)
    print('\n')
    # list elements in path environment variable
    [print(item) for item in os.environ['PATH'].split(';')]
