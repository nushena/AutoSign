# 自动签到系统

一个支持多网站自动签到的工具，基于插件化设计，可以轻松扩展支持更多网站。

## 快速开始

1. 只需下载 `run.py` 文件或克隆整个仓库
2. 直接运行 `run.py`，系统会自动安装所需依赖并下载其他必要文件：

```bash
python run.py
```

## 功能特点

- **插件化设计**：通过独立的插件文件支持不同网站的签到
- **自动更新**：从 GitHub 仓库获取最新版本的插件和核心文件
- **Cookie 管理**：自动保存和加载各网站的 Cookie 信息
- **运行锁机制**：防止同一天内重复签到
- **ChatGPT 集成**：支持调用 ChatGPT API 处理复杂场景
- **QQ 推送通知**：使用 NapCat 框架推送签到结果到 QQ 群或好友
- **代理支持**：支持通过代理服务器进行签到，提高成功率
- **验证码处理**：自动保存验证码图片，支持手动或自动识别
- **智能环境管理**：自动创建虚拟环境并安装依赖

## 安装方法

### 方法一：快速安装（推荐）

只需下载 `run.py` 文件并运行，系统会自动完成以下操作：

1. 安装所需的依赖库
2. 下载最新版本的核心文件和插件
3. 创建必要的配置文件

### 方法二：手动安装

1. 克隆或下载本项目到本地
2. 安装依赖项：

```bash
pip install -r requirements.txt
```

## 配置说明

首次运行程序会自动创建`.env`文件，需要手动编辑并填入以下信息：

```
# OpenAI API配置
OPENAI_API_KEY=<你的OpenAI API密钥>
OPENAI_BASE_URL=<OpenAI API代理网址，可选>

# QQ推送配置（基于NapCat框架）
GROUP_MSG_API_URL=<QQ群消息API地址>
GROUP_ID=<QQ群号>
API_TOKEN=<API访问令牌>

# 代理设置
PROXY_URL=<代理服务器地址，可选>
```

### 代理配置详细说明

本项目支持使用代理服务进行签到，代理URL格式示例：
```
PROXY_URL=https://service.xxxx.com/xxxxx
```

返回代理IP txt模式

配置代理后，签到操作将通过代理服务器进行，提高成功率和稳定性。

### QQ 推送配置说明

本项目使用 [NapCat](https://github.com/NapNeko/NapCatQQ) 框架实现 QQ 消息推送功能。NapCat 是一个基于 NTQQ 的现代化 Bot 协议框架，可以实现 QQ 消息的发送和接收。

配置步骤：

1. 安装并配置 NapCat（可参考[NapCat-Docker](https://github.com/NapNeko/NapCat-Docker)快速部署）
2. 获取 NapCat 的 API 地址和访问令牌
3. 在 `.env` 文件中配置以下参数：
   - `GROUP_MSG_API_URL`：NapCat 的群消息发送 API 地址，通常格式为 `http://<NapCat服务器IP>:<端口>/send_group_msg`
   - `GROUP_ID`：接收通知的 QQ 群号
   - `API_TOKEN`：NapCat API 的访问令牌

配置完成后，签到系统会自动将签到结果推送到指定的 QQ 群。

## 使用方法

运行主程序：

```bash
python run.py
```

程序会自动执行以下操作：

1. 检查环境并自动安装所需依赖
2. 从 GitHub 获取最新版本的插件和核心文件
3. 运行所有启用的签到插件

首次运行时，系统会自动创建所需的目录结构和配置文件，无需手动设置。

## 插件开发

可以参考`packet/插件例子.py`创建新的签到插件。插件基本结构：

```python
from seleniumbase import SB
from nushen import Nushen

def run():
    # 插件配置
    pluginBoolean = True  # 设置为True启用插件
    pluginName = '网站名称'
    pluginUrl = 'https://example.com/'

    # 初始化Nushen实例
    nushen = Nushen()

    # 检查运行锁（防止同一天重复运行）
    if nushen.getRunBlock(pluginName):
        nushen.dbPrint(pluginName+'运行锁', "今日任务已完成", True)
        return

    # 使用SeleniumBase进行自动化操作
    with SB(test=True, uc=True) as sb:
        # 自动化操作代码
        # ...

        # 保存Cookie
        nushen.setCookies(pluginName, sb.get_cookies(), pluginUrl)

        # 设置运行锁（标记今日已完成）
        nushen.setRunBlock(pluginName)

        # 发送通知
        nushen.dbPrint(pluginName, "任务完成", True)

def getVersion():
    # 插件版本号，用于自动更新
    return '202508051419'  # 格式：YYYYMMDDHHMM
```

## 项目结构

```
├── run.py                 # 主程序入口
├── nushen.py              # 核心功能库
├── chatgpt.py             # ChatGPT API调用
├── requirements.txt       # 依赖项列表
├── update.json            # 更新配置文件
├── .env                   # 环境配置文件（需手动创建）
├── packet/                # 插件目录
│   ├── 插件例子.py        # 插件示例
│   └── ...                # 其他插件
├── cookies/               # Cookie存储目录
├── runblock/              # 运行锁目录
├── captcha_images/        # 验证码图片存储目录
└── downloaded_files/      # 驱动下载文件存储目录
```

## 更新说明

程序支持自动更新，会从 GitHub 仓库获取最新版本的插件和核心文件。

**GitHub仓库地址：** https://github.com/nushena/AutoSign

自动更新机制：
1. 程序启动时会测试多个GitHub代理的速度，选择最快的一个进行更新
2. 比较本地和远程版本号（格式：YYYYMMDDHHMM）
3. 自动下载需要更新的文件

如需禁用自动更新，可以修改相应文件中的`getVersion()`函数：

```python
def getVersion():
    # 修改为 999999999999 可以禁用自动更新
    return '999999999999'
```

## 注意事项

- 首次运行时需要手动配置`.env`文件
- 部分网站可能需要先手动登录一次，以保存 Cookie
- 如遇到签到失败，可以检查网站是否更改了页面结构
- QQ 推送功能需要正确配置 NapCat 相关参数才能使用

## 问题排查

1. **依赖项安装失败**：尝试手动安装各个依赖项
2. **无法连接 GitHub**：检查网络连接或代理设置
3. **签到失败**：检查 Cookie 是否有效，可能需要重新手动登录
4. **插件不执行**：确认插件中的`pluginBoolean`设置为`True`
5. **QQ 推送失败**：检查 NapCat 服务是否正常运行，以及`.env`中的配置是否正确
6. **代理连接失败**：检查`.env`中的`PROXY_URL`配置是否正确，确保API密钥有效
7. **验证码识别失败**：检查`captcha_images`目录中的验证码图片，识别是否正确

## 支持的网站

当前支持的网站签到：

1. **吾爱破解** - 吾爱破解论坛每日签到
2. **清风货源** - 清风货源网站签到
3. **科学刀** - 科学刀网站签到
4. **酒入论坛** - 酒入论坛每日签到

## 贡献指南

欢迎提交新的签到插件或改进现有插件：

1. 参考 `packet/插件例子.py` 创建新插件
2. 确保插件包含完整的错误处理
3. 提交Pull Request到GitHub仓库

## 许可证

本项目采用MIT许可证，详情请参阅LICENSE文件。
