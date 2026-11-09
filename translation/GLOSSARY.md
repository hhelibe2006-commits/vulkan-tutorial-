# 翻译规范与术语表（简体中文）

本文件是 `zh/` 目录全部译文的唯一权威规范。所有译者（包括自动化代理）必须严格遵守。

## 1. 语体与读者

- 面向**有编程基础、正在学习 Vulkan 的开发者**，简体中文技术教程口吻。
- 用第二人称**「你」**（不用「您」）。
- 语言简洁、直接、可执行；避免翻译腔（"被进行"、"将会被"、"成功地"之类）。
- 保留原文的**信息密度与段落顺序**，不合并、不拆分、不"优化"、不增删内容、不加译者注。
- 疑问句、口语化引导句（如 "Let's go!"）译成自然中文（"出发吧！"）。

## 2. 结构保真（硬性要求，校验脚本会检查）

1. **代码块与字面块内容一字不改**：由 `----`、`....`、`++++`、`====`、`****`、`____`、`--` 界定的块，以及 `[source,...]` 后的代码，全部原样保留（含缩进、空行、注释）。
2. **不翻译**：行内代码 `` `...` ``、函数名、类型名、枚举值、宏、变量名、命令行、文件路径、URL、SPDX/版权头、`//` 注释行。
3. **指令目标不变，只译显示文本**：
   - `xref:路径.adoc[显示文本]` → 路径不变，只译显示文本。
   - `link:URL[显示文本]` → URL 不变，只译显示文本。
   - `image::/images/x.png[替代文本]` → 路径不变，替代文本可译。
   - `include::...[]` → 完全不变。
4. **锚点与属性行不变**：`[[id]]`、`[#id]`、`:attr:`、`[source,c++]`、`[,c++]`、`[NOTE]` 等原样保留。
5. **提示块关键词保留**：`NOTE:`、`TIP:`、`WARNING:`、`IMPORTANT:`、`CAUTION:` 保留英文大写加冒号，其后正文译成中文。
6. **标题层级不变**：`=`、`==`、`===` 数量与位置不变；标题文字按第 5 节规范译名。
7. **列表、表格、空行节奏不变**：`*`、`**`、`|===` 等结构符号不动。
8. **交叉引用显示文本**必须与目标章节的中文标题一致（见 `translation/titles_zh.json`）。

## 3. 标点与排版

- 使用中文全角标点：，。；：？！（）——、……「」或""。
- **中英文之间加一个半角空格**：`Vulkan 1.4 引入了动态渲染`。
- 行内代码与中文之间同样加空格：`vkCreateInstance` 函数。
- 数字、版本号、单位、百分比原样：`1920×1080`、`60 FPS`、`16 ms`。
- 括号内为纯英文标识时用半角括号并保留空格，例如 `（`VK_SUCCESS`）` 应写成 `（`VK_SUCCESS`）` 中的代码保持反引号。

## 4. 术语表（必须遵守）

### 4.1 Vulkan 核心对象

| 英文 | 中文 | 备注 |
| --- | --- | --- |
| instance | 实例 | `VkInstance` 不译 |
| physical device | 物理设备 | |
| logical device | 逻辑设备 | |
| queue / queue family | 队列 / 队列族 | |
| surface / window surface | 表面 / 窗口表面 | `VkSurfaceKHR` 不译 |
| swap chain | 交换链 | |
| swap chain image | 交换链图像 | |
| image | 图像 | 与 texture 区分 |
| image view | 图像视图 | |
| sampler | 采样器 | |
| combined image sampler | 组合图像采样器 | |
| buffer | 缓冲区 | |
| vertex buffer | 顶点缓冲区 | |
| index buffer | 索引缓冲区 | |
| uniform buffer | 统一缓冲区 | |
| storage buffer | 存储缓冲区 | |
| staging buffer | 暂存缓冲区 | |
| device memory / host memory | 设备内存 / 主机内存 | |
| allocation | 分配 | |
| descriptor | 描述符 | |
| descriptor set | 描述符集 | |
| descriptor pool | 描述符池 | |
| descriptor set layout | 描述符集布局 | |
| push constant | 推送常量 | |
| pipeline | 管线 | graphics pipeline = 图形管线 |
| pipeline layout | 管线布局 | |
| shader | 着色器 | |
| shader module | 着色器模块 | |
| specialization constant | 特化常量 | |
| render pass | 渲染通道 | 本项目使用动态渲染，但概念讲解时保留 |
| subpass | 子通道 | |
| attachment | 附件 | 渲染附件 |
| framebuffer | 帧缓冲区 | |
| command buffer | 命令缓冲区 | 录制动词：record = 录制 |
| command pool | 命令池 | |
| submission / submit | 提交 | |
| fence | 栅栏 | |
| semaphore | 信号量 | |
| timeline semaphore | 时间线信号量 | |
| pipeline barrier | 管线屏障 | |
| memory barrier | 内存屏障 | |
| access / availability / visibility | 访问 / 可用性 / 可见性 | |
| query / occlusion query | 查询 / 遮挡查询 | |
| timestamp query | 时间戳查询 | |
| extension | 扩展 | |
| layer / validation layer | 层 / 验证层 | |
| feature | 特性 | |
| capability | 能力 | |
| device address | 设备地址 | |
| handle | 句柄 | |
| RAII | RAII | 不译 |
| Vulkan-Hpp | Vulkan-Hpp | 不译 |

### 4.2 图形管线与光栅化

