@echo off
echo 检查Python...
where python >nul 2>nul
if %errorlevel%==0 (
    echo Normal,检查需求库...
    python -m pip show requests >nul 2>nul
    if %errorlevel%==0 (
        echo requests库已安装，开始运行脚本(run.py)...
        python run.py
    ) else (
        echo 检测到未安装requests库
        set /p install_pip="是否自动安装requests库(Y/N): "
        if /i "%install_pip%"=="Y" (
            python -m pip install requests
            if %errorlevel%==0 (
                python run.py
            ) else (
                echo requests库安装失败
            )
        ) else (
            echo 已取消安装requests库
        )
    )
) else (
    echo 未检测到Python环境，请下载安装后重新运行脚本
    start https://www.python.org/downloads/
)