---
title: Build Assimp from Src Code
date: 2016-05-01 00:33:20
tags: Assimp
categories: 框架
---

Draft for Assimp buliding.

------

# Intruduction (from offical site)

> Open Asset Import Library (short name: Assimp) is a portable Open Source library to import
> various well-known 3D model formats in a uniform manner.
> ...
> The most recent version also knows how to export 3d files and is therefore suitable as a
> general-purpose 3D model converter.
> ...
> Written in C++, it is available under a liberal BSD license.
> There is a C API as well as bindings to various other languages, including C#/.net, Python and D.

------

# Feature List

> * Written in portable, ISO-compliant C++
> * Easily configurable and customizable
> * Core interface / API is provided for both C++ and C
> * Command-line interface to perform common operations (i.e. quick file stats, convert models, extract embedded textures) from the shell
> * Imports bones, vertex weights and animations (i.e. skinning, skeletal animations)
> * Loads multiple UV and vertex color channels (current limit is 8)
> * Works well with UNICODE input files
> * Supports complex multi-layer materials
> * Supports embedded textures, both compressed (e.g. PNG) or just raw color data
> * No external dependencies except boost (zlib and irrxml are also needed, but they're included in the repository so you don't need to bother). And there's even a workaround to * compile Assimp without boost - with some minor limitations.
> * Due to its export interface, Assimp serves as general-purpose 3D model converter

The last one is the most import feature for me, and it just in most recent version in github.

------

# Install DX11

## download DX11 SDk

This is the June 2010 DirectX SDK.
http://www.microsoft.com/download/details.aspx?id=6812

## maybe you will see error "S1023"

"S1023" error when you install the DirectX SDK (June 2010)
https://support.microsoft.com/en-us/kb/2728613

## resolution

To resolve this issue, you must uninstall all versions of the Visual C++ 2010 Redistributable before installing the June 2010 DirectX SDK. You may have one or more of the following products installed:

- Microsoft Visual C++ 2010 x86 Redistributable
- Microsoft Visual C++ 2010 x64 Redistributable

You can use Add or Remove Programs in Control Panel to uninstall the products.
Or, you can run the following commands from an administrator command prompt:

```
MsiExec.exe /passive /X{F0C3E5D1-1ADE-321E-8167-68EF0DE699A5}
MsiExec.exe /passive /X{1D8E6291-B0D5-35EC-8441-6616F567A0F7}
```

## install DX SDK again

After uninstalling the Microsoft Visual C++ 2010 Redistributable products,
you may install the June 2010 DirectX SDK.
http://www.microsoft.com/download/details.aspx?id=6812

## install MVC++2010 x86/64 again

After installing the June 2010 DirectX SDK,
you may then reinstall the most current version of the Visual C++ 2010 Redistributable Package.
http://www.microsoft.com/download/details.aspx?id=26999

------

# Clone laster version from github

```shell
git clone https://github.com/assimp/assimp.git
```

------

# Generate MSVC prj(x64) by CMake

x64 is just because now we using python-64bit

```
cd assimp
cmake -G "Visual Studio 14 2015 Win64" CMakeLists.txt
```

- build "ALL_BUILD" by MSVC
- add ./assimp/bin/Release/  to $PATH

------

# Install Python port

```shell
cd ./assimp/port/PyAssimp
python setup.py install

```

------

# Try to run without error

try to run script as bellow without error

```python
from pyassimp import *
```
