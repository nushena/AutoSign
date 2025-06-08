import threading
import time
from seleniumbase import SB
from nushen import Nushen
from selenium.webdriver.common.by import By

def run():
    pluginBoolean = True
    pluginName = '科学刀'
    pluginUrl = 'https://www.kxdao.net/plugin.php?id=ahome_dayquestion:pop'
    browserX=0
    browserY=0
    if not pluginBoolean:
        print(f"{pluginName} 插件未开启")
        return
    nushen = Nushen()
    # proxyUrl=nushen.getProxy()
    # nushen.dbPrint(pluginName,"使用代理 {proxyUrl}")
    # sb.set_wire_proxy(proxyUrl)
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
            username = sb.get_text("strong.vwmy a")
            nushen.dbPrint(pluginName, f"当前用户名: {username}")
            userGroup = sb.get_text("a#g_upmine")
            nushen.dbPrint(pluginName, f"当前{userGroup}")
            userPoints = sb.get_text("a#extcreditmenu")
            nushen.dbPrint(pluginName, f"当前{userPoints}")
            # 判断是否已经答题
            already_answered = False
            try:
                if sb.find_elements('#um p a img[src*="ahome_dayquestion/images/end.gif"]',timeout=3):
                    already_answered = True
                    nushen.dbPrint(pluginName, "今日已答题")
            except:
                pass
            # 判断是否已经签到
            already_signed = False
            try:
                if sb.find_elements('#pper_a img[src*="dsu_amupper/images/wb.png"]', timeout=3):
                    already_signed = True
                    nushen.dbPrint(pluginName, "今日已签到")
            except:
                pass
            if (already_answered and already_signed):
                # 今日已完成 设置运行锁
                nushen.setRunBlock(pluginName)
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
            
        # 签到逻辑
        try:
            if not already_signed:
                sb.click('#pper_a')
                nushen.dbPrint(pluginName, "点击签到按钮")
                sb.sleep(5)
        except Exception as e:
            nushen.dbPrint(pluginName, f"签到过程出错: {str(e)}",True)
            
        # 答题逻辑
        try:
            if not already_answered:
                sb.refresh()
                question = sb.get_text('#myform div span font',timeout=5)
                nushen.dbPrint(pluginName, f"当前问题: {question}")
                # 获取所有答案选项
                answer_elements = sb.find_elements('div.qs_option')
                
                # 遍历答案选项
                for i, answer_element in enumerate(answer_elements, 1):
                    # 使用WebElement的text属性获取文本
                    answer_text = answer_element.text.strip()
                    nushen.dbPrint(pluginName, f"答案 {i}: {answer_text}")
                    
                    # 检查是否是特定答案文本
                    click_messages = ['好的', '明白', '知道了', '明白了']
                    if any(msg == answer_text for msg in click_messages):
                        # 使用WebElement的find_element方法找到输入元素并点击
                        input_element = answer_element.find_element(By.TAG_NAME, 'input')
                        input_element.click()
                        correctAnswer = answer_text
                nushen.dbPrint(pluginName, f"点击 {correctAnswer}")
                sb.sleep(2)
                # 点击提交按钮
                sb.click('button[name="submit"][value="true"]')
                nushen.dbPrint(pluginName, "点击答题提交按钮")  
                sb.sleep(6)   
        except Exception as e:
            nushen.dbPrint(pluginName, f"获取问题或答题过程出错: {str(e)}",True)
            return
        
        # 保存cookie
        saveCookieRes = nushen.setCookies(pluginName, sb.get_cookies(), pluginUrl)
        if saveCookieRes:
            nushen.dbPrint(pluginName, "已保存cookie")
        
        nushen.dbPrint(pluginName, "任务结束",True)
    
def getVersion():
    # 你要想不更新就可以改成999999999999
    return '202506082246'