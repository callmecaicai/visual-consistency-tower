# 状态持有的负证据：IntPhys2 与 CausalVQA

类型: 反身评测 / 负证据
阶段: V · 表征共形
对应章节: §47
核心命题: 几何强、dense 强、tracking 强，不等于物理、因果和反事实状态真正闭合。

## 一、为什么阶段 V 必须写负证据

阶段 V 不能只记录强模型，否则会变成“乐观 world model 史”。真正的理论硬度来自：

> 哪些状态对象还没有被持有？

IntPhys2 与 CausalVQA 的价值在于，它们把阶段 V 的残差从“还不够准”推进到“当前状态持有制度本身仍不覆盖物理与因果”。

## 二、负证据总表

| 负证据 | 测什么 | 暴露什么 | 阶段 V 含义 |
|---|---|---|---|
| IntPhys2 | object permanence、immutability、spatio-temporal continuity、solidity | 视觉状态不等于直觉物理 | 几何状态不能冒充物理状态 |
| CausalVQA | counterfactual、hypothetical、anticipation、planning、descriptive | 状态持有不等于因果推理 | VLM / video model 的 causal closure 仍弱 |
| probe 排序反转 | linear、dense、geometry、physics 指标排序差异 | 好表征不可由单一指标裁判 | 进入反身度量 |
| dense artifact / registers | dense feature map artifact | dense feature 自身需要审计 | feature 不是透明窗口 |
| V-JEPA 2.1 dense gains | dense predictive state 有进展 | 仍需多状态对象验证 | H3-H4 候选，不是完成 |

## 三、IntPhys2 的理论位置

IntPhys2 测的是直觉物理原则，而不是普通视频识别。它追问：

```text
object permanence
solidity
spatio-temporal continuity
immutability
```

这些对象并非 depth / pose / pointmap 自动推出。它们要求系统持有更强的物理状态约束。

因此，IntPhys2 是对阶段 V 的提醒：

> 几何世界状态只是物理世界状态的前提，不是物理世界状态本身。

## 四、CausalVQA 的理论位置

CausalVQA 进一步把问题推向反事实、假设、预期和规划。它不是问“视频里有什么”，而是问：

```text
如果条件改变，会发生什么？
接下来可能发生什么？
要达到某结果应如何规划？
```

这已经越过单纯视觉状态，进入因果与行动接口。

## 五、阶段 V 的反身结论

这些负证据不会削弱阶段 V，反而让阶段 V 更硬：

```text
dense feature strong != physical state closure
geometry strong != causal state closure
planning interface strong != world model completion
```

阶段 V 的终极残差不是模型还不够强，而是：

> 我们还不知道用什么制度证明它真的持有了某类世界状态。

## 六、参考

- [IntPhys2 (arXiv 2025)](https://arxiv.org/abs/2506.09849)
- [CausalVQA (arXiv 2025)](https://arxiv.org/abs/2506.09943)
