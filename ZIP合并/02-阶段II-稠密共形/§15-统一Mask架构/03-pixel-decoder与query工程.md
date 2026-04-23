# §1 · FPN 回顾 —— 特征金字塔的构造细节

你记得"特征金字塔网络"但忘了具体搭法。先复习。

**Backbone (ResNet-50) 的天然四层输出**：

```
输入 H×W×3
  ↓ stem (7×7 conv, stride 2)
  ↓ maxpool (stride 2)
C2 = H/4  × W/4  × 256    ← stage 2 后
  ↓ stride 2
C3 = H/8  × W/8  × 512    ← stage 3 后
  ↓ stride 2
C4 = H/16 × W/16 × 1024   ← stage 4 后
  ↓ stride 2
C5 = H/32 × W/32 × 2048   ← stage 5 后
```

这四层的性质很固定：

- **越深**：channel 越多、分辨率越低、语义越强、空间越粗
- **越浅**：反之——空间精细但语义弱（只学到边缘/纹理）

**FPN 的核心问题**：单独一层 C_k 没法同时满足"大物体要低分辨率 + 小物体要高分辨率 + 所有都要强语义"的矛盾需求。

**FPN 的构造（三步）**：

```
(1) Lateral 1×1 conv: 把 C2/C3/C4/C5 的 channel 都压到 256 (统一)

(2) Top-down upsample + add:
    P5 = lateral(C5)
    P4 = lateral(C4) + upsample_2x(P5)    ← 高层语义注入
    P3 = lateral(C3) + upsample_2x(P4)
    P2 = lateral(C2) + upsample_2x(P3)

(3) 3×3 conv smoothing: 每个 P_k 再过一次 3×3 conv 消除上采样的混叠
```

**结果**：P2-P5 四层，都是 256 channel，但分辨率递减，**每层都同时包含"本层空间精细度 + 所有上层注入的语义"**。

**所以 FPN 不是瓶颈层**。它不是"压缩到一个最小表征再展开"——它是**多尺度特征的横向增强器**：每一尺度的 feature 都被"更高层的语义"补齐。你把它当成"语义在多尺度上的等势面分布"来理解更准确。

上采样用的是**最近邻插值（nearest upsample）**——无参数、不引入可学习组件，只做空间平铺。语义注入靠的是 lateral 的加法。

---

# §2 · Pixel decoder = FPN 的继承者 + 升级版

Pixel decoder 和 FPN 做同一件事，但更强。三代演进：

**(a) FCN 式 decoder (2015)**: transposed conv 逐层上采样——棋盘效应、参数多

**(b) FPN (2017)**: 最近邻 upsample + lateral add——简洁、强壮

**(c) MSDeformAttn-based pixel decoder (Mask2Former)**: 用 6 层 deformable attention encoder 跨尺度融合——比 FPN 的加法更灵活

Mask2Former 的 pixel decoder 输出的不是四个金字塔层，而是**一个 1/4 分辨率的高分辨率 feature + 三个金字塔层**。前者（1/4 res）专门给"mask 生成"用，后者给 transformer decoder 的 cross-attention 轮流用（§2.2 那里讲过）。

**关键转变**：名字从 "feature map"（CNN 语境）变成 "pixel embedding"（transformer 语境）——**同一个张量，不同的语义叙事**。下一节讲这个。

---

# §3 · "通道 = embedding size" 这个理解对不对

**结论：数学上完全对，语义叙事不同**。

[H, W, C] 这个 shape 从来没变过。变的是人对 C 的解读：

| 时代 | 对 C 的叙事 | 暗示的下游操作 |
| --- | --- | --- |
| AlexNet / VGG (2012-14) | **"filter 响应"** | 每个 channel = 某个卷积核的激活强度 |
| ResNet / FCN (2015-16) | **"feature channel"** | channel 间可以 concat / add / 1×1 conv 混合 |
| ViT / MaskFormer (2020+) | **"per-token embedding"** | 每个位置是一个向量，要和别的向量做点积/attention |

**叙事变化对应范式变化**：

- "filter 响应"的叙事下，后面接的是**又一层卷积**（继续学更高层特征）或**分类头**（C 维和类别概率挂钩）
- "embedding"的叙事下，后面接的是**点积 / attention / 相似度**——这是**表征学习 → retrieval/matching** 的思维切换

MaskFormer 论文里坚持叫 "pixel embedding" 而不叫 "feature map"，**本身就是一种范式宣告**：

> 我不再把这个张量当成"给分类头的输入"，我把它当成"一个可以被 query 检索的表征场"。
> 

