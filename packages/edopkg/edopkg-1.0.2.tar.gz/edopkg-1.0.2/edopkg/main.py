# encoding: utf-8
import os
import sys
from edo_client import get_client
from package import EdoPackage
from env import EdoEnvironment
from cmdparser import parse_args

reload(sys)
sys.setdefaultencoding('utf-8')

SYNC_COMMAND = ['clone', 'push', 'pull']

def main():

    # 命令解析
    cmd, args = parse_args()

    #  获取配置对象
    edo_env = EdoEnvironment()

    #  执行非同步命令
    if cmd not in SYNC_COMMAND:
        if cmd == 'server':
            edo_env.server(args.section)
        elif cmd == 'config':
            edo_env.config()
        elif cmd == 'convert':
            for pat in args.path_filter:
                transpile(pat)
        return

    # 计算local_root
    pkg_name = args.pkg_name if cmd == 'clone' else ''
    path_filter = args.path_filter if cmd != 'clone' else ''
    local_root = os.path.abspath(pkg_name) if pkg_name else find_package_root(args.path_filter)
    if pkg_name and os.path.exists(local_root):
        print u'软件包已存在，请使用pull命令'
        return
    elif not local_root:
        print u'无法找到软件包根目录'
        return

    # 相对路径转换: 计算path_filter相对于local_root的子路径
    abspath = os.path.abspath(args.path_filter) if path_filter else local_root
    path_filter = '' if abspath == local_root else os.path.relpath(abspath, local_root)

    #  读取配置
    oc_api, account, instance, username, password, client_id, \
        client_secret = edo_env.load_config(args.section)

    #  确认同步操作
    print u'当前服务器配置： %s, 账号 %s, 站点 %s' % (oc_api, account, instance)
    if cmd in ['push', 'pull'] and not confirm_sync(cmd):
        print u'同步被取消'
        return

    # 生成服务端连接
    wo_client = get_client('workonline', oc_api, account, instance, username,
                           password, client_id=client_id, client_secret=client_secret)

    # 初始化包管理器
    edo_pkg = EdoPackage(wo_client.package, local_root)

    # 执行同步命令
    if cmd == 'pull':
        edo_pkg.pull(path_filter)
    elif cmd == 'push':
        edo_pkg.push(path_filter)
    elif cmd == 'clone':
        edo_pkg.clone()

def confirm_sync(cmd):
    print u'%s 命令会删除不存在的内容，您确定要继续么？' % cmd
    sys.stdout.write(u'您的选择[y/n](y:继续 | n:取消):')
    return raw_input().lower() == 'y'

def find_package_root(path):
    # 优先在目标目录下查找
    base_path = os.path.abspath(path)
    config_path = os.path.join(base_path, 'config.yaml')
    # 不存在时往上级查找
    while not os.path.exists(config_path):
        if base_path != os.path.dirname(base_path):
            base_path = os.path.dirname(base_path)
            config_path = os.path.join(base_path, 'config.yaml')
        else:
            # 到达根时退出
            return False
    return base_path

def transpile(pattern):
    import glob
    from edopkg.pyaml import load, dump
    import re
    from textwrap import dedent

    for path in glob.iglob(pattern):
        ext = os.path.splitext(path)[-1]

        if ext in ['.yaml', '.yml']:
            data = load(open(path).read())
            script = data['script']
            with open(path.replace(ext, '.py'), 'w+') as f:
                # 写入函数签名
                function_signature = 'def {function}(request, context{comma}{args}):\n'
                function_signature = function_signature.format(function=data['name'], comma=', ' if data['args'] else '', args=data['args'])
                f.write(function_signature)
                # 写入标志行
                tag_line = '    # -*- PLEASE DO NOT MODIFY THIS LINE -*-\n'
                f.write(tag_line)
                # 写入脚本本体
                f.write('\n'.join(map(lambda line: ' ' * 4 + line, script.splitlines())))
        elif ext in ['.py']:
            # 读取py文件内容
            content = open(path).read()
            # 搜索标志行，提取函数内容
            lines = content.splitlines()
            for idx, line in enumerate(lines):
                mark = r'\s*# \-\*\- PLEASE DO NOT MODIFY THIS LINE \-\*\-\s*$'
                if re.match(mark, line):
                    break
            code = '\n'.join(lines[idx+1:])
            # 将脚本内容回填到 yaml 中
            data = load(open(path.replace(ext, '.yaml'), 'r').read())
            data['script'] = dedent(code)
            with open(path.replace(ext, '.yaml'), 'w+') as outputfile:
                outputfile.write(dump(data))
        else:
            print u'跳过无法转译的文件 ', path

if __name__ == '__main__':
    main()
