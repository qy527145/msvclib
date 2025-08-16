# MSVCLib

[![PyPI version](https://badge.fury.io/py/msvclib.svg)](https://badge.fury.io/py/msvclib)
[![Python Support](https://img.shields.io/pypi/pyversions/msvclib.svg)](https://pypi.org/project/msvclib/)
[![License](https://img.shields.io/pypi/l/msvclib.svg)](https://github.com/yourusername/msvclib/blob/main/LICENSE)

[English](#english) | [中文](#中文)

---

## 中文

### 背景

在安装某些 Python 第三方包时，如果仓库中只有源码包且包含 C 语言代码，可能会遇到以下错误：

```
error: microsoft visual c++ 14.0 or greater is required. get it with "microsoft c++ build tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

按照提示安装完整的 Visual Studio 会占用至少 6GB 的磁盘空间，这对于仅需要编译工具的用户来说过于臃肿。

### 解决方案

MSVCLib 基于 [PortableBuildTools](https://github.com/Data-Oriented-House/PortableBuildTools) 项目，提供了一个轻量级的解决方案。它将必要的 Microsoft Visual C++ 构建工具打包成 Python wheel，可通过 pip 轻松安装。

**v0.2.1 更新**：修复了 `uv tool install` 安装方式的路径查找问题，现在完全支持 uv 工具链安装。

### 安装

#### 使用 pip 安装

```bash
pip install msvclib
```

#### 推荐：全局安装或使用 uv

```bash
uv tool install msvclib
```

### 使用方法

当遇到 Microsoft Visual C++ 14.0 相关错误时，只需运行初始化命令：

```bash
msvcinit
```

初始化完成后，即可正常编译需要 C++ 构建工具的 Python 包。

### 优势

- **轻量级**：相比完整的 Visual Studio 安装，占用空间极小
- **便携性**：无需管理员权限，可在任何环境中使用
- **简单易用**：一条命令即可解决编译问题
- **多种安装方式**：支持 pip、uv tool 等多种安装方式

### 从源代码构建

如果你想从源代码构建 MSVCLib，请按照以下步骤：

#### 前置要求

- Python 3.6+
- [uv](https://github.com/astral-sh/uv) 包管理器
- [7-Zip](https://www.7-zip.org/) 压缩工具

#### 构建步骤

1. **下载 MSVC 构建工具**

   使用 [PortableBuildTools](https://github.com/Data-Oriented-House/PortableBuildTools) 下载必要的 MSVC 文件到本地：
   ```bash
   git clone https://github.com/Data-Oriented-House/PortableBuildTools.git
   cd PortableBuildTools
   # 按照 PortableBuildTools 的说明下载 MSVC 工具
   ```

2. **复制文件到 msvclib**

   将下载的 MSVC 文件复制到 msvclib 目录中：
   ```bash
   # 将 PortableBuildTools 下载的文件复制到 msvclib/ 目录
   cp -r path/to/downloaded/msvc/files/* msvclib/
   ```

3. **构建 wheel 包**

   使用 uv 构建 wheel 包：
   ```bash
   uv build --wheel
   ```

4. **重新压缩优化包大小**

   使用 7-Zip 的 Bzip2 算法重新压缩 wheel 包以减小体积：
   ```bash
   # 解压原始 wheel 包
   7z x dist/msvclib-*.whl -o temp_wheel/

   # 使用 Bzip2 算法极限压缩重新打包
   cd temp_wheel/
   7z a -tbzip2 -mx9 ../dist/msvclib-optimized.whl *
   ```

   > **注意**：使用 Bzip2 压缩可以显著减小包大小，且与 pip install 原生兼容。

---

## English

### Background

When installing certain Python third-party packages that contain only source code with C language components, you might encounter this error:

```
error: microsoft visual c++ 14.0 or greater is required. get it with "microsoft c++ build tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

Installing the full Visual Studio as suggested would consume at least 6GB of disk space, which is excessive for users who only need the build tools.

### Solution

MSVCLib is based on the [PortableBuildTools](https://github.com/Data-Oriented-House/PortableBuildTools) project and provides a lightweight solution. It packages the necessary Microsoft Visual C++ build tools into a Python wheel that can be easily installed via pip.

**v0.2.1 Update**: Fixed path finding issues with `uv tool install` installation method, now fully supports uv toolchain installation.

### Installation

#### Install with pip

```bash
pip install msvclib
```

#### Recommended: Global installation or using uv

```bash
uv tool install msvclib
```

### Usage

When encountering Microsoft Visual C++ 14.0 related errors, simply run the initialization command:

```bash
msvcinit
```

After initialization, you can compile Python packages that require C++ build tools without issues.

### Advantages

- **Lightweight**: Minimal disk space usage compared to full Visual Studio installation
- **Portable**: No administrator privileges required, works in any environment
- **Easy to use**: One command solves compilation issues
- **Multiple installation methods**: Supports pip, uv tool, and other installation methods

### Building from Source

If you want to build MSVCLib from source, follow these steps:

#### Prerequisites

- Python 3.6+
- [uv](https://github.com/astral-sh/uv) package manager
- [7-Zip](https://www.7-zip.org/) compression tool

#### Build Steps

1. **Download MSVC Build Tools**

   Use [PortableBuildTools](https://github.com/Data-Oriented-House/PortableBuildTools) to download necessary MSVC files locally:
   ```bash
   git clone https://github.com/Data-Oriented-House/PortableBuildTools.git
   cd PortableBuildTools
   # Follow PortableBuildTools instructions to download MSVC tools
   ```

2. **Copy Files to msvclib**

   Copy the downloaded MSVC files to the msvclib directory:
   ```bash
   # Copy PortableBuildTools downloaded files to msvclib/ directory
   cp -r path/to/downloaded/msvc/files/* msvclib/
   ```

3. **Build Wheel Package**

   Use uv to build the wheel package:
   ```bash
   uv build --wheel
   ```

4. **Recompress to Optimize Package Size**

   Use 7-Zip's Bzip2 algorithm to recompress the wheel package for smaller size:
   ```bash
   # Extract original wheel package
   7z x dist/msvclib-*.whl -o temp_wheel/

   # Repackage with Bzip2 algorithm for maximum compression
   cd temp_wheel/
   7z a -tbzip2 -mx9 ../dist/msvclib-optimized.whl *
   ```

   > **Note**: Using Bzip2 compression can significantly reduce package size while maintaining native pip install compatibility.

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- Based on [PortableBuildTools](https://github.com/Data-Oriented-House/PortableBuildTools)
- Thanks to all contributors who made this project possible