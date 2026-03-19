#!/usr/bin/env python3
import os
import glob
import re

LOG_DIR = "/Users/yangguang/.openclaw/workspace/skills/quant-analyzer/logs"

def analyze_logs():
    log_files = sorted(glob.glob(os.path.join(LOG_DIR, "*.log")))
    if not log_files:
        print("No logs found.")
        return

    print(f"Agent C: 发现 {len(log_files)} 份历史日志，开始按日深度回测计算...\n")

    pnl_pattern = re.compile(r'([A-Z0-9.]+)\s+[\d\.]+\s+[\d\.]+\s+([+-][\d\.]+)%')
    maxr_pattern = re.compile(r'maxR=([+-][\d\.]+)%')
    
    cumulative_sells = 0
    cumulative_wins = 0
    cumulative_pnl = 0.0
    cumulative_maxr = []

    for file in log_files:
        date_str = os.path.basename(file).replace("trading_", "").replace(".log", "")
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        daily_sells = 0
        daily_wins = 0
        daily_pnl = 0.0
        daily_maxr = []
        trades = []
        
        for line in lines:
            if "REPORT" in line and "section_4_trading_summary" in line and "SAR止损" in line:
                daily_sells += 1
                cumulative_sells += 1
                
                code = "UNKNOWN"
                pnl = 0.0
                pnl_match = pnl_pattern.search(line)
                if pnl_match:
                    code = pnl_match.group(1)
                    pnl = float(pnl_match.group(2))
                    daily_pnl += pnl
                    cumulative_pnl += pnl
                    if pnl > 0:
                        daily_wins += 1
                        cumulative_wins += 1
                        
                maxr = 0.0
                maxr_match = maxr_pattern.search(line)
                if maxr_match:
                    maxr = float(maxr_match.group(1))
                    daily_maxr.append(maxr)
                    cumulative_maxr.append(maxr)
                
                trades.append(f"{code} (PnL: {pnl}%, MaxR: +{maxr}%)")
                
        # Daily Summary
        if daily_sells > 0:
            d_win_rate = (daily_wins / daily_sells) * 100
            d_avg_pnl = daily_pnl / daily_sells
            d_avg_maxr = sum(daily_maxr) / len(daily_maxr) if daily_maxr else 0.0
            print(f"📅 【{date_str}】单日表现:")
            print(f"   平仓: {daily_sells}笔 | 胜率: {d_win_rate:.1f}% | 均盈亏: {d_avg_pnl:.2f}% | 均MaxR: +{d_avg_maxr:.2f}%")
            print(f"   明细: {', '.join(trades)}\n")
        else:
            print(f"📅 【{date_str}】单日表现: 无平仓交易\n")

    # Cumulative Summary
    if cumulative_sells > 0:
        c_win_rate = (cumulative_wins / cumulative_sells) * 100
        c_avg_pnl = cumulative_pnl / cumulative_sells
        c_avg_maxr = sum(cumulative_maxr) / len(cumulative_maxr) if cumulative_maxr else 0.0
        print("="*40)
        print("📈 【累计统计指标 (全局)】")
        print(f"总平仓: {cumulative_sells}笔 | 总胜率: {c_win_rate:.1f}% | 总均盈亏: {c_avg_pnl:.2f}% | 总均MaxR: +{c_avg_maxr:.2f}%")
        print("="*40)
        
        # 趋势对比分析
        if len(log_files) >= 2:
            print("\n🔍 【Agent C 趋势对比洞察】")
            print("通过对比昨日与今日的数据，发现:")
            print("1. 弹性趋势：从昨日到今日，MaxR 是否有提升？如果没有，说明市场进攻端持续承压。")
            print("2. 亏损控制：单日平均亏损是否被有效遏制在 SAR 止损的预期范围内。")

if __name__ == "__main__":
    analyze_logs()
