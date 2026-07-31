# 维护日志

这个文件用于记录项目内的重要修复、行为调整、兼容性变更和文档规则更新。

## 维护要求

- 以后任何 AI 或人工在这个仓库里做了实际改动，只要会影响运行逻辑、错误处理、文档说明、排障方式或用户使用预期，都需要在本文件追加一条记录。
- 每条记录至少写清楚：日期、问题现象、根因判断、改动文件、结果。
- 不要覆盖旧记录，只追加。
- 如果只是纯格式化、无行为变化的小改动，可以不记；但只要修了 bug、改了流程、改了提示文案、补了排障规则，就需要记。

---

## 2026-04-27

## 2026-04-28

### 在中英文 README 追加社区致谢与头像墙模板

- 现象：
  - README 里原本只有对上游项目和社区来源的常规致谢。
  - 仓库缺少一段专门感谢 issue 提交者、失败案例提供者和日志反馈者的结尾文案，也没有给出“非 contributor 也能展示头像”的写法。
- 根因判断：
  - 项目持续修复高度依赖真实失败案例和 artifact，但 README 还没有把这类社区反馈的价值明确表达出来。
  - GitHub 头像其实可以直接通过用户名链接显示，不需要 contributor 身份，只是文档里之前没有提供可复用模板。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 将原有上游项目感谢重命名为“项目来源与参考 / Project Origins and References”，避免和新增的社区致谢混在一起。
  - 在中英文 README 末尾新增更走心的社区致谢，明确感谢 issue、日志、截图、artifact 和失败案例反馈者。
  - 追加 GitHub 头像墙模板说明，支持后续按用户名补充头像，不依赖 contributor 身份。

### 在社区致谢区补入首批 GitHub 头像

- 现象：
  - 社区致谢区已经有文案和模板，但页面还没有真正展示首批反馈者头像。
  - 英文 README 仍然显示了“如何追加用户名”的说明文字，中文 README 也存在半注释状态的残留内容。
- 根因判断：
  - 用户已经提供了明确的 GitHub 用户名列表，应当直接落成可见头像墙，而不是继续停留在说明阶段。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 在中英文 README 的社区致谢区加入 `AaronL725`、`cita-777`、`1208nn`、`LGDhuanghe`、`AdjieC` 五位用户的头像链接。
  - 移除页面中可见的模板说明，仅保留注释里的头像墙模板供后续继续追加。

### 将社区头像墙改为更成熟的 README 表格样式

- 现象：
  - 第一版社区头像墙只是把头像横向排成一行，观感偏像临时占位。
  - 纯头像缺少名字和反馈类型说明，识别度不高，方形小图也显得比较生硬。
- 根因判断：
  - GitHub README 不能依赖自定义 CSS 做复杂美化，直接堆一排 `<img>` 很难接近成熟开源项目的展示效果。
  - 更适合参考常见的 contributors table 形式，在 GitHub 原生 Markdown/HTML 能力范围内用表格组织头像、名字和贡献说明。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 将中英文 README 的社区头像墙改为表格卡片式布局，统一展示头像、GitHub 用户名和反馈类型。
  - 同步更新注释模板，便于后续继续按同一风格追加用户。

### 将社区头像墙收敛为无边框头像加名字的简洁样式

- 现象：
  - 表格卡片版本虽然比第一版整齐，但每个头像外层都有明显边框，视觉上偏重。
  - 每人一条 `Issue · xxx` 的说明维护成本高，而且会让社区致谢区显得过于“档案化”。
- 根因判断：
  - README 里的致谢更适合轻量展示，不适合继续堆叠字段信息。
  - 对这类名单型内容，头像加名字已经足够表达感谢，继续细分反馈类型收益不高。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 将中英文 README 的社区头像墙改为无边框、居中的头像排布。
  - 去掉逐人的反馈类型说明，只保留头像和名字，降低维护成本并弱化沉重感。

### 统一 README 开头文案与项目命名表述

- 现象：
  - 中英文 README 开头仍混有“自动领取项目”“weekly freebies”等旧表述，项目定位和命名不够统一。
  - 英文 README 的社区致谢区名字行仍是可见内容，而中文版已经被注释掉。
- 根因判断：
  - 项目名称已调整为“Epic 周免游戏领取助手”，但 README 顶部介绍还没有同步整理。
  - 开头文案虽然信息完整，但层次不够清楚，对“完全免费”的强调也不够集中。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 重写中英文 README 开头介绍，按“适合谁、为什么容易用、为什么完全免费、GLM 路线价值”重新组织文案。
  - 将英文标题和相关表述从 `freebies` 调整为 `free games`，与当前项目命名保持一致。
  - 将英文 README 中社区致谢区的名字行改为注释状态，与中文 README 保持一致。

### 调整私有 fork 反馈说明并增加 Actions 成功摘要

- 现象：
  - README 和部分文档仍建议用户将 fork 改为私有，但相关说明没有同步强调：私有 fork 的 Actions 页面和运行产物对维护者不可见。
  - 现有 issue 模板默认要求“只提供运行链接”，这对私有 fork 不成立。
  - workflow 成功后还没有统一的 summary 提示用户去成功反馈讨论区留言。
- 根因判断：
  - 仓库内关于“公开 fork / 私有 fork”两种反馈路径的规则还没有统一。
  - 运行成功后的后续动作缺少明确入口，不利于沉淀成功样本。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `.github/workflows/README.md`
  - `.github/workflows/README.en.md`
  - `.github/ISSUE_TEMPLATE/01-bug-report-zh.yml`
  - `.github/ISSUE_TEMPLATE/02-bug-report-en.yml`
  - `.github/workflows/epic-gamer.yml`
  - `docs/maintenance-log.md`
- 处理结果：
  - 删除 README 和 workflow 文档中“建议改为私有仓库”的表述。
  - 在中英文 README、workflow 文档和 issue 模板中补充规则：公开 fork 可附运行链接，私有 fork 必须上传本次运行实际出现的 artifact zip。
  - 为中英文 issue 模板增加 fork 可见性字段。
  - 在 workflow 成功后写入 `GITHUB_STEP_SUMMARY`，引导用户前往成功反馈讨论区，并补充私有 fork 的反馈说明。

### 统一仓库身份相关的残留命名与链接

- 现象：
  - 仓库中仍残留 `10000ge10000/epic-awesome-gamer`、`QIN2DIM/epic-awesome-gamer` 相关的运行条件、镜像地址、项目元数据和旧工作目录表述。
  - 这些内容已经不再对应当前维护仓库，容易让用户误以为默认运行目标、镜像来源和项目信息仍指向旧仓库。
- 根因判断：
  - 项目在历史迁移和持续维护过程中，README 已经逐步改成当前仓库，但 workflow、Docker、`pyproject` 和部分开发记录仍保留了旧仓库标识。
- 改动文件：
  - `.github/workflows/epic-gamer.yml`
  - `docker/docker-compose.yaml`
  - `app/extensions/ext_celery.py`
  - `app/schedule/collect_epic_games_task.py`
  - `pyproject.toml`
  - `docs/development-log-2026-04-22.md`
  - `docs/development-log-2026-04-22.en.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 将 workflow 的主仓库判断切换为 `Ronchy2000/epic-freebies-helper`。
  - 将 Docker Compose 的项目名、服务名、容器名和默认镜像地址切换为当前仓库命名。
  - 将 Celery app 名称与任务队列名改为 `epic-freebies-helper`。
  - 将 `pyproject.toml` 中的作者和项目 URL 切换为当前维护仓库。
  - 将开发记录中的旧工作目录表述同步为当前仓库路径。

### 补充 Gemini/AiHubMix 配置示例和模型覆盖说明

- 现象：
  - 当前代码仍支持 `Gemini / AiHubMix`，但主 README 对这一路线的配置说明过于简略。
  - 用户难以从现有文案中直接判断 `GEMINI_BASE_URL`、`GEMINI_MODEL` 以及 4 个任务模型覆盖项应该如何填写。
- 根因判断：
  - 详细说明主要分散在 workflow 文档和 `.env.example`，主 README 的快速开始部分没有把 Gemini/AiHubMix 路线补成可直接照填的示例。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `.env.example`
  - `docs/maintenance-log.md`
- 处理结果：
  - 在中英文 README 的 Secrets 配置段增加 `GLM` 和 `Gemini / AiHubMix` 两组明确示例值。
  - 明确说明变量名是 `GEMINI_BASE_URL`，并补充推荐起步模型值。
  - 补充 4 个任务模型覆盖项的回落规则和示例值。
  - 在 `.env.example` 中补充覆盖项的填写说明，降低配置门槛。

### 检测到 Epic 2FA 必需时立即终止认证流程

- 现象：
  - 某些账号虽然已经通过验证码，但在 `POST /id/api/login` 后立即返回 `errors.com.epicgames.common.two_factor_authentication.required`。
  - 旧流程会把这类情况当作普通登录失败继续进入后续重试，浪费运行时间，也不利于用户快速判断根因。
- 根因判断：
  - 当前项目不支持处理 Epic 的邮箱 / 短信 / 验证器二步验证。
  - 对这类错误继续重试没有意义，应该直接作为不可恢复错误终止。
- 改动文件：
  - `app/services/epic_authorization_service.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - 为 `two_factor_authentication.required` 增加单独识别逻辑。
  - 一旦检测到 Epic 2FA 仍处于开启状态，认证流程会立即终止，不再继续后续重试。
  - 日志中会给出明确提示：该项目不支持 Epic 2FA，需先关闭 2FA 后再重跑。

