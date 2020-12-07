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

## 5
250 games with 20 rounds each.
Epsilon = 20
More (relatively small) hidden layers.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 20         | 3             | 0            | 78, 78, 78    | 2000            | 20      |

## 6
### TODO: Rerun this training, we had wrong results before
250 games with 20 rounds each.
Epsilon = 20
More different rewards. Change also kept for further trainings.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 20         | 3             | 0            | 78, 260       | 2000            | 20      |

## 7
### TODO: Rerun this training, we had wrong results before
250 games with 20 rounds each.
Epsilon = 20
One larger hidden layer

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 20         | 3             | 0            | 480           | 2000            | 20      |

## 8
### TODO: Rerun this training, we had wrong results before
250 games with 20 rounds each.
Epsilon = 20
Train against 2 basic and 1 random agent. He can learn more from basic agents?

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 20         | 1             | 2            | 78, 260       | 2000            | 20      |

## 9
### TODO: Rerun this training, we had wrong results before
250 games with 20 rounds each.
Epsilon = 20
Living reward of -0.01, which means that for each agent the last move counts for 100% but a negative reward of -0.01 is deducted for each previous move.  
Example for total of 3 moves:  
move 1: reward - 0.02  
move 2: reward - 0.01  
move 3: reward

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 20         | 1             | 2            | 78, 260       | 2000            | 20      |