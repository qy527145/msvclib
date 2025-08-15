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
        # 创建 bat 文件内容
        bat_content = """@echo off
echo Initializing MSVC environment...
call %~dp0\\..\\Lib\\site-packages\\msvclib\\devcmd.bat
set DISTUTILS_USE_SDK=1
echo MSVC environment initialized successfully!
echo You can now use Visual Studio build tools in this command prompt.
"""

        # 创建 PowerShell 脚本内容
        ps1_content = """# PowerShell script for MSVC environment initialization
Write-Host "Initializing MSVC environment..." -ForegroundColor Yellow

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$devcmdPath = Join-Path $scriptDir "..\\Lib\\site-packages\\msvclib\\devcmd.ps1"

# Source the PowerShell script
& $devcmdPath

# Set DISTUTILS_USE_SDK
$env:DISTUTILS_USE_SDK = "1"

Write-Host "MSVC environment initialized successfully!" -ForegroundColor Green
Write-Host "You can now use Visual Studio build tools in this PowerShell session." -ForegroundColor Cyan
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
    version="0.1.0",
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
