# 🚀 Local Knowledge Base - 本地知识库AI助手

> 一个零门槛的本地文档智能问答系统，让普通用户也能轻松搭建个人知识库

## 💡 项目背景

项目灵感源于我配置本地知识库的实际体验。我之前想尝试在Chatbox上配置MCP来关联本地知识库和模型对话，本意是想方便快速了解文件内容。当时跟着教程，整个过程因为涉及代码配置还是花了一点时间。

这个经历让我思考：**如果普通用户想给自己搞这个本地知识库会不会很复杂？**

能不能把这个流程简化呢？做成一个软件包的形式，用户可以在自己电脑里上传自己的文件、和模型对话，很傻瓜化，也不用会什么代码或者MCP，最多给他一个用户手册获取API Key，现在免费Key其实也挺多的。

某天早上6点醒来想到这个想法，那段时间正好在玩Claude Code，就心动不如行动了，直接开聊，从早上一直聊到中午，然后直接在GitHub上上传了项目，算是我作为产品经理的一个MVP。

上传到GitHub主要是因为我本身代码能力还是有上限，肯定有些厉害的程序员能玩出更酷的东西，就分享出来了。**这个经历对我来说也是从想法到落地的一次有意义的尝试。**

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()

## ✨ 核心特性

🎯 **零门槛使用** - 无需配置MCP、编程知识或复杂环境，下载即用  
📁 **Word文档支持** - 专门优化Word文档(.doc, .docx)解析  
🤖 **DeepSeek驱动** - 基于DeepSeek AI模型的智能问答  
💻 **傻瓜式操作** - 图形化界面，只需粘贴API Key即可开始  
🔒 **隐私安全** - 文档完全本地处理，数据不上传云端  
🆓 **完全免费** - 开源项目，仅需免费的DeepSeek API Key

## 📸 软件演示

### 界面展示
![功能演示1](screenshots/demo1.png)
*配置界面：只需粘贴DeepSeek API Key*

![功能演示2](screenshots/demo2.png)
*文件选择：支持本地文件夹选择*

![功能演示3](screenshots/demo3.png)
*智能问答：直接和你的Word文档对话*

> 💡 **使用流程**: 下载exe → 粘贴API Key → 选择文件夹 → 开始对话

## 🚀 快速开始

### 方式一：一键使用（推荐）

1. 下载 [本地知识库.exe](releases/v1.0/本地知识库.exe)
2. 双击运行程序
3. 获取并粘贴DeepSeek API Key
4. 选择包含Word文档的文件夹
5. 开始和你的文档对话！

### 方式二：从源码运行

1. 克隆项目
```bash
git clone https://github.com/qianyangyang-cloud/local-knowledge-base.git
cd local-knowledge-base
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行程序
```bash
python src/local-knowledge-base.py
```

## 🔑 获取免费API Key

1. 访问 [DeepSeek开放平台](https://platform.deepseek.com/)
2. 注册账户（支持手机号注册）
3. 在控制台创建API Key
4. 复制Key到软件中使用

> 💰 **费用说明**: DeepSeek提供免费额度，日常使用完全够用

## 📁 当前支持格式

- **Word文档**: `.doc`, `.docx`

> 🚧 **开发计划**: 欢迎贡献代码支持更多格式（PDF、TXT、Markdown等）

## 🛠️ 技术架构

- **前端**: Python + tkinter（原生GUI）
- **后端**: 本地文档解析 + DeepSeek API
- **打包**: PyInstaller单文件部署
- **支持**: Windows 10/11

## 💡 设计理念

**问题**：现有本地知识库方案对普通用户太复杂  
**解决**：将MCP配置简化为"下载-粘贴Key-选择文件夹"三步  
**目标**：让每个人都能拥有自己的本地AI助手  

## 🤝 开源贡献

这个项目是我从想法到落地的一次尝试，由于个人代码能力有限，特别欢迎：

- 🔧 功能扩展（支持更多文件格式）
- 🎨 界面优化
- 🚀 性能提升
- 📱 跨平台适配

1. Fork这个项目
2. 创建特性分支
3. 提交你的改进
4. 发起Pull Request

## 📄 开源协议

MIT License - 可自由使用、修改和分发

## 🙏 致谢

- **DeepSeek**: 提供强大且免费的AI能力
- **Claude Code**: AI协作开发的强大伙伴
- **开源社区**: 期待大家的贡献和建议

---

**如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！**

有问题可以提Issue，让我们一起让本地知识库更简单易用！