# 跨平台数据迁移设计

## 🌍 支持的平台

### 桌面端
- ✅ **Windows** (7/10/11)
- ✅ **macOS** (10.15+)
- ✅ **Linux** (Ubuntu, Debian, Fedora, Arch)

### 移动端（未来）
- ⏳ **Android** (9.0+)
- ⏳ **iOS** (13.0+)

---

## 🔧 跨平台技术方案

### 1. 数据格式统一

#### 文件路径处理
```python
# 使用 pathlib 处理跨平台路径
from pathlib import Path

# 自动适配 Windows \ 和 Unix /
data_dir = Path.home() / '.mindflow' / 'data'
```

#### 数据库
```python
# SQLite 天然跨平台
# 导出时使用相对路径，导入时转换为目标平台路径
```

#### 配置文件
```python
# 统一使用 JSON，UTF-8 编码
config = {
    'data_dir': str(Path.home() / '.mindflow'),  # 自动适配
    'encoding': 'utf-8'
}
```

### 2. 平台检测

```python
# src/core/platform_utils.py

import platform
import sys

class PlatformInfo:
    @staticmethod
    def get_platform() -> str:
        """获取当前平台"""
        system = platform.system().lower()
        if system == 'darwin':
            return 'macos'
        elif system == 'windows':
            return 'windows'
        elif system == 'linux':
            return 'linux'
        elif system == 'android':  # 需要额外检测
            return 'android'
        elif system == 'ios':
            return 'ios'
        return 'unknown'
    
    @staticmethod
    def get_data_dir() -> Path:
        """获取平台特定的数据目录"""
        platform_type = PlatformInfo.get_platform()
        
        if platform_type == 'windows':
            # C:\Users\<user>\AppData\Local\Mindflow
            return Path(os.getenv('LOCALAPPDATA')) / 'Mindflow'
        
        elif platform_type == 'macos':
            # ~/Library/Application Support/Mindflow
            return Path.home() / 'Library' / 'Application Support' / 'Mindflow'
        
        elif platform_type == 'linux':
            # ~/.local/share/mindflow
            return Path.home() / '.local' / 'share' / 'mindflow'
        
        elif platform_type == 'android':
            # /data/data/com.mindflow/files
            return Path('/data/data/com.mindflow/files')
        
        elif platform_type == 'ios':
            # Documents directory
            return Path.home() / 'Documents' / 'Mindflow'
        
        else:
            return Path.home() / '.mindflow'
```

---

## 📦 跨平台导出格式

### .mindflow 文件结构（平台无关）

```
backup.mindflow (ZIP)
├── metadata.json          # 元数据
│   ├── version: "1.0"
│   ├── export_platform: "windows"
│   ├── export_time: "2026-01-15T10:00:00"
│   ├── mindflow_version: "1.0.0"
│   └── checksum: "sha256..."
│
├── database.db           # SQLite（跨平台）
├── config.json          # 配置（使用相对路径）
│
├── extensions/          # Extension 数据
│   ├── knowledge_base/
│   ├── life_logger/
│   └── ...
│
├── vectors/             # 向量数据库
│   └── chroma/
│
└── attachments/         # 文件附件
    ├── images/
    ├── documents/
    └── ...
```

### 路径转换规则

```python
# 导出时：转换为相对路径
def export_path(absolute_path: Path) -> str:
    """将绝对路径转换为相对路径"""
    data_dir = PlatformInfo.get_data_dir()
    try:
        relative = absolute_path.relative_to(data_dir)
        return str(relative).replace('\\', '/')  # 统一使用 /
    except ValueError:
        # 如果不在数据目录下，保存完整路径
        return str(absolute_path)

# 导入时：转换为目标平台路径
def import_path(relative_path: str) -> Path:
    """将相对路径转换为目标平台的绝对路径"""
    data_dir = PlatformInfo.get_data_dir()
    return data_dir / relative_path
```

---

## 🔄 跨平台同步方案

### 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **本地导出/导入** | 简单、可靠、离线 | 手动操作 | 偶尔换设备 |
| **云端同步** | 自动、实时 | 需要网络、复杂 | 多设备日常使用 |
| **局域网同步** | 快速、隐私 | 需要同网络 | 家庭/办公室 |

### 推荐方案

#### Phase 1: 本地导出/导入（所有平台）
```bash
# 在旧设备（Windows）
mindflow export --output backup.mindflow

# 复制文件到新设备（macOS）
# 通过 U盘、网盘、邮件等

# 在新设备（macOS）
mindflow import --file backup.mindflow
```

#### Phase 5: 云端同步（桌面端优先）
```python
# 自动同步到云端
mindflow sync --enable

# 支持的云存储
- WebDAV（自建，推荐）
- OneDrive（Windows 优先）
- iCloud（macOS 优先）
- Google Drive（跨平台）
- Dropbox（跨平台）
```

---

## 📱 移动端特殊考虑

### Android

#### 数据存储位置
```
/data/data/com.mindflow/files/  # 应用私有目录
或
/sdcard/Android/data/com.mindflow/  # 外部存储
```

