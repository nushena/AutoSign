import threading
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
    
    # 获取运行锁
    if nushen.getRunBlock(pluginName):
        nushen.dbPrint(pluginName+'运行锁', "今日任务已完成",True)
        return
    # proxyUrl = str(nushen.getProxy())
    # nushen.dbPrint(pluginName,f"使用代理 {proxyUrl}")
    # with SB(test=True, uc=True, proxy=proxyUrl) as sb:
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
            print('加载cookie完成')
            sb.sleep(2)
        # 获取个人信息
        try:
            pass
            # 判断是否已经签到
            already_signed = False
            try:
                if sb.is_element_present('#pper_a66 img[src*="dsu_amupper/images/wb.png"]'):
                    already_signed = True
                    nushen.dbPrint(pluginName, "今日已签到")
            except Exception as e:
                pass
            if False:
                # 今日已完成 设置运行锁
                nushen.setRunBlock(pluginName)
        except Exception as e:
            nushen.dbPrint(pluginName,{str(e)})
            # 使用新的handle_login_required方法处理未登录情况
            if not nushen.handle_login_required(pluginName, sb, pluginUrl):
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
    return '202506300945'