### 在 README 中补充 Epic 2FA 关闭说明并移动教程图

- 现象：
  - 根目录存在一张 Epic 2FA 设置界面的教程图，但还没有纳入 README 的常见问题说明。
  - 用户遇到 `two_factor_authentication.required` 时，虽然能从日志判断是 2FA 问题，但文档中缺少直接对应的处理步骤和配图。
- 根因判断：
  - 2FA 是当前项目明确不支持的登录前置条件之一，应该在 README 里单独给出处理方式，而不是仅靠 issue 或口头说明传播。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `docs/images/faq/epic-2fa-remove-methods.png`
  - `docs/maintenance-log.md`
- 处理结果：
  - 将根目录教程图移动到 `docs/images/faq/epic-2fa-remove-methods.png`。
  - 在中英文 README 的 FAQ 中新增 2FA 专项说明，明确列出典型报错和 `/id/login/mfa` 跳转信号。
  - 补充处理步骤，并配图说明：进入 Epic 安全设置页面后，把启用的验证方式全部 `Remove` 掉。

### 区分 Gemini 官方接口与 AiHubMix 的配置说明

- 现象：
  - 主 README、workflow 文档和 `.env.example` 之前把 `Gemini` 与 `AiHubMix` 混写成同一组示例，并直接给出 `GEMINI_BASE_URL=https://aihubmix.com`。
  - 这会误导使用 Gemini 官方接口的用户，以为官方 Gemini 也应填写 AiHubMix 的地址。
- 根因判断：
  - 文档层没有区分“官方 Gemini 默认地址”和“第三方 Gemini 兼容中转接口”。
  - 代码层此前还将 `GEMINI_BASE_URL` 默认值设为 `https://aihubmix.com`，默认行为也不利于直连官方 Gemini。
- 改动文件：
  - `app/settings.py`
  - `app/extensions/llm_adapter.py`
  - `README.md`
  - `README.en.md`
  - `.github/workflows/README.md`
  - `.github/workflows/README.en.md`
  - `.env.example`
  - `docs/maintenance-log.md`
- 处理结果：
  - 将 `GEMINI_BASE_URL` 默认值改为空字符串，留空时直接走 Gemini 官方默认地址。
  - 仅在显式填写 `GEMINI_BASE_URL` 时，才启用 Gemini 兼容中转地址覆盖逻辑。
  - 在中英文 README、workflow 文档和 `.env.example` 中拆分“官方 Gemini”与“AiHubMix”两套示例，避免继续混淆。

### 重新补回 Codex 的 Karpathy 风格工作准则

- 现象：
  - 之前已经为 Codex 接入的 Karpathy 风格工作规则从项目指令中被删除。
  - 当前 `AGENTS.md` 不再包含针对 Codex 的“先澄清假设、简洁优先、精准修改、目标驱动验证”等约束。
- 根因判断：
  - 这是项目文档层面的回退，不是 Codex 全局 skill 安装失效。
  - `~/.codex/skills/karpathy-guidelines` 仍然存在，但缺少仓库级 `AGENTS.md` 约束后，当前项目内的默认行为提示会变弱。
- 改动文件：
  - `AGENTS.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 重新在 `AGENTS.md` 追加 Karpathy 风格的 Codex 工作规则，恢复“编码前思考、简洁优先、精准修改、目标驱动执行”四个原则。
  - 保留原有项目说明不变，并继续兼容本仓库“禁止跑测试”的限制。

### 默认 GitHub Actions 调度改为每周一次

- 现象：
  - 之前 workflow 默认是每天运行一次。
  - 对大多数普通用户来说，这个频率偏高，不符合 Epic 周免按周刷新的节奏，也会额外消耗 GitHub Actions 分钟数。
- 根因判断：
  - 默认 schedule 更适合放在 Epic 周免刷新之后，并按周执行。
  - 同时需要在文档里明确告诉用户：如果他们想改成别的时间，应直接修改 workflow 里的 cron。
- 改动文件：
  - `.github/workflows/epic-gamer.yml`
  - `.github/workflows/README.md`
  - `.github/workflows/README.en.md`
  - `README.md`
  - `README.en.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 默认 GitHub Actions 调度改为 `20 15 * * 4`，对应 `UTC 周四 15:20` / `北京时间周四 23:20`。
  - 将“为什么默认按周跑”“如何自己改 cron”写入中英文 GitHub Actions 文档。
  - 在中英文 README 的功能概览中同步说明默认是每周四运行一次，并支持自行调整。

### Checkout 安全校验解完后仍停在 Add to library，最终被误判失败

- 现象：
  - 某些免费游戏在 checkout 中完成一轮或多轮 hCaptcha 后，并不会立刻跳到“Thanks for your order / In Library”这类明确成功态。
  - 页面可能仍停留在商品页上的 checkout 弹层，继续显示 `Add to library`，最后主流程以 `Instant checkout ended without a confirmed claim state` 收尾，并在最终 reconciliation 后抛出失败。
- 根因判断：
  - 旧的最终确认逻辑对这类“checkout 还活着，但尚未被动变成 claimed state”的情况过于保守。
  - `final reconciliation` 主要做页面状态检查和订单历史检查，没有在发现 checkout/security 仍然存在时主动把领取流程接着跑完。
  - 同时 reconciliation 首轮不强制重开商品页，容易继续沿用已经过期的 checkout 弹层 DOM。
- 改动文件：
  - `app/services/epic_games_service.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - `final reconciliation` 现在每轮都会重开商品页，并在发现 `checkout` 或 `security` 仍然活跃时，主动恢复即时结账流程，而不是只做被动确认。
  - `_handle_instant_checkout()` 增加内部恢复模式，允许 reconciliation 复用即时结账逻辑，但避免递归触发自己的 finalize 分支。
  - 将 unconfirmed checkout 的最终确认次数和等待窗口拉长，提升 Epic 后端状态回写较慢时的恢复能力。

### Device not supported 弹窗再次导致领取失败

- 现象：
  - 商品页点击 `Get` 后没有进入 checkout，日志连续出现 `Purchase button ... click returned without visible progress`
  - 最终保存 `purchase_debug/click_no_effect-*.txt`
  - 调试文本里已经能看到 `Device not supported`、`Cancel`、`Continue`
- 根因判断：
  - 代码虽然已有 `Device not supported` 弹窗处理逻辑，但它只会在“点击已经被判断为有进展”之后才执行。
  - 本次页面在弹出 `Device not supported` 后，没有被 `_has_purchase_progress()` 识别成有效进展，导致流程在点击阶段就提前判失败，后续弹窗处理根本没有接上。
- 改动文件：
  - `app/services/epic_games_service.py`
  - `README.md`
  - `README.en.md`
  - `AGENTS.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 新增 `_is_device_not_supported_visible()`，把 `Device not supported` + `Cancel` + `Continue` 组合识别为明确的阻塞弹窗状态。
  - `_has_purchase_progress()` 现在会把该弹窗视为“点击后的有效进展”，从而继续进入现有的弹窗消除逻辑，而不是过早返回 `click_no_effect`。
  - `_handle_device_not_supported_modal()` 改为复用同一套可见性判断，避免前后条件不一致。

