# 研究线 A：JEPA / 预测式表征一手来源梳理

日期：2026-04-23  
范围：优先 2023-2026；只收论文、OpenReview、CVF Open Access、arXiv 官方页、Meta 官方博客/机构页。  
服务对象：`§45-JEPA与预测式表征`、`§46-图像中的世界状态持有`

## 一、10 条以内高价值结论

1. **JEPA 的本体不是“遮挡后再补全”，而是“给定上下文，预测另一区域的抽象状态表示”。**  
   2022 的 JEPA 位置论文已经把这一点写死：其优势是**在表征空间预测**，从而可以**消除无关细节**，例如路边树木纹理、地面材质等。

2. **所谓“抽象状态预测”，核心不是不要信息，而是不要那些对后续判断不必要、且天然多解的像素细节。**  
   I-JEPA 的可视化实验直接显示：预测器保留了高层对象部件与姿态，但丢弃精确纹理和背景细节。这正是“状态”与“像素”的分水岭。

3. **JEPA 相比 MAE/BEiT 的真正差异，不只是 loss 从 pixel/token 换到 embedding；而是“理解对象”从可见样本换成潜在状态。**  
   MAE/BEiT 仍要求恢复观测本身；JEPA 允许目标编码器先把观测压成抽象表示，再让预测器去对准这个表示。

4. **I-JEPA 是图像阶段最干净的范式化落地。**  
   它不依赖手工 view augmentations，不做像素重建，而是用大目标块 + 分布式上下文块，把模型推向语义级和结构级表征。

5. **I-JEPA 的最强图像证据不是“分类更高一点”，而是它在 object counting、depth prediction 等任务上优于 MAE，并且在计算效率上明显更优。**  
   这说明 latent prediction 抓到的不是只服务分类的语义，而是更接近结构性、几何性中间变量。

6. **到 2025，纯视觉 SSL 的最强图像证据已不再只靠 I-JEPA 单篇，而是扩展为“language-free scaling + dense feature stability”这一更大阵地。**  
   `Scaling Language-Free Visual Representation Learning` 证明在同数据控制下，纯视觉 SSL 可以达到 CLIP 级表现；`DINOv3` 则把 dense feature degeneration 这个老问题正面解决。  
   这两者严格说不全是 JEPA，但它们是你阶段 V 主张在图像线上的最强补强。

7. **V-JEPA 把同一原则从图像推到视频：预测 feature，而非生成 frame。**  
   但一旦进入时间维，它就已经不只是“图像中的世界状态”，而开始接近“物理世界演化的状态预测”。

8. **V-JEPA 2 是 2025 的真正前沿跃迁点，但它已经不是纯图像阶段 V 的核心证据，而是阶段 V 向“视频世界模型 / 行动规划”外延的接口。**  
   它的亮点是 understanding / prediction / planning 三件事合一；但这也意味着它超出了 `§46` 应该承担的收敛范围。

9. **最前沿结果同时说明两件事：JEPA 路线有效，但“世界状态持有”还远未闭合。**  
   一方面，V-JEPA 2 已经能做零样本机器人规划；另一方面，Meta 同期发布的 `IntPhys 2` 与 `CausalVQA` 显示当前前沿模型在直觉物理、反事实与预期问题上仍明显落后于人类。

## 二、关键一手来源与用途

1. **2022-06-27｜Yann LeCun, _A Path Towards Autonomous Machine Intelligence_｜OpenReview**  
   链接：<https://openreview.net/pdf/315d43ba26f55357a84cec9a7ed15a6610094f79.pdf>  
   用途：JEPA 的概念母本。这里第一次把“在表征空间预测、忽略无关细节、多模态用 latent z 表示”讲清。  

2. **2023-01-19 / CVPR 2023｜Assran et al., _Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture_｜arXiv / CVF**  
   链接：<https://arxiv.org/abs/2301.08243>  
   链接：<https://openaccess.thecvf.com/content/CVPR2023/papers/Assran_Self-Supervised_Learning_From_Images_With_a_Joint-Embedding_Predictive_Architecture_CVPR_2023_paper.pdf>  
   用途：I-JEPA 图像落地；直接支撑“抽象状态预测”“优于 MAE 的语义/结构表征”“效率优势”。

3. **2024-02-15｜Bardes et al., _Revisiting Feature Prediction for Learning Visual Representations from Video_｜arXiv**  
   链接：<https://arxiv.org/abs/2404.08471>  
   用途：V-JEPA 论文主来源。证明 feature prediction 可单独作为视频视觉学习目标。