#### 导出方式
1. 导出到本地存储
2. 分享到其他应用（邮件、云盘）
3. 通过 USB 传输

#### UI 适配
- 使用 Kivy 或 React Native
- 触摸优化界面
- 文件选择器

### iOS

#### 数据存储位置
```
~/Documents/Mindflow/  # 文档目录
或
~/Library/Application Support/Mindflow/  # 应用支持目录
```

#### 导出方式
1. 通过 Files 应用
2. AirDrop 分享
3. iCloud Drive 同步

#### UI 适配
- SwiftUI 或 React Native
- iOS 设计规范
- 文件共享扩展

---

## 🔐 跨平台安全

### 加密方案（平台无关）

```python
# 使用 cryptography 库（跨平台）
from cryptography.fernet import Fernet

def encrypt_export(data: bytes, password: str) -> bytes:
    """加密导出数据"""
    # 1. 从密码派生密钥（PBKDF2）
    key = derive_key(password)
    
    # 2. 加密数据
    f = Fernet(key)
    encrypted = f.encrypt(data)
    
    return encrypted

def decrypt_import(encrypted: bytes, password: str) -> bytes:
    """解密导入数据"""
    key = derive_key(password)
    f = Fernet(key)
    return f.decrypt(encrypted)
```

### 密钥存储

| 平台 | 密钥存储方案 |
|------|-------------|
| Windows | Windows Credential Manager |
| macOS | Keychain |
| Linux | Secret Service API (gnome-keyring) |
| Android | Android Keystore |
| iOS | iOS Keychain |

```python
# 使用 keyring 库（跨平台）
import keyring

# 存储 API Key
keyring.set_password('mindflow', 'claude_api_key', 'sk-xxx')

# 读取 API Key
api_key = keyring.get_password('mindflow', 'claude_api_key')
```

---

## 🚀 实现优先级

### Phase 1: 桌面端（Windows、macOS、Linux）
- [x] 跨平台路径处理
- [x] 本地导出/导入
- [x] 平台检测
- [x] 数据目录适配

### Phase 3: 云端同步（桌面端）
- [ ] WebDAV 同步
- [ ] OneDrive 集成
- [ ] iCloud 集成
- [ ] Google Drive 集成

### Phase 6: 移动端（Android、iOS）
- [ ] Android 应用
- [ ] iOS 应用
- [ ] 移动端 UI
- [ ] 移动端同步

---

## 📋 跨平台测试清单

### 导出测试
- [ ] Windows → Windows
- [ ] Windows → macOS
- [ ] Windows → Linux
- [ ] macOS → Windows
- [ ] macOS → Linux
- [ ] Linux → Windows
- [ ] Linux → macOS

### 路径测试
- [ ] 中文路径
- [ ] 空格路径
- [ ] 特殊字符路径
- [ ] 长路径（Windows 260 字符限制）

### 编码测试
- [ ] UTF-8 文件名
- [ ] 中文文件名
- [ ] Emoji 文件名

---

## 💡 用户指南

### 跨平台迁移步骤

#### 场景 1: Windows → macOS

```bash
# 1. 在 Windows 上导出
mindflow export --output C:\Users\<user>\Desktop\backup.mindflow

# 2. 复制文件到 macOS（通过 U盘、网盘等）

# 3. 在 macOS 上安装 Mindflow
brew install mindflow  # 或下载安装包

# 4. 导入数据
mindflow import --file ~/Desktop/backup.mindflow

# 5. 验证数据
mindflow verify
```

#### 场景 2: 多设备同步（云端）

```bash
# 1. 在主设备上启用同步
mindflow sync --enable --provider webdav --url https://your-server.com/dav

# 2. 在其他设备上登录同一账号
mindflow sync --login

# 3. 自动同步
# 数据会自动在所有设备间同步
```

---

## 🎯 技术栈更新

### 跨平台依赖

```python
# requirements.txt

# 跨平台路径
pathlib  # Python 标准库

# 平台检测
platform  # Python 标准库

# 密钥存储
keyring>=24.0.0

# 加密
cryptography>=41.0.0

# 移动端（可选）
kivy>=2.2.0  # Android/iOS UI
```

### 桌面应用打包

```bash
# Windows
pyinstaller --onefile mindflow.py

# macOS
py2app

# Linux
pyinstaller --onefile mindflow.py
# 或打包为 .deb, .rpm, AppImage
```

---

## ✅ 更新总结

**新增支持**:
1. ✅ Windows、macOS、Linux 完整支持
2. ⏳ Android、iOS 未来支持
3. ✅ 跨平台路径处理
4. ✅ 平台特定数据目录
5. ✅ 跨平台密钥存储
6. ✅ 跨平台加密方案

**文件更新**:
- `docs/DATA_MIGRATION.md` - 原文档
- `docs/CROSS_PLATFORM.md` - 本文档（跨平台详细设计）

**优先级**:
- Phase 1: 桌面端（Windows、macOS、Linux）
- Phase 6: 移动端（Android、iOS）
