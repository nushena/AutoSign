import threading
import time
from seleniumbase import SB
from nushen import Nushen
from selenium.webdriver.common.by import By
import random

def run():
    pluginBoolean = True
    pluginName = '酒入论坛'
    pluginUrl = 'https://www.jr37.xyz/home.php?mod=spacecp&ac=credit&showcredit=1'
    browserX=0
    browserY=0
    if not pluginBoolean:
        print(f"{pluginName} 插件未开启")
        return
    nushen = Nushen()
    # proxyUrl=nushen.getProxy()
    # nushen.dbPrint(pluginName,"使用代理 {proxyUrl}")
    # sb.set_wire_proxy(proxyUrl)
    # 获取运行锁
    if nushen.getRunBlock(pluginName):
        nushen.dbPrint(pluginName+'运行锁', "今日任务已完成",True)
        return
    already_signed=False
    with SB(test=True, uc=True) as sb:
        sb.open(nushen.deafultUrl)
        sb.set_window_size(browserX|nushen.browserX, browserY|nushen.browserY)
        sb.open(pluginUrl)
        sb.clear_all_cookies()
        
        # 加载cookie
        cookies = nushen.getCookie(pluginName, pluginUrl)
        if cookies:
            for cookie in cookies:
                try:
                    sb.add_cookie(cookie)
                except Exception:
                    pass
            sb.refresh()
        
        # 获取个人信息
        try:
            userName = sb.get_text('strong.vwmy')
            userCoin = sb.get_text('li.xi1')
            nushen.dbPrint(pluginName,f"当前用户: {userName}")
            nushen.dbPrint(pluginName,f"当前酒入币: {userCoin}")
        except Exception as e:
            nushen.dbPrint(pluginName,{str(e)})
            nushen.dbPrint(pluginName, "未能找到用户名元素，可能未登录或页面结构已改变",True)
            
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
                print(f"\r等待输入，还剩 {9-i} 秒...")
            if loginRes != '1':
                print("未知输入")
                return
                
            print('收到你的回复啦 快去登录 等待90秒')
            for i in range(91):
                time.sleep(1)
                print(f'快去登录 还剩{90-i}秒')
            print('正在保存cookie')
            # 保存cookie
            saveCookieRes = nushen.setCookies(pluginName, sb.get_cookies(), pluginUrl)
            if saveCookieRes:
                print("已保存cookie")

            else:
                print('保存cookie失败,未知问题')
            return
            
        # 任务逻辑
        try:
            sb.open('https://www.jr37.xyz/dsu_paulsign-sign.html')
            sb.sleep(5)
            if sb.find_element('h1.mt'):
                signedInfo = sb.get_text('h1.mt')
                if('今天已经签到过了' in signedInfo):
                    already_signed=True
                    nushen.dbPrint(pluginName,'今日已签到')
                    # 今日已完成 设置运行锁
                    nushen.setRunBlock(pluginName)
            
            if not already_signed:
                # 获取所有li元素
                li_elements = sb.find_elements('ul.qdsmile li')
                # nushen.dbPrint(pluginName, f"找到 {len(li_elements)} 个表情选项")
                
                # 随机选择一个li元素
                if li_elements:
                    random_li = random.choice(li_elements)
                    # nushen.dbPrint(pluginName, f"随机选择了一个表情")
                    # 点击选中的元素
                    random_li.click()
                    sb.sleep(1)
                    # nushen.dbPrint(pluginName, "点击了随机选择的表情")
                else:
                    sb.click('li#kx')
                    sb.sleep(1)
                hitokoto=nushen.hitokoto()
                sb.type('#todaysay',hitokoto)
                sb.sleep(2)
                sb.click('a[onclick*="showWindow(\'qwindow\', \'qiandao\'"]')
                nushen.dbPrint(pluginName, "签到完毕")
        except Exception as e:
            nushen.dbPrint(pluginName, f"签到过程出错: {str(e)}")
        
        # 保存cookie
        saveCookieRes = nushen.setCookies(pluginName, sb.get_cookies(), pluginUrl)
        if saveCookieRes:
            nushen.dbPrint(pluginName, "已保存cookie")
        nushen.dbPrint(pluginName, "任务结束",True)

def getVersion():
    # 你要想不更新就可以改成999999999999
    return '202506082246'