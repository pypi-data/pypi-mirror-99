import sys
import prestoweb.server.manage


def main():
    sys.argv = ['manage.py', 'runserver']
    prestoweb.server.manage.main()
