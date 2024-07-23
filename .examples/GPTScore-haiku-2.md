Here is the document reformatted to beautiful markdown, with some sections hidden behind <details> tags:

# Notes for GPTScore

<details>
<summary>Challenges</summary>

...
assessing the quality of the generation is an even more arduous task than the generation itself, and this issue has not been given adequate consideration recently. This paper proposes a novel evaluation framework, GPTSCORE, which utilizes the emergent abilities (e.g., zero-shot instruction) of generative pre-trained models to score generated texts. There are 19 pre-trained models explored in this paper, ranging in size from 80M (e.g., FLAN-T5-small) to 175B (e.g., GPT3). Experimental results on four text generation tasks, 22 evaluation aspects, and corresponding 37 datasets demonstrate that this approach can effectively allow us to achieve what one desires to evaluate for texts simply by natural language instructions. This nature helps us overcome several long-standing challenges in text evaluation–how to achieve customized, multi-faceted evaluation without the need for annotated samples. We make our code publicly available. 1
</details>

![Existing studies evaluate text quality with limited aspects (e.g., semantic equivalence, fluency) (Fig. 1-(a)), which are usually customized prohibitively, making it harder for users to evaluate aspects as they need (Freitag et al., 2021). (b) A handful of studies have examined multi-aspect evaluation (Yuan et al., 2021; Scialom et al., 2021; Zhong et al., 2022) but have not given adequate attention to the definition of the evaluation aspect and the latent relationship among them. Instead, the evaluation of an aspect is either empirically bound with metric variants (Yuan et al., 2021) or learned by supervised signals (Zhong et al., 2022). (c) Recently proposed evaluation methods (Mehri & Eskénazi, 2020; Rei et al., 2020; Li et al., 2021; Zhong et al., 2022) usually necessitate a complicated training procedure or costly manual annotation of samples (Fig. 1-(a,b)), which makes it hard to use these methods in industrial settings due to the amount of time needed for annotation and training to accommodate a new evaluation demand from the user.](https://i.imgur.com/zAjlpvs.png)

In this paper, we demonstrated the talent of the super large pre-trained language model (e.g., GPT-3) in achieving multi-aspect, customized, and training-free evaluation (Fig. 1-(c)). In essence, it skillfully uses the pre-trained model's zero-shot instruction (Chung et al., 2022), and in-context learning (Brown et al., 2020; Min et al., 2022) ability to deal with complex and ever-changing evaluation needs so as to solve multiple evaluation challenges that have been plagued for many years at the same time.

Specifically, given a text generated from a certain context, and desirable evaluation aspects (e.g., fluency), the high-level idea of the proposed framework is that the higher-quality text of a certain aspect will be more likely generated than uqualified ones based on the given context, where the "likely" can be measured by the conditional generation probability. As illustrated in Fig. 2, to capture users' true desires, an evaluation protocol will be initially established based on (a) the task specification, which typically outlines how the text is generated (e.g., generate a response for a human based on the conversation.) (b) aspect definition that documents the details of desirable evaluation aspects (e.g., the response should be intuitive to understand). Subsequently, each evaluation sample will be presented with the evaluated protocol with optionally moderate exemplar samples, which could facilitate the model's learning. Lastly, a large generative pre-trained model will be used to calculate how likely the text could be generated based on the above evaluation protocol, thus giving rise to our model's name: GPTSCORE.

![](https://i.imgur.com/5dZsbKS.png)

<details>
<summary>Training language models to follow instructions with human feedback</summary>

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

<details>
<summary>Emergent Ability</summary>

Recent works progressively reveal a variety of emergent abilities of generative pre-trained language models with appropriate tuning or prompting methods, such as in-context learning (Min et al., 2022), chain-of-thought reasoning (Wei et al., 2022), and zero-shot instruction (Ouyang et al., 2022). One core commonality of these abilities is to allow for handling customized requirements with a few or even zero annotated examples. It's the appearance of these abilities that allows us to re-invent a new way for text evaluation–evaluating from the textual description, which can achieve customizable, multi-faceted, and train-free evaluation.
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

<details>
<summary>Few-shot with Demonstration</summary>

The generative pre-trained language model can better perform tasks when pre-fixed with a few annotated samples (i.e., demonstrations). Our proposed framework is flexible in supporting this by extending the prompt template T with demonstrations.
</details>

<details>
<summary>Choice of Prompt Template</summary>

Prompt templates define how task description, aspect definition, and context are organized. Minging desirable prompts itself is a non-trivial task and there are extensive research works there (Liu et al., 2021; Fu et al., 2022). In this work, for the GPT3-based model, we opt for prompts that are officially provided by OpenAI.2 
2
https://beta.openai.com/examples

For instruction-based pre-trained models, we use prompts from NaturalInstruction (Wang et al., 2022) since it's the main training source for those instruction-based pre-train models.
</details>

<details>
<summary>Polyglot Prompt: Multilingual Multitask PrompTraining</summary>

Jinlan Fu, See-Kiong Ng, Pengfei Liu
This paper aims for a potential architectural improvement for multilingual learning and asks: Can different tasks from different languages be modeled in a monolithic framework, i.e. without any task/language-specific module? The benefit of achieving this could open new doors for future multilingual research, including allowing systems trained on low resources to be further assisted by other languages as well as other tasks. We approach this goal by developing a learning framework named Polyglot Prompting to exploit prompting methods for learning a unified semantic space for different languages and tasks with multilingual prompt engineering. We performed a comprehensive evaluation of 6 tasks, namely topic classification, sentiment classification, named entity recognition, question answering, natural language inference, and summarization, covering 24 datasets and 49 languages. The experimental results demonstrated the efficacy of multilingual multitask prompt-based learning and led to inspiring observations. We also present an interpretable multilingual evaluation methodology and show how the proposed framework, multilingual multitask prompt training, works. We release all datasets prompted in the best setting and code.
</details>

## 4. Experimental Settings

### 4.1. Tasks, Datasets, and Aspects
To achieve a comprehensive evaluation, in this paper, we cover a broad range of natural language generation tasks: Dialogue Response Generation, Text Summarization, Data-to-Text, and Machine Translation, which involves 37 datasets and 22 evaluation aspects in total. Tab. 8 summarizes the tasks, datasets, and evaluation aspects considered by each dataset. The definition of different aspects can be found in Tab. 1. More detailed illustrations about the datasets can be found in Appendix B.

(1) Dialogue Response Generation aims to automatically generate an engaging and informative response based on the dialogue history. Here, we choose to use the FED (Mehri & Eskénazi, 2020) datasets and consider both turn-level and dialogue-level evaluations. (2) Text Summarization is a task of automatically generating informative and fluent summary for a given long text. Here, we consider the following four datasets, SummEval (Bhandari et al., 2020), REALSumm (Bhandari et al., 2020), NEWSROOM (Grusky et al., 2018), and QAGS_XSUM (Wang et al., 2020), covering 10 aspects. (3) Data-to-Text aims to automatically generate a fluent and factual description for a given table. Our work considered BAGEL (Mairesse et al., 2010) and SFRES (Wen et al., 2015) datasets. (4) Machine Translation aims to translate a sentence from one language to another. We consider a subdatasets of Multidimensional Quality Metrics (MQM) (Freitag et al., 2021), namely, MQM-2020 (Chinese->English).

### 4.2. Scoring Models
ROUGE (Lin, 2004) is a popular automatic generation evaluation metric. We consider three variants ROUGE-1, ROUGE-2, and ROUGE-L. PRISM (Thompson & Post, 2020) is a reference-based evaluation method designed for machine translation with pre-trained paraphrase systems. BERTScore (Zhang et al., 2020) uses contextual representation from BERT to calculate the similarity between the generated text and the reference text. MoverScore (Zhao et al., 2019) considers both contextual representation and Word Mover's Distance (WMD, (Kusner et al., 2015)) DynaEval (Zhang et al., 2021) is a unified automatic evaluation framework for dialogue response generation tasks on the turn level and dialogue level.

GPTSCORE is our evaluation method, which is designed based on different pre-trained language models.

### 4.3. Scoring Dimension
Specifically, (1) For aspects INT, ENG, SPC, REL, COR, SEM, UND, and FLU of FED-Turn datasets from the open domain dialogue generation task, we choose the src->hypo variant since the human judgments of the evaluated dataset (i.e., FED-Turn) are also created based on the source. (2) For aspects COH, CON, and INF from SummEval and Newsroom, since data annotators labeled the data based on source and hypothesis texts, we chose src->hypo for these aspects.

(3) For aspects INF, NAT, and QUA from the data-to-text task, we choose src->hypo. Because the source text of the data-to-text task is not in the standard text format, which will be hard to handle by the scoring function. (4) For aspects ACC, FLU, and MQM from the machine translation task, we also choose src->hypo. Because the source text of the machine translation is a different language from the translated text (hypo). In this work, we mainly consider the evaluation of the English text. In the future, we can consider designing a scoring function based on BLOOM (Scao et al., 2022) that can evaluate texts in a cross-lingual setting.

### 4.4. Evaluation Dataset Construction
Sure, here's the rest of the document:

Unlike previous works (Matiana et al., 2021; Xu et al., 2022a;b; Castricato et al., 2022) that only consider the overall text quality, we focus on evaluating multi-dimensional text quality. In this work, we studied 37 datasets according to 22 evaluation aspects. Due to the expensive API cost of GPT3, we randomly extract and construct sub-datasets for meta-evaluation. For the MQM dataset, since many aspects of samples lack human scores, we extract samples with human scores in ACC, MQM, and FLU as much as possible.

## 5. Experiment Results

In this work, we focus on exploring whether language models with different structures and sizes can work in the following three scenarios. (a) vanilla (VAL): with non-instruction and non-demonstration; (b) instruction (IST): with instruction and non-demonstration; (c) instruction+demonstration (IDM): with instruction and demonstration.

Our significance test is to check (1) whether the performance of IST (IDM) is significantly better than VAL, and values achieved with the IST (IDM) settings will be marked † if it passes the significant test (p-value <0.05). (2) whether the performance of IDM is significantly better than IST, if yes, mark the value with IDM setting with ‡

### 5.1. Text Summarization

![Spearman correlations on NEWSROOM and QXSUM datasets for text summarization task. VAL and IST denote the evaluator with vanilla and instruction, respectively. Values with † denote the evaluator with instruction significantly outperforms with vanilla. Values in bold are the best performance in a set of variants (e.g., GPT3 family).](https://i.imgur.com/3InsxkW.png)

(1) Evaluator with instruction significantly improves the performance (values with † in Tab. 3).

(2) The benefit from instruction is more stable for the decoder-only models. In Tab. 3, the average Spearman score of both the GPT2 and OPT models, 9 out of 10 aspects are better than the vanilla setting (VAL) by using instruction (IST), while the equipment of instruction (IST) to the encoder-decoder model of FT5 on the NEWSROOM dataset fails to achieve gains. (3) As for the GPT3-based models, (a) the performance of GPT3-d01 is barely significantly better than GPT3-c01, which tries to balance power and speed. (b) GPT3-d03 performs better than GPT3-d01 significantly. We can observe these conclusions from Fig. 3, and both conclusions have passed the significance test at p < 0.05.

![](https://i.imgur.com/hWiAT2N.png)

### 5.2. Machine Translation

![Spearman correlations on MQM-2020 dataset for machine translation task. VAL, IST, and IDM denote the evaluator with vanilla, instruction, and the combination of instruction and demonstration, respectively. Values with † denote the evaluator with instruction significantly outperforms with vanilla, and values with ‡ denote the evaluator with the combination of instruction and demonstration significantly outperforms with only instruction. Values in bold are the best performance in a set of variants (e.g., GPT3 family).](https://i.imgur.com/3InsxkW.png)

The main observations are listed as follows:
(1) The introduction of instruction (IST) significantly improve the performance in three different aspects of ACC, FLU, and MQM. In Tab. 4, the average performance of 19 GPTSCORE based evaluators with instruction (IST) significantly outperforms vanilla (VAL). (2) The combination of instruction and demonstration (IDM) brings gains for the evaluator with different model structures. In Tab. 4, the performance of GPT3, GPT2, OPT, and FT5 improves a lot when instruction and demonstration (IDM) are introduced. (3) The evaluator built based on GPT3-c01 achieves comparable performance with GPT3-d01 and GPT3-d03. This can be found in Fig. 4. Since the GPT3-d01 and GPT3-d03 are most expensive variant of GPT3, the cheaper and comparative GPT3-c01 is a good choice for machine translation task.

### 5.3. Data to Text

![Spearman correlations on BAGEL dataset for data-to-text task. VAL, IST, and IDM denote the evaluator with vanilla, instruction, and the combination of instruction and demonstration, respectively. Values with † denote the evaluator with instruction significantly outperforms with vanilla, and values with ‡ denote the evaluator with the combination of instruction and demonstration significantly outperforms with only instruction. Values in bold are the best performance in a set of variants (e.g., GPT3 family).](https://i.imgur.com/jyOToya.png)

![Spearman correlations on SFRES dataset for data-to-text task. VAL, IST, and IDM denote the evaluator with vanilla, instruction, and the combination of instruction and demonstration, respectively. Values with † denote the evaluator with instruction significantly outperforms with vanilla, and values with ‡ denote the evaluator with the combination of instruction and demonstration significantly outperforms with only instruction. Values in bold are the best performance in a set of variants (e.g., GPT3 family).](https://i.imgur.com/S0yEbLX.png)

The main observations are listed as follows:
(1) Introducing instruction (IST) can significantly improve performance, and introducing demonstration (DM) will further improve performance. In Tab. 5, the average performance on the three aspects is significantly improved when adapting to the instruction, and the performance of using demonstration on NAT and FLU has further significantly improved. (2) The decoder-only model is better at utilizing demonstration to achieve high performance. In Tab. 5, compare to the encoder-decoder model FT5, the performance has a more significant improvement for the decoder-only model of GPT2 and OPT on NAT and FLU aspects after introducing DM, which holds for both BAGEL and SFRES. (3) GPT3 has strong compatibility with unformatted text.

### 5.4. Dialogue Response Generation

To test if GPTSCORE can generalize to more aspects, we choose the task of dialogue response generation as a testbed, which usually requires evaluating generated texts from a variety of dimensions (i.e., "interesting" and "fluent"). To reduce the computational cost, in this experiment, we focus on GPT3-based metrics since they have achieved superior performance as we observed in the previous experiments.

![Spearman correlations on FED turn- and dialogue-level datasets](https://i.imgur.com/Q5wl5b6.png)

The main observations are listed as follows.
(1) The performance of GPT3-d01 is much better than GPT3-d03, even though both of them have the same model size. The average Spearman correlation of GPT3-d01 outperforms GPT3-d03 by 40.8 on the FED Turn-level dataset, and 5.5 on the FED dialogue-level. (2) The GPT3-based model demonstrate stronger generalization ability.

## 6. Ablation Study

### 6.1. Effectiveness of Demonstration
To investigate the relationship between the demonstration sample size (denote as K) and the evaluation performance, we choose the machine translation task and the GPT3-based variants with model sizes ranging from 350M to 175B for further study.

The main observations are summarized as follows:
(1) The utilization of demonstration significantly improves the evaluation performance, which holds for these three aspects. (2) There is an upper bound on the performance gains from the introduction of the demonstration. For example, when K>4, the performance of ACC is hard to improve further. (3) When DM has only a few samples (such as K=1), small models (e.g., GPT3-a01) are prone to performance degradation due to the one-sidedness of the given examples.

### 6.2. Partial Order of Evaluation Aspect
To explore the correlation between aspects, we conducted an empirical analysis with INT (interesting) on the dialogue response generation task of the FED-Turn dataset. Specifically, take INT as the target aspect and then combine the definitions of other aspects with the definition of INT as the final evaluation protocols. The x-axis of Fig. 7-(a) is the aspect order achieved based on the Spearman correlation between INT and that aspect's human score. Fig. 7-(b) is the Spearman correlation o INT as the modification of the INT definition, and the scoring function is GPT3-c01.
The following table illustrates the definition composition process, where Sp denotes Spearman.

| X | Aspect | Aspect Definition | Sp |
| --- | --- | --- | --- |
| 1 | Interesting (INT) | Is this response interesting to the conversation? | 30.8 |
| 3 | INT, ENG, SPE | Is this an interesting response that is specific and engaging? | 48.6 |

Specifically, the definition of INT is "Is this response interesting to the conversation? " at x=1 in Fig. 7-(b). When INT combines with ENG, SPE (at x=3 in Fig. 7-(b)), its definition can be "Is this an interesting response that is specific and engaging?". And the new aspect definition boosts the performance from 30.8 (at x=1 in Fig. 7-(b)) to 48.6 (at x=3 in Fig. 7-(b)). The best performance of 51.4 (x=5 in Fig. 7-(b)) is achieved after combining five aspects (INT, ENG, SPE, COR, REL), which already exceeded 50.1 of the most potent scoring model GPT3-d01 with aspect definition built only on INT. Therefore, combining definitions with other highly correlated aspects can improve evaluation performance.

<details>
<summary>Dataset Details</summary>

Dialogue Response Generation aims to automatically generate an engaging and informative response based on the dialogue history. (1) FED (Mehri & Eskénazi, 2020) collects 124 conversations, including both human-machine (Meena (Adiwardana et al., 2020), Mitsuku5 ) and human-human dialogues, and manually annotated 9 and 11 evaluation aspects at the turn- and dialogue-level, respectively.

Text Summarization is a task of automatically generating an informative and fluent summary for a given long text. Here, we consider the following four datasets covering 6 evaluation aspects: semantic coverage, informativeness, relevance, fluency, coherence, and factuality. (1) SummEval (Bhandari et al., 2020) collects human judgments on 16 model-generated summaries on the CNN/Daily Mail dataset, covering aspects of coherence, consistency, fluency, and relevance. (2) REALSumm (Bhandari et al., 2020) evaluates the reliability of automatic metrics by measuring the pyramid recall of text generated by 25 systems. (3) NEWSROOM (Grusky et al., 2018) covers news, sports, entertainment, finance, and other topics and evaluates the quality of summaries generated by 7 systems, including informativeness, relevance, fluency, and coherence. (4) QAGS_XSUM (Wang et al., 2020) is another dataset focusing on the factuality aspect. It has 239 samples from XSUM and their summaries are generated by a fine-tuned BART model.

Data-to-Text aims to automatically generate a fluent and factual description for a given table. (1) BAGEL (Mairesse et al., 2010) contains 202 samples about restaurants in Cambridge. (2) SFRES (Wen et al., 2015) contains 581 samples about restaurants in San Francisco. These two datasets consider three evaluation aspects: informativeness, naturalness (relevance), and quality (fluency).
Machine Translation aims to translate a sentence from one language to another. We consider a sub-datasets of Multidimensional Quality Metrics (MQM) (Freitag et al., 2021), namely, MQM-2020 (Chinese->English). Due to limited annotations, here, we only consider three evaluation aspects: accuracy, fluency, and MQM with diverse scores.
</details>

<details>
<summary>Prompt Design</summary>

In this work, we have studied four popular text generation tasks: text summarization, machine translation, data-to-text, and dialogue response generation. The instructions for these tasks on different evaluation aspects are summarized in Tab. 11 and Tab. 12. Here, we convert the dialogue response generation task as a boolean question-answering task and incorporate the aspect definition into the question of the boolean question-answering task.
</details>
Unfortunately, there is no more content to the document after the "Prompt Design" section. The document ends there.
