# Weak to Strong Generalization: Eliciting Knowledge From Large Language Models

## Abstract

This research paper investigates the feasibility of using weak supervision to elicit the full capabilities of much stronger models. This is particularly relevant in the context of aligning future superhuman models, as humans may not be able to reliably evaluate their complex behavior. The paper explores the concept of weak-to-strong generalization using various pretrained language models in the GPT-4 family, applying them to natural language processing (NLP), chess, and reward modeling tasks.

<details>
<summary>Click to Expand: Abstract (Continued)</summary>

The findings reveal that naively fine-tuning strong models on labels generated by weaker models consistently leads to better performance compared to the weaker supervisors. However, a significant gap still exists between these models and those fine-tuned with ground truth supervision. This suggests that techniques like reinforcement learning from human feedback (RLHF) may not effectively scale to superhuman models without further advancements.

The paper explores methods to improve weak-to-strong generalization, including encouraging confident predictions, bootstrapping with intermediate models, and utilizing unsupervised fine-tuning. For instance, incorporating an auxiliary confidence loss when supervising GPT-4 with a GPT-2-level supervisor on NLP tasks enables recovering close to GPT-3.5-level performance. 

Overall, the research suggests that while challenges remain, making empirical progress on aligning superhuman models through weak supervision is feasible and presents a crucial step towards ensuring their safety and alignment with human values.
</details>

## 1. Introduction

### 1.1 Motivation: Aligning Superhuman Models

*   Modern language model assistants like ChatGPT rely on RLHF for alignment, reinforcing behaviors deemed good by human evaluators.
*   However, superhuman models will exhibit complex behaviors that surpass human understanding, making reliable evaluation and supervision difficult.
*   This raises a crucial challenge for aligning superhuman models: how can weak supervisors control significantly more intelligent models?

<details>
<summary>Click to Expand: Challenges of Human Supervision for Superhuman Models</summary>

Consider a superhuman assistant model generating a million lines of intricate code. Evaluating its adherence to user intentions, honesty in answering questions about the code, safety of execution, and other alignment-relevant aspects becomes highly challenging for humans. Consequently, the effectiveness of fine-tuning a superhuman model with human supervision on tasks like reward modeling or safety classification remains uncertain, especially when generalizing to complex behaviors beyond human evaluation capabilities.
</details>

### 1.2 Analogy: Weak Models Supervising Strong Models

*   This research explores an analogy to the human-superhuman supervision problem: can weak models effectively supervise strong models?
*   The approach involves fine-tuning large (strong) pretrained models on labels generated by smaller (weak) models, similar to the weak-to-strong learning problem.

<details>
<summary>Click to Expand: Why Weak-to-Strong Learning Might Be Possible</summary>

*   **Strong Model Capabilities:** Strong pretrained models possess inherent understanding of alignment-relevant tasks, like generating code and assessing its adherence to instructions.
*   **Eliciting Latent Knowledge:** The weak supervisor's role is to elicit existing knowledge within the strong model, rather than teaching new capabilities. 
*   **Weak-to-Strong Generalization:** This phenomenon allows strong models to generalize beyond the weak supervision, tackling even complex problems where the weak supervisor provides incomplete or flawed training labels.

</details>

## 2. Related Work

*   **Weakly-supervised learning:** This area deals with training models using unreliable labels, encompassing techniques like learning from noisy labels.
*   **Student-teacher training:** This framework, commonly used in semi-supervised learning and knowledge distillation, involves training a teacher model and then using its generated pseudo-labels to train a student model.
*   **Robustness of pretraining and fine-tuning:** Research indicates that pretraining on diverse data enhances robustness and generalization, while fine-tuning can sometimes hinder out-of-distribution performance.
*   **Debiasing:** This area focuses on mitigating biases in training data. However, most existing work addresses known biases, unlike the unknown biases present in weak supervision.
*   **Imitation and preference learning:** Alignment often involves guiding capable models towards desired behaviors, using methods like imitation learning and RLHF.
*   **Scalable oversight:** These techniques aim to enhance human supervision capabilities, such as using models to critique other models' outputs or decompose complex problems.

<details>
<summary>Click to Expand: Related Work: Additional Notes</summary>

*   **Instance-dependent errors:** The errors in weak supervision differ from the uniform label noise commonly addressed in related literature, posing additional challenges.
*   **Qualitative differences in supervision strength:** The focus of this research lies in significantly weaker supervision compared to prior work, akin to a "3rd grade-level" supervisor guiding a "12th grade-level" student model.
*   **Generalization beyond human supervision:** This work emphasizes generalizing beyond human capabilities, in contrast to scalable oversight methods that primarily improve human supervision.

</details> 

## 3. Methodology

This research investigates the weak-to-strong learning problem by employing the following steps:

1.  **Creating the Weak Supervisor:** Small pretrained models are fine-tuned on ground truth labels to establish a baseline performance level.
2.  **Training a Strong Student Model with Weak Supervision:** A large pretrained model is fine-tuned using the weak labels generated by the weak supervisor.
3.  **Training a Strong Model with Ground Truth Labels:** A large pretrained model is fine-tuned using ground truth labels to establish a ceiling for potential performance.

