# StockPillar Skill for Claude Code

让 Claude Code 通过自然语言调用 [StockPillar](https://stockpillar.layercake.com.cn) 的 A 股
量化数据 API，覆盖行情、技术指标、资金流、财务、行业事件、AI 供应链图谱、组合持仓
等近 60 个端点。

## 功能预览

装上之后，你可以直接用中文问 Claude：

- "现在贵州茅台多少钱？"
- "查 600519.SH 最近 60 天的 MA、MACD、RSI、KDJ"
- "今天有哪些股票出现了 MACD 金叉？"
- "筛选 ROE>15% 且 PE<20 的股票"
- "查看 AI 主题供应链五层图谱"
- "买入 600519.SH 100 股，成本价 1500"（会要求你确认后再执行）
- "查看最近 30 天的持仓交易流水"

Claude 会把请求拆解为对应的 API 调用，并用中文汇总结果。

## 安装

### 方式 1：克隆到用户级 skills 目录（全局可用）

```bash
git clone https://github.com/jerryTao1984/stockpillar-skill \
  ~/.claude/skills/stockpillar-skill
```

### 方式 2：克隆到项目内（仅当前项目可用，可随仓库提交）

```bash
cd /path/to/your/project
mkdir -p .claude/skills
git clone https://github.com/jerryTao1984/stockpillar-skill \
  .claude/skills/stockpillar-skill
```

## 配置

### 必需环境变量

```bash
export STOCKPILLAR_API_KEY="your-api-key-here"
```

API Key 申请方式：访问 [stockpillar.layercake.com.cn](https://stockpillar.layercake.com.cn) 注册账户。

### 可选环境变量

```bash
# 默认指向生产环境，无特殊需求可不设置
export STOCKPILLAR_API_URL="https://stockpillar.layercake.com.cn/api/skill/v1"
```

把这两行写到 `~/.zshrc` 或 `~/.bashrc`，重启终端即可。

## 验证安装

启动 Claude Code，输入：

```
查询贵州茅台的基本信息
```

如果 Claude 调出股票名称、行业、上市日期等信息，说明 skill 已生效。

也可以跑自带的 smoke test 脚本：

```bash
cd ~/.claude/skills/stockpillar-skill
python3 scripts/test_api.py
```

依赖：`requests`（可选 `colorama` 美化输出）。

## 安全说明

- 交易类 POST（`/positions` 买入、`/positions/{id}/sell` 卖出）必须经过用户在对话中显式
  确认才会执行。"买点茅台" 这种模糊表达不算确认，Claude 会反问数量、成本价等参数。
- Skill 不暴露任何供应链 mutation / 维护类端点，相关操作请通过 StockPillar Web 后台。
- API Key 必须放在环境变量里，**不要**写到 skill 配置文件或 git 仓库中。

## 文件结构

```
stockpillar-skill/
├── SKILL.md                  # 主入口，定义 skill 元数据和触发规则
├── references/               # 按需加载的端点详细规则
│   ├── route-index.md        # 60+ 个 API 路由的权威清单
│   ├── general-rules.md      # 自然语言到端点的映射、参数规范
│   ├── technical.md          # 技术指标、K 线、信号扫描
│   ├── market-data.md        # 实时行情、资金流、北向资金、两融
│   ├── financial-statements.md  # 财务三大表、业绩快报
│   ├── industries-events.md  # 行业、主题事件、事件后验
│   ├── supply-chain.md       # AI 供应链图谱、事件传导
│   ├── positions.md          # 持仓、买卖、流水、T+1、流动性约束
│   ├── top20.md              # 每日 Top20 榜单
│   └── reports-macro-misc.md # AI 研报、宏观、健康检查
└── scripts/
    └── test_api.py           # 端点冒烟测试
```

## 反馈与贡献

- 发现 API 路径过期、参数变更：在本仓库提 issue
- 端点描述不准确、Claude 路由偏差：附上你的提问原文 + Claude 实际调用的端点
- 新增 StockPillar 后端端点：等同步更新 [references/route-index.md](references/route-index.md)

## License

MIT
