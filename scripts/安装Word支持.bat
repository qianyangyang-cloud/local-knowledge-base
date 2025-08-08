@echo off
chcp 65001
echo ========================================
echo   安装Word文档支持库
echo ========================================
echo.

echo 正在安装python-docx库以支持.docx文件...
pip install python-docx

if %errorlevel% equ 0 (
    echo ✅ python-docx安装成功！
) else (
    echo ❌ python-docx安装失败
)

echo.
echo 正在安装pywin32库以支持.doc文件...
pip install pywin32

if %errorlevel% equ 0 (
    echo ✅ pywin32安装成功！
) else (
    echo ❌ pywin32安装失败
)

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 现在可以支持以下Word文档格式：
echo • .docx文件 (需要python-docx)
echo • .doc文件 (需要pywin32和Microsoft Word)
echo.
echo 现在运行程序即可读取Word文档！
echo.
pause