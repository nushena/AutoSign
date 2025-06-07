from seleniumbase import SB
from nushen import Nushen
from selenium.webdriver.common.by import By

def run():
    pluginBoolean = True
    pluginName = '吾爱破解'
    pluginUrl = 'https://www.52pojie.cn/home.php?mod=spacecp&ac=credit&showcredit=1'
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
    with SB(test=True, uc=True) as sb:
        sb.open(nushen.deafultUrl)
        sb.set_window_size(browserX|nushen.browserX, browserY|nushen.browserY)
        proxyUrl=nushen.getProxy()
        nushen.dbPrint(pluginName,"使用代理 {proxyUrl}")
        sb.set_wire_proxy(proxyUrl)
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
            userName=sb.get_text('strong.vwmy')
            userCoin=sb.get_text('li.xi1')
            userCoin=userCoin.replace('捐助»', '').strip()
            nushen.dbPrint(pluginName, f"用户名：{userName}，{userCoin}")
            already_signed = False
            if sb.find_elements("div#um p img[src*='image/common/wbs.png']"):
                already_signed = True
                nushen.dbPrint(pluginName, "今日已签到")
                # 今日已完成 设置运行锁
                nushen.setRunBlock(pluginName)
        except Exception as e:
            nushen.dbPrint(pluginName,{str(e)})
            nushen.dbPrint(pluginName, "未能找到用户名元素，可能未登录或页面结构已改变",True)
            return
            
        # 任务逻辑
        try:
            if not already_signed:
                sb.open('https://www.52pojie.cn/home.php?mod=task&do=apply&id=2')
                sb.sleep(2)
                nushen.dbPrint(pluginName,'签到完成')
        except Exception as e:
            nushen.dbPrint(pluginName, f"签到过程出错: {str(e)}")
        
        # 保存cookie
        saveCookieRes = nushen.setCookies(pluginName, sb.get_cookies(), pluginUrl)
        if saveCookieRes:
            nushen.dbPrint(pluginName, "已保存cookie")
        nushen.dbPrint(pluginName, "任务结束",True)

def getVersion():
    # 你要想不更新就可以改成999999999999
    return '202506071737'