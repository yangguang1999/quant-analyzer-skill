# Quant-Analyzer: A-Share System Diagnostic & Strategy Evolution Framework

## 💡 项目概述
**Quant-Analyzer** 是一个基于 OpenClaw 多智能体协同（Multi-Agent）框架构建的，专注于**实盘量化交易系统（Sunsee-Trade）**的深度复盘、诊断与策略优化框架。

本项目超越了简单的日志记录，旨在通过**统计学**、**基本面**和**执行合规性**的交叉验证，实现对策略的持续、科学迭代，确保系统在复杂市场环境中保持最优的数学期望。

---

## 🦸‍♂️ 专家团队 (The Analysis Team)
本框架由一个主控节点（基金经理）和四个专职子代理组成，协同工作以提供全面报告。

| 角色代号 | Agent 名称 (Agent Name) | 核心职责 |
| :--- | :--- | :--- |
| **Agent A** | **Market Echo (市场回音)** | 宏观与板块研究：负责 `web_search` 搜索当日大盘情绪、资金主线，为策略表现定下外部基准。 |
| **Agent B** | **Sentinel (哨兵/合规)** | 纪律与执行审查：死磕 Log 与 `strategy.md`，核对 SAR 止损、仓位约束是否严格执行，发现底层执行 Bug。 |
| **Agent C** | **Oracle (统计先知)** | **量化统计与自由探索（核心）**：拥有沙盒代码权限，遍历历史 Log 计算动态胜率、回撤、MaxR 统计趋势，并根据数据提出**“参数优化”**或**“因子权重调整”**的量化建议。 |
| **Agent D** | **Detective (个股侦探)** | 个股深度投研：对所有买卖/持仓股票进行基本面/新闻/资金面/技术面**逐一深挖**，解释“为何买入/卖出”，提供具体案例的定性支撑。 |

---

## ⚙️ 核心机制与工作流 (Core Workflow)
本框架的运行遵循严格的 SOP，重点在于**数据闭环**和**统计学指导**。

1.  **输入 (Input)**：每日的 `trading_YYYY-MM-DD.log`。
2.  **上下文 (Context)**：
    *   **静态**：`strategy.md`（策略核心规则）。
    *   **动态历史**：`yesterday_summary.md`（前一日的优化建议）。
    *   **长期记忆**：`memory.md`（所有 Agent 可读，记录蒸馏后的历史教训）。
3.  **流程 (SOP)**：见 `SKILL.md`。核心是 A、B、C、D 四个 Agent **并行工作**，主控最后汇编。
4.  **输出 (Output)**：结构化报告，并由 Agent C 将本期核心发现追加写入 `memory.md`，实现**自进化记忆**。

## ⚠️ 重点：Agent C 的数据科学能力
Agent C 现在可以自由探索所有历史 Log，进行**动态回测**。它将重点关注：
*   当前策略表现是否偏离了历史**最大回撤区间**。
*   当前弹升的 MaxR 是否持续低于 **+3%**（表明市场弹性枯竭）。

---
## 💾 状态文件与数据安全
*   `strategy.md`：核心策略（**请务必填写！**）
*   `logs/`：存放原始交易日志（**已配置 GitIgnore，不上传！**）
*   `memory.md`：系统总结的经验与统计发现（可读）。
*   `.gitignore`：已配置，用于保护隐私数据。

---
## 🚀 快速启动
1.  完善 `strategy.md` 中的策略参数。
2.  将最新 Log 放入 `logs/` 目录。
3.  触发分析：`execute quant-analyzer today` (或相应的 Cron 命令)。