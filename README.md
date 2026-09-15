<div align="center">
  <picture>
    <!-- Dark mode image -->
    <source media="(prefers-color-scheme: dark)" srcset="dark.png">
    <!-- Light mode image (fallback) -->
    <img src="light.png" alt="Description of the image" width="600">
  </picture>
</div>

<p align="center">
  <a href="https://discord.com/users/1131858354642358394" target="_blank">
    <img src="https://img.shields.io/badge/platform-windows-blue?style=for-the-badge" alt="idk" />
  </a>
  <a href="https://instagram.com/actually.alwin" target="_blank">
    <img src="https://img.shields.io/badge/license-mit-yellow?style=for-the-badge" alt="license" />
  </a>
</p>


# OneClean 🧹

> A fast, zero risk terminal utility designed to clean temporary build files, system caches, and junk without breaking active application sessions.

> [!IMPORTANT]
> OneClean is an **open-source hobby project.**
> **The Windows installer script is currently not code signed, so Windows may show a SmartScreen warning** because the application does not have an established publisher reputation.
> **This does not mean the warning should be ignored blindly.**
> If you are uncomfortable running the batch installer, you can inspect the source code and run OneClean directly using the Python instructions below.
> The source code used to build OneClean is available in this repository

---

## ⚡ Features

* **Lightweight:** Lightning fast execution with zero background resource usage
* **Safety Built in:** Automatically skips locked files checks file ages and routes items to the Recycle Bin by default

---

## 🚀 Installation

1. Install the latest release from https://github.com/FakePancak3/oneclean/releases
2. Extract the .zip file in any folder or wherever you want
3. Run install.bat
4. Type ``oneclean`` in command prompt to use oneclean

---

## 🔨 Build from source

If you'd like to build it from the repo instead of downloading from releases:
(Drag ``install.bat`` into /dist after building to add it to PATH)

1. ``git clone https://github.com/FakePancak3/oneclean``
2. ``cd oneclean``
3. ``python -m PyInstaller --onefile --icon=1.ico oneclean.py``