**Performance Gap Recovered (PGR):**

*   PGR measures the extent to which the performance gap between the weak and strong ceiling models is closed through weak supervision.
*   A PGR of 1 indicates perfect weak-to-strong generalization, while a PGR of 0 suggests no improvement over the weak supervisor.

**Advantages of the Methodology:**

*   **Flexibility:** The setup accommodates any combination of weak and strong models and tasks.
*   **Empirical testing:** The approach facilitates testing across diverse settings.
*   **Practical applications:**  Success in aligning models with weak supervision holds practical benefits even before the development of superhuman models. 

<details>
<summary>Click to Expand: Limitations of the Methodology</summary>

*   **Imitation saliency:** Future superhuman models may possess a greater ability to imitate weak model errors compared to the current strong models.
*   **Pretraining leakage:** The pretraining data used in this research implicitly contains human supervision, potentially making it easier to elicit capabilities from strong models. 

</details>

## 4. Main Results

### 4.1 Tasks

The research evaluates weak-to-strong generalization across three settings:

1.  **Popular NLP benchmarks:** This includes 22 diverse datasets covering ethics, commonsense reasoning, natural language inference, sentiment analysis, and other domains.
2.  **Chess puzzles:** This involves predicting the optimal first move in chess puzzles from lichess.org. 
3.  **ChatGPT reward modeling:** This focuses on training a reward model to predict human preferences between assistant model responses in dialogs, a critical step in RLHF.

### 4.2 Baseline Results: Weak-to-Strong Generalization Observed

*   **NLP tasks:** Strong models with weak supervision demonstrate significant generalization, often recovering around half of the performance gap between weak and strong models. 
*   **Chess puzzles:** Mixed results are observed, with PGR increasing with the size of the weak supervisor but decreasing with the size of the strong student.
*   **ChatGPT reward modeling:** Weak-to-strong generalization is generally poor, with only around 10% of the performance gap recovered.

<details>
<summary>Click to Expand: Question: Why is it surprising that strong models outperform weaker models?</summary>

It might seem intuitive that stronger models would outperform weaker models. However, the surprising aspect lies in the fact that even with weak supervision, where the training labels are generated by a less capable model and contain errors, the strong model still manages to learn and generalize beyond those limitations. This suggests that the strong model's inherent capabilities and knowledge, acquired during pretraining, play a significant role in its ability to perform well even with imperfect guidance.
</details>

### 4.3 Improving Weak-to-Strong Generalization

#### 4.3.1 Bootstrapping with Intermediate Model Sizes

*   Bootstrapping involves using a series of increasingly capable models to progressively align stronger models.
*   This approach shows promising results in the chess puzzle setting, significantly improving PGR, especially for larger student models. 
*   However, limited improvements are observed on NLP tasks and no improvements are seen in the reward modeling setting.

<details>
<summary>Click to Expand: Question: Can we estimate GPT-4 model size from Figure 4?</summary>

Figure 4 does not provide direct information about the specific model sizes used in the experiments, including GPT-4. The focus is on the relative performance improvement achieved through bootstrapping compared to naive fine-tuning with weak supervision. The x-axis represents the compute used for training the strong student models, but the exact model sizes are not specified. 
</details>

#### 4.3.2 Auxiliary Confidence Loss for NLP Tasks

*   An auxiliary confidence loss encourages the strong model to make confident predictions, even when contradicting the weak labels.
*   This method leads to substantial improvements in generalization for NLP tasks, particularly when the compute gap between weak and strong models is large. 

<details>
<summary>Click to Expand: Question: Is the large model trained to recover 80% of the gap between the strong model?</summary>

The statement refers to the ability of the large model (GPT-4) to recover 80% of the performance gap between the weak supervisor (GPT-2-level) and the strong ceiling model (presumably a model similar to GPT-4 but fine-tuned with ground truth labels). In other words, by incorporating the auxiliary confidence loss, the GPT-4 model trained with weak supervision achieves a performance level that is much closer to the strong ceiling model than the weak supervisor. The goal is to bridge the gap between the weak and strong models, not within the strong model itself. 
</details> 

## 5. Understanding Weak-to-Strong Generalization

### 5.1 Understanding Imitation

*   A potential failure mode in weak-to-strong learning is the strong model simply imitating the weak supervisor, including its errors.
*   This is particularly relevant in the context of aligning superhuman models, where naive human supervision might lead to imitation of human-level capabilities rather than the model's full potential.

#### 5.1.1 Overfitting to Weak Supervision

*   Strong models exhibit overfitting to weak supervisor errors, especially with larger gaps between weak and strong models.
*   Ground truth early stopping, which involves stopping training at the point of optimal performance on ground truth labels, leads to notable improvements in PGR.

#### 5.1.2 Student-Supervisor Agreement

