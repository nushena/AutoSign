from seleniumbase import SB
from nushen import Nushen
from selenium.webdriver.common.by import By

def run():
    pluginBoolean = True
    pluginName = '科学刀-john'
    pluginUrl = 'https://www.kxdao.net/plugin.php?id=ahome_dayquestion:pop'
    browserX=0
    browserY=0
    if not pluginBoolean:
        print(f"{pluginName} 插件未开启")
        return
    nushen = Nushen()
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
    return '202506062208'