# RS_CD 开源仓库路线图：按残差串联

这页不是单纯列仓库，而是回答一个更实用的问题：

**如果只看当前已经进入开源链的仓库，RS-CD 这条路线到底是怎样一步步被残差推出来的？**

这里采用当前项目的**实用标准**：

- 只要官方仓库已经公开；
- 并且至少放出了推理代码、训练代码或主要实现骨架；
- 就算它已经进入了我们的“开源路线”。

所以像 `UniChange` 这种“训练 / 推理代码已放、数据和 checkpoints 仍在补”的情况，这里也视为**已进入开源链**。

## 一、总判断

如果按开源仓库来读，`RS_CD` 的路线可以压成一句话：

**先解决“哪里变了”，再解决“如何用全局关系看变化”，再解决“怎样借大模型先验看变化”，接着解决“不给专门训练还能不能看变化”，最后才走到“变化能否被统一描述、提问和调度”。**

换成残差链，就是：

1. `局部差分不够稳`
2. `局部卷积看不见全局关系`
3. `监督 CD 的知识太窄`
4. `封闭类别限制真实场景`
5. `能出 mask 不等于能理解变化`

开源仓库正好把这条链留下来了。

## 二、第一阶段：光谱差分与 CNN 范式

### 这一阶段的核心问题

**双时相之间，哪些局部差异算“变化”？**

### 当前最该看的开源仓库

