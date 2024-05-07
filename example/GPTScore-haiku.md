# Notes for GPTScore

Assessing the quality of the generation is an even more arduous task than the generation itself, and this issue has not been given adequate consideration recently. This paper proposes a novel evaluation framework, GPTSCORE, which utilizes the emergent abilities (e.g., zero-shot instruction) of generative pre-trained models to score generated texts. There are 19 pre-trained models explored in this paper, ranging in size from 80M (e.g., FLAN-T5-small) to 175B (e.g., GPT3). Experimental results on four text generation tasks, 22 evaluation aspects, and corresponding 37 datasets demonstrate that this approach can effectively allow us to achieve what one desires to evaluate for texts simply by natural language instructions. This nature helps us overcome several long-standing challenges in text evaluation–how to achieve customized, multi-faceted evaluation without the need for annotated samples. We make our code publicly available.

![Existing studies evaluate text quality with limited aspects (e.g., semantic equivalence, fluency) (Fig. 1-(a)), which are usually customized prohibitively, making it harder for users to evaluate aspects as they need (Freitag et al., 2021). (b) A handful of studies have examined multi-aspect evaluation (Yuan et al., 2021; Scialom et al., 2021; Zhong et al., 2022) but have not given adequate attention to the definition of the evaluation aspect and the latent relationship among them. Instead, the evaluation of an aspect is either empirically bound with metric variants (Yuan et al., 2021) or learned by supervised signals (Zhong et al., 2022). (c) Recently proposed evaluation methods (Mehri & Eskénazi, 2020; Rei et al., 2020; Li et al., 2021; Zhong et al., 2022) usually necessitate a complicated training procedure or costly manual annotation of samples (Fig. 1-(a,b)), which makes it hard to use these methods in industrial settings due to the amount of time needed for annotation and training to accommodate a new evaluation demand from the user.](https://i.imgur.com/zAjlpvs.png)

In this paper, we demonstrated the talent of the super large pre-trained language model (e.g., GPT-3) in achieving multi-aspect, customized, and training-free evaluation (Fig. 1-(c)). In essence, it skillfully uses the pre-trained model's zero-shot instruction (Chung et al., 2022), and in-context learning (Brown et al., 2020; Min et al., 2022) ability to deal with complex and ever-changing evaluation needs so as to solve multiple evaluation challenges that have been plagued for many years at the same time.

Specifically, given a text generated from a certain context, and desirable evaluation aspects (e.g., fluency), the high-level idea of the proposed framework is that the higher-quality text of a certain aspect will be more likely generated than uqualified ones based on the given context, where the "likely" can be measured by the conditional generation probability. As illustrated in Fig. 2, to capture users' true desires, an evaluation protocol will be initially established based on (a) the task specification, which typically outlines how the text is generated (e.g., generate a response for a human based on the conversation.) (b) aspect definition that documents the details of desirable evaluation aspects (e.g., the response should be intuitive to understand). Subsequently, each evaluation sample will be presented with the evaluated protocol with optionally moderate exemplar samples, which could facilitate the model's learning. Lastly, a large generative pre-trained model will be used to calculate how likely the text could be generated based on the above evaluation protocol, thus giving rise to our model's name: GPTSCORE.

![](https://i.imgur.com/5dZsbKS.png)

<details>
<summary>Related Work</summary>

Training language models to follow instructions with human feedback. arXiv preprint arXiv:2203.02155,

Training language models to follow instructions with human feedback

Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, Ryan Lowe
Making language models bigger does not inherently make them better at following a user's intent. For example, large language models can generate outputs that are untruthful, toxic, or simply not helpful to the user. In other words, these models are not aligned with their users. In this paper, we show an avenue for aligning language models with user intent on a wide range of tasks by fine-tuning with human feedback. Starting with a set of labeler-written prompts and prompts submitted through the OpenAI API, we collect a dataset of labeler demonstrations of the desired model behavior, which we use to fine-tune GPT-3 using supervised learning. We then collect a dataset of rankings of model outputs, which we use to further fine-tune this supervised model using reinforcement learning from human feedback. We call the resulting models InstructGPT. In human evaluations on our prompt distribution, outputs from the 1.3B parameter InstructGPT model are preferred to outputs from the 175B GPT-3, despite having 100x fewer parameters. Moreover, InstructGPT models show improvements in truthfulness and reductions in toxic output generation while having minimal performance regressions on public NLP datasets. Even though InstructGPT still makes simple mistakes, our results show that fine-tuning with human feedback is a promising direction for aligning language models with human intent.
</details>

Experimentally, we ran through almost all common natural language generation tasks in NLP, and the results showed the power of this new paradigm. The main observations are listed as follows: (1) Evaluating texts with generative pre-training models can be more reliable when instructed by the definition of task and aspect, providing a degree of flexibility to accommodate various evaluation criteria. Furthermore, incorporating exemplified samples with in-context learning will further enhance the process. (2) Different evaluation aspects exhibit certain correlations. Combining definitions with other highly correlated aspects can improve evaluation performance. (3) The performance of GPT3-text-davinci-003, which is tuned based on human feedback, is inferior to GPT3-text-davinci-001 in the majority of the evaluation settings, necessitating deep explorations on the working mechanism of human feedback-based instruction learning (e.g., when it will fail).

## 2. Preliminaries
### 2.1. Text Evaluation
Text evaluation aims to assess the quality of hypothesis text h in terms of certain aspect a (e.g., fluency)

```
y = f (h, a, S)
 (1)
```
where (1) h represents the text to be evaluated (hypothesis text, e.g., generated summary in text summarization task). (2) a denotes the evaluation aspect (e.g., fluency). (3) S is a collection of additional texts that are optionally used based on different scenarios. For example, it could be a source document or a reference summary in the text summarization task. (4) Function f (·) could be instantiated as a human evaluation process or automated evaluation metrics.

### 2.2. Meta Evaluation
Meta evaluation aims to evaluate the reliability of automated metrics by calculating how well automated scores (yauto ) correlate with human judgment (yhuman ) using correlation functions g(yauto , yhuman ) such as spearman correlation.

### 2.3. Evaluation Strategy
Evaluation strategies define different aggregation methods when we calculate the correlation scores. Specifically, suppose that for each source text si , i ∈ [1, 2, · · · , n] (e.g., documents in text summarization task or dialogue histories for dialogue generation task), there are J system outputs hi,j , where j ∈ [1, 2, · · · , J]. fauto is an automatic scoring function (e.g., ROUGE (Lin, 2004)), and fhuman is the gold human scoring function. For a given evaluation aspect a, the meta-evaluation metric F can be formulated as follows. Sample-level defines that a correlation value is calculated for each sample separately based on outputs of multiple systems, then averaged across all samples.

We use the sample-level evaluation strategy for text summarization, data-to-text, and machine translation tasks. For the dialogue response generation task, the dataset-level evaluation strategy is utilized.

## 3. GPTSCORE
### 3.1. Generative Pre-trained Language Models
Existing pre-trained language models could be classified into the following three categories: (a) encoder-only models (e.g., BERT (Devlin et al., 2019), RoBerta (Liu et al., 2019)) that encode inputs with bidirectional attention; (b) encoder-decoder models (e.g., BART (Lewis et al., 2020), T5 (Raffel et al., 2020)) that encode inputs with bidirectional attention and generate outputs autoregressively; (c) decoder-only models (e.g., GPT2 (Radford et al., 2019), GPT3 (Brown et al., 2020), PaLM (Chowdhery et al., 2022)) that generate the entire text sequence autoregressively, where pre-trained models with decoding abilities (b, c) have caught much attention since they show impressive performance on zero-shot instruction and in-context learning

#### Emergent Ability
Recent works progressively reveal a variety of emergent abilities of generative pre-trained language models with appropriate tuning or prompting methods, such as in-context learning (Min et al., 2022), chain-of-thought reasoning (Wei et al., 2022), and zero-shot instruction (Ouyang et al., 2022). One core commonality of these abilities is to allow for handling customized requirements with a few or even zero annotated examples. It's the appearance of these abilities that allows us to re-invent a new way for text evaluation–evaluating from the textual description, which can achieve customizable, multi-faceted, and train-free evaluation.

<details>
<summary>References</summary>

Min, S., Lyu, X., Holtzman, A., Artetxe, M., Lewis, M., Hajishirzi, H., and Zettlemoyer, L. Rethinking the role of demonstrations: What makes in-context learning work? CoRR, abs/2202.12837, 2022. URL https://arxiv.org/abs/2202.12837.

Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?

Sewon Min, Xinxi Lyu, Ari Holtzman, Mikel Artetxe, Mike Lewis, Hannaneh Hajishirzi, Luke Zettlemoyer
Large language models (LMs) are able to in-context learn -- perform a new task via inference alone by conditioning on a few input-label pairs (demonstrations) and making predictions for new inputs. However, there has been little understanding of how the model learns and which aspects of the demonstrations contribute to end task performance. In this paper, we show that ground truth demonstrations are in fact not required -- randomly replacing labels in the demonstrations barely hurts performance on a range of classification and multi-choce tasks, consistently over 12 different models including GPT-3. Instead, we find that other aspects of the demonstrations are the key drivers of end task performance, including the fact that they provide a few examples of (1) the label space, (2) the distribution of the input text, and (3) the overall format of the sequence. Together, our analysis provides a new way of understanding how and why in-context learning works, while opening up new questions about how much can be learned from large language models through inference alone.

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Chi, E. H., Le, Q., and Zhou, D. Chain of thought prompting elicits reasoning in large language models. CoRR, abs/2201.11903, 2022. URL https://arxiv.org/abs/2201.11903.

Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, Denny Zhou
We explore how generating a chain of thought -- a series of intermediate reasoning steps -- significantly improves the ability of large language models to perform complex reasoning. In particular, we show how such reasoning abilities emerge naturally in sufficiently large language models via a simple method called chain of thought prompting, where a few chain of thought demonstrations are provided as exemplars in prompting. Experiments on three large language models show that chain of thought prompting improves performance on a range of arithmetic, commonsense, and symbolic reasoning tasks. The empirical gains can be striking. For instance, prompting a 540B-parameter language model with just eight chain of thought exemplars achieves state of the art accuracy on the GSM8K benchmark of math word problems, surpassing even finetuned GPT-3 with a verifier.
</details>

### 3.2. Generative Pretraining Score (GPTScore)
The core idea of GPTSCORE is that a generative pre-training model will assign a higher probability of high-quality generated text following a given instruction and context.

In our method, the instruction is composed of the task description d and the aspect definition a. Specifically, suppose that the text to be evaluated is h = {h1 , h2, · · · , hm}, the context information is S (e.g., source text or reference text), then GPTSCORE is defined as the following conditional probability:
```
m
X
GPTScore(h|d, a, S) =
 wt log p(ht |h<t , T (d, a, S), θ),
t=1
```
where wt is the weight of the token at position t. In our work, we treat each token equally. T (·) is a prompt template that defines the evaluation protocol, which is usually task-dependent and specified manually through prompt engineering

#### Few-shot with Demonstration
The generative pre-trained language model can better perform tasks when pre-fixed with a few annotated samples (i.e., demonstrations). Our proposed framework is flexible in supporting this by extending the prompt template T with demonstrations.

#### Choice of Prompt Template
Prompt templates define how task description, aspect definition, and context are organized. Minging desirable prompts itself is a non-trivial task and there are extensive research works there (Liu et al., 2021; Fu et al., 2022). In this work, for the GPT3-based model, we opt for prompts that are officially provided by OpenAI.2 For instruction-based pre-trained models, we use prompts from NaturalInstruction (Wang et al., 2022) since it's the main training source for those instruction-based pre-train models.

<details>
<summary>References</summary>

Polyglot Prompt: Multilingual Multitask PrompTraining

Jinlan Fu, See-Kiong Ng, Pengfei Liu
This paper aims for a potential architectural improvement for multilingual learning and asks: Can different tasks from different languages be modeled in a monolithic framework, i.e. without any task/language-specific module? The benefit of achieving this could open new doors for future multilingual research, including allowing systems trained on low resources to be further assisted by other languages as well as other tasks. We approach this goal by developing a learning framework named Polyglot Prompting to exploit prompting methods for learning a unified semantic space for different languages and tasks with multilingual prompt engineering. We performed a comprehensive evaluation of 6 tasks, namely topic classification, sentiment classification, named entity recognition, question answering, natural language inference, and summarization, covering 24 datasets and 49 languages. The experimental results demonstrated the efficacy of multilingual multitask prompt-based learning and led to inspiring observations. We also present an interpretable multilingual evaluation methodology and show how the proposed framework, multilingual multitask prompt training, works. We release all datasets prompted in the best setting and code.

Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing

Pengfei Liu, Weizhe Yuan, Jinlan Fu, Zhengbao Jiang, Hiroaki Hayashi, Graham Neubig
This paper surveys and organizes research works in a new paradigm in natural language processing, which we dub "prompt-based learning". Unlike traditional supervised learning, which trains a model to take in an input x and predict an output y as P(y|x), prompt-based learning is based on language models that model the probability of text directly. To use these models to perform prediction tasks, the original input x is modified using a template into a textual string prompt x' that has some unfilled slots, and then the language model is used to probabilistically fill the unfilled information to obtain a final string x, from which the final output y can be derived. This framework is powerful and attractive for a number of reasons: it allows the language model to be pre-trained on massive amounts of raw text, and by defining a new prompting function the model is able to perform few-shot or even zero-shot learning, adapting to new scenarios with few or no labeled data. In this paper we
Continuing the markdown formatting:

Super-NaturalInstructions: Generalization via Declarative Instructions on 1600+ NLP Tasks

Yizhong Wang, Swaroop Mishra, Pegah Alipoormolabashi, Yeganeh Kordi, Amirreza Mirzaei, Anjana Arunkumar, Arjun Ashok, Arut Selvan Dhanasekaran, Atharva Naik, David Stap, Eshaan Pathak, Giannis Karamanolakis, Haizhi Gary Lai, Ishan Purohit, Ishani Mondal, Jacob Anderson, Kirby Kuznia, Krima Doshi, Maitreya Patel, Kuntal Kumar Pal, Mehrad Moradshahi, Mihir Parmar, Mirali Purohit, Neeraj Varshney, Phani Rohitha Kaza, Pulkit Verma, Ravsehaj Singh Puri, Rushang Karia, Shailaja Keyur Sampat, Savan Doshi, Siddhartha Mishra, Sujan Reddy, Sumanta Patro, Tanay Dixit, Xudong Shen, Chitta Baral, Yejin Choi, Noah A. Smith, Hannaneh Hajishirzi, Daniel Khashabi
How well can NLP models generalize to a variety of unseen tasks when provided with task instructions? To address this question, we first introduce Super-NaturalInstructions, a benchmark of 1,616 diverse NLP tasks and their expert-written instructions. Our collection covers 76 distinct task types, including but not limited to classification, extraction, infilling, sequence tagging, text rewriting, and text composition. This large and diverse collection of tasks enables rigorous benchmarking of cross-task generalization under instructions -- training models to follow instructions on a subset of tasks and evaluating them on the remaining unseen ones. Furthermore, we build Tk-Instruct, a transformer model trained to follow a variety of in-context instructions (plain language task definitions or k-shot examples). Our experiments show that Tk-Instruct outperforms existing instruction-following models such as InstructGPT by over 9% on our benchmark despite being an order of magnitude smaller. We further analyze generalization as a function of various scaling parameters, such as the number of observed tasks, the number of instances per task, and model sizes. We hope our dataset and model facilitate future progress towards more general-purpose NLP models.

## Evaluation Aspects and Datasets
### Aspect Definitions
| Aspect | Task | Definition |
| --- | --- | --- |
| Semantic Coverage (COV) | Summ | How many semantic content units from the reference text are covered by the generated text? |
| Factuality (FAC) | Summ | Does the generated text preserve the factual statements of the source text? |
| Consistency (CON) | Summ, Diag | Is the generated text consistent in the information it provides? |
| Informativeness (INF) | Summ, D2T, Diag | How well does the generated text capture the key ideas of its source text? |
| Coherence (COH) | Summ, Diag | How much does the generated text make sense? |
| Relevance (REL) | Diag, Summ, D2T | How well is the generated text relevant to its source text? |
| Fluency (FLU) | Diag, Summ, D2T, MT | Is the generated text well-written and grammatical? |
| Accuracy (ACC) | MT | Are there inaccuracies, missing, or unfactual content in the generated text? |
| Multidimensional Quality Metrics (MQM) | MT | How is the overall quality of the generated text? |
| Interest (INT) | Diag | Is the generated text interesting? |
| Engagement (ENG) | Diag | Is the generated text engaging? |
| Specific (SPE) | Diag | Is the generated text generic or specific to the source text? |
| Correctness (COR) | Diag | Is the generated text correct or was there a misunderstanding of the source text? |
| Semantically appropriate (SEM) | Diag | Is the generated text semantically appropriate? |
| Understandability (UND) | Diag | Is the generated text understandable? |
| Error Recovery (ERR) | Diag | Is the system able to recover from errors that it makes? |
| Diversity (DIV) | Diag | Is there diversity in the system responses? |
| Depth (DEP) | Diag | Does the system discuss topics in depth? |
| Likeability (LIK) | Diag | Does the system display a likeable personality? |
| Flexibility (FLE) | Diag | Is the system flexible and adaptable to the user and their interests? |
| Inquisitiveness (INQ) | Diag | Is the system inquisitive throughout the conversation? |

### Prompt Design
Taking the evaluation of the fluency of the text summarization task as an example, based on the prompt provided by OpenAI,3 the task prompt is "{Text} Tl;dr {Summary}", the definition of fluency is "Is the generated text well-written and grammatical?" (in Tab. 1), and then the final prompt template is "Generate a fluent and grammatical summary for the following text: {Text} Tl;dr {Summary}", where demonstrations could be introduced by repeating instantiating "{Text} Tl;dr {Summary}" In Appendix D, we list the prompts for various aspects of all tasks studied in this work and leave a more comprehensive exploration on prompt engineering as a future work.

<details>
<summary>Footnote</summary>
3 https://beta.openai.com/examples/default-tldr-summary
</details>

### Scoring Dimension
GPTSCORE exhibits different variants in terms of diverse choices of texts being calculated. For example, given a generated hypothesis, we can calculate GPTSCORE either based on the source text (i.e., src->hypo, p(hypo|src)) or based on the gold reference (i.e., ref->hypo, p(hypo|ref)). In this paper, the criteria for choosing GPTSCORE variants are mainly designed to align the protocol of human judgments (Liu et al., 2022) that are used to evaluate the reliability of automated metrics.

## Experimental Settings
### Tasks, Datasets, and Aspects
To achieve a comprehensive evaluation, in this paper, we cover a broad range of natural language generation tasks: Dialogue Response Generation, Text Summarization, Data-to-Text, and Machine Translation, which involves 37 datasets and 22 evaluation aspects in total. Tab. 8 summarizes the tasks, datasets, and evaluation aspects considered by each dataset. The definition of different aspects can be found in Tab. 1. More detailed illustrations about the datasets can be found in Appendix B.

1. Dialogue Response Generation aims to automatically generate an engaging and informative response based on the dialogue history. Here, we choose to use the FED (Mehri & Eskénazi, 2020) datasets and consider both turn-level and dialogue-level evaluations. 
2. Text Summarization is a task of automatically generating informative and fluent summary for a given long text. Here, we consider the following four datasets, SummEval (Bhandari et al., 2020), REALSumm (Bhandari et al., 2020), NEWSROOM (Grusky et al., 2018), and QAGS_XSUM (Wang et al., 2020), covering 10 aspects.
3. Data-to-Text aims to automatically generate a fluent and factual description for a given table. Our work considered BAGEL (Mairesse et al., 2010) and SFRES (Wen et al., 2015) datasets.
4. Machine Translation aims to translate a sentence from one language to another. We consider a subdatasets of Multidimensional Quality Metrics (MQM) (Freitag et al., 2021), namely, MQM-2020 (Chinese->English).

### Scoring Models
ROUGE (Lin, 2004) is a popular automatic generation evaluation metric. We consider three variants ROUGE-1, ROUGE-2, and ROUGE-L. PRISM (Thompson & Post, 2020) is a reference-based evaluation method designed for machine translation with pre-trained paraphrase systems. BERTScore (Zhang et al., 2020) uses contextual representation from BERT to calculate the similarity between the generated text and the reference text. MoverScore (Zhao et al., 2019) considers both contextual representation and Word Mover's Distance (WMD, (Kusner et al., 2015)) DynaEval (Zhang et al., 2021) is a unified automatic evaluation framework for dialogue response generation tasks on the turn level and dialogue level.

GPTSCORE is our evaluation method, which is designed based on different pre-trained language models.

### Scoring Dimension
Specifically, (1) For aspects INT, ENG, SPC, REL, COR, SEM, UND, and FLU of FED-Turn datasets from the open domain dialogue generation task, we choose the src->hypo variant since the human judgments of the evaluated dataset (i.e., FED-Turn) are also created based on the source. (2) For aspects COH, CON, and INF from SummEval and Newsroom, since data annotators labeled the data based on source and hypothesis texts, we chose src->hypo for these aspects.

(3) For aspects INF, NAT, and QUA from the data-to-text task, we choose src->hypo. Because the source text of the data-to-text task is not in the standard text format, which will be hard to handle by the scoring function. (4) For aspects ACC, FLU, and MQM from the machine translation task, we also choose src->hypo. Because the source text of the machine translation is a different language from the translated text (hypo). In this work, we mainly consider the evaluation of the English text. In the future, we can consider designing a scoring function based on BLOOM (Scao et al., 2022) that can evaluate texts in a cross-lingual setting.

### Evaluation Dataset Construction
Unlike previous works (Matiana et al., 2021; Xu et al., 2022a;b; Castricato et al., 2022) that only consider the overall text quality, we focus on evaluating multi-dimensional text quality. In this work, we studied 37 datasets according to 22 evaluation aspects. Due to the expensive API cost of GPT3, we randomly extract and construct sub-datasets for meta-evaluation. For the MQM dataset, since many aspects of samples lack human scores, we extract samples with human scores in ACC, MQM, and FLU as much as possible.

## Experiment Results
In this work, we focus on exploring whether language models with different structures and sizes can work in the following three scenarios. (a) vanilla (VAL): with non-instruction and non-demonstration; (b) instruction (IST): with instruction and non-demonstration; (c) instruction+demonstration (IDM): with instruction and demonstration.

Our significance test is to check (1) whether the performance of IST (IDM) is significantly better than VAL, and values achieved with the IST (IDM) settings will be marked † if it passes the significant test (p-value <0.05). (2) whether the performance of IDM is significantly better than IST, if yes, mark the value with IDM setting with ‡

### Text Summarization
| Model | COH | CON | FLU | REL | COV |
| --- | --- | --- | --- | --- | --- |
| ROUGE-1 | 14.1 - | 20.8 - | 14.8 - | 26.2 - | 46.4 - |
| ROUGE-2 | 9.1 - | 17.2 - | 12.0 - | 17.4 - | 37.3 - |
| ROUGE-L | 12.9 - | 19.8 - | 17.6 - | 24.7 - | 45.1 - |
| BERTSc | 25.9 - | 19.7 - | 23.7 - | 34.7 - | 38.4 - |
| MoverSc | 11.5 - | 18.0 - | 15.7 - | 24.8 - | 34.4 - |
| PRISM | 26.5 - | 29.9 - | 26.1 - | 25.2 - | 32.3 - |
| BARTSc | 29.7 - | 30.8 - | 24.6 - | 28.9 - | 43.1 - |
| +CNN | 42.5 - | 35.8 - | 38.1 - | 35.9 - | 42.9 - |
| +CNN+Pa | 42.5 - | 37.0 - | 40.5 - | 33.9 - | 40.9 - |
| GPT3-a01 | 39.3 39.8† | 39.7 40.5† | 36.1 35.9 | 28.2 27.6 | 29.5 29.8† |
| GPT3-b01 | 42.7 45.2† | 41.0 41.4† | 37.1 39.1† | 32.0 33.4† | 35.0 35.2† |
| GPT3-c01 | 41.3 40.8 | 44.6 45.1† | 38.9 39.5† | 31.6 33.2† | 36.1 45.1† |
| GPT3-d01 | 40.0 40.1 | 46.6 47.5† | 40.5 41.0† | 32.4 34.3† | 36.0 33.9 |
| GPT3-d03 | 43.7 43.4 | 45.2 44.9 | 41.1 40.3 | 36.3 38.1† | 35.2 38.0† |
| GPT2-M | 36.0 39.2† | 34.6 35.3† | 28.1 30.7† | 28.3 28.3 | 41.8 43.3† |
| GPT2-L | 36.4 39.8† | 33.7 34.4† | 29.4 31.5† | 27.8 28.1† | 39.6 41.3† |
| GPT2-XL | 35.3 39.9† | 35.9 36.1† | 31.2 33.1† | 28.1 28.0 | 40.4 41.0† |
| GPT-J-6B | 35.5 39.5† | 42.7 42.8† | 35.5 37.4† | 31.5 31.9† | 42.8 43.7† |

(1) Evaluator with instruction significantly improves the performance (values with † in Tab. 3).

(2) The benefit from instruction is more stable for the decoder-only models. In Tab. 3, the average Spearman score of both the GPT2 and OPT models, 9 out of 10 aspects are better than the vanilla setting (VAL) by using instruction (IST), while the equipment of instruction (IST) to the encoder-decoder model of FT5 on the NEWSROOM dataset fails to achieve gains. (3) As for the GPT3-based models, (a) the performance of GPT3-d01 is barely significantly better than GPT3-c01, which tries to balance power and speed. (b) GPT3-d03 performs better than GPT3-d01 significantly. We can observe these conclusions from Fig. 3, and both conclusions have passed the significance test at p < 0.05.

![](https://i.imgur.com/hWiAT2N.png)

### Machine Translation
| Model | ACC | FLU | MQM |
| --- | --- | --- | --- |
| GPT3 | 27.2 27.1 29.7†,‡ | 11.3 10.4 16.4†,‡ | 30.3 31.2† 32.3†,‡ |
| GPT2 | 25.8 27.0† 30.3†,‡ | 9.
Continuing the markdown formatting:

### Machine Translation
| Model | ACC | FLU | MQM |
| --- | --- | --- | --- |
| GPT3 | 27.2 27.1 29.7†,‡ | 11.3 10.4 16.4†,‡ | 30.3 31.2† 32.3†,‡ |
| GPT2 | 25.8 27.0† 30.3†,‡ | 9.8 10.8† 15.8†,‡ | 30.1 30.3† 33.5†,‡ |
| OPT | 28.7 29.4† 30.3†,‡ | 10.0 12.2† 16.3†,‡ | 32.5 34.6† 35.1†,‡ |
| FT5 | 27.7 27.8† 28.3† | 9.6 11.0† 15.4† | 31.0 32.3† 32.3† |
| Avg. | 27.4 27.8† 29.7†,‡ | 10.2 11.1† 16.0†,‡ | 31.0 32.1† 33.3†,‡ |

The main observations are listed as follows:
1. The introduction of instruction (IST) significantly improve the performance in three different aspects of ACC, FLU, and MQM. In Tab. 4, the average performance of 19 GPTSCORE based evaluators with instruction (IST) significantly outperforms vanilla (VAL). 
2. The combination of instruction and demonstration (IDM) brings gains for the evaluator with different model structures. In Tab. 4, the performance of GPT3, GPT2, OPT, and FT5 improves a lot when instruction and demonstration (IDM) are introduced.
3. The evaluator built based on GPT3-c01 achieves comparable performance with GPT3-d01 and GPT3-d03. This can be found in Fig. 4. Since the GPT3-d01 and GPT3-d03 are most expensive variant of GPT3, the cheaper and comparative GPT3-c01 is a good choice for machine translation task.

![](https://i.imgur.com/3InsxkW.png)

### Data-to-Text
| Model | INF | NAT | FLU |
| --- | --- | --- | --- |
| BAGEL |
| GPT3 | 35.4 38.3† 43.6†,‡ | 21.7 26.5† 36.9†,‡ | 30.5 32.9† 43.4†,‡ |
| GPT2 | 40.8 43.2† 40.2 | 31.4 33.0† 33.5†,‡ | 36.7 39.3† 41.3†,‡ |
| OPT | 38.7 39.3† 38.6 | 31.4 30.0 33.7†,‡ | 37.7 37.1† 41.5†,‡ |
| FT5 | 41.5 41.5† 39.1† | 26.5 29.7† 28.6† | 38.1 41.1† 40.3† |
| Avg. | 39.1 40.6† 40.3† | 27.7 29.8† 33.2†,‡ | 35.8 37.6† 41.6†,‡ |
| SFRES |
| GPT3 | 30.4 25.1 31.5†,‡ | 25.0 30.4† 26.5† | 31.2 30.9 26.1 |
| GPT2 | 22.5 25.1† 20.5 | 31.0 31.9† 37.0†,‡ | 20.0 33.1† 36.2†,‡ |
| OPT | 25.2 26.9† 24.3 | 26.2 30.0† 36.6†,‡ | 21.3 25.6† 30.6†,‡ |
| FT5 | 24.0 21.9 19.7‡ | 34.3 34.6† 36.8†,‡ | 22.0 17.8 19.7‡ |
| Avg. | 25.5 24.7 24.0 | 29.1 31.7† 34.2†,‡ | 23.6 26.8† 28.2†,‡ |

The main observations are listed as follows:
1. Introducing instruction (IST) can significantly improve performance, and introducing demonstration (DM) will further improve performance. In Tab. 5, the average performance on the three aspects is significantly improved when adapting to the instruction, and the performance of using demonstration on NAT and FLU has further significantly improved.
2. The decoder-only model is better at utilizing demonstration to achieve high performance. In Tab. 5, compare to the encoder-decoder model FT5, the performance has a more significant improvement for the decoder-only model of GPT2 and OPT on NAT and FLU aspects after introducing DM, which holds for both BAGEL and SFRES.
3. GPT3 has strong compatibility with unformatted text.

![](https://i.imgur.com/jyOToya.png)
![](https://i.imgur.com/S0yEbLX.png)

### Dialogue Response Generation
To test if GPTSCORE can generalize to more aspects, we choose the task of dialogue response generation as a testbed, which usually requires evaluating generated texts from a variety of dimensions (i.e., "interesting" and "fluent"). To reduce the computational cost, in this experiment, we focus on GPT3-based metrics since they have achieved superior performance as we observed in the previous experiments. Tab. 6 shows the Spearman correlation of different aspects on FED turn- and dialogue-level datasets. The main observations are listed as follows.

1. The performance of GPT3-d01 is much better than GPT3-d03, even though both of them have the same model size. The average Spearman correlation of GPT3-d01 outperforms GPT3-d03 by 40.8 on the FED Turn-level dataset, and 5.5 on the FED dialogue-level. 
2. The GPT3-based model demonstrate stronger generalization ability.

![](https://i.imgur.com/Q5wl5b6.png)

## Ablation Study
### Effectiveness of Demonstration
To investigate the relationship between the demonstration sample size (denote as K) and the evaluation performance, we choose the machine translation task and the GPT3-based variants with model sizes ranging from 350M to 175B for further study.

The main observations are summarized as follows:
1. The utilization of demonstration significantly improves the evaluation performance, which holds for these three aspects. 
2. There is an upper bound on the performance gains from the introduction of the demonstration. For example, when K>4, the performance of ACC is hard to improve further.
3. When DM has only a few samples (such as K=1), small models (e.g., GPT3-a01) are prone to performance degradation due to the one-sidedness of the given examples.

### Partial Order of Evaluation Aspect
To explore the correlation between aspects, we conducted an empirical analysis with INT (interesting) on the dialogue response generation task of the FED-Turn dataset. Specifically, take INT as the target aspect and then combine the definitions of other aspects with the definition of INT as the final evaluation protocols. The x-axis of Fig. 7-(a) is the aspect order achieved based on the Spearman correlation between INT and that aspect's human score. Fig. 7-(b) is the Spearman correlation o INT as the modification of the INT definition, and the scoring function is GPT3-c01.

Specifically, the definition of INT is "Is this response interesting to the conversation? " at x=1 in Fig. 7-(b). When INT combines with ENG, SPE (at x=3 in Fig. 7-(b)), its definition can be "Is this an interesting response that is specific and engaging?". And the new aspect definition boosts the performance from 30.8 (at x=1 in Fig. 7-(b)) to 48.6 (at x=3 in Fig. 7-(b)). The best performance of 51.4 (x=5 in Fig. 7-(b)) is achieved after combining five aspects (INT, ENG, SPE, COR, REL), which already exceeded 50.1 of the most potent scoring model GPT3-d01 with aspect definition built only on INT. Therefore, combining definitions with other highly correlated aspects can improve evaluation performance.

## Dataset Details
### Dialogue Response Generation
Dialogue Response Generation aims to automatically generate an engaging and informative response based on the dialogue history. (1) FED (Mehri & Eskénazi, 2020) collects 124 conversations, including both human-machine (Meena (Adiwardana et al., 2020), Mitsuku5 ) and human-human dialogues, and manually annotated 9 and 11 evaluation aspects at the turn- and dialogue-level, respectively.

### Text Summarization
Text Summarization is a task of automatically generating an informative and fluent summary for a given long text. Here, we consider the following four datasets covering 6 evaluation aspects: semantic coverage, informativeness, relevance, fluency, coherence, and factuality. (1) SummEval (Bhandari et al., 2020) collects human judgments on 16 model-generated summaries on the CNN/Daily Mail dataset, covering aspects of coherence, consistency, fluency, and relevance. (2) REALSumm (Bhandari et al., 2020) evaluates the reliability of automatic metrics by measuring the pyramid recall of text generated by 25 systems. (3) NEWSROOM (Grusky et al., 2018) covers news, sports, entertainment, finance, and other topics and evaluates the quality of summaries generated by 7 systems, including informativeness, relevance, fluency, and coherence. (4) QAGS_XSUM (Wang et al., 2020) is another dataset focusing on the factuality aspect. It has 239 samples from XSUM and their summaries are generated by a fine-tuned BART model.

### Data-to-Text
Data-to-Text aims to automatically generate a fluent and factual description for a given table. (1) BAGEL (Mairesse et al., 2010) contains 202 samples about restaurants in Cambridge. (2) SFRES (Wen et al., 2015) contains 581 samples about restaurants in San Francisco. These two datasets consider three evaluation aspects: informativeness, naturalness (relevance), and quality (fluency).

### Machine Translation
Machine Translation aims to translate a sentence from one language to another. We consider a sub-datasets of Multidimensional Quality Metrics (MQM) (Freitag et al., 2021), namely, MQM-2020 (Chinese->English). Due to limited annotations, here, we only consider three evaluation aspects: accuracy, fluency, and MQM with diverse scores.

## Prompt Design
In this work, we have studied four popular text generation tasks: text summarization, machine translation, data-to-text, and dialogue response generation. The instructions for these tasks on different evaluation aspects are summarized in Tab. 11 and Tab. 12. Here, we convert the dialogue response generation task as a boolean question-answering task and incorporate the aspect definition into the question of the boolean question-answering task.

| Aspect | Instruction |
| --- | --- |
| FED Turn-Level |
| INT | Answer the question based on the conversation between a human and AI.\nQuestion: Are the responses of AI interesting? (a) Yes. (b) No.\nConversation: {History}\nAnswer: Yes. |
| ENG | Answer the question based on the conversation between a human and AI.\nQuestion: Are the responses of AI engaging? (a) Yes. (b) No.\nConversation: {History}\nAnswer: Yes. |
| UND | Answer the question based on the conversation between a human and AI.\nQuestion: Are the responses of AI understandable? (a) Yes. (b) No.\nConversation: {History}\nAnswer: Yes. |
| REL | Answer the question based on the conversation between a human and AI.\nQuestion: Are the responses of AI relevant to the conversation? (a) Yes. (b) No.\nConversation: {History}\nAnswer: Yes. |
| ... |

![](https://i.imgur.com/V8OZ7g3.png)

<details>
<summary>Why did they convert the dialogue response generation task as a boolean question-answering task?</summary>
The paper states that they convert the evaluation of the dialogue response generation task into a boolean question-answering task in order to incorporate the aspect definition into the question of the question-answering task. This allows them to present each evaluation sample with the evaluated protocol that includes the aspect definition, which can facilitate the model's learning.
</details>
