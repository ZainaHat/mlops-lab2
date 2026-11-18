# Model selection

## The question

This model predicts whether a telecom customer is likely to churn. A wrong prediction could cause the company to miss a customer who is about to leave, or spend retention resources on a customer who would have stayed.

## Candidates

| Candidate | Why I tried it | AUC | F1 | F1 per slice (lowest) | p95 latency (ms) | Size (KB) | MLflow run ID |
|---|---|---:|---:|---:|---:|---:|---|
| Logistic Regression | Simple, fast baseline | 0.783 | 0.512 | 0.000 | 5.99 | 3.55 | c410737d17b24e3e98707f67ed5a8dc4 |
| Random Forest | Captures nonlinear patterns | 0.759 | 0.529 | 0.167 | 24.72 | 3106 | 4f6f86e6307c4eecbc9f31eb27411a30 |
| Gradient Boosting | Strong ensemble candidate | 0.775 | 0.496 | 0.222 | 5.42 | 141 | 81f2b004d3f34894954694e5337d6af2 |

## The champion

I selected **Random Forest** as the champion because it achieved the highest overall F1 score (0.529), compared with Logistic Regression (0.512) and Gradient Boosting (0.496).

Random Forest also achieved a better worst-slice F1 (0.167) than Logistic Regression (0.000).

The trade-offs are its lower AUC (0.759), higher p95 latency (24.72 ms), and larger model size (3106 KB). I accepted these trade-offs because the model provides the best overall F1 among the three candidates while staying within my proposed latency budget.

## My promotion rules

- **Latency budget (p95): 30 ms**, because predictions should remain reasonably fast for the application.
- **Minimum gain to replace the champion (F1 points): 0.02**, because a new model should show a meaningful improvement rather than a very small difference.

These are proposed promotion thresholds for the next stages of the project.

## What I would check next

I would investigate model performance across customer contract types, especially groups with low F1 scores or small sample sizes. I would also monitor data drift because customer behavior may change over time, affecting the model's performance in production.