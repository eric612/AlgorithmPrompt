## Config Register Rule

概要：寄存器分为 `CONTROL`（基础/平台/时序）与 `ALGORITHM`（校准/数据）两类。所有运行时参数必须在寄存器表中列出，并标明 `Shadow`、`Lifetime` 与 `Category`。

重要变更：关于 `Shadow` / 更新时序的规范已抽取到独立文件：`_rules/shadow_update_semantics.md`（请以该文件为唯一权威）。

要点回顾：

- `Category`：`CONTROL` 或 `ALGORITHM`。若某 `CONTROL` 寄存器的修改会直接改变像素数学结果（可视觉观测），应重新分类为 `ALGORITHM` 或附带 C-simulatable 验证向量。
- `Shadow` 字段：必须填写，取值见 `shadow_update_semantics.md` 中的枚举（例如 `FRAME_BOUNDARY`, `STAGED_COMMIT` 等）。
- `Lifetime`：`BOOT_ONLY` 或 `RUNTIME`，表明能否在运行时修改。

寄存器表示例（必须包含下列列）：

| Register | Bits | Type | Default | Shadow | Lifetime | UpdateTrigger | Category | Description |
|---|---:|---|---:|---:|---:|---:|---:|---|
| LUT_BASE_A | AXI_ADDR | - | 0 | DOUBLE_BUFFER | RUNTIME | COMMIT | ALGORITHM | 主 LUT 槽 A 基址 |
| GLOBAL_GAIN | U12.10 | - | 1024 | FRAME_BOUNDARY | RUNTIME | AUTO_FRAME | ALGORITHM | 全局放大系数 |
| OUTPUT_RING_DEPTH | U8 | - | 32 | STATIC | BOOT_ONLY | - | CONTROL | SoC 集成选择，boot-only |

参见 `_rules/shadow_update_semantics.md` 获取完整语义、PR 清单与校验建议（建议把自动检查脚本集成到 CI）。
