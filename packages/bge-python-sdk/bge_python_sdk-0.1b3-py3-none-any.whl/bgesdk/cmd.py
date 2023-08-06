#!/usr/bin/env python

import argparse
import configparser
import os
import stat
import sys

from os.path import expanduser
from posixpath import join, exists, abspath, isdir

from . import version
from .client import API


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


def get_user_home():
    return expanduser("~")


def get_home():
    return abspath('.')


def select_one(options):
    print("请选择：")
    while True:
        for idx, element in enumerate(options):
            print("{}) {}".format(idx+1,element))
        i = input("请输入序号: ")
        try:
            if 0 < int(i) <= len(options):
                return options[int(i)-1]
        except:
            pass


def init_parser():
    home = get_home()
    parser = argparse.ArgumentParser(
        description='BGE 开放平台 SDK 命令行工具提供了初始化模型脚手架、部署模型、'
                    '初始化模型文档配置文件、\n上传图片、部署模型文档等命令。',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        help='显示当前 BGE 开放平台 Python SDK 版本号。',
        version='version v{}'.format(version.__version__)
    )
    subparsers = parser.add_subparsers(
        dest='command',
        help='SDK 命令行工具可选子命令。'
    )
    config_p = subparsers.add_parser(
        'config',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help='配置命令行工具。'
    )
    config_p.add_argument(
        '--project',
        default='DEFAULT',
        help='配置项目名称，不同的 BGE 项目可以支持读取、写入不同配置。'
    )
    config_p.set_defaults(method=write_config, parser=config_p)
    model_p = subparsers.add_parser(
        'model',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help='模型初始化脚手架、部署等相关命令。'
    )
    model_p.set_defaults(method=print_subparser_help, parser=model_p)
    model_subparsers = model_p.add_subparsers(
        dest='subcommand',
        help='可选子命令。'
    )
    # 初始化脚手架命令
    init_p = model_subparsers.add_parser(
        'init',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help='初始化一个新的模型开发脚手架项目。'
    )
    init_p.set_defaults(method=init_scaffold, parser=init_p)
    init_p.add_argument(
        'scaffold_name',
        type=str,
        help='脚手架名字。'
    )
    init_p.add_argument(
        '-f',
        '--force',
        default=False,
        action='store_true',
        help='强制初始化。'
    )
    init_p.add_argument(
        '--home',
        type=str,
        default=home,
        help='脚手架项目生成的父级目录，默认为当前目录。'
    )
    # 部署子命令
    deploy_p = model_subparsers.add_parser(
        'deploy',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help='上传模型源码完成模型部署。'
    )
    deploy_p.set_defaults(method=deploy_model, parser=deploy_p)
    deploy_p.add_argument(
        'model_id',
        type=str,
        help='模型编号。'
    )
    deploy_p.add_argument(
        'source_file',
        type=str,
        help='.zip 格式模型源文件。'
    )
    deploy_p.add_argument(
        '--project',
        default='DEFAULT',
        help='配置项目名称，不同的 BGE 项目可以支持读取、写入不同配置。'
    )
    deploy_p.add_argument(
        '--runtime',
        type=str,
        default='python3',
        choices=['python2', 'python3'],
        help='模型运行环境。'
    )
    deploy_p.add_argument(
        '--handler',
        type=str,
        default='index.handler',
        help='模型入口模块和函数配置。'
    )
    deploy_p.add_argument(
        '--memory_size',
        type=int,
        default='128',
        help='模型运行内存占用大小，单位：MB。'
    )
    deploy_p.add_argument(
        '--timeout',
        type=int,
        default=900,
        help='模型运行环境，单位：秒。'
    )
    deploy_p.add_argument(
        '--comment',
        type=str,
        help='模型备注。'
    )
    return parser


def print_subparser_help(args):
    """打印 subparser 帮助信息"""
    parser = args.parser
    parser.print_help(sys.stderr)


def init_scaffold(args):
    scaffold_name = args.scaffold_name
    home = args.home
    force = args.force
    if home is None:
        home = get_home()
    scaffold_dir = join(home, scaffold_name)
    if not force:
        if not exists(home):
            print('Error! home folder "%s" not found.' % home)
            return
        if exists(scaffold_dir):
            print('Error! scaffold "%s" exists.' % scaffold_dir)
            return
    else:
        if not exists(scaffold_dir):
            os.makedirs(scaffold_dir)
    lib_dir = join(scaffold_dir, 'lib' )
    for dir_ in [scaffold_dir, lib_dir]:
        sys.stdout.write(f'Creating {dir_} ... ')
        sys.stdout.flush()
        if not exists(dir_):
            os.makedirs(dir_)
            print('done')
        elif not isdir(dir_):
            print('faild')
            print(f'ERROR! {dir_} exists, but is not a directory.')
            return
        else:
            print('exists')
    sys.stdout.write(f'Installing bge-python-sdk ... ')
    os.system(f'pip install --no-deps bge-python-sdk -t {lib_dir}')
    print(f'bgesdk installed in {lib_dir}')
    script_name = 'index.py'
    script_path = join(scaffold_dir, script_name)
    code = index_py_template.format(interpreter=sys.executable)
    with open(script_path, 'wb') as file_out:
        file_out.write(code.encode())
    st = os.stat(script_path)
    os.chmod(script_path, st.st_mode | stat.S_IEXEC)
    print('done')


def deploy_model(args):
    """部署模型"""
    project = args.project
    model_id = args.model_id
    source_file = args.source_file
    runtime = args.runtime
    handler = args.handler
    memory_size = args.memory_size
    timeout = args.timeout
    comment = args.comment
    config = _read_config()
    if project not in config:
        raise ValueError('project {} not configged'.format(project))
    section_config = config[project]
    client_id = section_config['client_id']
    client_secret = section_config['client_secret']
    access_token = section_config['access_token']
    max_retries = section_config['max_retries']
    endpoint = section_config['endpoint']
    api = API(access_token, endpoint=endpoint, max_retries=max_retries)
    api.deploy


def _read_config():
    user_home = get_user_home()
    config_dir = join(user_home, '.bge')
    if not exists(config_dir):
        os.makedirs(config_dir)
    config_path = join(config_dir, 'bge.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def write_config(args):
    project = args.project
    user_home = get_user_home()
    config_dir = join(user_home, '.bge')
    if not exists(config_dir):
        os.makedirs(config_dir)
    print('请输入项目“{}”的 BGE 开放平台配置：\n'.format(project))
    config_path = join(config_dir, 'bge.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    for key in ['client_id', 'client_secret', 'redirect_uri', 'endpoint',
                'timeout', 'verbose']:
        if project not in config:
            config[project] = {}
        config_section = config[project]
        value = config_section.get(key, '-')
        value = input('？请输入 {} [{}]：'.format(key, value))
        if value:
            config_section[key] = value
    with open(config_path, 'w') as config_file:
        config.write(config_file)
    print('')
    print('配置已保存至：{}'.format(config_path))


def main():
    parser = init_parser()
    if len(sys.argv) < 2:
        parser.print_help(sys.stderr)
        sys.exit(1)
    input_args = sys.argv[1:]
    args = parser.parse_args(input_args)
    args.method(args)


if __name__ == '__main__':
    main()