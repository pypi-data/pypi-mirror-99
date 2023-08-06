import sys
import argparse
# from .classmodule import MyClass
# from .funcmodule import my_function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", help="Initialize the FileEncrypter CLI.", default=False, action='store_true')
    parser.add_argument("--sync", help="Synchronize local with the connected database.", default=False, action='store_true')
    parser.add_argument("--path", "-p", help="File path")
    parser.add_argument("--operation",'-o',choices=['none', 'encrypt','e','decrypt','d'], type=str, default='none', help="display a square of a given number")
    args = parser.parse_args()

    print(args)
    print('in main')
    args = sys.argv[1:]
    print('count of args :: {}'.format(len(args)))
    for arg in args:
        print('passed argument :: {}'.format(arg))
    # my_function('hello world')
    # my_object = MyClass('Thomas')
    # my_object.say_name()
if __name__ == '__main__':
    main()