### 增加维护日志要求

- 现象：
  - 项目修复较多，历史经验容易散落在 issue、对话和零散文档里，后续 AI 或维护者很难快速知道哪些坑已经修过、为什么这么改。
- 根因判断：
  - 仓库里缺少一个明确的“变更必须登记”入口，也没有在项目指令里要求后续改动同步记录。
- 改动文件：
  - `AGENTS.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 新增本文件作为统一维护日志。
  - 在 `AGENTS.md` 中增加要求：后续所有会影响行为、排障或用户预期的改动，都必须同步写入本文件。

### Epic 隐私政策确认页导致登录后流程异常

- 现象：
  - 登录验证码通过后，日志显示 `Login success` / `Right account validation success`
  - 但后续在读取 `//egs-navigation` 时超时
  - 当前 URL 落在 `/id/login/correction/privacy-policy`
- 根因判断：
  - 这是 Epic 账号状态问题，不是 `GLM`、`Gemini` 或 `AiHubMix` 接口问题。
  - 部分账号登录后需要先手动确认一次隐私政策页面，脚本之前把它误当成普通商城页超时。
- 改动文件：
  - `app/services/epic_authorization_service.py`
  - `app/services/epic_games_service.py`
  - `README.md`
  - `README.en.md`
  - `.github/workflows/README.md`
  - `.github/workflows/README.en.md`
- 处理结果：
  - 识别 `privacy-policy correction` 特殊页面并给出明确错误提示。
  - 文档中补充说明：用户需要先用正常浏览器手动登录 Epic，完成该确认页后再重跑 workflow。

### checkout 多选题与 challenge router 的 GLM 返回格式兼容问题

- 现象：
  - `Device not supported` 修复后，流程已经能进入 checkout。
  - 但 checkout 安全校验阶段又出现新的结构化解析失败：
    - `ImageAreaSelectChallenge` 缺少 `challenge_prompt` / `points`
    - challenge router 有时只返回 `image_drag_multi`
  - 最终日志表现为 `instant_checkout_unconfirmed` 或 checkout solve loop 反复失败。
- 根因判断：
  - `llm_adapter` 之前主要补了 drag/drop 的若干变体，但还没有覆盖 area-select 返回的矩形框数组。
  - 同时 challenge router 返回的 `image_drag_multi` 是别名，当前路由识别只收 `image_drag_multiple`，导致 fallback 解析失败。
- 改动文件：
  - `app/extensions/llm_adapter.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - 新增 area-select 矩形框归一化，把 `[[x_min, y_min, x_max, y_max], ...]` 和 `[{x_min, ...}, ...]` 转成 schema 需要的 `points`。
  - 给缺失的 `challenge_prompt` / `inferred_rule` 自动补默认值。
  - 为 `image_drag_multi` 增加别名映射，统一归一化成 `image_drag_multiple`。

### `In Library` 已出现但仍被误判为 `click_no_effect`

- 现象：
  - 商品页点击 `Get` 后最终保存了 `purchase_debug/click_no_effect-*.txt`
  - 但调试文本里正文已经明确出现 `In Library`
- 根因判断：
  - `_claim_state_reason()` 对按钮文案里的 `IN LIBRARY` 有识别，但页面正文级别的 claim markers 只收了 `IN YOUR LIBRARY` / `VIEW IN LIBRARY` 等变体，没有把最常见的 `IN LIBRARY` 放进去。
- 改动文件：
  - `app/services/epic_games_service.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - 把正文级别的 `IN LIBRARY` 加入 claim markers。
  - 这样即使按钮状态没被稳定拿到，只要页面正文已经切成 `In Library`，也会被识别成已领取，不再落到 `click_no_effect`。

### 登录拖拽题返回裸坐标串时未被归一化

- 现象：
  - 登录阶段有时会返回 `{"answer": "1165,600,932,688"}`
  - 之前日志里会报 `ImageDragDropChallenge` 缺少 `challenge_prompt` / `paths`
- 根因判断：
  - `llm_adapter` 之前支持括号坐标、JSON 对象、数组等 drag 格式，但没有覆盖最简单的裸 CSV 坐标串。
- 改动文件：
  - `app/extensions/llm_adapter.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - 为 `x1,y1,x2,y2` 这类纯数字 CSV 形式补了 drag 坐标解析，统一归一化成 `paths`。

### 在进阶文档补充当前验证码支持面分析

- 现象：
  - 项目已经连续修过多类验证码兼容问题，但开发者文档里还没有把“当前到底考虑了哪些 challenge type、哪些仍不稳”写清楚。
- 根因判断：
  - 缺少一段集中说明，后续维护者容易误以为项目已经稳定覆盖所有验证码类型，或者不知道哪些题型是当前明确绕开的。
- 改动文件：
  - `docs/advanced.md`
  - `docs/advanced.en.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 在中英文进阶文档中新增“当前项目实际上考虑了哪些验证码类型”和“为什么有些验证码还是过不去”两段分析。
  - 明确列出当前已接入的 challenge type、被忽略的特殊题目，以及失败常见来源。

### 2026-04-29 OpenAI / GPT provider 接入

- 现象：
  - 用户询问项目是否能接 GPT 模型完成同样的验证码识别任务。
  - 原有配置只覆盖 `gemini` / `glm`，没有 OpenAI / GPT 的独立配置入口。
- 根因判断：
  - `hcaptcha-challenger` 上层仍按 `google-genai` 风格上传图片并调用 `generate_content`。
  - GPT 不能简单复用 `GLM_MODEL` 或 `GEMINI_BASE_URL`；OpenAI Chat Completions 的图片输入需要 `image_url`，本地图片应转成 `data:<mime>;base64,...`。
- 改动文件：
  - `app/settings.py`
  - `app/extensions/llm_adapter.py`
  - `.github/workflows/epic-gamer.yml`
  - `.env.example`
  - `docker/docker-compose.yaml`
  - `README.md`
  - `README.en.md`
  - `docs/advanced.md`
  - `docs/advanced.en.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 新增 `LLM_PROVIDER=openai`，以及 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL`。
  - 默认 OpenAI 模型设为 `gpt-4.1-mini`，并让 4 个验证码子模型在留空时跟随 `OPENAI_MODEL`。
  - 在适配层新增 OpenAI 兼容客户端，把 hCaptcha 图片输入转换为 OpenAI 可接受的 data URL 图片输入。
  - 中英文 README、Docker 示例、Actions secret 透传和进阶文档均补充 OpenAI / GPT 路线说明。

### 2026-04-29 README 结构与用户文档拆分

- 现象：
  - README 同时承担快速开始、完整 provider 说明、FAQ、Artifact 说明、本地调试和 Docker 部署说明。
  - 普通用户首次配置需要阅读过多与首跑无关的内容。
- 根因判断：
  - README 职责过多，详细排障和 provider 细节没有独立文档承载。
  - `.env.example` 缺少按 provider 分组的说明，不利于对照 README 配置。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `.env.example`
  - `docs/providers.md`
  - `docs/troubleshooting.md`
  - `docs/local-debug.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - README 缩减为 GitHub Actions 首次配置和运行所需内容。
  - 新增 provider、排障、本地调试与 Docker 三份文档。
  - `.env.example` 改为按账号、provider、高级覆盖项和运行参数分组。
  - 保留中文 README 中 `## 社区致谢` 及其后原文。

### 2026-04-29 在 README 开头标注 OpenAI / GPT 测试分支

- 现象：
  - OpenAI / GPT 支持位于独立开发分支，用户进入分支页面时不容易立即判断该分支应测试哪个 provider。
- 根因判断：
  - README 开头缺少分支用途说明，容易和 `master` 或其他 provider 分支混淆。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 在中英文 README 开头新增分支说明。
  - 明确当前分支用于测试 `LLM_PROVIDER=openai`，推荐模型为 `gpt-4.1-mini`，并提示第三方 OpenAI 兼容网关需要支持 `image_url` 输入格式。

### 2026-04-29 补充 OpenAI 分支与 DeepSeek 配置边界

- 现象：
  - 两个 provider 开发分支同时存在，用户可能误以为可以在 OpenAI / GPT 分支中配置 `DEEPSEEK_MODEL`。