4. **2024-02-20｜Meta 官方博客，_V-JEPA: The Next Step Toward Yann LeCun’s Vision of Advanced Machine Intelligence_**  
   链接：<https://about.fb.com/es/news/2024/02/v-jepa-el-siguiente-paso-hacia-la-vision-de-yann-lecun-de-la-machine-intelligence-avanzada-ami/>  
   用途：官方立场。明确强调 V-JEPA 不是 generative video model，而是 abstract representation prediction；并给出 1.5x-6x 的效率表述。

5. **2025-04-01｜Fan et al., _Scaling Language-Free Visual Representation Learning_｜arXiv**  
   链接：<https://arxiv.org/abs/2504.01017>  
   用途：图像线最强补强证据之一。控制数据后，纯视觉 SSL 可达到 CLIP 级别，并且视觉 SSL 的 scaling 还未饱和。

6. **2025-06-11｜Assran et al., _V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning_｜arXiv**  
   链接：<https://arxiv.org/abs/2506.09985>  
   用途：JEPA 路线最新主论文；说明该线已进入 world model / planning 级叙事。

7. **2025-06-11｜Meta 官方博客，_Our New Model Helps AI Think Before it Acts_**  
   链接：<https://about.fb.com/news/2025/06/our-new-model-helps-ai-think-before-it-acts/>  
   用途：官方把 V-JEPA 2 明确称为 world model，并把 understanding / prediction / planning 作为三件核心能力公开命名。

8. **2025-06-11｜Bordes et al., _IntPhys 2_｜arXiv**  
   链接：<https://arxiv.org/abs/2506.09849>  
   用途：负证据。前沿模型在复杂场景直觉物理上多数仍接近 chance，证明“世界状态持有”没有因为视频预训练就被解决。

9. **2025-06-11｜Foss et al., _CausalVQA_｜arXiv**  
   链接：<https://arxiv.org/abs/2506.09943>  
   用途：负证据。前沿模型在 anticipation / hypothetical / planning 类问题上显著落后人类。

10. **2025-08-13 / 2025-08-14｜Siméoni et al., _DINOv3_｜arXiv / Meta publication**  
    链接：<https://arxiv.org/abs/2508.10104>  
    链接：<https://ai.meta.com/research/publications/dinov3/>  
    用途：不是 JEPA 正统，但它是图像阶段 V 最强的现实补强之一：解决 dense feature 长训退化问题，说明阶段 V 的图像前沿已从“要不要重建”转向“如何长期保持可迁移 dense world features”。

## 三、四个核心问题的直接回答

### 3.1 什么叫抽象状态预测，而不是像素重建

- 抽象状态预测 = 预测一个区域在表征空间中的状态，而不是恢复该区域所有像素值。
- 它允许模型丢掉多解的、偶然的、任务无关的细节，只保留对对象、部件、姿态、几何延续、前后关系有用的信息。
- 这不是“更粗糙的重建”，而是换了预测对象：
  以前预测的是 `观测本身`；
  现在预测的是 `生成该观测所需的潜在解释变量`。
- JEPA 母论文给的例子很关键：预测车在岔路口前后的位置、朝向、速度，而不是树木纹理和路面材质。

### 3.2 JEPA 相比 MAE / BEiT 的本体差异

- **MAE**：随机 mask 后重建缺失像素；对象仍是图像样本。  
- **BEiT**：随机 mask 后恢复离散 visual tokens；对象仍是 tokenized observation。  
- **JEPA / I-JEPA**：给定上下文，预测目标区域的 embedding；对象变成抽象状态。
- 所以三者真正差异不是“decoder 有多大”，而是：
  `MAE/BEiT` 仍回答“缺的观测是什么”；
  `JEPA` 回答“缺的地方在状态层应当是什么”。
- 你书里的“IV 的桥 vs V 的主线”在这里是成立的：  
  MAE/BEiT 是通往阶段 V 的桥；JEPA 才是阶段 V 的正题。

### 3.3 这条线在图像视觉中的最强证据和最前沿变化

- **最强正证据一**：I-JEPA 在图像上已经证明，embedding prediction 能学到不依赖手工增强的语义级表征，并在 object counting、depth prediction 上优于 MAE。
- **最强正证据二**：2025 的 language-free scaling 证明，纯视觉 SSL 的上限不必默认低于语言监督；此前许多“视觉不如 CLIP”其实混入了数据差异。
- **最强正证据三**：DINOv3 解决 dense feature 长训退化，说明图像阶段的前沿问题已从“能否学到表征”升级到“能否长期稳定持有 dense world features”。
- **最强负证据**：即便 V-JEPA 2 已走到 world model 与 planning，2025 的 IntPhys 2 / CausalVQA 仍显示现有模型在物理直觉、反事实、预期性问题上远未闭合。

