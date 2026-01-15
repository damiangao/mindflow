# 数据迁移和多设备支持设计

## 🎯 需求

用户更换设备时需要能够：
1. 导出所有数据
2. 在新设备上导入数据
3. 保持数据完整性
4. （可选）多设备同步

---

## 📦 数据迁移方案

### 方案 1: 本地导出/导入（MVP）

#### 导出功能
```python
# 导出所有数据为单个文件
mindflow export --output backup.mindflow

# 导出内容：
# - 数据库（SQLite）
# - 用户配置
# - Extension 配置
# - 向量数据库
# - 文件附件
```

**文件格式**: `.mindflow` (实际是 ZIP 压缩包)
```
backup.mindflow/
├── database.db           # SQLite 数据库
├── config.json          # 系统配置
├── extensions/          # Extension 配置
├── vectors/             # 向量数据库
└── attachments/         # 文件附件
```

#### 导入功能
```python
# 在新设备上导入
mindflow import --file backup.mindflow

# 导入流程：
# 1. 验证文件完整性
# 2. 解压到临时目录
# 3. 恢复数据库
# 4. 恢复配置
# 5. 重建索引
```

### 方案 2: 云端同步（Phase 5+）

#### 同步策略
- **增量同步**: 只同步变更的数据
- **冲突解决**: 最后写入优先 + 冲突标记
- **选择性同步**: 用户可选择同步哪些数据

#### 支持的云存储
- WebDAV（自建）
- OneDrive
- Google Drive
- Dropbox
- S3 兼容存储

---

## 🗄️ 数据库设计更新

### 新增表：数据同步

```sql
-- 设备信息表
CREATE TABLE devices (
    id TEXT PRIMARY KEY,
    device_name TEXT NOT NULL,
    device_type TEXT,  -- desktop, mobile
    last_sync_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 同步记录表
CREATE TABLE sync_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    table_name TEXT,
    record_id TEXT,
    operation TEXT,  -- create, update, delete
    sync_at TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(id)
);

-- 数据版本表（用于冲突检测）
CREATE TABLE data_versions (
    table_name TEXT,
    record_id TEXT,
    version INTEGER,
    updated_at TIMESTAMP,
    device_id TEXT,
    PRIMARY KEY (table_name, record_id)
);
```

---

## 🔧 实现方案

### Phase 1: 本地导出/导入（MVP）

#### 1. 导出模块
```python
# src/core/data_export.py

class DataExporter:
    def export_all(self, output_path: str):
        """导出所有数据"""
        with zipfile.ZipFile(output_path, 'w') as zf:
            # 1. 导出数据库
            self._export_database(zf)
            
            # 2. 导出配置
            self._export_config(zf)
            
            # 3. 导出 Extension 数据
            self._export_extensions(zf)
            
            # 4. 导出向量数据库
            self._export_vectors(zf)
            
            # 5. 导出附件
            self._export_attachments(zf)
            
            # 6. 生成元数据
            self._export_metadata(zf)
    
    def _export_metadata(self, zf):
        """导出元数据"""
        metadata = {
            'version': '1.0',
            'export_time': datetime.now().isoformat(),
            'device_id': self.get_device_id(),
            'mindflow_version': get_version(),
            'checksum': self.calculate_checksum()
        }
        zf.writestr('metadata.json', json.dumps(metadata))
```

#### 2. 导入模块
```python
# src/core/data_import.py

class DataImporter:
    def import_all(self, file_path: str):
        """导入所有数据"""
        with zipfile.ZipFile(file_path, 'r') as zf:
            # 1. 验证元数据
            self._validate_metadata(zf)
            
            # 2. 备份当前数据
            self._backup_current_data()
            
            # 3. 导入数据库
            self._import_database(zf)
            
            # 4. 导入配置
            self._import_config(zf)
            
            # 5. 导入 Extension 数据
            self._import_extensions(zf)
            
            # 6. 导入向量数据库
            self._import_vectors(zf)
            
            # 7. 导入附件
            self._import_attachments(zf)
            
            # 8. 重建索引
            self._rebuild_indexes()
```

#### 3. UI 集成
```python
# Gradio UI
with gr.Tab("数据管理"):
    with gr.Row():
        export_btn = gr.Button("导出数据")
        import_btn = gr.Button("导入数据")
    
    export_file = gr.File(label="导出文件")
    import_file = gr.File(label="选择导入文件")
    
    status = gr.Textbox(label="状态")
```

