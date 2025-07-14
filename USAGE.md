# 使用说明

## 🚀 快速开始

1. **配置私钥**
   ```bash
   # 编辑私钥文件，每行一个私钥
   nano private_keys.txt
   ```

2. **配置代理** (可选)
   ```bash
   # 编辑代理文件，每行一个代理
   nano proxies.txt
   ```

3. **运行自动化**
   ```bash
   # 处理所有钱包
   python3 sosovalue_automation.py
   
   # 限制处理5个钱包
   python3 sosovalue_automation.py --max-wallets 5
   
   # 静默模式运行
   python3 sosovalue_automation.py -q
   ```

## 📋 命令行选项

- `--max-wallets N` - 限制处理的钱包数量
- `--quiet` 或 `-q` - 静默模式，减少输出
- `--help` - 显示帮助信息

## 💡 提示

- 私钥文件格式：每行一个私钥，以0x开头
- 代理文件格式：`http://user:pass@ip:port`
- 脚本会自动处理所有任务，无需手动确认
- 支持智能重试和错误处理

## 🔧 高级用法

```bash
# 批量处理，静默模式，限制钱包数量
python3 sosovalue_automation.py --max-wallets 10 -q

# 配合cron定时执行
0 9 * * * cd /path/to/script && python3 sosovalue_automation.py -q
```
