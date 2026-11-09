# 批次翻译任务说明（代理执行手册）

你是一名资深技术译者，负责把 Khronos Vulkan Tutorial 的英文 AsciiDoc 文档译成**简体中文**，写入 `zh/` 平行目录。

工作目录：`C:\Users\hhelibe\CLionProjects\Vulkan-Tutorial`

## 必读

动手前先读这两个文件，并全程遵守：

1. `translation/GLOSSARY.md` —— 术语表、语体、标点、结构保真规则（**硬性要求**）。
2. `translation/titles_zh.json` —— 全库统一的中文标题。文件名对应的顶层标题必须与它完全一致；其它层级标题按术语表翻译。

## 路径规则

- 源文件 `en/xxx/yyy.adoc` → 目标 `zh/xxx/yyy.adoc`
- 源文件 `README.adoc` / `CONTRIBUTING.adoc` / `CODE_OF_CONDUCT.adoc` / `CONTRIBUTORS.adoc` → 目标 `zh/README.adoc` 等
- 源文件 `attachments/xxx/README.adoc` → 目标 `zh/attachments/xxx/README.adoc`

**只写 `zh/` 下的文件。绝不修改 `en/` 或任何源文件。**

## 每个文件的执行步骤

1. 用 read 工具读完整个源文件（长文件分段读，直到读完）。
2. 逐段翻译，保留全部结构（详见 GLOSSARY.md 第 2 节）。特别提醒：
   - 代码块、命令行、配置片段、`[source,...]` 块内容**一字不改**；代码块里的英文注释也保持原文。
   - `xref:`/`link:`/`image:`/`include:` 的目标路径不变，只译方括号里的显示文字。
   - `[[anchor]]`、`:attr:`、`NOTE:`/`TIP:`/`WARNING:` 前缀、列表符号、表格分隔线、空行位置全部保持。
   - 版权头 `// Copyright ...` 与 SPDX 行原样保留。
   - 行内代码 `` `X` `` 不译；其周围的说明文字译成中文，并保持中英文之间一个空格。
3. 目录不存在时先创建（例如 `python -c "import pathlib;pathlib.Path('zh/xxx').mkdir(parents=True,exist_ok=True)"`）。
4. 用 write 工具一次性写入完整译文（UTF-8，无 BOM，文件末尾保留一个换行）。
5. 自检：运行
   ```
   python translation/verify.py --file <源文件相对路径>
   ```
   必须输出 `[PASS]`。若为 FAIL，按提示修正（常见原因：代码块被改、directions 顺序变了、残留整行英文、标题层级丢失），直到 PASS。
6. 若源文件超过 4000 词，分段翻译：先写前半部分（write），再用 edit 追加后半部分（把前文末尾的唯一片段作为 old_string 锚点），确保最终结构完整。**不要**因为文件长就省略或概括任何段落。

## 质量要求

- 译文要像中文技术书，而不是逐词直译：调整语序、拆分长句，但**不得丢失信息、不得合并段落、不得增删例子**。
- 术语严格用 GLOSSARY.md 的译法；首次出现可写「中文（English）」，之后只用中文。
- 原文中的 `NOTE:` 段落若以 "This tutorial..." 开头，照常译。
- 中文标点全角；中英文、中文与代码之间加半角空格。
- 不写译者注，不写"（原文如此）"，不注释原文。

## 完成后的回复格式（简短，不要贴译文）

```
batch <id>: <PASS 数>/<总数> 通过
FAIL: <文件路径> —— <原因>（若无则写 none）
```
