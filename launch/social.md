# RealBio: social copy for review

Status: draft, not posted. The benchmark artifacts are the link target; do not describe the revised preprint as published until its final public link is added. Approved current name: RealBio. Use `realbio-social-card.png` or the QC result figure, not old product leaderboards.

## LinkedIn

Choosing the right workflow is only one decision a bioinformatics assistant must make. It also needs to extract the parameters a researcher actually specified, choose an appropriate method and recognize protocol-specific quality warnings.

RealBio examines these component decisions with fixed references and transparent scoring. In paired comparisons across 14 model endpoints, a described, benchmark-derived workflow vocabulary raises mean routing accuracy from 0.382 to 0.913. Parameter extraction becomes more complete with candidate-key guidance, but forbidden fills increase: the joint correct-and-no-forbidden-fill rate reaches 0.371, below the guided F1 of 0.701.

The QC study illustrates why one headline score is insufficient. The original method card improves overall accuracy while suppressing WARN recall. A complete revision improves balanced accuracy on 60 out-of-family protocol items by 0.102 [95% interval 0.050–0.154] over the original card.

These are decision-level results. No scientific workflow is executed in the scored comparisons. Candidate information and labels are author-constructed, and model-generated relabeling is reported as sensitivity analysis, not independent expert validation.

We are sharing the fixed items, saved predictions, scoring code and offline analyses so others can inspect the findings and their limits.

https://github.com/bioMate-AI/realbio-benchmark

#Bioinformatics #LLMEvaluation #ReproducibleResearch #AIforScience

## X thread (each paragraph is one post)

1/ RealBio examines workflow routing, parameter extraction, method selection and protocol-QC decisions. It compares the same model endpoints with and without specified context. Workflows are not executed in these scored experiments.

2/ A described, benchmark-derived vocabulary raises mean routing accuracy from 0.382 to 0.913 across 14 endpoints. The 63-label list comes from benchmark references; this is not independent retrieval from a full production catalog.

3/ More complete parameter extraction can bring more unwanted fills. Guided F1 reaches 0.701; joint correct-and-no-forbidden-fill success reaches 0.371. Four endpoints are paired, three from one model family.

4/ Overall QC accuracy can hide WARN-recall failure. On 60 out-of-family items, the revised card improves balanced accuracy over the original by 0.102 [0.050, 0.154]. Both sets use the authors' labeling framework.

5/ Reproducible scores are useful; they do not establish independent label validity or successful scientific execution. Code, references and archived predictions: https://github.com/bioMate-AI/realbio-benchmark

## 微信公众号 / 中文长帖

**RealBio：科研助手选对流程之后，还需要做对什么？**

选工作流、提取参数、选择统计方法、识别数据质量警告，都是生物信息学平台的重要决策。RealBio 将这些能力拆开评测，比较相同模型在不同上下文条件下的表现。

在14个模型端点的配对比较中，提供带描述的固定工作流候选表后，平均路由准确率从0.382升至0.913。候选表由评测参考标签构成，共63个标签，并不代表从完整生产目录中独立检索的结果。参数提示提高了提取完整度，也增加了不该填写的参数：提示条件下F1为0.701，但“所有必填值匹配、且不填禁止项”的联合成功率仅为0.371。该配对实验只有4个模型，其中3个属于同一模型家族。

协议质控实验进一步说明，总体准确率提高，不等于每类错误都减少。原始方法卡提高了总体准确率，却降低了WARN召回率。完整修订后，在60个新协议类别题目上，相比原始卡的平衡准确率提高0.102，95%区间为0.050–0.154。

这些结果针对固定参考答案下的决策，没有执行实际科研工作流。质控题目与标签沿用作者制定的框架；已有大模型重标注只用于敏感性分析，不是独立专家验证。我们公开题目、逐项预测、计分规则和离线复现程序，希望研究者能够检查结果，也检查限制。

项目：https://github.com/bioMate-AI/realbio-benchmark

## 小红书

**科研AI总分提高，哪类错误却更多了？**

RealBio把科研助手的路由、参数、方法选择和协议质控逐项检查。14个模型加入固定候选表后，平均路由准确率0.382→0.913；但参数提取得更全的同时，也更容易多填不该填的内容。

另一个发现：原始质控卡提高总体准确率，却漏掉更多WARN。修订后，60个新协议题目的平衡准确率相比原卡提高0.102。

这是决策评测，不是完整流程执行成功率。候选表和质控标签的构造方式、计分限制与逐项结果都一起公开。

项目链接：https://github.com/bioMate-AI/realbio-benchmark

#科研AI #生物信息学 #大模型评测 #科研工具