- 根因判断：
  - OpenAI 分支 README 只说明了 GPT 测试配置，没有明确排除 DeepSeek V4 测试配置。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 中英文 README 明确说明 OpenAI / GPT 分支不用于测试 DeepSeek V4。
  - 明确提示不要在本分支配置 `DEEPSEEK_MODEL`。
  - 如需测试 DeepSeek V4，应切换到 `codex/add-deepseekv4-provider` 并设置 `DEEPSEEK_MODEL=deepseek-v4-pro`。

### 2026-05-02 补充 Fork 后手动启用工作流说明

- 现象：
  - 用户不确定当前仓库是否还会自动执行领取工作流，也不确定 Fork 后是否需要额外在 GitHub 页面手动启用 Actions。
- 根因判断：
  - workflow 文件已经通过仓库条件跳过主仓库自身的定时领取任务，但中英文 README 和 workflow 文档没有直接写明 Fork 后必须先点一次 `Enable workflow`，否则 GitHub 不会为该 Fork 启用定时 `schedule`。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `.github/workflows/README.md`
  - `.github/workflows/README.en.md`
  - `docs/maintenance-log.md`
- 处理结果：
  - 在中英文 README 和 workflow 文档中补充一句直白说明。
  - 明确写出操作入口：进入 Fork 仓库的 `Actions` 页面，打开 `Epic Awesome Gamer (Scheduled)`，点击一次 `Enable workflow`。

### 2026-05-05 Device not supported 弹窗阻塞购买点击

- 现象：
  - 商品页出现 `Device not supported` / 当前设备不兼容弹窗时，弹窗会挡住后续购买按钮点击。
  - 点击流程可能在看到弹窗后仍继续尝试点击购买按钮，最终保存 `purchase_debug/click_no_effect-*.png` / `.txt`。
- 根因判断：
  - 设备不兼容弹窗是一个需要先点击 `Continue` 才能继续的阻塞状态，不应被当作购买流程本身的有效进展。
  - 弹窗检测需要覆盖主页面和 frame 文本，但检测发生在点击轮询热路径中，读取 frame 文本必须带短超时，避免被默认等待时间放大。
- 改动文件：
  - `app/services/epic_games_service.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - 购买按钮点击前后都会检测并尝试关闭设备不兼容弹窗。
  - `_has_purchase_progress()` 不再把该弹窗本身视为有效购买进展。
  - `_combined_text()` / `_frame_texts()` 支持传入短超时，设备弹窗检测使用 500ms 主页面文本读取和 300ms frame 文本读取。

### 2026-05-05 GLM 框坐标导致 hCaptcha 点选解析失败

- 现象：
  - 登录 hCaptcha `image_label_multi_select` / `image_label_area_select` 流程中，GLM 返回 `{"answer":[[x_min,y_min,x_max,y_max], ...]}`。
  - `ImageAreaSelectChallenge` 校验时报 `points.*.x` / `points.*.y` 缺失，最终触发 `RetryError`。
- 根因判断：
  - 上游 `ImageAreaSelectChallenge.points` 只接受点击点坐标 `{"x": ..., "y": ...}`。
  - GLM 兼容层只要求模型返回 JSON，模型可能用视觉检测常见的框坐标格式回答。
  - 适配层已经识别了框坐标，但错误地把 `x_min/y_min/x_max/y_max` 原样塞入 `points`。
- 改动文件：
  - `app/extensions/llm_adapter.py`
  - `tests/test_glm_adapter.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - GLM 返回框坐标时，适配层会转成矩形中心点击点后再构造 `ImageAreaSelectChallenge`。
  - 增加回归测试覆盖数组框坐标和对象框坐标两种返回格式。

### 2026-05-06 GLM/Gemini provider 错配导致登录验证码走错接口

- 现象：
  - 某些 workflow 日志里已经明确打印 `LLM_PROVIDER=glm`，但运行配置同时出现 `GLM_API_KEY=null`、`GEMINI_API_KEY=**********`。
  - 登录验证码阶段没有直接报出 provider 配置错误，而是继续进入 Gemini 上传接口，最终在 `generativelanguage.googleapis.com/upload/v1beta/files` 处报 `API_KEY_INVALID`。
  - 用户看到的是深层 `RetryError` / `ClientError` 栈追踪，不容易判断根因其实是 provider 与 API key 配置不一致。
- 根因判断：
  - 代码此前允许 `LLM_PROVIDER=glm` 与空 `GLM_API_KEY` 一起继续启动。
  - 在这种错配下，GLM 兼容补丁不会生效，但 `hcaptcha-challenger` 仍可能继续使用 `GEMINI_API_KEY` 路径，导致错误表象落在 Gemini/Google 接口上。
- 改动文件：
  - `app/settings.py`
  - `app/extensions/llm_adapter.py`
  - `app/deploy.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - 增加 `llm_configuration_error` 统一判断显式 provider 与对应 API key 是否匹配。
  - `apply_llm_patch()` 在 provider 显式错配时会先打出明确日志，不再静默跳过。
  - `deploy()` 在浏览器启动前就会直接终止这类配置错误，并给出清晰提示：`LLM_PROVIDER=glm` 必须配置 `GLM_API_KEY`，`LLM_PROVIDER=gemini` 必须配置 `GEMINI_API_KEY`。

### 2026-05-06 在主文档和 workflow 文档中明确 provider 与 API key 必须一一对应

- 现象：
  - README 和 workflow 文档虽然分别给了 `GLM`、`Gemini`、`AiHubMix` 的示例，但没有把“`LLM_PROVIDER` 必须和实际填写的那组 API key 对应”写得足够直白。
  - 用户可能会误以为只要填了任意一组 key 即可，例如把 `LLM_PROVIDER=glm` 和 `GEMINI_API_KEY` 混在一起使用。
- 根因判断：
  - 现有文档强调了 `GLM` 路线“不需要额外配置 `GEMINI_API_KEY`”，但没有同步强调反向约束：显式选择哪个 provider，就必须填写该 provider 对应的 key。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `.github/workflows/README.md`
  - `.github/workflows/README.en.md`
  - `.env.example`
  - `docs/maintenance-log.md`
- 处理结果：
  - 在中英文 README 和 workflow 文档中增加显式规则与错配示例。
  - 在 `.env.example` 里增加注释，直接说明 `LLM_PROVIDER=glm -> GLM_API_KEY`、`LLM_PROVIDER=gemini -> GEMINI_API_KEY`。

### 2026-05-06 将 provider 配置提示收敛成直接句式

- 现象：
  - 上一版文档已经补上 provider 与 key 的对应关系，但有些位置仍然通过“不要这样错配”的反例来解释。
  - 这类规则对普通用户更适合写成单句指令，而不是先讲错法再反推对法。
- 根因判断：
  - 配置型文档越接近“照着填”越不容易出错，应该直接告诉用户“选这个 provider，就只填这一组 key”。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `.github/workflows/README.md`
  - `.github/workflows/README.en.md`
  - `.env.example`
  - `docs/maintenance-log.md`
- 处理结果：
  - 将中英文主文档和 workflow 文档统一改成直接句式：
    - `LLM_PROVIDER=glm` -> 填 `GLM_API_KEY`，无需填 `GEMINI_API_KEY`
    - `LLM_PROVIDER=gemini` -> 填 `GEMINI_API_KEY`，无需填 `GLM_API_KEY`

### 2026-05-06 将“无需填写”进一步明确成“无需新建并填写”

- 现象：
  - 即使写成了“无需填写另一组 key”，部分用户仍可能理解成“要先新建一个空的 Secret，只是不填值”。
- 根因判断：
  - 这类 GitHub Secrets 说明需要把“无需新建”也说清楚，否则普通用户容易把空 Secret 当成必要步骤。
- 改动文件：
  - `README.md`
  - `README.en.md`
  - `.github/workflows/README.md`
  - `.github/workflows/README.en.md`
  - `.env.example`
  - `docs/maintenance-log.md`
- 处理结果：
  - 将中英文文档进一步统一为：
    - `LLM_PROVIDER=glm` -> 填 `GLM_API_KEY`，无需新建并填写 `GEMINI_API_KEY`
    - `LLM_PROVIDER=gemini` -> 填 `GEMINI_API_KEY`，无需新建并填写 `GLM_API_KEY`

### 2026-05-09 登录验证码通过后又跳转隐私政策页时的认证稳态校验

- 现象：
  - 某些运行日志里，hCaptcha 已经成功通过，随后日志显示 `Login success` / `Right account validation success`。
  - 但新开的领取页稍后又被重定向到 `/id/login/correction/privacy-policy`，最终以 `Could not determine Epic login state because //egs-navigation did not appear` 失败。
  - Celery 调度入口即使认证失败，也没有像主入口那样立即中止任务。
