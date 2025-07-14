#!/bin/bash

echo "🚀 SoSoValue 任务自动化工具 - 安装脚本"
echo "作者: 0xTAN | 推特: https://x.com/cgyj9wzv29saahq"
echo "============================================"

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if [[ $(echo "$python_version >= 3.7" | bc -l) -eq 1 ]]; then
    echo "✅ Python版本: $(python3 --version)"
else
    echo "❌ 需要Python 3.7或更高版本"
    exit 1
fi

# 安装依赖
echo "📦 安装Python依赖..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 检查Node.js (用于CF Token服务)
if command -v node &> /dev/null; then
    echo "✅ Node.js版本: $(node --version)"
else
    echo "⚠️ 未找到Node.js，如需使用内置CF Token服务请安装Node.js"
fi

# 检查配置文件
echo "🔧 检查配置文件..."

if [ ! -f "private_keys.txt" ]; then
    echo "⚠️ 未找到 private_keys.txt，请参考示例文件创建"
    echo "   cp private_keys.txt.example private_keys.txt"
    echo "   然后编辑 private_keys.txt 填入真实私钥"
fi

if [ ! -f "proxies.txt" ]; then
    echo "ℹ️ 未找到 proxies.txt (可选)，如需使用代理请创建此文件"
    echo "   cp proxies.txt.example proxies.txt"
    echo "   然后编辑 proxies.txt 填入代理信息"
fi

echo ""
echo "🎉 安装完成！"
echo ""
echo "📋 下一步："
echo "1. 启动CF Token服务 (重要!):"
echo "   - 方法1: node index.js"
echo "   - 方法2: docker run -d -p 3000:3000 cf-clearance-scraper"
echo "   - 或确保在localhost:3000有CF Token服务"
echo "2. 配置 private_keys.txt 文件"
echo "3. (可选) 配置 proxies.txt 文件"
echo "4. 运行: python3 run.py"
echo ""
echo "📖 更多信息请查看 README.md"
echo "🐦 关注推特: https://x.com/cgyj9wzv29saahq"
