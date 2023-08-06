import sys
import argparse

from posixpath import isfile

def init(title):
    parser = argparse.ArgumentParser(prog=title)
    subparsers = parser.add_subparsers(
        dest='subcommand', help='model commands help')
    model_parser = subparsers.add_parser('model', help='command help')
    model_subparsers = model_parser.add_subparsers(
        dest='model_command', help='model commands')
    # 初始化脚手架命令
    init_parser = model_subparsers.add_parser(
        'init', help='init model scaffold')
    init_parser.add_argument('--name', '-n', type=str, help='scaffold name')
    # 部署子命令
    deploy_parser = model_subparsers.add_parser(
        'deploy', help='deploy a model')
    deploy_parser.add_argument('--model_id', '-m', help='model id')
    return parser

def select_one(options):
    print("请选择：")
    for idx, element in enumerate(options):
        print("{}) {}".format(idx+1,element))
    i = input("请输入序号: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i)
    except:
        pass

from posixpath import join, exists, abspath, dirname, pardir
import os

def init_scaffold(name):
    home = abspath('.')
    scaffold_dir = join(home, name)
    lib_dir  = join(scaffold_dir, 'lib' )
    for dir_ in [scaffold_dir, lib_dir]:
        sys.stdout.write(f'Creating {dir_} ... ')
        sys.stdout.flush()
        if not exists(dir_):
            os.makedirs(dir_)
            print ('done')
        elif not os.path.isdir(dir_):
            print ('faild')
            print (f'ERROR! {dir_} exists, but is not a directory.')
            return
        else:
            print ('exists')
    select_one(['model', 'id'])
    sys.stdout.write(f'Installing bge-python-sdk ... ')
    os.system(f'pip install --no-deps bge-python-sdk -t {lib_dir}')
    print (f'bgesdk installed in {lib_dir}')
    import stat
    script_name = 'index.py'
    script_path = os.path.join(scaffold_dir, script_name)
    code = index_py_template.format(interpreter=sys.executable)
    with open(script_path, 'wb') as file_out:
        file_out.write(code.encode())
    st = os.stat(script_path)
    os.chmod(script_path, st.st_mode | stat.S_IEXEC)
    print ('done')

index_py_template = '''\
import sys
sys.path.insert(0, './lib')

import bgesdk

def main(event, context):
    return bgesdk.__version__

def handler(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html;charset=utf-8')]
    start_response(status, response_headers)
    return [str(bgesdk).encode('utf-8')]

'''

def deploy_model(model_id):
    pass


def main(input_args):
    parser = init('bge')
    if not input_args:
        input_args = ['--help']
    args = parser.parse_args(input_args)
    subcommand = args.subcommand
    if subcommand == 'model':
        if args.model_command == 'init':
            init_scaffold(args.name)
        if args.model_command == 'deploy':
            deploy_model(args.model_id)

if __name__ == '__main__':
    input_args = sys.argv[1:]
    main(input_args)