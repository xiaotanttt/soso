#!/usr/bin/env python3
"""
SoSoValue 任务自动化 - 快速启动脚本
作者: 0xTAN
推特: https://x.com/cgyj9wzv29saahq
"""

import os
import sys
import requests

def show_startup_banner():
    """显示启动横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗ ██╗  ██╗████████╗ █████╗ ███╗   ██╗      /\\_/\\                   ║
║  ██╔═████╗╚██╗██╔╝╚══██╔══╝██╔══██╗████╗  ██║     ( o.o )                  ║
║  ██║██╔██║ ╚███╔╝    ██║   ███████║██╔██╗ ██║      > ^ <                   ║
║  ████╔╝██║ ██╔██╗    ██║   ██╔══██║██║╚██╗██║                              ║
║  ╚██████╔╝██╔╝ ██╗   ██║   ██║  ██║██║ ╚████║                              ║
║   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝                              ║
║                                                                              ║
║                    SoSoValue 任务自动化工具 - 快速启动                      ║
║                                                                              ║
║                    作者: 0xTAN                                               ║
║                    推特: https://x.com/cgyj9wzv29saahq                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """检查依赖是否安装"""
    try:
        import requests
        import web3
        from eth_account.messages import encode_defunct
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_cf_token_service():
    """检查CF Token服务是否运行"""
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        print("✅ CF Token服务运行正常")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ CF Token服务未启动")
        print("请先启动CF Token服务:")
        print("  方法1: node index.js")
        print("  方法2: docker run -d -p 3000:3000 cf-clearance-scraper")
        print("  或确保在localhost:3000端口有CF Token服务运行")
        return False
    except Exception as e:
        print(f"⚠️ CF Token服务检查异常: {e}")
        print("请确保CF Token服务在localhost:3000端口运行")
        return False

def check_config_files():
    """检查配置文件"""
    if not os.path.exists('private_keys.txt'):
        print("❌ 未找到 private_keys.txt 文件")
        print("请参考 private_keys.txt.example 创建配置文件")
        return False
    
    with open('private_keys.txt', 'r') as f:
        keys = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
    
    if not keys:
        print("❌ private_keys.txt 文件为空")
        return False
    
    print(f"✅ 找到 {len(keys)} 个私钥")
    
    if os.path.exists('proxies.txt'):
        with open('proxies.txt', 'r') as f:
            proxies = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
        print(f"✅ 找到 {len(proxies)} 个代理")
    else:
        print("⚠️ 未找到代理文件，将不使用代理")
    
    return True

def main():
    """主函数"""
    # 显示启动横幅
    show_startup_banner()
    
    print("🔍 系统环境检查...")
    print("="*60)
    
    # 检查依赖
    if not check_requirements():
        return
    
    # 检查CF Token服务
    if not check_cf_token_service():
        return
    
    # 检查配置
    if not check_config_files():
        return
    
    print("\n🎉 所有检查通过，启动自动化程序...")
    print("="*60)
    
    # 导入并运行主程序
    try:
        from sosovalue_automation import main as run_automation
        run_automation()
    except Exception as e:
        print(f"❌ 运行失败: {e}")
    
    # 显示结束信息
    print("\n" + "="*60)
    print("🙏 感谢使用！如有问题请联系:")
    print("🐦 推特: https://x.com/cgyj9wzv29saahq")
    print("📧 GitHub Issues: 提交技术问题")
    print("🐱 喵~ 祝你使用愉快！")
    print("="*60)

if __name__ == "__main__":
    main()
