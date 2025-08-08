@echo off
chcp 65001
echo ========================================
echo     🚀 本地知识库打包工具
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未检测到Python
    echo 请先安装Python: https://python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python环境正常
echo.

REM 切换到脚本目录
cd /d "%~dp0"

REM 检查PyInstaller
echo 📦 检查PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ❌ PyInstaller安装失败
        pause
        exit /b 1
    )
)

echo ✅ PyInstaller已准备就绪
echo.

REM 清理之前的构建
echo 🧹 清理旧构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo ✅ 清理完成
echo.

echo 🔨 开始打包...
echo 这可能需要几分钟，请耐心等待...
echo.

REM 使用spec文件打包
pyinstaller build.spec --clean --noconfirm

if %errorlevel% neq 0 (
    echo.
    echo ❌ 打包失败！
    echo 可能原因：
    echo 1. 缺少必要的依赖包
    echo 2. 权限不足
    echo 3. 磁盘空间不足
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ 打包成功！
echo.
echo 📁 打包文件位置：
echo    %cd%\dist\本地知识库.exe
echo.

REM 检查文件是否存在
if exist "dist\本地知识库.exe" (
    echo 🎉 可执行文件已生成！
    echo.
    echo 📋 文件信息：
    for %%A in ("dist\本地知识库.exe") do echo    大小: %%~zA 字节
    echo.
    echo 💡 使用说明：
    echo 1. 复制 "dist\本地知识库.exe" 到任何位置
    echo 2. 双击运行即可使用
    echo 3. 无需安装Python，可分发给其他用户
    echo.
    
    set /p choice="是否现在运行测试？(y/n): "
    if /i "%choice%"=="y" (
        echo 🚀 启动应用测试...
        start "" "dist\本地知识库.exe"
    )
) else (
    echo ❌ 找不到生成的exe文件
)

echo.
pause