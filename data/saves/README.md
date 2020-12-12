# Overview of all trainings


## BaseLine
10 games with 20 rounds each.
Untrained agent

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| (/) 20     | 2             | 1            | 78, 260       | (/) 2000        | (/) 5   | 0.9   |

## 0


## 1
1000 games with 10 rounds each.
Epsilon = 0

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 100        | 0             | 3            | 100, 300      | 2000            | 0       | 0.9   |

## 2
250 games with 20 rounds each.
Epsilon = 0

Try if he doesn't need epsilon greedy policy if he can learn from his opponents who are already random agents.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 50         | 3             | 0            | 78, 260       | 2000            | 0       | 0.9   |

## 3
250 games with 20 rounds each.
Epsilon = 20

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 50         | 3             | 0            | 78, 260       | 2000            | 20      | 0.9   |

## 4
250 games with 20 rounds each.
Epsilon = 20

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 100        | 3             | 0            | 78, 260       | 2000            | 20      | 0.9   |

## 5
250 games with 20 rounds each.
Epsilon = 20
More (relatively small) hidden layers.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 20         | 3             | 0            | 78, 78, 78    | 2000            | 20      | 0.9   |

## 6
250 games with 20 rounds each.
Epsilon = 20
More different rewards. Change also kept for further trainings.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 50         | 3             | 0            | 78, 260       | 2000            | 20      | 0.9   |

## 7
### TODO: Rerun this training, we had wrong results before
250 games with 20 rounds each.
Epsilon = 20
One larger hidden layer

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 20         | 3             | 0            | 480           | 2000            | 20      | 0.9   |

## 8
250 games with 20 rounds each.
Epsilon = 20
Train against 2 basic and 1 random agent. He can learn more from basic agents?

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 50         | 1             | 2            | 78, 260       | 2000            | 20      | 0.9   |

## 9
250 games with 20 rounds each.
Epsilon = 20
Living reward of -0.01, which means that for each agent the last move counts for 100% but a negative reward of -0.01 is deducted for each previous move.  
Example for total of 3 moves:  
move 1: reward - 0.02  
move 2: reward - 0.01  
move 3: reward

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 50         | 1             | 2            | 78, 260       | 2000            | 20      | 0.9   |

## 10
250 games with 20 rounds each.  
Epsilon = 20  
Includes living reward as in training 9.  
Change buffer capacity from 2000 to 500 to investigate effect on training loss.  

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 50         | 1             | 2            | 78, 260       | 500             | 20      | 0.9   |

## 11
250 games with 20 rounds each.  
Epsilon = 0  
Includes living reward as in training 9.  
Enabled lower epsilon over time starting over 4000 training on batches and with epsilon starting at 100%.  

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 50         | 1             | 2            | 78, 260       | 2000            | 0       | 0.9   |

## 12
Basicagent looks like it yields better result, so training on basic agents
(working towards batch size= 100 (since most games average 80 turns) , epsilon of 5)
250 games with 20 rounds each.
Epsilon = 20
More different rewards. Change also kept for further trainings.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 50         | 0             | 3            | 78, 260       | 2000            | 20      | 0.9   |

## 13
250 games with 20 rounds each.  
Epsilon = 20  
Includes living reward as in training 9, but now against 3 random agents.  

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 50         | 3             | 0            | 78, 260       | 2000            | 20      | 0.9   |

## 14
250 games with 20 rounds each.  
Epsilon = 20  
Includes living reward as in training 9.  
Enabled lower epsilon over time starting over 4000 training on batches and with epsilon starting at 100%.  
Variation on training 11 but epsilon after lowering is now 20.  

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 50         | 1             | 2            | 78, 260       | 2000            | 20      | 0.9   |

## 15
Basicagent looks like it yields better result, so training on basic agents
250 games with 20 rounds each.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 100        | 0             | 3            | 78, 260       | 2000            | 5       | 0.9   |

## 16
Basicagent looks like it yields better result, so training on basic agents
250 games with 20 rounds each.
Before gamma was 0.9

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 100        | 0             | 3            | 78, 260       | 2000            | 5       | 0.1   |

## 17
Training 2 dql-agents
250 games with 20 rounds each.
Before gamma was 0.9

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 100        | 1             | 1            | 78, 260       | 2000            | 5       | 0.1   |

## 18
Based on results of training 1 to 15 we try to guess the best possible parameters.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 100        | 0             | 3            | 78, 260       | 500             | 5       | 0.9   |

## 19
Based on results of training 1 to 15 we try to guess the best possible parameters.  
Differs from #18 as this has lower epsilon over time starting over 4000 training on batches and with epsilon starting at 10%.
Final 1000 batches are with fixed epsilon equal to 1%.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 100        | 0             | 3            | 78, 260       | 500             | 1       | 0.9   |

## 20
Based on results of training 1 to 15 we try to guess the best possible parameters.  
Differs from #19 as this has buffer capacity equal to 2000.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 100        | 0             | 3            | 78, 260       | 2000            | 1       | 0.9   |

## 21
Based on results of training 1 to 15 we try to guess the best possible parameters.  
Differs from #19 as this has gamma equal to 0.1.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 100        | 0             | 3            | 78, 260       | 500             | 1       | 0.1   |

## 22
Based on results of training 1 to 15 we try to guess the best possible parameters.  
Differs from #19 as this has now early stopping enabled!

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 100        | 0             | 3            | 78, 260       | 500             | 1       | 0.9   |

## 23
Based on results of training 1 to 15 we try to guess the best possible parameters.  
Differs from #22 as this has now lower eps over time DISabled. Epsilon = 5  
Early stopping is enabled.  

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 100        | 0             | 3            | 78, 260       | 500             | 5       | 0.9   |

## 24
Based on results of training 1 to 15 we try to guess the best possible parameters.  
Differs from #21 as this has gamma equal to 0.5.

| Batch size | random agents | basic agents | hidden layers | buffer capacity | epsilon | Gamma |
| -----------|---------------|--------------|---------------|-----------------|---------| ----- |
| 100        | 0             | 3            | 78, 260       | 500             | 1       | 0.5   |