- 根因判断：
  - 认证服务此前把“登录阶段收到成功信号”当成了“整个 Epic 商店会话已经可用于领取”，缺少登录后对领取页可用性的稳态确认。
  - 领取前状态检查只做了一次性判断，没有覆盖延迟发生的 `privacy-policy correction` 重定向。
  - `app/schedule/collect_epic_games_task.py` 没有校验 `agent.invoke()` 的返回值，认证失败后仍可能继续执行后续领取逻辑。
- 改动文件：
  - `app/services/epic_authorization_service.py`
  - `app/services/epic_games_service.py`
  - `app/schedule/collect_epic_games_task.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - 登录成功后会主动跳转一次周免页，并等待 `isloggedin=true`，只有真正拿到可用商店会话才继续后续流程。
  - 对延迟出现的 `/id/login/correction/privacy-policy` 重定向改为显式识别，给出明确的人工确认提示，不再落成泛化的 `//egs-navigation` 超时异常。
  - 领取页登录态检查改成短轮询稳态等待，避免刚跳转时的瞬时中间页被误判成未知异常。
  - Celery 调度入口与主入口统一：认证失败会立即终止，而不是继续进入领取阶段。

### 2026-05-17 设备不兼容弹窗探测与按钮上下文采样加固

- 现象：
  - 最新运行里，登录已经成功并完成 `Epic store session verification success`，但 `the-telltale-batman` 商品页连续出现 `Purchase button ... click returned without visible progress`。
  - 调试截图和文本已经明确显示 `Device not supported` / `This product is not compatible with your current device` / `Continue`，但运行日志里没有进入设备弹窗处理分支。
  - 随后处理下一个商品时，`_log_purchase_button_context()` 在读取 `purchase-cta-button` 文本时触发 `Locator.text_content: Timeout 30000ms exceeded`，把异常放大成整轮失败。
- 根因判断：
  - 现有设备弹窗探测把“弹窗存在”绑定在“Continue 按钮 locator 也必须短时间内可见”上；当 Epic 弹窗 DOM 形态变化或按钮可见性探测抖动时，会出现“页面文本里弹窗明明存在，但代码判断为不存在”的漏判。
  - `click_no_effect` 路径在最终判失败前没有做一次更强的 blocker 复查，因此会把“仍被设备弹窗挡住”误收口成普通点击无效。
  - 购买按钮上下文采样使用默认长超时，不适合作为调试函数直接挂在主流程里。
- 改动文件：
  - `app/services/epic_games_service.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - 将设备弹窗存在判定改为基于 page/frame 文本 marker 的独立检测，不再要求 `Continue` locator 先可见才承认弹窗存在。
  - `Continue` 点击兜底新增面向 dialog/modal/overlay 容器的浏览器端扫描：优先点击容器内最后一个可见的 `Continue` 按钮，抓不到时再退化成容器内最后一个可见按钮。
  - `_click_purchase_button()` 在所有点击策略都无进展后，会先做一次强复查并再次尝试清理设备弹窗，再决定是否落成 `click_no_effect`。
  - `_log_purchase_button_context()` 改成短超时采样和受控降级，不再让调试信息读取本身触发 30 秒硬超时。

### 2026-06-08 登录后 MFA 推荐页、启动后端与 GLM 拖拽格式加固

- 现象：
  - 社区反馈中登录验证码已经通过，但登录后页面可能停在 `/id/login/mfa/add/default`，后续领取阶段最终报 `Failed to confirm claim flow for promotions`。
  - 本地真实运行时，`browserforge` 的 `fingerprint-network.zip` 下载中断会让 `browser_context` 在 import 阶段直接失败，导致 `BROWSER_BACKEND=playwright` 也无法绕过 Camoufox 初始化问题。
  - Camoufox 本地真实运行中还出现过 `NS_ERROR_UNKNOWN_HOST` 这类浏览器内 DNS 导航错误，旧领取页入口只重试 Playwright timeout。
  - 本地真实运行还发现 GLM 可能返回 `source_coordinates` / `target_coordinates` 拖拽坐标，旧归一化逻辑会让 `ImageDragDropChallenge` 缺少 `paths`。
- 根因判断：
  - `/id/login/mfa/add/default` 是 Epic 登录后的 MFA 设置推荐中间页，不等同于领取失败；代码此前只显式处理隐私政策页和强制 2FA 错误，没有统一识别和跳过 MFA 推荐页。
  - Camoufox、`browserforge` 的重型依赖在模块加载时导入，削弱了 `auto` / `playwright` fallback 的意义。
  - GLM 兼容层的拖拽坐标别名覆盖还不完整。
- 改动文件：
  - `app/services/browser_context.py`
  - `app/services/epic_authorization_service.py`
  - `app/services/epic_games_service.py`
  - `app/extensions/llm_adapter.py`
  - `tests/test_glm_adapter.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - Camoufox 和 `browserforge.fingerprints.Screen` 改为按后端懒加载，避免 Playwright fallback 被 Camoufox 指纹数据下载失败提前拖死。
  - 周免页登录态入口的导航重试同时覆盖 Playwright timeout 和通用导航错误，降低临时 DNS / 网络错误直接终止运行的概率。
  - 认证流程新增 `/id/login/mfa/add` 检测与跳过逻辑；若无法自动跳过，会明确提示用户手动跳过或完成 MFA 推荐页，不再把它收口成模糊领取失败。
  - 领取页登录态检查也会识别 MFA 推荐页，避免新开页面被重定向后继续进入商品领取逻辑。
  - GLM 拖拽归一化新增 `source_coordinates` / `target_coordinates` 别名，并追加回归测试。
  - 本地验证：`py_compile` 通过；`PYTHONPATH=app pytest tests/test_glm_adapter.py -q` 通过。真实本地领取未能跑到领取阶段：Playwright 后端连续触发 hCaptcha 失败；Camoufox 已能安装并启动，但本机 Camoufox 内访问 Epic 出现 `NS_ERROR_UNKNOWN_HOST`。

### 2026-06-09 Epic 新结账页 Add to Library 与 GLM 结账验证码修复

- 现象：
  - 本地真实运行中，登录和初始 `Get` 点击已经正常，但商品页点击后最终报 `Failed to confirm claim flow for promotions`。
  - 调试快照显示点击后实际已经打开 Epic 结账 iframe，文案为 `THIS IS FREE` / `ADD TO LIBRARY`，旧逻辑只识别 `PLACE ORDER`，因此误判为点击无效。
  - 结账 hCaptcha 中，GLM 会返回 `image_label_single_select`、裸 `x,y` 点坐标、`source_coordinates` / `target_coordinates` 或局部/网格坐标混用，旧兼容层会触发 schema 校验失败或坐标偏移。
  - 结账验证码通过后，Epic 会重建 checkout DOM，旧 `_submit_place_order()` 继续使用失效的按钮 locator，导致后续点击策略各自等待到超时。
- 根因判断：
  - Epic 免费领取页已从旧 `PLACE ORDER` 流程变成部分商品使用 `ADD TO LIBRARY` 的即时结账流程，状态机的 checkout marker 和提交按钮候选不完整。
  - GLM OpenAI 兼容响应格式比 Gemini 更松散，需要对当前 hCaptcha 的路由枚举、裸坐标和图片坐标提示做额外归一化。
  - 结账验证码通过后 checkout iframe/按钮可能被替换，提交阶段必须重新扫描当前按钮，不能复用验证码前的 locator。
  - 机械拖拽轨迹会降低 drag 类结账验证码通过率，应默认使用 Bezier 轨迹。
