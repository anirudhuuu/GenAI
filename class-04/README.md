# Fine Tuning

Fine-tuning customizes a pre-trained model (like GPT or Gemini) on specific data to adapt it for a particular task or domain.

You can use **Full fine-tuning**, parameter-efficient fine-tuning (PEFT) like **LoRA**, or instruction tuning depending on your goals and resources.

- **Full fine-tuning** updates all model parameters, requiring significant compute and data.
- **PEFT** (like LoRA) introduces small trainable parameters (e.g., low-rank matrices) while keeping most of the model frozen, making it faster and cheaper for large models.

![Diagram of Fine-tuning](./images/01-diagram.png)

Transformer models are primarily trained for tasks like next-token prediction, but fine-tuning allows adapting them for tasks such as classification, summarization, or domain-specific applications.

OpenAI and Google handle the heavy lifting of pre-training on massive datasets. Fine-tuning lets you adapt these models to your niche datasets for better performance.

You can fine-tune models for:

- **Domain adaptation** (e.g., medical, legal data)
- **Task-specific objectives** using labeled datasets (e.g., sentiment analysis, text generation).

![Diagram of Domain & Task Specific Training](./images/02-diagram.png)

## Fine-tuning Strategies

1. Full parameter fine-tuning
2. LoRA (Low-Rank Adaptation) fine-tuning

### Full Parameter Fine-tuning

Transformers are deep neural networks with layers, parameters, and weights that process data. Full fine-tuning adjusts **all** these weights across the model, making it the most flexible but also the most resource-intensive method.

- **Weights**: Learned values that guide predictions.
- **Layers**: Stacked processing units, each with its own weights.

> **Weights** control neuron connections and are updated during training to minimize prediction errors.
>
> **Backpropagation** adjusts weights by calculating gradients based on loss, enabling the model to learn.

**Cons of Full Fine-tuning:**

- High GPU & compute cost
- Increased energy and hardware requirements
- Often requires self-hosting infrastructure

### LoRA (Low-Rank Adaptation) Fine-tuning

LoRA is a **parameter-efficient** technique where the base model’s weights are **frozen**. Instead of updating them, small low-rank matrices are injected into specific layers to capture task-specific adaptations.

For each training step:

- Loss is calculated between predicted vs. expected outputs.
- Only the added low-rank matrices are updated, not the original model weights.

This drastically reduces compute and memory needs, enabling fine-tuning of large models on modest hardware.

> LoRA = Frozen base model + Trainable low-rank matrices.

It’s ideal when you need efficient domain/task adaptation without the cost of full fine-tuning.
