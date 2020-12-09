# Overview of all trainings


## BaseLine
10 games with 20 rounds each.
Untrained agent

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| (/) 20     | 2             | 1            | 78, 260       | (/) 2000        | (/) 5   |

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
250 games with 20 rounds each.
Epsilon = 20
More different rewards. Change also kept for further trainings.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 50         | 3             | 0            | 78, 260       | 2000            | 20      |

## 7
### TODO: Rerun this training, we had wrong results before
250 games with 20 rounds each.
Epsilon = 20
One larger hidden layer

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 20         | 3             | 0            | 480           | 2000            | 20      |

## 8
250 games with 20 rounds each.
Epsilon = 20
Train against 2 basic and 1 random agent. He can learn more from basic agents?

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 50         | 1             | 2            | 78, 260       | 2000            | 20      |

## 9
250 games with 20 rounds each.
Epsilon = 20
Living reward of -0.01, which means that for each agent the last move counts for 100% but a negative reward of -0.01 is deducted for each previous move.  
Example for total of 3 moves:  
move 1: reward - 0.02  
move 2: reward - 0.01  
move 3: reward

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 50         | 1             | 2            | 78, 260       | 2000            | 20      |

## 10
250 games with 20 rounds each.  
Epsilon = 20  
Includes living reward as in training 9.  
Change buffer capacity from 2000 to 500 to investigate effect on training loss.  

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 50         | 1             | 2            | 78, 260       | 500             | 20      |

## 11
250 games with 20 rounds each.  
Epsilon = 0  
Includes living reward as in training 9.  
Enabled lower epsilon over time starting from 4000.  

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 50         | 1             | 2            | 78, 260       | 2000            | 0       |

## 12
Basicagent looks like it yields better result, so training on basic agents
(working towards batch size= 100 (since most games average 80 turns) , epsilon of 5)
250 games with 20 rounds each.
Epsilon = 20
More different rewards. Change also kept for further trainings.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 50         | 0             | 3            | 78, 260       | 2000            | 20      |

## 13
250 games with 20 rounds each.  
Epsilon = 20  
Includes living reward as in training 9, but now against 3 random agents.  

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 50         | 3             | 0            | 78, 260       | 2000            | 20      |

## 14
250 games with 20 rounds each.  
Epsilon = 20  
Includes living reward as in training 9.  
Enabled lower epsilon over time starting from 4000.  
Variation on training 11 but epsilon after lowering is now 20.  

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon |
| -----------|---------------|--------------|---------------|-----------------|---------|
| 50         | 1             | 2            | 78, 260       | 2000            | 20      |
