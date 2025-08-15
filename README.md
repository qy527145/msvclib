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

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- Based on [PortableBuildTools](https://github.com/Data-Oriented-House/PortableBuildTools)
- Thanks to all contributors who made this project possible