@echo off
REM Typst 编译脚本 - Windows 批处理版本

setlocal enabledelayedexpansion

REM 检查 Typst 是否安装
where typst >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] Typst 未安装
    echo.
    echo 安装方法：
    echo   Windows: winget install --id Typst.Typst
    echo   或访问: https://github.com/typst/typst/releases
    exit /b 1
)

REM 显示版本
for /f "tokens=*" %%i in ('typst --version') do set VERSION=%%i
echo [成功] Typst 已安装: %VERSION%

REM 解析参数
set INPUT_FILE=%1
set OUTPUT_FILE=%2

if "%INPUT_FILE%"=="" (
    echo [错误] 请指定输入文件
    echo.
    echo 用法: %0 ^<输入文件.typ^> [输出文件.pdf]
    echo.
    echo 示例:
    echo   %0 main.typ
    echo   %0 main.typ report.pdf
    exit /b 1
)

if not exist "%INPUT_FILE%" (
    echo [错误] 输入文件不存在: %INPUT_FILE%
    exit /b 1
)

REM 确定输出文件
if "%OUTPUT_FILE%"=="" (
    set OUTPUT_FILE=%INPUT_FILE:.typ=.pdf%
)

REM 执行编译
echo.
echo 编译中: %INPUT_FILE% -^> %OUTPUT_FILE%
echo.

typst compile "%INPUT_FILE%" "%OUTPUT_FILE%"

if %errorlevel% equ 0 (
    echo.
    echo [成功] 编译完成: %OUTPUT_FILE%
    
    REM 显示文件大小
    for %%A in ("%OUTPUT_FILE%") do (
        set SIZE=%%~zA
        set /a SIZE_KB=!SIZE! / 1024
        echo   文件大小: !SIZE_KB! KB
    )
) else (
    echo.
    echo [错误] 编译失败
    exit /b 1
)