你理解对了。**通道 = 视觉里的 embedding size** 这个等式是成立的；但理解为"embedding"还是"feature channel"，决定了后续操作的形状——这是一个**心智模型层面的区分**，不是数学层面的区分。

---

# §4 · 分割里 C 维向量 → per-pixel 分类 = "隐式 query"

**你这个洞察是整个 MaskFormer 工作的魂**。让我把它形式化，你会看到它比你想的还要深。

## 4.1 FCN 的最后一层到底在做什么

FCN 倒数第二步：得到 pixel embedding $E_{pix} in mathbb{R}^{HW times D}$（D 一般是 256 或 512）

FCN 最后一步：class head 是一个**线性层** $W_{cls} in mathbb{R}^{D times (K+1)}$（K 是类别数）

```
logits = E_pix @ W_cls         shape [HW, K+1]
         每一行是像素 i 的 K+1 个 logit
pred[i] = argmax(softmax(logits[i]))
```

**关键观察**：$W_{cls}$ 的第 c 列 $W_{cls}[:, c] \in \mathbb{R}^D$ 是什么？

**它是"第 c 类的类原型向量"（class prototype）**。

所以：

$$

text{logits}[i, c] = E_{pix}[i] cdot W_{cls}[:, c]

$$

**这就是一个点积**。像素 i 的 embedding 和第 c 类的原型向量的**对齐度**。

**把 FCN 的分类头展开来读**：

> 每个像素和 K 个可学习的"类原型向量"做点积，看自己最像哪一个。
> 

**你的洞察完全命中**——**FCN 的分类头就是 K 个隐式 query**！每个 class prototype 是一个"查询向量"，查询"你这个像素是不是属于我这类"。

## 4.2 MaskFormer 做了什么变形

FCN:

```
K 个类原型 × D  →  每个像素对 K 个原型点积  →  argmax → 像素类别
```

MaskFormer:

```
N 个 mask query × D  →  每个像素对 N 个 query 点积 → sigmoid → 每个 query 的 mask
                       ↓
                    每个 query 还有独立的 class head (K+1 维 softmax)
```

**两处改动**：

**(1) 解耦 N 和 K**

- FCN: query 数量 = 类别数。换数据集（类别数变）必须换分类头
- MaskFormer: query 数量 N 固定（=100），类别数 K 由独立的 class head 承担——**这两个维度解耦**
- 这个解耦就是**开放词汇的前提**——只要把 class head 换成 CLIP text similarity，类别数就可以无限

**(2) 改变 query 的 argmax 方向**

- FCN 的 argmax 是"**对每个像素**在 K 个 query 里选一个"——像素是主体
- MaskFormer 的操作是"**对每个 query**在 HW 个像素里激活一组"——query 是主体

**第二点看似微妙，实则是本体论翻转**：

- FCN 世界观：像素是第一公民，每个像素独立选类
- MaskFormer 世界观：query 是第一公民，每个 query 自己认领一片像素

这就是为什么 MaskFormer 能自然扩展到"实例分割"——每个 query 认领的像素就是一个实例。FCN 做不到，因为 FCN 的公民是像素，同类像素没法被拆成两个实例。

## 4.3 把你的话彻底精确化

你说的这句：

> 分割中的各个类的概率其实也是一个隐式 query，代表的是在一个类别形状库里面，和这里的各个形状的相似度分别有多少。这里的 C 的形状库大小和类别数解耦了。
> 

精确版本：

> FCN 的 per-pixel classification 可以**等价重写**为"每个像素查询 K 个可学习的类原型向量"。
> 

> 
> 

> 这是一个**形状数量等于类别数 K**的隐式查询库——K 是 prototypes 的个数，不是每个 prototype 的维度；每个 prototype 是 D 维。
> 

> 
> 

> MaskFormer 做的事：把"prototype 数 = K"改成"prototype 数 = N（任意）"，并把类别识别 offload 到独立的 class head 上。**prototype 库的大小 N 和类别数 K 彻底解耦**。
> 

你原话里混了"prototype 数"和"prototype 维度"（你说的 C 其实指 prototype 数），但核心洞察完全对。

## 4.4 一句话总结

**FCN 和 MaskFormer 数学上是同构的。区别只在"prototype 数 = 类别数"这一绑定是否被打破。打破之后，所有开放词汇/prompt-based 工作才有落脚点**。

这是**解耦**在深度学习里一次极漂亮的案例——把两个历史上被捆绑的维度拆开，下游能力空间立刻爆炸式扩张。

---