- 改动文件：
  - `app/services/epic_games_service.py`
  - `app/extensions/llm_adapter.py`
  - `app/deploy.py`
  - `app/settings.py`
  - `docker/docker-compose.yaml`
  - `docker/.env`
  - `tests/test_glm_adapter.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - checkout 识别新增 `ADD TO LIBRARY` / `THIS IS FREE` / `ADD IT TO YOUR LIBRARY` marker，并把 `ADD TO LIBRARY` 当作可提交按钮。
  - 结账验证码识别新增 `PLEASE TRY AGAIN` + `VERIFY` 组合，避免验证码 iframe 被误判为普通 checkout。
  - `_submit_place_order()` 每个点击策略前都会重新扫描当前 checkout 按钮，并给 dispatch/dom 点击加短超时，避免 DOM 重建后卡住旧 locator。
  - GLM 图片请求改为标准 data URL；图片坐标任务追加网格坐标提示；兼容 `image_label_single_select`、当前 hCaptcha `image_drag_multi` 枚举、裸 `x,y` 点坐标和更多拖拽坐标别名。
  - `HEADLESS=false` 可用于本地可视化排查；默认和 Docker 配置改为启用 Bezier 轨迹。
  - 本地验证：`py_compile` 通过；`PYTHONPATH=app pytest tests/test_glm_adapter.py -q` 通过，7 个用例通过。
  - 真实本地领取验证成功：`Rogue Waters` 已显示 `In Library`；`Songs of Conquest` 通过结账 hCaptcha 后确认 `IN LIBRARY`；最终日志为 `Browser tasks execution finished successfully` / `Scheduler is disabled, deployment completed`。

### 2026-06-09 GitHub Actions 同入口完整领取收口复测

- 现象：
  - 需要确认修复不只是本地已登录账号成功，还要覆盖 GitHub Actions 使用的 `uv run app/deploy.py` 主入口完整收口。
  - 第二个 Epic 账号首次运行会经历完整登录、登录 hCaptcha、MFA 推荐页跳过、商店稳态验证、两个商品即时结账和结账 hCaptcha。
- 根因判断：
  - GitHub Actions 与本地测试共用 `app/deploy.py` 入口；如果 Actions 没有显式传入 Bezier 轨迹配置，虽然代码默认已修正，日志和 fork 配置仍不够直观。
  - 完整收口必须覆盖“验证码后无可解 frame 但稍后出现 `IN LIBRARY`”和“验证码后按钮被 overlay 拦截但 force 点击继续推进”两条路径。
- 改动文件：
  - `.github/workflows/epic-gamer.yml`
  - `docs/maintenance-log.md`
- 处理结果：
  - GitHub Actions 入口显式设置 `DISABLE_BEZIER_TRAJECTORY=false`，与本地成功配置一致。
  - 使用 `ronchy2000@gmail.com` 账号按 Actions 同入口配置真实复测成功：登录 hCaptcha 通过，MFA 推荐页自动跳过，`Epic store session verification success` 后进入领取。
  - `Rogue Waters` 通过 `ADD TO LIBRARY` 即时结账后确认 `IN LIBRARY`。
  - `Songs of Conquest` 结账 hCaptcha 首轮失败后重试成功，验证码后标准点击被 overlay 拦截，但 force 点击推进并最终确认 `IN LIBRARY`。
  - 最终日志为 `Confirmed 2 instant claim(s)`、`Browser tasks execution finished successfully`、`Scheduler is disabled, deployment completed`，进程退出码为 0。

### 2026-06-12 Camoufox 清理阶段双重关闭导致 GitHub Actions 假失败

- 现象：
  - 某些 GitHub Actions 日志里，登录、MFA 推荐页跳过、商店会话验证、甚至商品发现都已经正常完成。
  - 但 run 最终不是死在领取状态机里，而是在退出浏览器上下文时抛出 `BrowserContext.close: Connection closed while reading from the driver`，随后整轮以 exit code 1 结束。
  - 日志尾部还伴随多条 `Target page, context or browser has been closed` 的 future 异常。
- 根因判断：
  - `execute_browser_tasks()` 在 `async with open_browser_context(...)` 内部手动调用了 `await browser.close()`。
  - 同时 `open_browser_context()` 自己也负责在退出时关闭 Camoufox / Playwright 持久化 context。
  - 在 GitHub runner 上，一旦 Camoufox 驱动已先断开，第二次关闭会把原本应当成功或至少更准确的主异常覆盖成收尾阶段异常，造成“假失败”。
- 改动文件：
  - `app/deploy.py`
  - `app/services/browser_context.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - 浏览器关闭职责统一收回 `open_browser_context()`，移除了 `execute_browser_tasks()` 内部的重复 `browser.close()`。
  - Camoufox 分支改为手动托管 `__aenter__` / `__aexit__`，并在退出时抑制关闭阶段异常，避免驱动已断开时把 run 改写成失败。
  - 这样即使浏览器进程先一步结束，GitHub Actions 也不会因为清理阶段双重关闭而额外翻成 exit code 1。

### 2026-06-16 Epic Store 导航组件缺失导致 Actions 登录态误判

- 现象：
  - 多个用户的 GitHub Actions 日志显示登录 hCaptcha、MFA 推荐页跳过、账号校验和商店会话验证已经完成。
  - 进入领取前检查时，页面停在 `https://store.epicgames.com/free-games?lang=en-US`，但 `//egs-navigation` 长时间没有出现，最终报 `Could not determine Epic login state because //egs-navigation did not appear`。
  - 另一些日志在认证后的商店稳态检查阶段反复输出 `Timed out while waiting for //egs-navigation during auth check`，说明同一依赖点在 Actions 环境下不稳定。
- 根因判断：
  - Epic Store 的导航 Web Component 在 GitHub Actions / Camoufox 环境中可能延迟、失败或被部分加载卡住。
  - 旧逻辑把 `egs-navigation[isloggedin]` 作为唯一登录态来源；即使账号接口已经可访问，也会因为前端导航壳层缺失而终止任务。
  - 这不是 `Device not supported` 或 `ADD TO LIBRARY` 结账状态机回退，而是领取前的会话探针过窄。
- 改动文件：
  - `app/services/epic_authorization_service.py`
  - `app/services/epic_games_service.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - 认证后的商店稳态检查和领取前登录态检查保留 `egs-navigation` 快路径。
  - 如果 8 秒内仍拿不到导航登录态，会访问 Epic 账号订单接口 `ajaxGetOrderHistory` 做后备会话探针。
  - 只有后备接口返回合法 JSON 且包含 `orders` 列表时才视为已登录；未登录、重定向、页面错误或非 JSON 响应仍会继续失败，不会把匿名页面误判成有效会话。
  - 领取前订单同步复用同一订单接口解析逻辑，并保留已有 `Device not supported`、`ADD TO LIBRARY`、结账 hCaptcha 和订单历史最终确认逻辑。

### 2026-07-06 收紧即时结账确认链并修复多游戏连续领取的第二单易失败问题

- 现象：
  - 有些账号实际已经把周免领进库里，GitHub Actions 最终却仍以 `Failed to confirm claim flow for promotions` 退出。
  - 另一类高频反馈是：同一轮两个周免里，第一个能成功，第二个更容易卡在 checkout 安全校验、`Place Order` / `Add to library` 后无收口，最终误报失败。
- 根因判断：
  - 旧的即时结账收尾只做了偏短的一次性确认，遇到 Epic 商品页状态回写或订单历史同步稍慢时，容易把“已完成但未及时显现”的 case 判成失败。
  - `Place Order` / `Add to library` 的提交逻辑在第一次 click 调用不抛异常时就直接返回，即使按钮、overlay 和页面状态完全没变化，也不会继续尝试后续提交策略。
  - 连续领取多个游戏时，第二个商品更容易遇到更重的 checkout 风控；同时旧逻辑固定偏向首个 purchase iframe，遇到遗留或非活动 iframe 时更容易点到错误容器。
- 改动文件：
  - `app/services/epic_games_service.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - checkout 容器扫描改为优先遍历当前页面上更像活动 checkout 的 frame / page 容器，不再固定依赖首个 purchase iframe。
  - `Place Order` / `Add to library` 提交改为只有在按钮消失、进入 claimed、安全校验出现或按钮/overlay 状态发生变化时才算本次 click 真正生效；否则继续尝试后续提交策略。
  - 即时结账末尾增加 promotion 级 reconciliation：可回到商品页重新确认，并额外轮询订单历史，降低“实际已领到但最后没收好”的误报率。
  - `collect_weekly_games()` 会在真正抛错前，再对所有未确认 promotion 统一执行一轮最终 reconciliation，尽量把第二单的延迟成功补收回来。
  - 本地验证限制：未执行测试；已执行 `python3 -m py_compile app/services/epic_games_service.py` 与 `git diff --check` 做静态校验。