### Phase 5: 云端同步（可选）

#### 1. 同步引擎
```python
# src/core/sync_engine.py

class SyncEngine:
    def __init__(self, storage_provider):
        self.provider = storage_provider
        self.device_id = self.get_device_id()
    
    def sync(self):
        """执行同步"""
        # 1. 获取本地变更
        local_changes = self.get_local_changes()
        
        # 2. 获取远程变更
        remote_changes = self.get_remote_changes()
        
        # 3. 检测冲突
        conflicts = self.detect_conflicts(local_changes, remote_changes)
        
        # 4. 解决冲突
        resolved = self.resolve_conflicts(conflicts)
        
        # 5. 应用变更
        self.apply_changes(resolved)
        
        # 6. 上传本地变更
        self.upload_changes(local_changes)
```

#### 2. 存储提供商抽象
```python
# src/core/storage_provider.py

class StorageProvider(ABC):
    @abstractmethod
    def upload(self, local_path: str, remote_path: str):
        pass
    
    @abstractmethod
    def download(self, remote_path: str, local_path: str):
        pass
    
    @abstractmethod
    def list_files(self, remote_dir: str) -> List[str]:
        pass

class WebDAVProvider(StorageProvider):
    """WebDAV 实现"""
    pass

class OneDriveProvider(StorageProvider):
    """OneDrive 实现"""
    pass
```

---

## 📋 开发计划更新

### Phase 1 新增任务
- [ ] 实现数据导出功能
- [ ] 实现数据导入功能
- [ ] 添加数据完整性校验
- [ ] UI 集成导出/导入按钮

### Phase 5 新增任务（可选）
- [ ] 实现同步引擎
- [ ] 实现 WebDAV 存储提供商
- [ ] 实现冲突检测和解决
- [ ] 添加同步设置界面
- [ ] 实现选择性同步

---

## 🔐 安全考虑

### 1. 数据加密
```python
# 导出时加密
def export_encrypted(output_path: str, password: str):
    # 1. 导出数据
    temp_file = export_all()
    
    # 2. 加密
    encrypted = encrypt_file(temp_file, password)
    
    # 3. 保存
    save(encrypted, output_path)
```

### 2. 敏感数据处理
- API Keys 不导出（需要在新设备重新配置）
- 或使用密码加密后导出

---

## 📊 用户体验

### 导出流程
```
1. 用户点击"导出数据"
2. 选择导出位置
3. （可选）设置加密密码
4. 显示进度条
5. 完成后提示文件位置
```

### 导入流程
```
1. 用户点击"导入数据"
2. 选择 .mindflow 文件
3. （如果加密）输入密码
4. 显示导入预览
5. 确认导入
6. 显示进度条
7. 完成后重启应用
```

---

## 🎯 MVP 优先级

### 必须实现（Phase 1）
- ✅ 本地导出功能
- ✅ 本地导入功能
- ✅ 数据完整性校验
- ✅ UI 集成

### 可选实现（Phase 5+）
- ⏳ 云端同步
- ⏳ 多设备管理
- ⏳ 增量同步
- ⏳ 冲突解决

---

## 📝 使用示例

### CLI 命令
```bash
# 导出数据
mindflow export --output ~/backup.mindflow

# 导出并加密
mindflow export --output ~/backup.mindflow --encrypt

# 导入数据
mindflow import --file ~/backup.mindflow

# 查看导出文件信息
mindflow info --file ~/backup.mindflow
```

### Python API
```python
from mindflow.core import DataExporter, DataImporter

# 导出
exporter = DataExporter()
exporter.export_all('backup.mindflow')

# 导入
importer = DataImporter()
importer.import_all('backup.mindflow')
```

---

## ✅ 更新总结

**新增功能**:
1. 数据导出/导入系统
2. 数据完整性校验
3. 设备管理（为未来同步做准备）
4. 云端同步架构（Phase 5）

**更新文档**:
- `docs/DEVELOPMENT_V2.md` - Phase 1 和 Phase 5 任务
- `docs/DATABASE.md` - 新增同步相关表
- `docs/DATA_MIGRATION.md` - 本文档

**优先级**: Phase 1 实现本地导出/导入，Phase 5 实现云端同步