*   High student-supervisor agreement, exceeding the weak supervisor's accuracy, suggests imitation of errors.
*   The auxiliary confidence loss effectively reduces student-supervisor agreement, particularly by mitigating the imitation of supervisor mistakes.

<details>
<summary>Click to Expand: Question: Explain: 'larger student models agree LESS with the ERRORS of the supervisor than smaller student models?'</summary>

This seemingly counterintuitive finding suggests that larger student models, despite having greater capacity to learn and potentially imitate, are less prone to replicating the errors of the weaker supervisor. This could be due to several factors, such as:

*   **Stronger Priors:** Larger models may have more robust and accurate internal representations of the task, making them less susceptible to being swayed by the incorrect labels provided by the weak supervisor.
*   **Regularization Effects:** The increased complexity of larger models may act as a form of regularization, preventing them from overfitting to the specific errors present in the weak supervision. 
*   **Learning Dynamics:** The learning process of larger models might prioritize capturing the underlying patterns and relationships in the data, rather than simply memorizing the labels, leading to better generalization and less reliance on the potentially flawed weak supervision.
</details>

<details>
<summary>Click to Expand: Question: a hard time fitting errors?</summary>

This phrase suggests that larger models have difficulty accurately reproducing or learning the specific mistakes made by the weaker supervisor. It implies that the larger models' learning process prioritizes capturing the true underlying patterns in the data, rather than simply mimicking the erroneous labels provided by the weak supervisor.
</details>

#### 5.1.3 Inverse Scaling for Imitating the Supervisor

*   Larger student models exhibit inverse scaling, showing less agreement with supervisor errors compared to smaller student models.
*   This indicates that pretrained models may struggle to fit the errors of smaller models, particularly in fine-tuning settings with limited data.

### 5.2 Saliency in the Strong Model Representations

#### 5.2.1 Eliciting Strong Model Knowledge with Prompting

*   Zero-shot and few-shot prompting with ground truth labels demonstrate significant performance improvements for larger models, suggesting the ease of eliciting task-relevant knowledge. 
*   However, using weak labels in prompting leads to worse performance, indicating that weak-to-strong learning remains challenging in the prompting setting.
*   The current setup might be more disanalogous for prompting than for fine-tuning due to potential pretraining leakage.

<details>
<summary>Click to Expand: Highlight this point</summary>

This finding is crucial as it suggests that for very large language models, simply providing a few examples of the desired task can effectively unlock their knowledge and capabilities, without the need for extensive fine-tuning or complex training procedures. This has significant implications for the future of AI development and alignment, as it hints at the possibility of guiding powerful models with minimal human intervention.
</details>

#### 5.2.2 Generative Supervision Improves RM Weak-to-Strong Generalization

*   Unsupervised fine-tuning on task-relevant data can enhance task saliency and improve weak-to-strong generalization.
*   In the reward modeling setting, generative fine-tuning on ChatGPT comparison data significantly increases PGR.
*   Combining generative fine-tuning with ground truth early stopping yields even more substantial PGR improvements.

#### 5.2.3 Fine-tuning on Weak Supervision to Increase Concept Saliency

*   Fine-tuning on weak labels increases the linearity of the ground truth concept in the strong model's representations. 
*   This suggests that linear probe-based weak-to-strong methods might be effective after initial fine-tuning on weak labels. 

## 6. Discussion 

### 6.1 Remaining Disanalogies

*   **Imitation saliency:** Future superhuman models might exhibit a greater tendency to imitate weak supervisor errors compared to the strong models studied in this research. 
*   **Pretraining leakage:** The implicit human supervision present in the pretraining data might make it easier to elicit capabilities from strong models, unlike future superhuman models where alignment-relevant capabilities may be more latent and challenging to elicit. 

<details>
<summary>Click to Expand: Highlight this</summary>

This observation is crucial as it highlights a potential limitation of the current approach and emphasizes the need for further research into methods that can effectively elicit latent knowledge from superhuman models, where their capabilities might not be readily apparent or easily accessible through simple prompting or fine-tuning.
</details>

### 6.2 Future Work

To address the challenge of aligning superhuman models, further research is needed in the following areas:

*   **Analogous setups:** Developing more analogous setups that address the remaining disanalogies, such as imitation saliency and pretraining leakage.
*   **Scalable methods:** Exploring and evaluating methods that can effectively elicit desired capabilities from strong models while satisfying properties like disagreement with incorrect weak supervision, naturalness/saliency, and consistency.
*   **Scientific understanding:** Gaining a deeper understanding of the factors influencing concept elicitation, developing methods to estimate generalization error, and utilizing scaling laws to extrapolate generalization across various model sizes.

## 7. Conclusion

The rapid progress in AI necessitates reliable methods for aligning superhuman models. This research demonstrates the feasibility of making empirical progress on this challenge by using weak supervision to elicit knowledge from strong models. While challenges and disanalogies remain, the findings suggest a promising path towards ensuring the safe and beneficial development of future AI systems.
