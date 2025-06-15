import os
import sys
import importlib.util
import time
import re


def load_and_run_module(file_path):
    """
    加载并运行指定的Python模块
    
    Args:
        file_path (str): Python文件的路径
    """
    try:
        # 获取项目根目录的绝对路径
        root_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 将项目根目录添加到Python路径
        if root_dir not in sys.path:
            sys.path.insert(0, root_dir)
            
        # 获取模块名（不包含.py扩展名）
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # 加载模块
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            print(f"无法加载模块: {file_path}")
            return
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 如果模块有run方法，执行它
        if hasattr(module, 'run'):
            # print(f"正在运行 {module_name} 中的 run() 方法...")
            module.run()
        else:
            print(f"警告: {module_name} 没有 run() 方法")
            
    except Exception as e:
        print(f"运行 {file_path} 时出错: {str(e)}")

def scan_and_run_packets():
    """扫描并运行packet文件夹中的所有Python文件"""
    packet_dir = "packet"
    
    # 确保packet文件夹存在
    if not os.path.exists(packet_dir):
        print("packet文件夹不存在")
        return
        
    # 获取所有.py文件
    py_files = [f for f in os.listdir(packet_dir) 
                if f.endswith('.py') and os.path.isfile(os.path.join(packet_dir, f))]
    
    if not py_files:
        print("packet文件夹中没有找到Python文件")
        return
        
    # print(f"找到以下Python文件：{', '.join(py_files)}")
    
    # 依次加载并运行每个文件
    from nushen import Nushen
    nushen = Nushen()
    nushen.dbPrint("Nushen", "开始运行签到插件",True)
    for py_file in py_files:
        print(f'正在运行 {py_file}')
        file_path = os.path.join(packet_dir, py_file)
        load_and_run_module(file_path)
    nushen.dbPrint("Nushen", "签到插件运行结束",True)

