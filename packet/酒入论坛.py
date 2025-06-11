import threading
import time
from seleniumbase import SB
from nushen import Nushen
from selenium.webdriver.common.by import By
import random
import os

def run():
    pluginBoolean = False
    pluginName = '酒入论坛'
    # pluginUrl = 'https://www.jr37.xyz/home.php?mod=spacecp&ac=credit&showcredit=1'
    pluginUrl = 'https://www.jr37.xyz/'
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
    already_signed=False
    # proxyUrl = str(nushen.getProxy())
    # nushen.dbPrint(pluginName,f"使用代理 {proxyUrl}")
    # with SB(test=True, uc=True, proxy=proxyUrl) as sb:
    with SB(test=True, uc=True) as sb:
        sb.open(nushen.deafultUrl)
        sb.set_window_size(browserX|nushen.browserX, browserY|nushen.browserY)
        sb.open(pluginUrl)
        sb.clear_all_cookies()
        
        # 加载cookie
        # cookies = nushen.getCookie(pluginName, pluginUrl)
        # if cookies:
        #     for cookie in cookies:
        #         try:
        #             sb.add_cookie(cookie)
        #         except Exception:
        #             pass
        #     sb.refresh()
        # 点击登录按钮
        sb.sleep(4)
        sb.click("a[onclick*='showWindow']")
        nushen.dbPrint(pluginName,'尝试登录')
        sb.sleep(6)
        sb.type('input[name="username"]','怒神')
        sb.sleep(2)
        sb.type('input[name="password"]','Wangge1212')
        try:
            # handle_captcha方法处理验证码
            captcha_img_selector = 'img[src*="misc.php"][onclick*="updateseccode"]'
            captcha_input_selector = 'input[name="seccodeverify"]'
            captchaComplete=False
            try:
                for i in range(8):
                    nushen.handle_captcha(sb, captcha_img_selector, captcha_input_selector, pluginName)
                    # 检查验证码是否验证成功
                    sb.click('div.rfm')
                    sb.sleep(6)
                    captcha_verified = sb.is_element_present("span[id^='checkseccodeverify_'] img[src*='static/image/common/check_right.gif']")
                    if captcha_verified:
                        nushen.dbPrint(pluginName, "验证码验证成功")
                        captchaComplete=True
                        break
                    else:
                        nushen.dbPrint(pluginName, "验证码可能未通过验证")
                        sb.click('a[onclick*="updateseccode"]')
                        sb.sleep(4)
            except Exception as e:
                pass
            if not captchaComplete:
                nushen.dbPrint(pluginName,'登录失败',True)
                return
            sb.sleep(4)
            nushen.dbPrint(pluginName,'点击登录')
            sb.click('button[name="loginsubmit"]')
            sb.sleep(5)
        except Exception as e:
            nushen.dbPrint(pluginName, f"处理验证码出错: {str(e)}")     
        nushen.dbPrint(pluginName,'登录结束')
        # 获取个人信息
        try:
            sb.open("https://www.jr37.xyz/home.php?mod=spacecp&ac=credit&showcredit=1")
            sb.sleep(4)
            userName = sb.get_text('strong.vwmy')
            userCoin = sb.get_text('li.xi1')
            nushen.dbPrint(pluginName,f"当前用户: {userName}")
            nushen.dbPrint(pluginName,f"当前酒入币: {userCoin}")
        except Exception as e:
            nushen.dbPrint(pluginName,{str(e)})
            
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
        # saveCookieRes = nushen.setCookies(pluginName, sb.get_cookies(), pluginUrl)
        # if saveCookieRes:
        #     nushen.dbPrint(pluginName, "已保存cookie")
        nushen.dbPrint(pluginName, "任务结束",True)

def getVersion():
    # 你要想不更新就可以改成999999999999
    return '202506111523'