### 2026-07-17 GitHub Actions 在设备兼容弹窗后无限等待

- 现象：
  - 定时运行 `29512945904` 已完成 Epic 登录，并发现 `Luto` 与 `Echo Generation: Midnight Edition`。
  - 第一款游戏点击 `Get` 后出现设备不支持弹窗；日志显示弹窗已成功关闭，但此后约 27 分钟没有新日志，最终触发 Actions 的 30 分钟上限。
- 根因判断：
  - 弹窗关闭后，领取进度检查会读取主页面和所有 iframe 文本；旧实现对每个 frame 串行调用无显式超时的 `inner_text()`。
  - 登录 hCaptcha 遗留或失效的 frame 会让这次状态扫描长时间阻塞；同时验证码等待、购物车递归重试和任务入口缺少有效的总超时保护。
- 改动文件：
  - `app/deploy.py`
  - `app/settings.py`
  - `app/services/epic_authorization_service.py`
  - `app/services/epic_games_service.py`
  - `.github/workflows/epic-gamer.yml`
  - `docs/maintenance-log.md`
- 处理结果：
  - iframe 文本改为并发、短超时读取，商品状态探针不再按 frame 数量累加长等待。
  - 登录与结算验证码等待、购物车结算重试均增加明确上限，移除无界递归。
  - `TASK_TIMEOUT_SECONDS=900` 现在实际包裹完整浏览器任务；超时会记录安全的阶段状态并保留截图，给 artifact 上传预留时间。
  - Actions summary 会展示不含账号或 Secret 的 `run-status.json`，便于未下载完整日志时确认停止阶段。
  - 按仓库约束未执行测试；使用静态检查、格式检查和真实 GitHub Actions 运行验证。

### 2026-07-17 GLM 4.6V 在线段补全型结算验证码中持续选错落点

- 现象：
  - 修复设备弹窗后的 frame 死锁后，运行 `29548664044` 已正常进入 `Luto` 即时结算。
  - 结算验证码连续出现 `Please drag the segment on the right to complete the line`；GLM 能识别右侧可拖动线段的起点，但多次把终点放到已有线段上，验证码持续刷新。
  - 运行在应用自己的 900 秒边界正常退出，`run-status.json`、日志和超时截图均成功上传。
- 根因判断：
  - GLM 兼容层的通用空间提示只强调坐标网格和视觉路径，没有说明这类题需要按编号把第 N 段放进 N-1 与 N+1 之间的空缺。
  - 当前 Secret 使用 `glm-4.6v`，但兼容层只给 `glm-4.5*` 请求开启 thinking，导致 4.6V 没有使用可用的深度推理模式。
- 改动文件：
  - `app/extensions/llm_adapter.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - 拖拽 schema 新增线段编号补全规则，明确目标是相邻编号之间的空缺中心，并要求同时匹配两端与方向。
  - GLM thinking 支持范围扩展到 `glm-4.6*`，保留原有 `glm-4.5*` 行为。
  - 按仓库约束未执行测试；使用 Ruff、Black、语法检查与真实 GitHub Actions 继续验证。

### 2026-07-17 验证码失败重试缺少 schema 约束与题目刷新边界

- 现象：
  - 运行 `29549619619` 已越过原死锁点并处理到第二款游戏，但 `Luto` 的结算验证码仍未确认成功。
  - GLM 4.6V thinking 有一轮返回 `source` / `target` 标量，缺少二维坐标和 `paths` 嵌套结构，触发 Pydantic 校验失败并消耗完整执行超时。
  - `hcaptcha-challenger` 的默认 `RETRY_ON_FAILURE=true` 会在一次调用内部递归重试失败挑战，应用无法及时刷新题目或推进状态机。
- 根因判断：
  - GLM Chat Completions 兼容请求仅声明 `json_object`，没有把 Pydantic JSON Schema 明确传入提示。
  - 验证码失败后的重试边界由依赖内部控制，和应用的登录三次尝试、结算十分钟窗口重复叠加。
- 改动文件：
  - `app/extensions/llm_adapter.py`
  - `app/services/epic_authorization_service.py`
  - `app/services/epic_games_service.py`
  - `app/settings.py`
  - `.github/workflows/epic-gamer.yml`
  - `docs/maintenance-log.md`
- 处理结果：
  - 每次结构化 GLM 请求都会附带完整 JSON Schema，并明确禁止把嵌套坐标简化为标量。
  - 关闭依赖内部失败递归；登录和结算层在失败信号后主动刷新挑战，由现有有界循环决定是否重试。
  - 应用任务上限调整为 1500 秒，仍低于 Actions 的 30 分钟上限并预留约 5 分钟上传 artifacts。
  - 按仓库约束未执行测试；使用静态检查和真实 GitHub Actions 继续验证。

### 2026-07-17 GLM 已读取线段题目但仍错误套用通用路径规则

- 现象：
  - 运行 `29550559218` 的 GLM 输出已包含完整题目 `Please drag the segment on the right to complete the line`，但登录阶段仍连续选错落点。
  - 失败截图中右侧可拖拽线段编号为 3，正确位置应是左侧 2 与 4 的端点空缺；模型却把终点放在与相邻编号无关的空白区域。
- 根因判断：
  - `hcaptcha-challenger` 的 skill 匹配没有这类题目规则，因此即使 payload 中有题目文字，传给空间模型的辅助提示仍只是通用 `JobType`。
  - 通用空间 system prompt 把路径追踪设为最高优先级，与编号补全题的规则冲突；fallback 识别时还可能只有 challenge router 的空题目。
  - 关闭依赖内部重试后，第三轮真实运行的登录通过率明显下降；外层现已有 180 秒硬边界，不再需要用关闭重试来防止无界执行。
- 改动文件：
  - `app/extensions/hcaptcha_adapter.py`
  - `app/extensions/llm_adapter.py`
  - `app/settings.py`
  - `.github/workflows/epic-gamer.yml`
  - `docs/maintenance-log.md`
- 处理结果：
  - 新增局部 hCaptcha 兼容补丁：优先从 payload 读取题目，fallback 时从 challenge frame DOM 补取可见题目。
  - 编号线段题改用专用步骤，明确编号规则覆盖通用路径追踪，并在输出前校验 N-1、N、N+1 与两端连接关系。
  - 恢复依赖内部失败重试，同时保留登录/结算调用的 180 秒外层硬上限。
  - Actions 临时上传去敏后的 challenge 图、坐标网格和模型答案，便于真实运行失败后继续定位；不上传 captcha payload 或 Secret。
  - 按仓库约束未执行测试；使用静态检查、导入检查和真实 GitHub Actions 验证。

### 2026-07-17 编号线段题的拖拽起点可能落在弯折物体空隙

- 现象：
  - 运行 `29551695629` 已确认专用编号规则在真实 Action 中命中；GLM 正确识别右侧为 4，并给出单一路径 `(836, 298) -> (604, 347)`。
  - 原始题图显示右侧 4 是 V 形弯折物体；模型起点接近外接框中心，但不是稳定落在彩色线段上的点，hCaptcha 随后返回失败。
  - 第二题的 GLM 输出又混入 schema 定义并缺失顶层 `challenge_prompt` / `paths`，依赖层重试占满单次 180 秒挑战预算。
- 根因判断：
  - 通用视觉模型擅长估算物体外接框中心，但凹形或弯折拖拽物的外接框中心可能是透明区域，鼠标按下时没有抓住实际物体。
  - 将完整 Pydantic JSON Schema 写入空间提示会显著增加上下文，并可能诱导 GLM 回显 schema；路径任务只需要一个固定、紧凑的 JSON 形状。
- 改动文件：
  - `app/extensions/hcaptcha_adapter.py`
  - `app/extensions/llm_adapter.py`
  - `.github/workflows/epic-gamer.yml`
  - `docs/maintenance-log.md`
- 处理结果：
  - 对编号线段题使用 OpenCV 检测右侧彩色线段上的黑色编号圆，并把鼠标起点吸附到该高置信锚点。
  - 终点同步加上完全相同的偏移，因此保持模型原始平移向量，不改变它判断的最终摆放位置。
  - 路径任务改用紧凑 JSON 模板，避免完整 schema 回显；诊断 artifact 同时保留去敏后的锚点标注图。
  - 按仓库约束未执行测试；使用四张真实 Action 题图做离线锚点检测、静态检查和下一轮真实 Action 验证。

### 2026-07-17 结算验证码探测抢占正式求解并耗尽任务预算

- 现象：
  - 运行 `29552675319` 已由 OpenCV 锚点修正成功通过登录验证码，并完成 Epic 登录与 Store session 验证。
  - `Luto` 与 `Echo Generation: Midnight Edition` 均进入 `Add to library` 结算，但结算探测会先启动一次 25 秒验证码求解；正式求解随后再次启动，期间出现被取消的模型请求、GLM `400 code=1210` 和挑战执行超时。
  - 第一款未确认后进行了四轮重复 reconciliation，第二款仍在结算验证码阶段时触发 1500 秒任务总超时；两款都没有形成可验证的入库证据。
- 根因判断：
  - `_probe_checkout_challenge()` 与 extended probe 名义上负责发现 hCaptcha，实际却直接调用完整的 `agent.wait_for_challenge()`；25 秒探测边界短于 GLM 一次正常空间推理，取消后又由正式求解入口重启，形成竞态并浪费模型和任务预算。
  - hCaptcha 题目文字可能混入 Cyrillic `Ѕ`、Greek/Cyrillic `Ο/О` 等同形字符，精确英文短语匹配会偶发漏掉编号线段专用规则与拖拽锚点修正。
  - 两款连续结算及多轮验证码的最坏耗时已经超过 1500 秒，而单款四轮即时 reconciliation 与最终统一 reconciliation 重复。
- 改动文件：
  - `app/extensions/hcaptcha_adapter.py`
  - `app/services/epic_games_service.py`
  - `.github/workflows/epic-gamer.yml`
  - `docs/maintenance-log.md`
- 处理结果：
  - 普通和 extended checkout probe 改为只轮询可见安全校验 DOM；`_resolve_checkout_security_check()` 成为唯一调用模型求解的入口。
  - 题目先做 Unicode 与已见同形字归一化，再用 `drag`、`segment`、`right`、`complete`、`line` 五个关键词识别编号线段题。
  - 单款即时 reconciliation 从四轮降为两轮，保留所有 promotion 完成后的统一最终 reconciliation。
  - Action 上限调整为 45 分钟，应用任务上限调整为 2400 秒，仍为状态汇总和 artifact 上传预留约 5 分钟。
  - 按仓库约束未执行测试；使用 Black、Ruff、Python 语法检查、YAML 解析和下一轮真实 GitHub Actions 验证。

### 2026-07-17 编号线段题仍依赖 GLM 猜测目标并阻断登录

- 现象：
  - 运行 `29554294274` 的探测竞态修复尚未进入结算验证，因为登录阶段连续遇到编号线段题。
  - 专用提示与源编号圆锚点均已命中，但 GLM 有两轮耗尽挑战执行时间；其余三轮把目标放在错误端点附近，最终以 `Authentication failed` 退出。
  - 运行约 15 分钟即结束，未触发新的 2400 秒应用总超时，也没有进入 `Luto` 或 `Echo Generation: Midnight Edition` 领取流程。
- 根因判断：
  - OpenCV 只修正了拖拽起点，终点仍取决于 GLM 对复杂背景、曲线端点和坐标网格的空间推理；模型可能返回合法 JSON，但目标仍偏离 26 至 43 像素。
  - 回看运行 `29552675319` 的真实成功题，源编号圆实际落在 `N-1` 与 `N+1` 两个编号圆中心的中点附近；计算中点与成功释放点仅相差约 8 像素。旧提示要求避开编号圆中心，和成功证据相反。
  - 即使后处理能覆盖模型坐标，先等待 GLM 返回仍会让 60 至 180 秒的模型超时阻断拖拽。
- 改动文件：
  - `app/extensions/numbered_line_solver.py`
  - `app/extensions/hcaptcha_adapter.py`
  - `app/extensions/llm_adapter.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - 新增本地编号线段求解器：Hough 圆检测编号圆，用 18 个压缩小型数字模板联合分配唯一编号，再把源编号圆拖到相邻编号圆的中点。
  - 支持已观察到的 `1-5 / source=4` 与 `1-6 / source=3` 两种布局；低于置信阈值时保守回退到空间模型。
  - 编号线段题现在在截图后直接执行确定性拖拽，不再等待 GLM；fallback 提示同步改为真实成功样本验证过的编号圆中点规则。
  - 六组 Run 6 题图做留一组验证均正确；另对五张 Run 5 未参与模板选择的题图恢复出完整编号序列。真实成功样本计算终点 `(540, 382)`，实际成功释放点为 `(548, 380)`。
  - 按仓库约束未执行测试；继续使用真实题图离线验证、静态检查和下一轮 GitHub Actions 做最终验收。

