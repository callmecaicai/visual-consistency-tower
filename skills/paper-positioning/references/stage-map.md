# Stage Map

## Stage I · 判别共形

Primary problem:

- image-level label prediction
- CNN training dynamics
- optimizer / normalization / activation / residual training

Likely chapters:

- `§01-§02`: data foundation and early deep classification shock
- `§03-§05`: trainability, normalization, optimizer, residual revolution

## Stage II · 稠密共形

Primary problem:

- detection
- segmentation
- depth
- dense prediction
- promptable dense vision

Likely chapters:

- `§11`: full-convolution shift
- `§12`: dilation, multi-scale
- `§13`: detection pipeline
- `§14`: anchor-free, DETR, query
- `§15`: unified mask architecture
- `§16`: prompting, open vocabulary, SAM, Grounding DINO

## Stage III · 语言共形

Primary problem:

- language enters visual understanding
- CLIP alignment
- multimodal backbone
- VLM understanding and instruction following
- grounding with language

Likely chapters:

- `§21`: early fusion /外挂极限
- `§22`: CLIP and contrastive alignment
- `§23`: language-anchored dense tasks
- `§24`: unified multimodal backbone
- `§25`: VLM emergence, frozen LLM, instruction tuning, native multimodality
- `§26`: language-conditioned promptable vision
- `§27`: cost of borrowing language, blindness/accounting/application evidence

## Stage IV · 生成共形

Primary problem:

- image generation
- diffusion
- GAN
- text-conditioned image synthesis
- image generation as understanding

Likely chapters:

- `§31`: density / energy / autoregressive prehistory
- `§32`: GAN and adversarial awakening
- `§33`: latent space, codebook, flow, internal language
- `§34`: diffusion and internal time
- `§35`: text-conditioned image generation interface
- `§36`: image-generation systematization and frontier
- `§37`: generator-to-representation bridge

## Stage V · 表征共形

Primary problem:

- world representation
- holding world states
- predictive representation learning
- JEPA
- DINO-style self-supervision
- non-generative understanding
- reflexive metric pressure

Planned chapters:

- `§41-§49`

## Boundary Heuristics

- Open-vocabulary detection/segmentation usually lands in `II §16` or `III §23`
- VLM understanding lands in `III`
- Image generation lands in `IV`
- World representation and state prediction without pixel output land in `V`
- Domain-specific RS/VLM work usually lands in `应用域`, but only after a main chapter anchor is chosen
