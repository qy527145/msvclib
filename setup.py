import os
from setuptools import setup
from setuptools.command.install import install


class CustomInstall(install):
    """自定义安装命令，用于复制批处理文件到安装目录"""

    def run(self):
        # 先执行默认的安装
        install.run(self)

        # 复制批处理文件到安装目录
        self._copy_batch_files()

    def _copy_batch_files(self):
        """创建批处理文件到Scripts目录"""
        if not self.install_scripts:
            return

        scripts_dir = self.install_scripts
        os.makedirs(scripts_dir, exist_ok=True)

        # 创建 msvcinit.bat 和 msvcinit.ps1 文件
        self._create_msvcinit_bat(scripts_dir)

    def _create_msvcinit_bat(self, scripts_dir):
        """创建 msvcinit.bat 和 msvcinit.ps1 文件"""
        # 创建 bat 文件内容 - 使用动态路径查找，带备用方案
        bat_content = """@echo off
setlocal enabledelayedexpansion
echo Initializing MSVC environment...

REM 方法1: 尝试传统的相对路径 (pip install)
set MSVCLIB_PATH=%~dp0..\\Lib\\site-packages\\msvclib
if exist "%MSVCLIB_PATH%\\devcmd.bat" goto :found

REM 方法2: 尝试 uv tool 路径
uv --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "delims=" %%i in ('uv tool dir 2^>nul') do (
        set MSVCLIB_PATH=%%i\\msvclib\\Lib\\site-packages\\msvclib
        if exist "!MSVCLIB_PATH!\\devcmd.bat" goto :found
    )
)

REM 方法3: 使用 Python 动态查找 msvclib 包的安装位置
python -c "import msvclib, os; print(os.path.dirname(msvclib.__file__))" > "%TEMP%\\msvclib_path.txt" 2>nul
if %errorlevel% equ 0 (
    set /p MSVCLIB_PATH=<"%TEMP%\\msvclib_path.txt"
    del "%TEMP%\\msvclib_path.txt"
    if exist "%MSVCLIB_PATH%\\devcmd.bat" goto :found
)

REM 方法4: 在当前脚本目录查找
set MSVCLIB_PATH=%~dp0msvclib
if exist "%MSVCLIB_PATH%\\devcmd.bat" goto :found

echo Error: Cannot find msvclib devcmd.bat in any expected location.
echo Please ensure msvclib is properly installed.
echo Tried locations:
echo   - %~dp0..\\Lib\\site-packages\\msvclib
echo   - uv tool virtual environment
echo   - Python package location (dynamic)
echo   - %~dp0msvclib
exit /b 1

:found
echo Found msvclib at: %MSVCLIB_PATH%
endlocal & set "MSVCLIB_DEVCMD_PATH=%MSVCLIB_PATH%\\devcmd.bat"
call "%MSVCLIB_DEVCMD_PATH%"
set DISTUTILS_USE_SDK=1
echo MSVC environment initialized successfully!
echo You can now use Visual Studio build tools in this command prompt.
"""

        # 创建 PowerShell 脚本内容 - 使用动态路径查找，带备用方案
        ps1_content = """# PowerShell script for MSVC environment initialization
Write-Host "Initializing MSVC environment..." -ForegroundColor Yellow

function Find-MsvcLibPath {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

    # 方法1: 尝试传统的相对路径 (pip install)
    $msvcLibPath = Join-Path $scriptDir "..\\Lib\\site-packages\\msvclib"
    if (Test-Path (Join-Path $msvcLibPath "devcmd.ps1")) {
        return $msvcLibPath
    }

    # 方法2: 尝试 uv tool 路径
    try {
        $uvVersion = uv --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            $uvToolDir = uv tool dir 2>$null
            if ($LASTEXITCODE -eq 0 -and $uvToolDir) {
                $msvcLibPath = Join-Path $uvToolDir "msvclib\\Lib\\site-packages\\msvclib"
                if (Test-Path (Join-Path $msvcLibPath "devcmd.ps1")) {
                    return $msvcLibPath
                }
            }
        }
    } catch {}

    # 方法3: 使用 Python 动态查找 msvclib 包的安装位置
    try {
        $msvcLibPath = python -c "import msvclib, os; print(os.path.dirname(msvclib.__file__))" 2>$null
        if ($LASTEXITCODE -eq 0 -and (Test-Path (Join-Path $msvcLibPath "devcmd.ps1"))) {
            return $msvcLibPath
        }
    } catch {}

    # 方法4: 在当前脚本目录查找
    $msvcLibPath = Join-Path $scriptDir "msvclib"
    if (Test-Path (Join-Path $msvcLibPath "devcmd.ps1")) {
        return $msvcLibPath
    }

    return $null
}

try {
    $msvcLibPath = Find-MsvcLibPath

    if (-not $msvcLibPath) {
        Write-Host "Error: Cannot find msvclib devcmd.ps1 in any expected location." -ForegroundColor Red
        Write-Host "Please ensure msvclib is properly installed." -ForegroundColor Red
        Write-Host "Tried locations:" -ForegroundColor Yellow
        Write-Host "  - Traditional pip install location" -ForegroundColor Yellow
        Write-Host "  - uv tool virtual environment" -ForegroundColor Yellow
        Write-Host "  - Python package location (dynamic)" -ForegroundColor Yellow
        Write-Host "  - Script directory" -ForegroundColor Yellow
        exit 1
    }

    $devcmdPath = Join-Path $msvcLibPath "devcmd.ps1"

    Write-Host "Found msvclib at: $msvcLibPath" -ForegroundColor Cyan

    # Source the PowerShell script
    & $devcmdPath

    # Set DISTUTILS_USE_SDK
    $env:DISTUTILS_USE_SDK = "1"

    Write-Host "MSVC environment initialized successfully!" -ForegroundColor Green
    Write-Host "You can now use Visual Studio build tools in this PowerShell session." -ForegroundColor Cyan
}
catch {
    Write-Host "Error initializing MSVC environment: $_" -ForegroundColor Red
    Write-Host "Please ensure msvclib is properly installed and accessible." -ForegroundColor Red
    exit 1
}
"""

        # 创建 bat 文件
        bat_path = os.path.join(scripts_dir, 'msvcinit.bat')
        try:
            with open(bat_path, 'w', encoding='utf-8') as f:
                f.write(bat_content)
            print(f"成功创建 msvcinit.bat 到 {scripts_dir}")
        except Exception as e:
            print(f"警告：创建 msvcinit.bat 失败: {e}")

        # 创建 PowerShell 脚本
        ps1_path = os.path.join(scripts_dir, 'msvcinit.ps1')
        try:
            with open(ps1_path, 'w', encoding='utf-8') as f:
                f.write(ps1_content)
            print(f"成功创建 msvcinit.ps1 到 {scripts_dir}")
        except Exception as e:
            print(f"警告：创建 msvcinit.ps1 失败: {e}")


def get_package_data():
    """获取包数据文件"""
    package_data = []
    msvclib_dir = os.path.join(os.path.dirname(__file__), 'msvclib')

    if os.path.exists(msvclib_dir):
        for root, dirs, files in os.walk(msvclib_dir):
            for file in files:
                # 获取相对于msvclib目录的路径
                rel_path = os.path.relpath(os.path.join(root, file), msvclib_dir)
                package_data.append(rel_path)
    return package_data


# 读取README文件，处理可能的编码问题
def read_readme():
    """安全地读取README文件"""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    except (FileNotFoundError, UnicodeDecodeError):
        return "Lightweight Microsoft Visual C++ build tools for Python"


setup(
    name="msvclib",
    version="0.2.1",
    description="Lightweight Microsoft Visual C++ build tools for Python",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="wmymz",
    author_email="wmymz@icloud.com",
    url="https://github.com/qy527145/msvclib",
    python_requires=">=3.6",
    packages=['msvclib'],
    package_dir={"": "."},
    package_data={
        "msvclib": get_package_data()
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Compilers",
    ],
    keywords=["msvc", "visual-studio", "build-tools", "compiler", "windows", "python"],
    cmdclass={
        'install': CustomInstall
    },
    zip_safe=False,
)
