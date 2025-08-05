import threading
import time
from seleniumbase import SB
from nushen import Nushen
from selenium.webdriver.common.by import By

def run():
    pluginBoolean = True
    pluginName = '清风货源'
    pluginUrl = 'https://296a.my/user/qiandao.php'
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
    proxyUrl = str(nushen.getProxy('210100'))
    nushen.dbPrint(pluginName,f"使用代理 {proxyUrl}")
    with SB(test=True, uc=True, proxy=proxyUrl) as sb:
    # with SB(test=True, uc=True) as sb:
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
            sb.open(pluginUrl)
            sb.sleep(4)
        # 获取个人信息
        try:
            userBalance=sb.get_text("span#rewardcount")
            nushen.dbPrint(pluginName, f"账户余额: {userBalance}")
            # 判断是否已经签到
            already_signed = False
            try:
                if '今天已签到' in sb.get_text('button[id="qiandao"] span b'):
                    already_signed = True
                    nushen.dbPrint(pluginName, "今日已签到")
            except Exception as e:
                pass
            if already_signed:
                # 今日已完成 设置运行锁
                nushen.setRunBlock(pluginName)
        except Exception as e:
            nushen.dbPrint(pluginName,{str(e)})
            # 使用新的handle_login_required方法处理未登录情况
            if not nushen.handle_login_required(pluginName, sb, pluginUrl):
                return
            
        # 任务逻辑
        try:
            if not already_signed:
                sb.click('button[id="qiandao"]')
                sb.sleep(10)
                checkInBonus=sb.get_text('div.layui-layer-content')
                nushen.dbPrint(pluginName,checkInBonus)
        except Exception as e:
            nushen.dbPrint(pluginName, f"签到过程出错: {str(e)}")
        
        # 保存cookie
        saveCookieRes = nushen.setCookies(pluginName, sb.get_cookies(), pluginUrl)
        if saveCookieRes:
            nushen.dbPrint(pluginName, "已保存cookie")
        nushen.dbPrint(pluginName, "任务结束",True)

def getVersion():
    # 你要想不更新就可以改成999999999999
    return '202508051419'