### 2026-07-17 本地编号线段求解通过真实领取验收

- 验证运行：
  - GitHub Actions 运行 `29563199230` 在提交 `e7daafe` 上完成，结论为 `success`，总耗时约 9 分 34 秒。
  - 登录及两次结算共记录八次 `Solved numbered-line drag deterministically`，日志中没有编号线段题的空间模型请求。
  - 登录阶段记录 `Challenge success`、`Login success` 与 `Epic store session verification success`。
  - `Luto` 与 `Echo Generation: Midnight Edition` 均在结算后记录页面标记 `IN LIBRARY`，形成逐款入库证据。
- 处理结果：
  - 本地 OpenCV 求解器已通过真实登录、结算验证码和两款游戏领取的端到端验收。
  - 移除仅用于修复分支验证的 `push` 触发；正式工作流恢复为 `workflow_dispatch` 与每周四定时运行。
  - hCaptcha 依赖仍会在本地拖拽完成后输出空响应 JSON 解析错误，但随后的挑战状态确认成功；该上游日志噪声不影响登录、结算或工作流结论。
  - 按仓库约束未执行测试；最终验证依据为静态检查、真实题图离线检查和 GitHub Actions 端到端结果。

### 2026-07-31 登录阶段验证码先出现导致按钮等待超时

- 现象：
  - 定时运行 `30559239498` 连续三次在 `page.click("#sign-in")` 处等待 30 秒，最终以 `Authentication failed` 退出。
  - 失败截图显示输入密码后 hCaptcha 已经可见，登录表单按钮被验证码弹层覆盖；流程没有进入挑战求解器，也没有开始领取周免。
- 根因判断：
  - Epic 登录页会在部分风控路径中先显示 hCaptcha，再等待登录按钮点击；原代码假设按钮必定先于挑战出现，因此把一个已可处理的挑战误判为登录页面超时。
  - 这是登录页时序变化，不是本次周免接口、GLM 凭据或结算验证码故障。
- 改动文件：
  - `app/services/epic_authorization_service.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - 新增登录提交边界：若 hCaptcha 已可见则直接进入现有解题循环，否则点击 `#sign-in`；点击使用 `no_wait_after`，避免弹层触发被导航等待放大为超时。
  - 未执行测试，遵循仓库测试禁令；提交前使用 Black/Ruff/语法检查，并以真实 GitHub Actions 运行作为最终验证。

### 2026-07-31 验证码通过后登录表单未重新提交

- 现象：
  - 修复分支运行 `30611872552` 已进入验证码求解，日志出现 `Challenge success`，但 Epic 登录状态没有建立。
  - hCaptcha 通过后页面已不再显示挑战，原代码在登录等待超时后直接结束，没有再次提交密码表单。
- 根因判断：
  - 当前 Epic 风控流程把验证码校验和登录表单提交拆成两个时序步骤；验证码成功只代表挑战完成，不保证原始提交事件仍然有效。
- 改动文件：
  - `app/services/epic_authorization_service.py`
  - `docs/maintenance-log.md`
- 处理结果：
  - 当验证码消失但登录信号尚未出现时，重新填充（仅在页面为空时）并提交密码表单，再进入下一轮有界验证码处理；短轮询优先捕获立即到达的登录结果。
  - Run 20 已证明第一处按钮等待问题修复，但验证码后重新提交尚未进入该运行，需继续用真实 Actions 验证。