- [rcdaudt/fully_convolutional_change_detection](https://github.com/rcdaudt/fully_convolutional_change_detection)
- [justchenhao/STANet](https://github.com/justchenhao/STANet)
- [likyoo/Siam-NestedUNet](https://github.com/likyoo/Siam-NestedUNet)

### 这几个仓库分别代表什么

`FC-EF / FC-Siam` 代表的是最早的深度学习 CD 正式起点。  
它真正奠定的不是某个具体网络，而是三种最基本的双时相融合方式：

- 早融合
- 特征拼接
- 特征差分

`STANet` 代表的是纯 CNN 时期的成熟化。  
它开始显式问：单靠 Siamese 差分不够，能不能把跨时相注意力也加进去。

`SNUNet-CD` 则代表 CNN 这条线对“多尺度细节”和“稠密跳连”的极限压榨。

### 这一阶段真正解决了什么

- 让 change detection 从经典光谱差分正式进入深度监督表征
- 让“变化”第一次作为像素级学习对象稳定下来
- 把二值 CD 的标准输入输出范式定死：`A / B -> change map`

### 这一阶段的出口残差

**CNN 解决了局部表征，但没有真正解决全局关系。**

也就是：

- 很多变化并不是局部纹理差，而是更大的空间关系差
- 同一对象在不同位置、不同时间的外观变化很大
- 模型仍然主要是在问“哪里不一样”，还不是“这种不一样在全局里是否成立”

所以第二阶段必须出现。

## 三、第二阶段：Transformer 架构

### 这一阶段的核心问题

**变化能不能在全局关系里成立，而不只是局部卷积差分？**

### 当前最该看的开源仓库

- [justchenhao/BIT_CD](https://github.com/justchenhao/BIT_CD)
- [wgcban/ChangeFormer](https://github.com/wgcban/ChangeFormer)

### 这两个仓库分别代表什么

`BIT` 是 CD 真正把变化抬到 token 关系层的开始。  
它的关键不是“用了 Transformer”这么简单，而是：

- 把双时相图像压成少量 semantic tokens
- 在 token 空间建模跨时相关系
- 再把这种关系回写到像素空间

`ChangeFormer` 则把 Transformer CD 做成了一条正式可复用路线。  
如果说 `BIT` 是关键拐点，`ChangeFormer` 就是这条拐点后真正被社区接受的结构化版本。

### 这一阶段真正解决了什么

- 让变化从局部 patch 差异，升级成全局语境里的关系差异
- 让“同一类变化在远距离上下文中的一致性”第一次被正式建模
- 让 CD 有能力处理更复杂的空间依赖，而不只是边缘和局部形变

### 这一阶段的出口残差

**Transformer 解决了全局关系，但没有解决知识来源。**

问题变成：

- 模型仍然严重依赖监督数据
- change map 仍然多是封闭集、二值、像素级目标
- 它会“看关系”，但不会“借更广泛的世界知识来看变化”

所以第三阶段不是继续堆结构，而是借 foundation model。

## 四、第三阶段：基础模型迁移

### 这一阶段的核心问题

**CD 自己的监督太窄，能不能借更大的视觉 / 语言先验？**

### 当前最该看的开源仓库

- [KyanChen/TTP](https://github.com/KyanChen/TTP)
- [dyzy41/ChangeCLIP](https://github.com/dyzy41/ChangeCLIP)
- [likyoo/BAN](https://github.com/likyoo/BAN)
- [ViTAE-Transformer/MTP](https://github.com/ViTAE-Transformer/MTP)
- [KyanChen/RSPrompter](https://github.com/KyanChen/RSPrompter)

### 这几个仓库分别在补什么残差

`TTP`：补的是 **SAM 不懂双时相**。  
它试图把单图 foundation model 的 latent knowledge 拉进双时相变化场景。

`ChangeCLIP`：补的是 **CD 没有开放语义锚点**。  
它把变化检测接到语言-视觉对齐空间。

`BAN`：补的是 **单一 foundation model 各有盲区**。  
SAM 会分但不懂语义，CLIP 懂概念但不会精定位，DINOv2 稳但不懂文本；所以要做统一 adapter。

`MTP`：补的是 **下游迁移太被动**。  
不是等 change detection 来了再适配，而是在预训练阶段就把多任务遥感知识压进去。

`RSPrompter`：虽然不是 CD 本体论文，但它是理解 SAM / prompt 路线在遥感里如何落地的重要代码入口。

### 这一阶段真正解决了什么

- CD 不再只靠自己那点监督数据
- 变化开始被更强的视觉先验、语义先验和遥感基础模型先验约束
- 社区开始承认：CD 不是孤立任务，而是 foundation model 适配问题

### 这一阶段的出口残差

**能力虽然更强了，但大多是借来的。**

也就是：

- 变化的定义仍然不够开放
- 类别仍然常常是封闭的
- 模型会利用大模型先验，但变化本身还不是一个开放可查询对象

所以第四阶段自然会问：

**如果不给 CD 专门训练，它还能不能靠 foundation prior 直接工作？**

## 五、第四阶段：开放词汇与免训练

### 这一阶段的核心问题

**不给专门训练，变化还能不能被开放词汇地召回？**

### 当前最该看的开源仓库

- [Z-Zheng/pytorch-change-models](https://github.com/Z-Zheng/pytorch-change-models) `AnyChange`
- [Dmygithub/AdaptOVCD](https://github.com/Dmygithub/AdaptOVCD)
- [yogurts-sy/Seg2Change](https://github.com/yogurts-sy/Seg2Change)
- [NKU-HLT/UniChange](https://github.com/NKU-HLT/UniChange) 的一部分开放词汇入口也值得顺带看

### 这几个仓库分别代表什么

`AnyChange`：代表 **Segment-Everything + mask matching** 这一条。  
它的思想非常干净：先把两时相都分出来，再去找不再对应的实例。

`AdaptOVCD`：代表 **training-free pipeline systemization**。  
它不是只证明“可以做”，而是把完整流程做出来：特征、差分、融合、精修。

`Seg2Change`：代表 **把 open-vocabulary segmentation 直接适配成 OVCD**。  
也就是说，不再把变化当成单独训练的大任务，而是把现有 OVS 能力转接过来。

### 这一阶段真正解决了什么

- 变化开始摆脱封闭类别约束
- 变化开始支持 query-conditioned / open-vocabulary 的调用方式
- 变化第一次在实用上接近“你想查什么，就去找什么变化”

### 这一阶段的出口残差

**会找变化，不等于会理解变化。**

当前这些方法仍然主要输出：

- mask
- proposal
- open-vocabulary label

但它们还不真正回答：

- 发生了什么变化
- 为什么这类变化重要
- 这个变化和上下文、任务、对话怎样统一

所以第五阶段会出现变化理解系统。

## 六、第五阶段：变化理解与统一系统

### 这一阶段的核心问题

**变化能不能不只是一张图，而成为可描述、可提问、可统一调度的对象？**

### 当前最该看的开源仓库

- [Chen-Yang-Liu/Change-Agent](https://github.com/Chen-Yang-Liu/Change-Agent)
- [ermongroup/TEOChat](https://github.com/ermongroup/TEOChat)
- [Bili-Sakura/RSCC](https://github.com/Bili-Sakura/RSCC)
- [NKU-HLT/UniChange](https://github.com/NKU-HLT/UniChange)

### 这几个仓库分别代表什么

`Change-Agent`：代表 **从单任务模型到工具调度系统**。  
变化不再只是检测，而是检测、caption、计数、分析一起调度。

`TEOChat`：代表 **时序 EO VLM**。  
它已经不只盯着双时相 change map，而是在更大的时序 EO assistant 里处理变化。

`RSCC`：代表 **变化理解的数据和评测基座**。  
它的重要性不在单模型，而在于它给“变化描述”这件事提供了一个公开基准。

`UniChange`：代表 **统一 BCD / SCD / MLLM 的方向**。  
即便它还不是完整放全的数据权重生态，也已经说明：变化检测正在从单任务头，转成统一多模态框架。

### 这一阶段真正解决了什么

- 变化开始被描述、问答、交互化
- 二值 CD、语义 CD、caption、agent 调度开始统一到一条线
- 变化开始从“图像差异”升级成“可被语言组织的任务对象”

### 这一阶段的出口残差

**任务统一了，但变化仍然不等于世界状态。**

现在这些系统大多还是：

- 把变化作为一次性输入输出任务处理
- 借 LLM / VLM 去描述它
- 但没有真正把“变化”持有成长期、稳定、可反复调用的时序状态对象

这就是整个 `RS_CD` 当前最深的残差。

## 七、如果按“开源仓库学习顺序”来走

最稳的顺序不是按发表年份扫，而是按残差难度走：

1. `FC-EF / FC-Siam`
2. `STANet`
3. `SNUNet-CD`
4. `BIT`
5. `ChangeFormer`
6. `TTP`
7. `ChangeCLIP`
8. `BAN`
9. `MTP`
10. `AnyChange`
11. `AdaptOVCD`
12. `Seg2Change`
13. `Change-Agent`
14. `TEOChat`
15. `RSCC`
16. `UniChange`

这样走的原因是：

- 前 1-5 个让你把传统 CD 主线完全吃透；
- 6-9 个让你看清 foundation model 是怎么接进来的；
- 10-12 个让你看清开放词汇和免训练如何形成；
- 13-16 个才是变化理解系统层。

## 八、最终压缩版

如果把整套开源路线再压成最短的一句：

**FC-Siam 系列把“变化”变成可学习对象，BIT / ChangeFormer 把它抬到全局关系层，TTP / ChangeCLIP / BAN / MTP 把它接上 foundation prior，AnyChange / AdaptOVCD / Seg2Change 把它推向开放词汇与免训练，Change-Agent / TEOChat / RSCC / UniChange 则开始把它做成变化理解系统。**

而整个链条最深的残差直到现在还没真正被吃掉：

**变化语义仍然大多是借来的，而不是 RS-CD 自己持有的稳定时序状态。**
