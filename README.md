# 🚀 Local Knowledge Base - 本地知识库AI助手

> 一个基于DeepSeek AI的本地文档智能问答系统，保护隐私的同时享受AI服务

## 💡 创作初衷

早上六点，一个念头突然闪现：现有知识库平台让用户担心隐私问题，尤其是办公场景下上传文件时的数据安全。大家都知道隐私协议更多是保障公司而非用户。

**"如果能做成本地部署包该多好？"** 下载exe，挂个模型key，用户就能在本地和AI对话，完全掌控自己的数据。

三个小时后，这个想法变成了现实。通过Claude Code的协助，从灵感到MVP一气呵成。

现在，我把源代码和产品无偿分享给社区，希望代码厉害的程序员们可以继续发挥创意。**本产品经理的努力就到这里了，接下来交给开源社区！** 🎯

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()

## ✨ 特性

🔒 **隐私安全** - 文档完全本地处理，只有AI对话内容发送给API  
📁 **多格式支持** - 支持 Word、PDF、代码文件、文本等多种格式  
🤖 **智能问答** - 基于DeepSeek AI，理解文档内容并智能回答  
🎯 **简单易用** - 图形化界面，无需技术背景即可使用  
⚡ **快速响应** - 本地索引，秒级文档检索  
🆓 **完全免费** - 开源项目，仅需DeepSeek API费用

## 📹 软件演示

> 📹 **完整演示视频**: [本地知识库demo.mp4](screenshots/本地知识库demo.mp4)

![演示视频](screenshots/本地知识库demo.mp4)

*视频展示了完整的使用流程：配置API Key → 选择文档 → AI智能问答*

## 🚀 快速开始

### 方式一：直接运行（推荐）

1. 下载 [最新发布版本](releases/v1.0/本地知识库.exe)
2. 双击运行 `本地知识库.exe`
3. 配置DeepSeek API Key
4. 选择文档文件夹开始使用

### 方式二：从源码运行

1. 克隆项目
```bash
git clone https://github.com/yourusername/local-knowledge-base.git
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

## 🔑 API Key 获取

1. 访问 [DeepSeek Platform](https://platform.deepseek.com/)
2. 注册并登录账户
3. 创建API Key
4. 在软件中配置使用

## 📁 支持的文件格式

- **文档类型**: `.txt`, `.md`, `.doc`, `.docx`
- **代码文件**: `.py`, `.js`, `.java`, `.cpp`, `.c`, `.html`, `.css`
- **配置文件**: `.json`, `.xml`, `.yaml`, `.yml`, `.ini`, `.cfg`
- **日志文件**: `.log`

## 🛠️ 构建说明

如果你想自己打包exe文件：

```bash
# 安装打包依赖
pip install pyinstaller

# Windows用户可直接运行
scripts/打包程序.bat

# 或者手动打包
pyinstaller build/build.spec
```

## 💡 使用技巧

- 📂 选择包含多个文档的文件夹进行批量分析
- 🎯 提问时越具体，AI回答越准确
- 🔍 支持中英文文档和对话
- 💾 文档内容会被缓存，重复使用更快

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 这个项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [DeepSeek](https://platform.deepseek.com/) - 提供强大的AI能力
- [Claude Code](https://claude.ai/code) - 开发过程中的AI编程助手
- [PyInstaller](https://pyinstaller.org/) - Python打包工具
- [tkinter](https://docs.python.org/3/library/tkinter.html) - GUI框架

**特别感谢** Claude Code 让从想法到产品的实现如此流畅，3小时完成MVP的背后是AI辅助开发的力量！

## 📞 联系方式

如果你觉得这个项目有用，请给个 ⭐ Star 支持一下！

有问题可以提 Issue 或联系开发者。

---

**🌟 如果这个项目对你有帮助，别忘了点个 Star！**