| 英文 | 中文 |
| --- | --- |
| rasterization | 光栅化 |
| vertex / fragment / compute shader | 顶点 / 片元 / 计算着色器 |
| fragment | 片元 |
| primitive | 图元 |
| triangle | 三角形 |
| viewport | 视口 |
| scissor | 剪刀矩形 |
| culling / back-face culling | 剔除 / 背面剔除 |
| depth test / depth buffer | 深度测试 / 深度缓冲区 |
| stencil | 模板 |
| blending / alpha blending | 混合 / alpha 混合 |
| multisampling / MSAA | 多重采样 |
| mipmap / mip level | mipmap / mip 层级 |
| mipmapping | mipmap 生成 |
| anisotropy / anisotropic filtering | 各向异性 / 各向异性过滤 |
| texture | 纹理 |
| texture sampling | 纹理采样 |
| UV coordinate | UV 坐标 |
| clip space / NDC | 裁剪空间 / 规范化设备坐标（NDC） |
| perspective projection | 透视投影 |
| normal / tangent / bitangent | 法线 / 切线 / 副切线 |
| transform / transformation matrix | 变换 / 变换矩阵 |
| pivot | 轴心 |
| mesh | 网格 |
| model / scene graph | 模型 / 场景图 |
| culling / frustum culling | 剔除 / 视锥剔除 |
| draw call | 绘制调用 |
| present / presentation | 呈现 / 呈现 |
| frames in flight | 飞行帧 |
| refresh rate | 刷新率 |
| tearing | 撕裂 |
| double / triple buffering | 双缓冲 / 三缓冲 |
| dynamic rendering | 动态渲染 |
| local read | 本地读取（`VK_KHR_dynamic_rendering_local_read` 不译） |

### 4.3 计算、同步、性能

| 英文 | 中文 |
| --- | --- |
| compute pipeline | 计算管线 |
| workgroup | 工作组 |
| subgroup | 子组 |
| invocation | 调用（线程实例） |
| dispatch | 派发 |
| shared memory / LDS | 共享内存 / 本地数据共享（LDS） |
| occupancy | 占用率 |
| latency hiding | 延迟隐藏 |
| memory model | 内存模型 |
| memory consistency | 内存一致性 |
| coherence | 一致性 |
| warp / wavefront | 波前（按厂商保留 warp / wave） |
| cooperative matrix | 协作矩阵 |
| mixed precision | 混合精度 |
| quantization | 量化 |
| throughput | 吞吐量 |
| bottleneck | 瓶颈 |
| overhead | 开销 |
| profile / profiling | 性能分析 |
| GPU-driven | GPU 驱动 |
| indirect draw / dispatch | 间接绘制 / 间接派发 |
| bindless | 无绑定 |
| zero-copy | 零拷贝 |
| readback | 回读 |

### 4.4 光线追踪

| 英文 | 中文 |
| --- | --- |
| ray tracing | 光线追踪 |
| ray query | 光线查询 |
| acceleration structure | 加速结构 |
| BLAS / TLAS | BLAS / TLAS（不译，首次可注"底层/顶层加速结构"） |
| shadow ray | 阴影光线 |
| reflection / refraction | 反射 / 折射 |
| denoising | 降噪 |
| opacity micromap | 不透明度微图 |

### 4.5 ML / OpenXR / 引擎

| 英文 | 中文 |
| --- | --- |
| machine learning / ML | 机器学习 / ML |
| inference | 推理 |
| training | 训练 |
| neural network | 神经网络 |
| layer (NN) | 层 |
| tensor | 张量 |
| weight / bias | 权重 / 偏置 |
| activation function | 激活函数 |
| convolution | 卷积 |
| pooling | 池化 |
| forward propagation | 前向传播 |
| backpropagation | 反向传播 |
| transfer learning | 迁移学习 |
| fine-tuning | 微调 |
| LoRA | LoRA（不译） |
| quantization | 量化 |
| ONNX / NNEF / TFLite | 不译 |
| model format | 模型格式 |
| OpenXR | 不译 |
| runtime | 运行时 |
| session | 会话 |
| swapchain (XR) | 交换链 |
| action / action space | 动作 / 动作空间 |
| pose | 位姿 |
| foveated rendering | 注视点渲染 |
| variable rate shading | 可变速率着色 |
| late latching | 延迟锁存 |
| comfort | 舒适度 |
| presence | 临场感 |
| engine / rendering engine | 引擎 / 渲染引擎 |
| renderer | 渲染器 |
| scene | 场景 |
| component / entity | 组件 / 实体 |
| subsystem | 子系统 |
| frame / frame time | 帧 / 帧时间 |
| asset pipeline | 资产管线 |
| PBR | PBR（基于物理的渲染） |
| shadow map | 阴影贴图 |
| light / lighting | 光照 / 光照 |
| material | 材质 |
| shader compilation | 着色器编译 |
| SPIR-V / Slang / GLSL / HLSL | 不译 |

## 5. 标题规范

- 一律使用 `translation/titles_zh.json` 中的规范译名；该文件覆盖全库所有文档标题。
- 正文中的 `xref:` 显示文本若指向某章节，必须与该章节中文标题完全一致。
- 标题不加标点结尾；疑问句标题可保留问号。
- 专有名词保持原文：`Vulkan`、`Slang`、`Vulkan-Hpp`、`OpenXR`、`glTF`、`SIGGRAPH`。

## 6. 交付与校验

- 每个源文件对应 `zh/` 下同路径文件；不得遗漏、不得合并文件。
- 译文写完后运行 `python translation/verify.py --file <源文件路径>` 自检；必须 `PASS`。
- 校验内容：代码块逐行一致、`xref/link/image/include` 目标序列一致、`[[id]]` 集合一致、标题行数与层级一致、无残留整行英文正文。
