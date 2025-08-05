import datetime
import json
import os
from typing import Dict, List, Optional, Union, Any
from urllib.parse import urlparse
from chatgpt import gpt_4o_mini_api
import requests
from dotenv import load_dotenv
import threading
import time
import ddddocr

class Nushen:
    """
    Nushen类用于处理网站自动化任务，包括cookie管理和日志记录功能
    """
    
    def __init__(self):
        """
        初始化Nushen类实例
        
        设置默认URL和代理服务器地址
        """
        self.deafultUrl = "https://www.baidu.com"
        self.proxy = "http://127.0.0.1:7890"
        self.browserX=1024
        self.browserY=768
        self.dbPrintList=[]

    def dbPrint(self, pluginName: str, pluginMessage: str = "", isEnd: bool = False) -> None:
        """
        输出带有时间戳的日志信息
        
        参数:
            pluginName: str - 插件名称或消息内容
            pluginMessage: str - 要输出的日志信息，可选
            isEnd: bool - 是否结束并发送累积的消息，可选
            
        返回:
            None
        """
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nowPrint=f"[{current_time}] {pluginName}: {pluginMessage}"
        print(nowPrint)
        self.dbPrintList.append(nowPrint)
        if(isEnd):
            dbprint='\n'.join(self.dbPrintList)
            self.putPrint(dbprint)
            self.dbPrintList=[]
    
    def putPrint(self,message):
        load_dotenv()
        url = os.getenv("GROUP_MSG_API_URL", "")
        group_id = os.getenv("GROUP_ID", "")
        token = os.getenv("API_TOKEN", "")
        
        if not url or not token:
            print("错误：GROUP_MSG_API_URL 或 API_TOKEN 环境变量未设置")
            return None
            
        parmas={
                "group_id": group_id,
                "message": [
                    {
                        "type": "text",
                        "data": {
                            "text": message
                        }
                    }
                    ]
                }
        headers={
                "authorization": f"Bearer {token}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "Connection": "keep-alive"
                }
        try:
            # print(f"正在发送消息到: {url}")
            response = requests.get(url, json=parmas, headers=headers)
            # print(f"请求状态码: {response.status_code}")
            # print(f"响应内容: {response.text}")
            return response
        except Exception as e:
            print(f"发送消息时出错: {str(e)}")
            return None

    def chatgpt(self, message: str) -> str:
        """
        调用ChatGPT API发送消息并获取回复
        
        参数:
            message: str - 要发送给ChatGPT的消息
            
        返回:
            str - ChatGPT的回复内容
        """
        messages = [{'role': 'user','content': message},]
        res = gpt_4o_mini_api(messages)
        return res

    def _is_valid_cookie(self, cookie: Dict[str, Any]) -> bool:
        """
        检查cookie是否有效
        
        参数:
            cookie: Dict[str, Any] - 要检查的cookie字典
            
        返回:
            bool - 如果cookie有效返回True，否则返回False
        """
        # 检查cookie是否为字典类型
        if not isinstance(cookie, dict):
            return False
        
        # 检查cookie是否包含name属性
        if not cookie.get('name'):
            return False
            
        # 检查cookie是否包含value属性
        if not cookie.get('value'):
            return False
            
        # 所有检查都通过，cookie有效
        return True
    
    def _format_cookie(self, cookie: Dict[str, Any], domain: str, name: str) -> Optional[Dict[str, Any]]:
        """
        格式化cookie，添加必要的属性
        
        参数:
            cookie: Dict[str, Any] - 要格式化的cookie字典
            domain: str - cookie所属的域名
            
        返回:
            Optional[Dict[str, Any]] - 格式化后的cookie字典，如果cookie无效则返回None
        """
        if not self._is_valid_cookie(cookie):
            return None
        deleteCookieName=[
                          ['吾爱破解','htVC_2132_lastvisit','htVC_2132_seccodecSAi3p','htVC_2132_seccodecSAi3pRGt'],
                          ['科学刀','JWUN_2132_lastvisit','JWUN_2132_pc_size_c','JWUN_2132_sendmail'],
                        ]
        for deleteCookie in deleteCookieName:
            if name in deleteCookie[0]:
                if cookie.get('name') in deleteCookie[1:]:
                    return None
        cookie['domain'] = domain
        if cookie.get('sameSite') not in ["Strict", "Lax", "None"]:
            cookie['sameSite'] = "None"
        if cookie['sameSite'] == "None":
            cookie['secure'] = True
        return cookie

    def getCookie(self, name: str, url: str) -> List[Dict[str, Any]]:
        """
        获取指定名称和URL的cookie
        
        参数:
            name: str - cookie文件名（不含扩展名）
            url: str - cookie所属的URL
            
        返回:
            List[Dict[str, Any]] - 有效的cookie列表，如果没有有效cookie则返回空列表
            
        异常:
            可能引发的异常会被捕获并记录，返回空列表
        """
        try:
            # 从URL获取域名
            domain = "." + urlparse(url).netloc.split(":", 1)[0]
            if domain.startswith(".."):
                domain = domain[1:]
                
            cookie_path = os.path.join('cookies', f'{name}.json')
            if not os.path.exists(cookie_path):
                os.makedirs(os.path.dirname(cookie_path), exist_ok=True)
                with open(cookie_path, 'w', encoding='utf-8') as f:
                    json.dump([], f, indent=4)
                return []
            
            with open(cookie_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
                valid_cookies = []
                for cookie in cookies:
                    formatted = self._format_cookie(cookie, domain, name)
                    if formatted:
                        valid_cookies.append(formatted)
                return valid_cookies
        except Exception as e:
            print(f'获取Cookie时发生错误：{str(e)}')
            return []
            
    def setCookies(self, name: str, cookies: List[Dict[str, Any]], url: Optional[str] = None) -> bool:
        """
        保存cookies到文件
        
        参数:
            name: str - 保存的文件名（不含扩展名）
            cookies: List[Dict[str, Any]] - 要保存的cookie列表
            url: Optional[str] - 可选，cookie所属的URL，用于提取域名
            
        返回:
            bool - 保存成功返回True，失败返回False
            
        异常:
            引发的异常会被捕获并记录，返回False
        """
        try:
            # 获取域名
            domain = None
            if url:
                domain = "." + urlparse(url).netloc.split(":", 1)[0]
                if domain.startswith(".."):
                    domain = domain[1:]
            
            # 格式化有效的cookie
            formatted_cookies = []
            for cookie in cookies:
                formatted = self._format_cookie(cookie, domain, name) if domain else None
                if formatted or self._is_valid_cookie(cookie):
                    formatted_cookies.append(formatted or cookie)
            
            # 保存到文件
            cookie_path = os.path.join('cookies', f'{name}.json')
            os.makedirs(os.path.dirname(cookie_path), exist_ok=True)
            with open(cookie_path, 'w', encoding='utf-8') as f:
                json.dump(formatted_cookies, f, indent=4)
            
            return True
        except Exception as e:
            print(f'保存Cookie时发生错误：{str(e)}')
            return False

    def setRunBlock(self, name):
        """
        创建运行锁，用于防止同一插件在同一天内多次运行
        
        参数:
            name: str - 插件名称，用于创建唯一的运行锁文件
            
        返回:
            bool - 创建成功返回True，失败返回False
            
        异常:
            捕获所有异常并返回False
        """
        try:
            filePath = os.path.join('runblock', f'{name}.runblock')
            os.makedirs(os.path.dirname(filePath), exist_ok=True)
            with open(filePath, 'w', encoding='utf-8') as f:
                f.write(datetime.datetime.now().strftime('%Y-%m-%d'))
            self.dbPrint(name, "创建运行锁成功")
            return True
        except Exception as e:
            print(f'创建运行锁时发生错误：{str(e)}')
            return False

    def getRunBlock(self, name):
        """
        获取运行锁状态，检查指定插件是否在当天已经运行
        
        参数:
            name: str - 插件名称，用于查找对应的运行锁文件
            
        返回:
            bool - 如果插件今天已运行返回True，否则返回False
            
        异常:
            捕获所有异常并返回False
        """
        try:
            filePath = os.path.join('runblock', f'{name}.runblock')
            if not os.path.exists(filePath):
                return False
            with open(filePath, 'r', encoding='utf-8') as f:
                if f.read() == datetime.datetime.now().strftime('%Y-%m-%d'):
                    return True
                else:
                    return False
        except Exception as e:
            print(f'检查运行锁时发生错误：{str(e)}')
            return False

    def hitokoto(self):
        try:
            # 构建请求URL和参数
            url = 'https://api.yyy001.com/api/yiyan'
            # 发送请求
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # 如果响应状态码不是200，则抛出异常
            resData = response.text
            
            # 添加字符长度限制（10-40字符）
            if len(resData) < 10:
                # 不够10个字符时自动补齐
                while len(resData) < 10:
                    resData += "，" + resData  # 使用原内容进行补充
            elif len(resData) > 40:
                # 超过40个字符时截断
                resData = resData[:40]     
            return resData
            
        except requests.RequestException as e:
            self.dbPrint("Hitokoto", f"获取一言时发生错误: {str(e)}")
            default_msg = '每一天都是一个全新的开始'
            print(f"使用默认一言：{default_msg}，长度：{len(default_msg)}")
            return default_msg

    def getProxy(self,address=''):
        load_dotenv()
        proxy_url = os.getenv("PROXY_URL")
        if not proxy_url:
            return ''
        url = f"{proxy_url}"
        if address:
            url += f"&area={address}"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return ''
        resData = response.text
        return resData
        
    def handle_login_required(self, pluginName: str, sb, pluginUrl: str) -> bool:
        """
        处理未登录情况，提供统一的用户交互和Cookie保存逻辑
        
        参数:
            pluginName: str - 插件名称
            sb - SB实例
            pluginUrl: str - 插件URL
            
        返回:
            bool - 如果用户成功登录并保存了cookie返回True，否则返回False
        """
        self.dbPrint(pluginName, "未能找到用户名元素，可能未登录或页面结构已改变", True)
        
        # 使用线程处理输入超时
        loginRes = ""  # 初始化变量
        
        # 定义输入线程函数
        def input_thread_func():
            nonlocal loginRes  # 使用nonlocal关键字访问外部变量
            loginRes = input("是否要登录？输入1继续 (等待8秒): ")
        
        # 创建并启动输入线程
        input_thread = threading.Thread(target=input_thread_func)
        input_thread.daemon = True  # 设置为守护线程，主线程结束时自动结束
        input_thread.start()
        
        # 等待8秒或用户输入
        for i in range(9):
            if not input_thread.is_alive():  # 如果线程已结束（用户已输入）
                break
            time.sleep(1)
        if loginRes != '1':
            print("未知输入")
            return False
        sb.clear_all_cookies()
        sb.refresh()
        print('收到你的回复啦 快去登录 等待90秒')
        for i in range(91):
            time.sleep(1)
            print(f'快去登录 还剩{90-i}秒')
        print('正在保存cookie')
        # 保存cookie
        saveCookieRes = self.setCookies(pluginName, sb.get_cookies(), pluginUrl)
        if saveCookieRes:
            print("已保存cookie")
        else:
            print('保存cookie失败,未知问题')
        return saveCookieRes

    def save_captcha_image(self, sb, selector: str, pluginName: str) -> str:
        """
        保存验证码图片到指定目录
        
        参数:
            sb - SeleniumBase实例
            selector: str - 验证码图片的CSS选择器
            pluginName: str - 插件名称，用于日志记录
            
        返回:
            str - 保存的验证码图片路径，如果保存失败则返回空字符串
        """
        try:
            # 创建验证码保存目录
            captcha_dir = "captcha_images"
            if not os.path.exists(captcha_dir):
                os.makedirs(captcha_dir)
                
            # 生成验证码文件名（使用时间戳确保唯一性）
            captcha_file = os.path.join(captcha_dir, f"captcha_{pluginName}_{int(time.time())}.png")
            
            # 使用SeleniumBase的save_element_as_image_file方法保存验证码图片
            sb.save_element_as_image_file(selector, captcha_file)
            
            # 记录日志
            self.dbPrint(pluginName, f"验证码已保存到: {captcha_file}")
            
            # 返回验证码文件路径
            return captcha_file
        except Exception as e:
            self.dbPrint(pluginName, f"保存验证码图片时出错: {str(e)}")
            return ""

    def handle_captcha(self, sb, captcha_img_selector: str, captcha_input_selector: str, pluginName: str) -> bool:
        """
        处理验证码，使用ddddocr自动识别，识别失败时回退到手动输入
        
        参数:
            sb - SeleniumBase实例
            captcha_img_selector: str - 验证码图片的CSS选择器
            captcha_input_selector: str - 验证码输入框的CSS选择器
            pluginName: str - 插件名称，用于日志记录
            
        返回:
            bool - 如果验证码处理成功返回True，否则返回False
        """
        try:
            # 保存验证码图片
            captcha_file = self.save_captcha_image(sb, captcha_img_selector, pluginName)
            if not captcha_file:
                return False
            
            # 尝试使用ddddocr自动识别验证码
            try:
                # 初始化ddddocr
                ocr = ddddocr.DdddOcr(show_ad=False)
                
                # 读取验证码图片
                with open(captcha_file, 'rb') as f:
                    img_bytes = f.read()
                
                # 识别验证码
                captcha_code = ocr.classification(img_bytes)
                
                # 记录日志
                self.dbPrint(pluginName, f"验证码自动识别结果: {captcha_code}")
                
                # 输入验证码
                sb.type(captcha_input_selector, captcha_code)
                
                return True
                
            except Exception as e:
                # 如果自动识别失败，回退到手动输入
                self.dbPrint(pluginName, f"自动识别验证码失败: {str(e)}，回退到手动输入")
                
                # 获取用户输入的验证码
                captcha_code = input(f"请查看 {captcha_file} 并输入验证码: ")
                
                # 输入验证码
                sb.type(captcha_input_selector, captcha_code)
                
                return True
                
        except Exception as e:
            self.dbPrint(pluginName, f"处理验证码时出错: {str(e)}")
            return False



def getVersion():
    # 你要想不更新就可以改成999999999999
    return '202508051421'