@echo off
chcp 65001
echo ========================================
echo     📦 商业发布包创建工具
echo ========================================
echo.

cd /d "%~dp0"

REM 创建发布目录
set RELEASE_DIR=Local-Knowledge-Base-v1.0-Release
if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
mkdir "%RELEASE_DIR%"

echo 📁 创建发布包结构...

REM 检查exe文件
if not exist "dist\本地知识库.exe" (
    echo ❌ 找不到打包的exe文件
    echo 请先运行 "打包程序.bat" 完成打包
    pause
    exit /b 1
)

REM 复制主程序
echo 📄 复制主程序...
copy "dist\本地知识库.exe" "%RELEASE_DIR%\" >nul

REM 创建用户手册
echo 📚 创建用户手册...
(
echo # 本地知识库 v1.0 使用手册
echo.
echo ## 🎯 产品简介
echo 本地知识库是一款基于AI的文档智能问答软件，帮助用户快速分析和理解本地文档内容。
echo.
echo ## 🚀 快速开始
echo 1. 双击运行 "本地知识库.exe"
echo 2. 在左侧配置DeepSeek API Key
echo 3. 选择文件夹或文件加载文档
echo 4. 在右侧开始AI对话
echo.
echo ## 🔑 API Key获取
echo 1. 访问 https://platform.deepseek.com/
echo 2. 注册并登录账户
echo 3. 在API管理页面创建新的API Key
echo 4. 复制粘贴到软件中使用
echo.
echo ## 📁 支持的文件格式
echo - 文本文件：.txt, .md
echo - 代码文件：.js, .py, .java, .cpp, .c, .html, .css
echo - 配置文件：.json, .xml, .yaml, .yml
echo - 其他文本格式：.ini, .cfg, .log
echo.
echo ## 💡 使用技巧
echo - 选择文件夹时会自动读取其中所有支持的文件
echo - 可以同时选择多个文件进行分析
echo - 问题越具体，AI回答越准确
echo - 支持中英文文档和对话
echo.
echo ## 🔒 隐私保护
echo - 所有文档都在本地处理，不会上传到服务器
echo - 只有AI对话内容会发送给API服务商
echo - 无需联网即可浏览和管理文档
echo.
echo ## 📞 技术支持
echo 如遇问题请联系：support@localknowledge.com
echo.
echo ## 📄 许可证
echo 本软件采用商业许可证，仅授权购买用户使用。
echo 版权所有 © 2025 本地知识库开发团队
) > "%RELEASE_DIR%\使用手册.md"

REM 创建系统要求说明
echo 💻 创建系统要求说明...
(
echo # 系统要求
echo.
echo ## 最低配置
echo - 操作系统：Windows 10 或更高版本
echo - 内存：4GB RAM
echo - 硬盘：至少500MB可用空间
echo - 网络：需要联网获取AI回复
echo.
echo ## 推荐配置
echo - 操作系统：Windows 11
echo - 内存：8GB RAM或更高
echo - 硬盘：1GB可用空间
echo - 网络：稳定的宽带连接
echo.
echo ## 注意事项
echo - 首次运行可能需要Windows防火墙允许
echo - 某些杀毒软件可能误报，请添加信任
echo - 建议在管理员权限下安装和运行
) > "%RELEASE_DIR%\系统要求.md"

REM 创建快速启动脚本
echo 🚀 创建启动脚本...
(
echo @echo off
echo title 本地知识库 v1.0
echo cd /d "%%~dp0"
echo start "" "本地知识库.exe"
) > "%RELEASE_DIR%\启动本地知识库.bat"

REM 创建许可证文件
echo 📜 创建许可证...
(
echo 软件许可协议
echo ================
echo.
echo 本地知识库软件许可协议
echo.
echo 版权所有 (c) 2025 本地知识库开发团队
echo.
echo 1. 本软件仅供已购买许可证的用户使用
echo 2. 禁止未经授权的复制、分发或修改
echo 3. 用户有权在其设备上安装和使用本软件
echo 4. 技术支持和更新服务包含在许可证中
echo 5. 本软件按"现状"提供，不提供任何明示或暗示的保证
echo.
echo 如有疑问请联系：legal@localknowledge.com
) > "%RELEASE_DIR%\LICENSE.txt"

REM 创建版本信息
echo 📋 创建版本信息...
(
echo 本地知识库 v1.0.0
echo 构建日期：%date% %time%
echo.
echo 更新日志：
echo - [新增] 支持DeepSeek AI模型
echo - [新增] 本地文件夹和文件选择功能
echo - [新增] 多种文件格式支持
echo - [新增] 智能文档问答功能
echo - [新增] 现代化用户界面
) > "%RELEASE_DIR%\版本信息.txt"

REM 获取文件信息
for %%A in ("%RELEASE_DIR%\本地知识库.exe") do set FILE_SIZE=%%~zA

echo.
echo ✅ 商业发布包创建完成！
echo.
echo 📦 发布包信息：
echo    位置: %cd%\%RELEASE_DIR%\
echo    主程序大小: %FILE_SIZE% 字节
echo.
echo 📁 包含文件：
echo    ✓ 本地知识库.exe          (主程序)
echo    ✓ 启动本地知识库.bat      (快速启动)
echo    ✓ 使用手册.md             (用户手册)
echo    ✓ 系统要求.md             (系统要求)
echo    ✓ 版本信息.txt            (版本信息)
echo    ✓ LICENSE.txt             (许可协议)
echo.
echo 💼 商业化建议：
echo 1. 可将整个文件夹打包成ZIP分发
echo 2. 建议售价：¥99-299 (根据目标用户群体调整)
echo 3. 可在软件市场、官网或企业直销
echo 4. 考虑提供试用版 (功能限制或时间限制)
echo.

set /p choice="是否现在测试发布版本？(y/n): "
if /i "%choice%"=="y" (
    echo 🚀 启动发布版本测试...
    start "" "%RELEASE_DIR%\本地知识库.exe"
)

echo.
echo 🎉 发布包已准备就绪，可以开始销售了！
pause