# 项目结构说明

```
SoSoValue-Task-Automation/
├── sosovalue_automation.py    # 主要自动化脚本
├── run.py                     # 快速启动脚本
├── requirements.txt           # Python依赖
├── README.md                  # 项目说明文档
├── LICENSE                    # 许可证
├── .gitignore                # Git忽略文件
├── STRUCTURE.md              # 项目结构说明 (本文件)
├── install.sh                # Linux/Mac安装脚本
├── install.bat               # Windows安装脚本
├── private_keys.txt.example  # 私钥配置示例
└── proxies.txt.example       # 代理配置示例
```

## 文件说明

### 核心文件

- **sosovalue_automation.py**: 主要的自动化脚本，包含所有核心功能
- **run.py**: 快速启动脚本，包含环境检查和配置验证
- **requirements.txt**: Python依赖包列表

### 配置文件

- **private_keys.txt**: 私钥配置文件 (需要用户创建)
- **proxies.txt**: 代理配置文件 (可选)
- **private_keys.txt.example**: 私钥配置示例
- **proxies.txt.example**: 代理配置示例

### 安装脚本

- **install.sh**: Linux/Mac自动安装脚本
- **install.bat**: Windows自动安装脚本

### 文档文件

- **README.md**: 详细的项目说明和使用指南
- **LICENSE**: MIT许可证
- **STRUCTURE.md**: 项目结构说明 (本文件)

### 其他文件

- **.gitignore**: Git版本控制忽略文件，防止敏感信息被提交

## 使用流程

1. **克隆项目**: `git clone <repository-url>`
2. **运行安装脚本**: `./install.sh` (Linux/Mac) 或 `install.bat` (Windows)
3. **配置私钥**: 复制并编辑 `private_keys.txt.example` 为 `private_keys.txt`
4. **配置代理** (可选): 复制并编辑 `proxies.txt.example` 为 `proxies.txt`
5. **运行程序**: `python run.py` 或 `python sosovalue_automation.py`

## 安全注意事项

- `private_keys.txt` 和 `proxies.txt` 已在 `.gitignore` 中，不会被Git跟踪
- 请勿将包含真实私钥的文件上传到公共仓库
- 建议在本地环境中使用，避免在公共服务器上运行
