# 中文翻译工程说明

本目录存放 Khronos Vulkan Tutorial 简体中文翻译的**工具与规范**，译文本身在仓库根的 `zh/` 目录。

## 目录约定

| 路径 | 作用 |
| --- | --- |
| `zh/` | 译文，与 `en/` 结构一一对应；根级文档为 `zh/README.adoc` 等；附件说明为 `zh/attachments/.../README.adoc` |
| `antora-zh/` | 中文 Antora 组件：`antora.yml`、`nav.adoc`、`build.py`（跨平台装配脚本） |
| `antora-zh-playbook.yml` | 中文站点构建入口 |
| `translation/GLOSSARY.md` | 术语表与翻译规范（**唯一权威**） |
| `translation/titles_en.json` / `titles_zh.json` | 全库文档标题 → 规范中文标题 |
| `translation/documents.json` | 源文件 ↔ 目标文件清单（457 条） |
| `translation/batches/*.json` | 分批清单，每批 ≤ 6000 词、≤ 10 个文件 |
| `translation/verify.py` | 结构校验器 |
| `translation/build_plan.py` | 重新生成清单与批次 |
| `translation/build_nav.py` | 由英文 nav 生成中文 nav |

## 翻译一篇的流程

1. 在 `translation/batches/` 找到该文件所属批次 JSON。
2. 按 `translation/GLOSSARY.md` 翻译；代码块、xref/link/image 目标、锚点、属性行保持原样。
3. 写入 `zh/` 下对应路径。
4. 校验：`python translation/verify.py --file <源文件>`，必须 `PASS`。

## 常用命令

```bash
python translation/build_plan.py              # 生成清单与批次（源文件增删后运行）
python translation/verify.py --missing        # 还有哪些没译
python translation/verify.py --summary        # 按课程统计进度
python translation/verify.py                  # 校验全部已译文件
python translation/verify.py --batch b003     # 校验单个批次
```

校验内容：字面块逐行一致、`xref/link/image/include` 目标序列一致、`[[锚点]]` 集合一致、标题层级一致、属性行一致、无残留整行英文正文。

## 构建中文站点

```bash
cd antora-zh
python build.py            # 或 make（CI/Linux）
cd ..
npx antora antora-zh-playbook.yml
```

`build.py` 会把 `zh/` 装配成 `antora-zh/modules/ROOT/pages`，把 `images/` 装配成 `modules/ROOT/images/images`（与 `antora/Makefile` 的做法一致，保证 `/images/...` 链接可用），并复用 `attachments/`。

## 新增或修改英文原文后

1. 重新运行 `python translation/build_plan.py`。
2. `python translation/verify.py --missing` 找出新增文件。
3. 翻译新增文件；如果原文被改动，`verify.py` 会在对应文件报 FAIL，按提示更新译文。
