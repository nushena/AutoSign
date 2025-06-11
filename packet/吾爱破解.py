import threading
import time
from seleniumbase import SB
from nushen import Nushen

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
    proxyUrl = str(nushen.getProxy())
    nushen.dbPrint(pluginName,f"使用代理 {proxyUrl}")
    with SB(test=True, uc=True, proxy=proxyUrl) as sb:
    # with SB(test=True, uc=True) as sb:
        sb.open(nushen.deafultUrl)
        sb.set_window_size(browserX+nushen.browserX, browserY+nushen.browserY)
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
            sb.sleep(2)
        
        # 获取个人信息
        try:
            userName=sb.get_text('strong.vwmy')
            userCoin=sb.get_text('li.xi1')
            userCoin=userCoin.replace('捐助»', '').strip()
            nushen.dbPrint(pluginName, f"用户名：{userName}，{userCoin}")
            already_signed = False
            try:
                if sb.is_element_present("div#um p img[src*='image/common/wbs.png']"):
                    already_signed = True
                    nushen.dbPrint(pluginName, "今日已签到")
                    # 今日已完成 设置运行锁
                    nushen.setRunBlock(pluginName)
            except:
                pass
        except Exception as e:
            nushen.dbPrint(pluginName,{str(e)})
            # 使用新的handle_login_required方法处理未登录情况
            if not nushen.handle_login_required(pluginName, sb, pluginUrl):
                return
            
        # 任务逻辑
        try:
            if not already_signed:
                sb.open('https://www.52pojie.cn/home.php?mod=task&do=apply&id=2')
                sb.sleep(4)
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
    return '202506111810'