def getFastProxy():
    import requests
    examplesUrl='https://raw.githubusercontent.com/nushena/AutoSign/refs/heads/main/update.json'
    proxyList=[
        'https://github-speedup.com/',
        'https://ghfast.top/',
        'https://gh-proxy.com/',
        'https://github.moeyy.xyz/',
    ]
    
    results = []
    
    print("开始测试各代理速度...")
    
    for proxy in proxyList:
        proxy_url = proxy + examplesUrl
        try:
            start_time = time.time()
            response = requests.get(proxy_url, timeout=5)
            end_time = time.time()
            
            if response.status_code == 200:
                elapsed_time = end_time - start_time
                results.append((proxy, elapsed_time))
                print(f"代理 {proxy} 访问成功，耗时: {elapsed_time:.2f}秒")
            else:
                print(f"代理 {proxy} 返回状态码: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"代理 {proxy} 请求超时（>5秒）")
        except Exception as e:
            print(f"代理 {proxy} 请求失败: {str(e)}")
    
    # 按速度排序并返回最快的代理
    if results:
        fastest_proxy = min(results, key=lambda x: x[1])
        print(f"最快的加速源是: {fastest_proxy[0]}，耗时: {fastest_proxy[1]:.2f}秒")
        return fastest_proxy[0]
    else:
        print("所有代理均请求失败")
        return 

def checkVersion():
    import requests
    FastProxyUrl=getFastProxy()
    updateUrl=FastProxyUrl+'https://raw.githubusercontent.com/nushena/AutoSign/refs/heads/main/update.json'
    updateUrl=updateUrl.strip()
    print(updateUrl)
    if not FastProxyUrl:
        print('无法更新，连接失败')
        return
    # 检查.env
    env_file = ".env"
    if not os.path.exists(env_file):
        # 创建.env文件并写入默认配置
        with open(env_file, "w", encoding="utf-8") as f:
            f.write("OPENAI_API_KEY=<openai-key>\n")
            f.write("OPENAI_BASE_URL=<openai-代理网址>\n")
            f.write("GROUP_MSG_API_URL=<群聊-api>\n")
            f.write("GROUP_ID=<群聊-id>\n")
            f.write("API_TOKEN=<api-token>\n")
            f.write("PROXY_URL=<提取代理-api>\n")
        print(".env文件已创建，请编辑并填入您的API密钥和代理设置")
    try:
        # 获取update.json内容
        response = requests.get(updateUrl, timeout=5)
        if response.status_code != 200:
            print(f"获取更新信息失败，状态码: {response.status_code}")
            return
            
        update_info = response.json()
        print("成功获取更新信息")
        
        # 检查并更新每个插件
        for plugin in update_info:
            plugin_name = plugin.get('name')
            remote_version = plugin.get('version')
            file_path = plugin.get('filePath')
            download_url = plugin.get('downloadUrl')
            
            # 检查本地是否存在该插件
            local_version = None
            if os.path.exists(file_path):
                try:
                    # 使用extract_version_from_file函数获取版本，而不是动态导入
                    local_version = extract_version_from_file(file_path)
                    if local_version is None:
                        print(f"无法从文件 {file_path} 中提取版本信息")
                except Exception as e:
                    print(f"获取插件 {plugin_name} 版本时出错: {str(e)}")
            
            # 判断是否需要更新
            need_update = local_version is None or local_version < remote_version
            
            if need_update:
                print(f"插件 {plugin_name} 需要更新: 本地版本 {local_version or '不存在'}, 远程版本 {remote_version}")
                
                # 创建目录(如果不存在)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # 下载插件
                try:
                    download_response = requests.get(FastProxyUrl + download_url, timeout=10)
                    if download_response.status_code == 200:
                        with open(file_path, 'wb') as f:
                            f.write(download_response.content)
                        print(f"插件 {plugin_name} 已更新到版本 {remote_version}")
                    else:
                        print(f"下载插件 {plugin_name} 失败，状态码: {download_response.status_code}")
                except Exception as e:
                    print(f"下载插件 {plugin_name} 时出错: {str(e)}")
            else:
                print(f"插件 {plugin_name} 已是最新版本: {local_version}")
                
    except Exception as e:
        print(f"检查更新时出错: {str(e)}")

def extract_version_from_file(file_path):
    """
    直接从文件中提取版本信息，而不执行代码
    
    Args:
        file_path (str): 文件路径
        
    Returns:
        str or None: 版本字符串，如果未找到则返回None
    """
    try:
        # 以二进制模式打开文件，避免编码问题
        with open(file_path, 'rb') as f:
            content = f.read()
            
        # 尝试解码文件内容，使用不同的编码方式
        for encoding in ['utf-8', 'gbk', 'latin1']:
            try:
                text = content.decode(encoding)
                # 使用正则表达式查找getVersion函数中的返回值
                version_match = re.search(r"def\s+getVersion\s*\(\s*\).*?return\s+['\"]([^'\"]+)['\"]", 
                                         text, re.DOTALL)
                if version_match:
                    return version_match.group(1)
            except UnicodeDecodeError:
                continue
                
        return None
    except Exception as e:
        print(f"从文件 {file_path} 提取版本时出错: {str(e)}")
        return None

def checkEnv():
    # 检查虚拟环境
    venv_dir = ".venv"
    if not os.path.exists(venv_dir):
        print("虚拟环境不存在，正在创建...")
        try:
            import venv
            venv.create(venv_dir, with_pip=True)
            print("虚拟环境创建成功")
        except Exception as e:
            print(f"创建虚拟环境失败: {str(e)}")
            sys.exit(1)

    # 获取虚拟环境的Python解释器路径
    if os.name == 'nt':  # Windows
        venv_python = os.path.join(venv_dir, 'Scripts', 'python.exe')
    else:  # Linux/Mac
        venv_python = os.path.join(venv_dir, 'bin', 'python')

    # 检查是否已经在虚拟环境中
    if 'VIRTUAL_ENV' not in os.environ:
        print("当前不在虚拟环境中，正在切换到虚拟环境...")
        try:
            import subprocess
            # 设置环境变量
            env = os.environ.copy()
            env['VIRTUAL_ENV'] = os.path.abspath(venv_dir)
            if os.name == 'nt':  # Windows
                env['PATH'] = os.path.join(env['VIRTUAL_ENV'], 'Scripts') + os.pathsep + env['PATH']
            else:  # Linux/Mac
                env['PATH'] = os.path.join(env['VIRTUAL_ENV'], 'bin') + os.pathsep + env['PATH']
            
            # 使用虚拟环境的Python解释器运行当前脚本
            print(f"使用Python解释器: {venv_python}")
            subprocess.run([venv_python, __file__], env=env, check=True)
            sys.exit(0)
        except subprocess.CalledProcessError as e:
            print(f"切换到虚拟环境失败: {str(e)}")
            sys.exit(1)

    # 检查环境
    try:
        import requests
        import openai
        import dotenv
        import requests
        import selenium
        import seleniumbase
        import ddddocr
    except ImportError as e:
        print(f"导入错误: {str(e)}")
        print("正在安装依赖...")
        import subprocess
        try:
            subprocess.check_call([venv_python, "-m", "pip", "install", "-r", "requirements.txt", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])
            print("依赖安装完成")
        except subprocess.CalledProcessError as e:
            print(f"安装依赖失败: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    checkEnv()
    checkVersion()
    scan_and_run_packets()

def getVersion():
    # 你要想不更新就可以改成999999999999
    return '202506152141'