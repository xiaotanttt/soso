# SoSoValue 任务自动化工具

基于真实API捕获数据构建的SoSoValue日常任务自动化脚本，可以自动完成日常任务。

**作者**: 0xTAN  
**推特**: https://x.com/cgyj9wzv29saahq

## 🎯 功能特性

- ✅ **自动完成日常任务**: 推特点赞、观看新闻、推特发帖验证
- 🧠 **智能推特ID策略**: 多种推特ID生成算法，自动匹配最佳策略
- 🔄 **多钱包批量处理**: 支持批量处理多个钱包账户
- 🌐 **代理池支持**: 随机使用代理池，提高安全性
- 🧪 **智能重试机制**: 自动检测限流并重试，确保稳定运行
- 📝 **详细日志**: 完整的执行日志和结果报告
- 🛡️ **错误处理**: 完善的异常处理和重试机制

## 🚀 快速开始

### 1. 环境要求

```bash
pip install requests web3
```

### 2. 启动CF Token服务

**重要**: 脚本需要CF Token服务来处理Cloudflare验证，必须先启动此服务。

#### 方法一: 使用Node.js服务
```bash
# 安装依赖
npm install

# 启动CF clearance scraper服务 (端口3000)
node index.js
```

#### 方法二: 使用Docker (推荐)
```bash
# 拉取并运行CF Token服务
docker run -d -p 3000:3000 cf-clearance-scraper
```

#### 方法三: 手动启动
如果你有现成的CF Token解决方案，确保在 `localhost:3000` 端口提供服务，接受POST请求：
```json
{
  "url": "https://sosovalue.com/zh/exp",
  "siteKey": "0x4AAAAAAA4PZrjDa5PcluqN",
  "mode": "turnstile-min"
}
```

### 3. 配置文件

#### 私钥文件 (private_keys.txt)
```
0x你的私钥1
0x你的私钥2
0x你的私钥3
...
```

#### 代理文件 (proxies.txt) - 可选
```
http://username:password@proxy1:port
http://username:password@proxy2:port
...
```

### 4. 运行自动化

```bash
python sosovalue_automation.py
```

选择运行模式：
- **处理所有钱包**: 批量处理所有私钥文件中的钱包
- **限制钱包数量**: 指定处理前N个钱包

## 📋 支持的任务类型

| 任务类型 | 任务键值 | 状态 |
|---------|---------|------|
| 推特点赞 | `EXP_TWITTER_DAILY_LIKE` | ✅ 支持 |
| 观看新闻 | `EXP_WATCH_DAILY_NEWS` | ✅ 支持 |
| 推特发帖 | `TWITTER_DAILY_POST` | ✅ 支持 |

## 🧠 智能推特ID策略

系统采用多种智能策略生成推特ID，按优先级自动测试：

### 优先级1: 固定成功ID
- 使用经过验证的固定ID格式

### 优先级2: 用户ID变体
- 基于用户ID的数学变换
- 用户ID±1, ±2等变体

### 优先级3: 时间戳相关
- 基于当前时间戳的ID生成
- 毫秒级时间戳转换

### 优先级4: 钱包地址转换
- 基于钱包地址的哈希转换
- 16进制到数字的智能转换

## 🔧 高级用法

### 编程方式使用

```python
from sosovalue_automation import SoSoValueAutomator

# 创建自动化器
automator = SoSoValueAutomator(
    private_keys_file="your_keys.txt",
    proxies_file="your_proxies.txt"
)

# 运行自动化
results = automator.run_automation(max_wallets=5)

# 查看结果
for result in results:
    print(f"钱包 {result['wallet_address']}: {result['tasks_completed']}/3 任务完成")
```

### 定时执行

#### Linux/Mac (crontab)
```bash
# 每天上午9点自动执行
0 9 * * * cd /path/to/script && python sosovalue_automation.py < echo "1\ny"
```

## 🛠️ 故障排除

### 常见问题

#### 1. CF Token服务错误
- **现象**: `Connection refused` 或 `CF Token获取失败`
- **原因**: CF Token服务未启动或端口不正确
- **解决**: 
  ```bash
  # 检查服务是否运行
  curl http://localhost:3000
  
  # 重新启动服务
  node index.js
  ```

#### 2. 认证失败
- **原因**: CF Token服务问题或网络连接问题
- **解决**: 确保CF Token服务正常运行，检查网络连接

#### 3. 推特任务失败
- **原因**: 推特ID策略不匹配
- **解决**: 系统会自动尝试多种策略，通常能自动解决

#### 4. 网络连接错误
- **原因**: 网络问题或代理失效
- **解决**: 检查代理配置，系统会自动重试

#### 5. 限流错误 (429)
- **原因**: 请求过于频繁
- **解决**: 系统自动检测并等待，无需手动处理

### 调试模式

如需详细调试信息，可以修改代码中的日志级别。

## 🔒 安全注意事项

- ⚠️ **保护私钥安全** - 不要将私钥文件上传到公共仓库
- 🔄 **定期更新代理** - 使用稳定的代理服务
- 🛡️ **使用风险自负** - 这是自动化工具，请确保符合网站使用条款
- 📝 **保留日志** - 建议保留执行日志以便问题排查
- 🌐 **CF Token服务** - 确保CF Token服务的安全性，建议本地运行

## 📈 技术架构

### 核心组件

1. **认证系统**: Web3钱包签名认证
2. **任务引擎**: 智能任务执行流程
3. **策略引擎**: 多策略推特ID生成
4. **代理管理**: 随机代理池管理
5. **重试机制**: 智能重试和限流处理
6. **CF Token服务**: Cloudflare验证处理

### 依赖服务

- **CF Token服务**: 处理Cloudflare Turnstile验证
- **代理服务**: 可选的HTTP代理支持
- **Web3服务**: 以太坊钱包签名功能

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个工具！

### 开发指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📞 联系方式

- **作者**: 0xTAN
- **推特**: https://x.com/cgyj9wzv29saahq
- **GitHub Issues**: 技术问题和Bug报告

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**免责声明**: 本工具仅供教育和研究目的。使用者需自行承担使用风险，并确保遵守相关网站的服务条款。
