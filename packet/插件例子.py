import time
from seleniumbase import SB
from nushen import Nushen
from selenium.webdriver.common.by import By

def run():
    pluginBoolean = False
    pluginName = '插件'
    pluginUrl = 'https://www.demo.com/'
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
            pass
        
            if False:
                # 今日已完成 设置运行锁
                nushen.setRunBlock(pluginName)
        except Exception as e:
            nushen.dbPrint(pluginName,{str(e)})
            nushen.dbPrint(pluginName, "未能找到用户名元素，可能未登录或页面结构已改变",True)
            loginRes=input("是否要登录 1继续 (等待8秒)")
            for i in range(9):
                time.sleep(1)
                if loginRes!='':break
            if loginRes!=1:return
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
            pass
        except Exception as e:
            nushen.dbPrint(pluginName, f"签到过程出错: {str(e)}")
        
        # 保存cookie
        saveCookieRes = nushen.setCookies(pluginName, sb.get_cookies(), pluginUrl)
        if saveCookieRes:
            nushen.dbPrint(pluginName, "已保存cookie")
        nushen.dbPrint(pluginName, "任务结束",True)

def getVersion():
    # 你要想不更新就可以改成999999999999
    return '202506071738'