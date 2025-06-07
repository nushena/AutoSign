import datetime
import json
import os
from typing import Dict, List, Optional, Union, Any
from urllib.parse import urlparse
from chatgpt import gpt_4o_mini_api
import requests
from dotenv import load_dotenv

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
    
    def _format_cookie(self, cookie: Dict[str, Any], domain: str) -> Optional[Dict[str, Any]]:
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
        deleteCookieName=['JWUN_2132_lastvisit','JWUN_2132_pc_size_c','JWUN_2132_sendmail',
                          'm1cT_2132_lastvisit','htVC_2132_lastvisit','htVC_2132_seccodecSAi3p',
                          'htVC_2132_seccodecSAi3pRGt'
                         ]
        if cookie.get('name') in deleteCookieName:
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
                    formatted = self._format_cookie(cookie, domain)
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
                formatted = self._format_cookie(cookie, domain) if domain else None
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

    def getProxy(self):
        load_dotenv()
        proxy_url = os.getenv("PROXY_URL")
        if not proxy_url:
            return ''
        url = f"{proxy_url}"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return ''
        resData = response.text
        return resData

def getVersion():
    # 你要想不更新就可以改成999999999999
    return '202506071739'