### 3.4 哪些内容严格属于阶段 V，哪些其实仍是阶段 IV 或视频/世界模型外延

- **严格属于阶段 V 的核心**：
  图像自监督表征学习；
  latent / embedding prediction；
  对象、部件、几何、遮挡、对应、布局等图像内可证实的潜状态；
  dense transferable visual features。

- **仍更像阶段 IV 的桥**：
  MAE / BEiT / iBOT / MaskFeat 这类 masked modeling。  
  它们很重要，但严格说仍以“恢复观测”或其近邻目标为中心，属于 IV -> V 的技术桥。

- **属于阶段 V 的边界外延，而非 `§46` 正文主干**：
  V-JEPA、V-JEPA 2、action-conditioned latent world model、机器人 planning。  
  它们证明阶段 V 的方向有生命力，但对象已经从“图像内潜状态”扩展成“时间中的世界演化与行动后果”。

## 四、可直接写进 §45 的段落要点

1. `§45` 应明确写一句：  
   **JEPA 的关键不是“又一种 SSL recipe”，而是把视觉学习的最终对象从观测恢复切换成状态预测。**

2. 可直接加入一个对照句：  
   **MAE/BEiT 问“遮挡处原来长什么样”，JEPA 问“遮挡处在状态层应当是什么”。**

3. 建议补一个“为何抽象不是空泛”的论证：  
   I-JEPA 的 target 不是任意抽象，而是由目标编码器从真实图像块中抽出的表征，因此它仍被观测约束，只是不再被像素细节绑死。

4. 建议在本章中直接点名 I-JEPA 的两个关键设计：
   大 target blocks；
   空间上分布式、信息量足够的 context blocks。  
   这说明 JEPA 的“语义性”不是自动出现的，而是被 masking strategy 强行塑形出来的。

5. 可以加一段“为什么比对比学习再进一步”：  
   对比学习回答“是否还是同一对象”；JEPA 进一步回答“在给定上下文时，未见部分应该处在什么状态”。

## 五、可直接写进 §46 的段落要点

1. `§46` 最好把“图像中的世界状态”收窄定义为：  
   **由单图或多图图像证据所约束、能在遮挡、视角变化、裁剪扰动和跨图对应中保持稳定的一组潜在结构变量。**

2. 强烈建议显式写出“只到图像证据，不到 rollout”：  
   这一章讨论的不是完整世界模型，不是长期规划，不是机器人控制，而是图像里可被持有的部分世界状态。

3. 建议把状态对象固定为六项：
   对象身份；
   部件/拓扑；
   几何/深度；
   遮挡顺序；
   correspondence；
   布局与关系。

4. 可以加入一句边界判断：  
   **V-JEPA 2 证明了这条路可以通向 planning，但这个结果更适合被当作阶段 V 的“外推证据”，而不是 `§46` 对图像世界状态的直接定义。**

5. 建议补一段负证据，避免本章过度乐观：  
   2025 的 IntPhys 2 与 CausalVQA 表明，当前前沿模型虽能持有部分结构状态，却仍未达到稳健的直觉物理与反事实理解。

## 六、对阶段 V 骨架的调整建议

1. **骨架大体不用重排，`§45 -> §46 -> §47` 的顺序是对的。**

2. **但 `§45` 需要再加一个小节：`JEPA 不是 masked modeling 的变体，而是对象切换`。**  
   现在正文已很接近这点，但还可以更“钉死”。

3. **`§46` 需要显式分出两层边界：**
   图像内世界状态；
   视频/世界模型外延。  
   否则 V-JEPA 2 会不断把本章拉向“广义 world model 综述”。

4. **`§41` 可补一个前史桥梁提示：MaskFeat / feature prediction。**  
   它比单说 MAE/BEiT 更能解释为什么“从 pixel 到 feature”不是突然发生，而是有过渡带。

5. **阶段 V 的最强图像证据不应只押在 I-JEPA 一篇上。**  
   建议在 `§45` 或 `结语` 中补一句：  
   `I-JEPA 立命题，Scaling Language-Free Visual Representation Learning 与 DINOv3 负责把这条命题在图像前沿上继续坐实。`

6. **`§47` 可提前埋一句：为什么 IntPhys 2 / CausalVQA 这类 benchmark 很重要。**  
   因为它们说明真正的问题已经从“会不会分类/检索”转向“会不会持有可用于预期、反事实和物理判断的状态”。

## 七、当前一句话结论

> JEPA 这条线的真正贡献，不是把重建做得更省，而是第一次把视觉学习的对象从“可见样本”切换为“可预测的潜在状态”；但一旦这条线推到视频与规划，它就开始越出 `§46` 的图像边界，进入更广义的世界模型问题。
