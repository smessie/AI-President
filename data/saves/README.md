# Overview of all trainings
## 0


## 1
1000 games with 10 rounds each.
Epsilon = 0

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 100        | 0             | 3            | 100, 300      | 2000            | 0       |

## 2
250 games with 20 rounds each.
Epsilon = 0

Try if he doesn't need epsilon greedy policy if he can learn from his opponents who are already random agents.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 50         | 3             | 0            | 78, 260       | 2000            | 0       |

## 3
250 games with 20 rounds each.
Epsilon = 20

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 50         | 3             | 0            | 78, 260       | 2000            | 20      |

## 4
250 games with 20 rounds each.
Epsilon = 20

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 100        | 3             | 0            | 78, 260       | 2000            | 20      |