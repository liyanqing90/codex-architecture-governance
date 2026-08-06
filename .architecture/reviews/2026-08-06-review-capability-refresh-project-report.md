# Hengmu capability refresh 项目 Finding 独立核验报告

## 审查对象与架构形状

- subject：Hengmu（repository identity `hengmu`），project review，scope `.`
- 源码提交：`130000d59fd119647ec8cbde149ab3e3a7cd5ab3`
- 候选：`.architecture/reviews/2026-08-06-review-capability-refresh-project-candidates.yaml`；Review ID `hengmu-20260806-review-capability-refresh-candidates`；SHA-256 `8abc088c1f68f280be70201d150a1382c0d03f74c6bd809f3d99b61b6872e1f3`
- 核验日期：2026-08-06；Profile、constraints、critical flows、gate policy 与三套 Rule Pack 均按候选绑定回读。
- 架构形状：`.codex-plugin/plugin.json → Skills/路由 → resources/契约、Knowledge、Rule Packs → Python CLI → 候选/Verified Review、Evidence Provider 运行记录与 deterministic Gate`。系统是本地、可分发的治理插件；Provider 是显式配置的项目-owned 子进程，产品边界不包含 hosted agent runtime、通用扫描器、包管理器或 autonomous upgrader。

## 确认强项（非新增 Finding）

- Audit、独立 verification、solution decision、remediation 与 Gate 保持分离；稳定入口不拥有 Finding、Decision 或 policy authority。
- Review 1.2 已有 candidate path/ID/hash、Finding semantic fingerprint、Profile/事实/Knowledge Selection、Rule Pack 与 critical-flow 绑定；本次残余风险集中在绑定边界而非缺少整个 provenance 链。
- Evidence Provider 执行路径直接调用 argv，限制环境变量、超时与检测条件，并记录 catalog/configuration/executable/Git/output 哈希及 post-run 状态；固定提交上的 no-shell 与结构化输出校验存在。
- technology-evolution Decision 已具备 companion Markdown 内容哈希、current volatile claims、completed pilot、observed measures 与逐项证据绑定；本次仅对阈值结果关系保留证据不足状态。
- 本次绑定验证确认 13 条 selected Knowledge、31 条 Rule coverage 和 6 条 critical-flow coverage 可以被机器校验。

## 仅 confirmed 风险

1. **HGM-TRACE-001 — high，confidence 0.94，PROJECT.CONTRACT.001。**
   `validate_review` 绑定候选路径、ID、字节哈希和 Finding 语义，但不比较候选 `review.commit` 与 Verified `review.commit`；`verify_review_evidence` 对 source/schema evidence 接受证据自带的 Git commit。由此，verified artifact 的源码快照声明与候选/当前源码证据可以脱节，diff-aware Gate 可能沿用 stale conclusion。

2. **HGM-PROVIDER-001 — medium，confidence 0.94，PROJECT.SECURITY.001。**
   Provider safety denylist 对 npm 未覆盖 `ci` 等依赖安装/解析动作；固定提交上的直接探针确认 `npm ci` 通过安全校验，而公共 Provider 契约禁止此类副作用。显式启用后，命令可进入执行边界并改变依赖、网络与 lifecycle-script 权限。

3. **HGM-PROVIDER-002 — medium，confidence 0.84，PROJECT.DEPLOY.001。**
   Provider run 绑定实际 executable、配置、输出与 Git 状态，但没有 dependency closure 或 external cache content binding。相同提交和配置在不同 PATH/toolchain/cache 输入下可能产生不同 deterministic 结果，单次运行仍会通过现有哈希校验。

4. **HGM-COVERAGE-001 — medium，confidence 0.82，PROJECT.TEST.001。**
   assessed coverage 行没有 inspected-evidence 字段；Gate 的 evidence resolution 只遍历 Finding evidence。一个无 Finding 的 Verified Review 可以声明所有 Rule/flow assessed 与 coverage complete，却没有机器可解析的逐项证据路径，因而无法区分有依据的 no-finding 与未绑定的覆盖声明。

## Finding 处置与计数

| Finding | 状态 | 备注 |
|---|---|---|
| HGM-TRACE-001 | confirmed | 保留候选 severity；V2 |
| HGM-PROVIDER-001 | confirmed | 保留候选 severity；V2 |
| HGM-PROVIDER-002 | confirmed | 保留候选 severity；V2 |
| HGM-EVOLUTION-001 | needs-evidence | 保留候选 severity；V2；未计入 confirmed 风险 |
| HGM-COVERAGE-001 | confirmed | 保留候选 severity；V2 |

- raw findings：5
- confirmed：4
- rejected：0
- needs-evidence：1
- 所有 Finding 均保留候选 semantic fingerprint、facts/inferences/unknowns、applicability、Rule Pack version 与 source candidate binding；未遗留 candidate verification state。

## 覆盖

- Rule Packs：`project-core`、`plugin-platform`、`test-automation-platform`，版本均为 `1.0.0`；31/31 Rule rows，各出现一次。
- Rule 状态：28 assessed、3 not_applicable、0 not_assessed。
- Critical flows：6/6 assessed，0 not_assessed。
- Selected Knowledge：13/13；Selection 与 compact Context 的锁和逐项哈希已验证。
- `coverage_complete: true`。

## 检查输入、证据与限制

本次回读了候选及其 4 个协调输入（repository facts、Profile、Knowledge Selection、Knowledge Context），Profile/constraints/critical flows/gate policy、3 个 Rule Pack、Provider 配置，以及固定提交中的 `architecture_tool.py`、Review/Provider/Decision Schema、Evidence Provider 与 solution-decision 契约、相关 Skill、Provider/Evolution/Review 测试。

限制如下：

- 当前项目 Provider 均 disabled，quality Provider 也未配置可运行 executable；本次没有生成或引用 Evidence Provider run，结论基于固定提交的 source/schema/contract/test evidence。
- 本地 Codex/model surface 不提供稳定的 token、prompt-cache 或真实模型行为 telemetry；compact Context 的实际 token/caching savings 未被本地静态证据证明。
- 当前工作树保留协调者提供的 4 个 input 与候选文件，未被本次修改；本报告未执行 Gate，因此不对 dirty-tree 下的 Gate outcome 作结论。
- HGM-EVOLUTION-001 的 threshold-outcome 关系没有实际已接受反例或明确的机器化契约证据，故保持 needs-evidence。
