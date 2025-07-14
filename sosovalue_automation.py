#!/usr/bin/env python3
"""
SoSoValue 任务自动化工具
基于真实API发现构建的智能多钱包任务自动化系统

作者: 0xTAN
推特: https://x.com/cgyj9wzv29saahq
版本: 1.0.0
"""

import requests
import json
import time
import random
import argparse
import sys
from web3 import Web3
from eth_account.messages import encode_defunct

def show_banner():
    """显示启动横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗ ██╗  ██╗████████╗ █████╗ ███╗   ██╗    ██████╗ ██╗   ██╗         ║
║  ██╔═████╗╚██╗██╔╝╚══██╔══╝██╔══██╗████╗  ██║   ██╔═══██╗██║   ██║         ║
║  ██║██╔██║ ╚███╔╝    ██║   ███████║██╔██╗ ██║   ██║   ██║██║   ██║         ║
║  ████╔╝██║ ██╔██╗    ██║   ██╔══██║██║╚██╗██║   ██║▄▄ ██║██║   ██║         ║
║  ╚██████╔╝██╔╝ ██╗   ██║   ██║  ██║██║ ╚████║   ╚██████╔╝╚██████╔╝         ║
║   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝    ╚══▀▀═╝  ╚═════╝          ║
║                                                                              ║
║                    SoSoValue 任务自动化工具 v1.0.0                          ║
║                                                                              ║
║                    🧠 智能推特ID策略 | 🔄 多钱包批量处理                     ║
║                    🌐 代理池支持     | 🛡️ 完善错误处理                       ║
║                                                                              ║
║                    作者: 0xTAN                                               ║
║                    推特: https://X.com/cgyJ9WZV29saahQ                      ║
║                                                                              ║
║  ⚠️  重要提醒: 请勿使用重要钱包运行此脚本，建议使用测试钱包！                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

class SoSoValueAutomator:
    def __init__(self, private_keys_file='private_keys.txt', proxies_file='proxies.txt'):
        self.private_keys_file = private_keys_file
        self.proxies_file = proxies_file
        self.private_keys = []
        self.proxies = []
        
    def load_private_keys(self):
        """从文件加载私钥"""
        try:
            with open(self.private_keys_file, 'r') as f:
                self.private_keys = [line.strip() for line in f.readlines() if line.strip()]
            print(f"📂 成功加载 {len(self.private_keys)} 个私钥")
            return True
        except Exception as e:
            print(f"❌ 加载私钥失败: {e}")
            return False

    def load_proxies(self):
        """从文件加载代理"""
        try:
            with open(self.proxies_file, 'r') as f:
                self.proxies = [line.strip() for line in f.readlines() if line.strip()]
            print(f"🌐 成功加载 {len(self.proxies)} 个代理")
            return True
        except Exception as e:
            print(f"❌ 加载代理失败: {e}")
            return False

    def get_random_proxy(self):
        """随机选择一个代理"""
        if not self.proxies:
            return None
        proxy_url = random.choice(self.proxies)
        return {
            'http': proxy_url,
            'https': proxy_url
        }

    def generate_smart_twitter_ids(self, user_id, wallet_address):
        """基于分析结果生成智能推特ID列表"""
        twitter_ids = []
        
        # 策略1: 固定成功ID (已验证有效)
        twitter_ids.append({
            "id": "1234567890123456789",
            "strategy": "固定成功ID",
            "priority": 1
        })
        
        # 策略2: 用户ID变体 (分析中最成功的策略)
        try:
            user_id_int = int(user_id)
            twitter_ids.extend([
                {"id": str(user_id_int + 1), "strategy": "用户ID+1", "priority": 2},
                {"id": str(user_id_int - 1), "strategy": "用户ID-1", "priority": 2},
                {"id": str(user_id_int + 2), "strategy": "用户ID+2", "priority": 3},
                {"id": str(user_id_int - 2), "strategy": "用户ID-2", "priority": 3},
            ])
        except:
            pass
        
        # 策略3: 18位ID变体 (分析中有效)
        twitter_ids.extend([
            {"id": "123456789012345678", "strategy": "18位固定ID", "priority": 2},
            {"id": "987654321098765432", "strategy": "18位反向ID", "priority": 3},
        ])
        
        # 策略4: 时间戳相关 (分析中有效)
        current_time_ms = int(time.time() * 1000)
        twitter_ids.extend([
            {"id": str(current_time_ms)[:19], "strategy": "当前时间戳毫秒", "priority": 3},
            {"id": str(current_time_ms - 1000)[:19], "strategy": "时间戳-1秒", "priority": 4},
        ])
        
        # 策略5: 钱包地址相关 (分析中有效)
        try:
            wallet_hex = wallet_address[-16:]  # 取后16位
            wallet_int = int(wallet_hex, 16)
            wallet_id = str(wallet_int)[:19]  # 取前19位
            twitter_ids.append({
                "id": wallet_id,
                "strategy": "钱包地址转换",
                "priority": 3
            })
        except:
            pass
        
        # 按优先级排序
        twitter_ids.sort(key=lambda x: x["priority"])
        
        return twitter_ids

    def test_twitter_id_with_retry(self, session, twitter_id_info, max_retries=3):
        """测试推特ID，带重试机制"""
        twitter_id = twitter_id_info["id"]
        strategy = twitter_id_info["strategy"]
        
        for attempt in range(max_retries):
            try:
                endpoint = f"https://gw.sosovalue.com/task/task/support/twitter/verify/TWITTER_DAILY_POST/{twitter_id}"
                response = session.get(endpoint, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == 0 and data.get('data') is True:
                        return True, f"成功 - {strategy} ({twitter_id})"
                    else:
                        return False, f"验证失败 - {strategy}: data={data.get('data')}"
                elif response.status_code == 429:
                    # 遇到限流，等待后重试
                    wait_time = (attempt + 1) * 5
                    print(f"      ⏳ 遇到限流，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    continue
                else:
                    return False, f"HTTP错误 {response.status_code} - {strategy}"
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return False, f"请求异常 - {strategy}: {e}"
        
        return False, f"重试失败 - {strategy}"

    def get_auth_session(self, private_key, proxy=None):
        """获取认证session"""
        session = requests.Session()
        
        # 设置代理
        if proxy:
            session.proxies.update(proxy)
            print(f"   🌐 使用代理: {proxy['http'].split('@')[1]}")
        
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Origin": "https://www.sosovalue.com",
            "Referer": "https://www.sosovalue.com/",
            "User-Device": "web"
        })
        
        try:
            account = Web3().eth.account.from_key(private_key)
            wallet_address = account.address
            
            print("   🔐 获取CF Token...")
            cf_payload = {
                "url": "https://sosovalue.com/zh/exp",
                "siteKey": "0x4AAAAAAA4PZrjDa5PcluqN",
                "mode": "turnstile-min"
            }
            cf_response = requests.post('http://localhost:3000/cf-clearance-scraper', json=cf_payload, timeout=60)
            cf_token = cf_response.json().get('token')
            
            print("   🎯 获取Challenge...")
            challenge_res = session.post(
                "https://gw.sosovalue.com/authentication/auth/getChallenge",
                json={"walletAddress": wallet_address, "invitationCode": "ZA73ZSYL"},
                timeout=15
            )
            challenge_data = challenge_res.json()
            inviter_address = challenge_data.get('data', {}).get('inviterWalletAddress')
            nonce = "8fb7c56353d7993ad99802098e0dc979b7797ccca91e84a0c16c025f296631d9"
            
            print("   ✍️ 签名消息...")
            message_to_sign = f"I confirm that {inviter_address} invited me to register at sosovalue.com\\n\\nNonce: {nonce}"
            signed_message = account.sign_message(encode_defunct(text=message_to_sign))
            
            print("   🚪 执行登录...")
            login_payload = {
                "thirdpartyId": wallet_address,
                "invitationCode": "ZA73ZSYL",
                "message": message_to_sign,
                "signatureHex": signed_message.signature.hex(),
                "thirdpartyName": "rainbowkit",
                "walletName": "okx_wallet"
            }
            
            login_url = f"https://gw.sosovalue.com/authentication/auth/thirdPartyWalletLoginV2?cf-turnstile-response={cf_token}"
            login_res = session.post(login_url, json=login_payload, timeout=20)
            login_data = login_res.json()
            
            if login_data.get('code') == 0:
                auth_token = login_data.get('data', {}).get('token')
                user_id = login_data.get('data', {}).get('userId')
                
                session.headers.update({
                    "Authorization": f"Bearer {auth_token}"
                })
                
                return session, auth_token, user_id, wallet_address
                    
        except Exception as e:
            print(f"   ❌ 登录失败: {e}")
        
        return None, None, None, None

    def change_task_status(self, session, task_id, task_key, status):
        """步骤1: 更改任务状态"""
        try:
            payload = {
                "taskId": task_id,
                "taskKey": task_key,
                "status": status
            }
            
            response = session.post(
                "https://gw.sosovalue.com/task/task/support/changeTaskStatus",
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') in [0, 40302]:
                    return True, "状态变更成功"
                else:
                    return False, data.get('msg', f"状态变更失败，code: {data.get('code')}")
            else:
                return False, f"HTTP错误: {response.status_code}"
                
        except Exception as e:
            return False, f"请求异常: {e}"

    def complete_daily_task(self, session, task_key):
        """步骤2: 完成日常任务"""
        try:
            endpoint = f"https://gw.sosovalue.com/task/task/support/daily/other/complete/0/{task_key}"
            response = session.post(endpoint, json={}, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    return True, "任务完成成功"
                else:
                    return False, data.get('msg', '任务完成失败')
            else:
                return False, f"HTTP错误: {response.status_code}"
                
        except Exception as e:
            return False, f"请求异常: {e}"

    def complete_smart_twitter_task(self, session, task_id, user_id, wallet_address):
        """智能推特任务完成 - 使用多种策略"""
        try:
            # 步骤1: 更改任务状态
            status_success, status_msg = self.change_task_status(session, task_id, "TWITTER_DAILY_POST", 2)
            if status_success:
                time.sleep(2)
            
            # 步骤2: 生成智能推特ID列表
            twitter_ids = self.generate_smart_twitter_ids(user_id, wallet_address)
            print(f"      🧠 生成了 {len(twitter_ids)} 个智能推特ID策略")
            
            # 步骤3: 按优先级测试每个ID
            for i, twitter_id_info in enumerate(twitter_ids):
                print(f"      📝 测试策略 {i+1}: {twitter_id_info['strategy']}")
                
                success, message = self.test_twitter_id_with_retry(session, twitter_id_info)
                
                if success:
                    print(f"      ✅ {message}")
                    return True, message
                else:
                    print(f"      ❌ {message}")
                
                # 策略间延迟
                time.sleep(2)
            
            return False, "所有推特ID策略都失败了"
                
        except Exception as e:
            return False, f"请求异常: {e}"

    def process_single_wallet(self, private_key, wallet_index, total_wallets):
        """处理单个钱包的任务"""
        print(f"\n{'='*60}")
        print(f"🔄 处理钱包 {wallet_index}/{total_wallets}")
        print(f"{'='*60}")
        
        # 随机选择代理
        proxy = self.get_random_proxy()
        
        # 获取认证session
        session, auth_token, user_id, wallet_address = self.get_auth_session(private_key, proxy)
        
        if not auth_token:
            print("   ❌ 登录失败")
            return {
                "wallet_index": wallet_index,
                "wallet_address": "未知",
                "status": "login_failed",
                "tasks_completed": 0
            }
        
        print(f"   ✅ 登录成功: {wallet_address}")
        print(f"   👤 用户ID: {user_id}")
        
        # 定义所有任务
        daily_tasks = [
            {
                "name": "推特每日点赞",
                "task_key": "EXP_TWITTER_DAILY_LIKE",
                "task_id": "1815641487118300000",
                "type": "daily"
            },
            {
                "name": "观看每日新闻", 
                "task_key": "EXP_WATCH_DAILY_NEWS",
                "task_id": "1815633321592385830",
                "type": "daily"
            },
            {
                "name": "推特每日发帖",
                "task_key": "TWITTER_DAILY_POST",
                "task_id": "1815641150143569921",
                "type": "twitter"
            }
        ]
        
        completed_tasks = 0
        
        # 处理每个任务
        for i, task in enumerate(daily_tasks):
            print(f"\n   🎯 任务 {i+1}: {task['name']}")
            
            try:
                if task['type'] == 'twitter':
                    success, message = self.complete_smart_twitter_task(
                        session, task['task_id'], user_id, wallet_address
                    )
                elif task['type'] == 'daily':
                    # 步骤1: 更改任务状态
                    status_success, status_msg = self.change_task_status(
                        session, task['task_id'], task['task_key'], 2
                    )
                    
                    if status_success:
                        time.sleep(2)
                    
                    # 步骤2: 完成任务
                    success, message = self.complete_daily_task(session, task['task_key'])
                else:
                    success, message = False, "不支持的任务类型"
                
                if success:
                    print(f"      ✅ {message}")
                    completed_tasks += 1
                else:
                    print(f"      ❌ {message}")
                    
            except Exception as e:
                print(f"      ❌ 任务执行异常: {e}")
            
            # 任务间延迟
            if i < len(daily_tasks) - 1:
                time.sleep(5)
        
        print(f"\n   📊 钱包结果: 完成任务 {completed_tasks}/{len(daily_tasks)}")
        
        return {
            "wallet_index": wallet_index,
            "wallet_address": wallet_address,
            "status": "success",
            "tasks_completed": completed_tasks,
            "total_tasks": len(daily_tasks)
        }

    def run_automation(self, max_wallets=None, quiet=False):
        """运行智能多钱包任务自动化"""
        # 显示启动横幅（非静默模式）
        if not quiet:
            show_banner()
        
        print("🚀 启动SoSoValue智能任务自动化系统")
        if not quiet:
            print("🧠 基于深度分析的智能推特ID生成策略")
            print("="*80)
        
        # 加载配置
        if not self.load_private_keys():
            return None
        
        self.load_proxies()  # 代理加载失败不影响运行
        
        # 限制钱包数量
        private_keys_to_process = self.private_keys
        if max_wallets and max_wallets < len(self.private_keys):
            private_keys_to_process = self.private_keys[:max_wallets]
            print(f"🔢 限制处理前 {max_wallets} 个钱包")
        
        print(f"📋 将处理 {len(private_keys_to_process)} 个钱包")
        print(f"🌐 代理池大小: {len(self.proxies)}")
        print(f"🧠 智能推特ID策略:")
        print(f"   - 固定成功ID (优先级1)")
        print(f"   - 用户ID变体 (优先级2)")
        print(f"   - 18位ID变体 (优先级2)")
        print(f"   - 时间戳相关 (优先级3)")
        print(f"   - 钱包地址转换 (优先级3)")
        
        results = []
        start_time = time.time()
        
        # 处理每个钱包
        for i, private_key in enumerate(private_keys_to_process, 1):
            try:
                result = self.process_single_wallet(private_key, i, len(private_keys_to_process))
                results.append(result)
                
                # 钱包间延迟 - 避免限流
                if i < len(private_keys_to_process):
                    delay = random.randint(15, 30)
                    print(f"\n⏳ 等待 {delay} 秒后处理下一个钱包...")
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"\n❌ 钱包 {i} 处理异常: {e}")
                results.append({
                    "wallet_index": i,
                    "wallet_address": "异常",
                    "status": "error",
                    "tasks_completed": 0
                })
        
        # 统计结果
        execution_time = time.time() - start_time
        successful_wallets = len([r for r in results if r['status'] == 'success'])
        total_tasks_completed = sum(r['tasks_completed'] for r in results)
        
        # 显示最终结果
        print("\n" + "="*80)
        print("📊 智能自动化最终结果")
        print("="*80)
        print(f"⏱️  总耗时: {execution_time/60:.1f} 分钟")
        print(f"👛 钱包统计:")
        print(f"   - 总数: {len(private_keys_to_process)}")
        print(f"   - 成功: {successful_wallets}")
        print(f"   - 失败: {len(private_keys_to_process) - successful_wallets}")
        print(f"📋 任务统计:")
        print(f"   - 总完成: {total_tasks_completed}")
        print(f"   - 平均每钱包: {total_tasks_completed/len(private_keys_to_process):.1f} 个任务")
        
        # 按任务类型统计
        twitter_success = 0
        daily_success = 0
        for result in results:
            if result.get('tasks_completed', 0) >= 3:  # 全部任务完成
                twitter_success += 1
                daily_success += 1
            elif result.get('tasks_completed', 0) >= 2:  # 只完成日常任务
                daily_success += 1
        
        print(f"📊 任务成功率:")
        print(f"   - 日常任务 (点赞+新闻): {daily_success}/{len(private_keys_to_process)} ({daily_success/len(private_keys_to_process)*100:.1f}%)")
        print(f"   - 推特任务 (智能优化): {twitter_success}/{len(private_keys_to_process)} ({twitter_success/len(private_keys_to_process)*100:.1f}%)")
        
        print(f"\n📝 详细结果:")
        for result in results:
            status_icon = {"success": "✅", "login_failed": "❌", "error": "⚠️"}.get(result['status'], "❓")
            success_rate = f"{result['tasks_completed']}/3" if result.get('tasks_completed') is not None else "0/3"
            print(f"   {status_icon} 钱包 {result['wallet_index']}: {result['wallet_address'][:10]}... - 完成 {success_rate} 任务")
        
        # 显示结束横幅
        print("\n" + "="*80)
        print("🎉 感谢使用 0xTAN 的 SoSoValue 任务自动化工具！")
        print("🐦 关注推特获取更多更新: https://x.com/cgyj9wzv29saahq")
        print("🐱 喵~ 祝你每天都能获得满满的EXP！")
        print("="*80)
        
        return results


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='SoSoValue 任务自动化工具')
    parser.add_argument('--max-wallets', type=int, help='限制处理的钱包数量')
    parser.add_argument('--quiet', '-q', action='store_true', help='静默模式，减少输出')
    args = parser.parse_args()
    
    automator = SoSoValueAutomator()
    
    # 使用命令行参数或默认值
    max_wallets = args.max_wallets
    
    if not args.quiet:
        if max_wallets:
            print(f"💡 将处理前 {max_wallets} 个钱包")
        else:
            print("💡 将处理所有钱包")
        print("🔧 提示: 使用 --max-wallets N 限制钱包数量，使用 -q 启用静默模式")
    
    # 确认执行
    print(f"\n⚠️  即将执行智能任务自动化")
    if max_wallets:
        print(f"📊 处理钱包数量: {max_wallets}")
    else:
        print(f"📊 处理钱包数量: 全部")
    print("📋 每个钱包将执行3个任务:")
    print("   - 推特每日点赞")
    print("   - 观看每日新闻") 
    print("   - 推特每日发帖 (智能ID策略)")
    print("🌐 将随机使用代理池中的代理")
    print("⏱️  预计耗时: 每个钱包约2-3分钟")
    print("🧠 智能特性:")
    print("   - 多种推特ID生成策略")
    print("   - 按优先级测试")
    print("   - 自动重试机制")
    print("   - 限流检测和等待")
    
    # 直接开始执行，不需要确认
    if not args.quiet:
        print("\n🚀 开始执行智能任务自动化...")
    results = automator.run_automation(max_wallets=max_wallets, quiet=args.quiet)
    
    if results:
        print("\n🎉 智能任务自动化执行完成！")
    else:
        print("\n❌ 自动化执行失败！")


if __name__ == "__main__":
    main()
