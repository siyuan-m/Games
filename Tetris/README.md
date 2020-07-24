# Tetris - 'AI'

## Tetris Game
Simple python Tetris with both human and 'AI' players available. 
The gaming mechanism is from https://gist.github.com/silvasur/565419 with a heavy graphic redesign.

## 'AI'
'AI' is in quotes because it is not true artificial intelligence - the heuristics and associated weights were not 
determined via genetic algorithms or q learning. This was partly due to lack of computational power, data available to train 
the model, and the curiosity of comparing the performance of 'hard-coded' algorithms and various machine learning
produced algorithms. Heuristics considered are the potential number of cleared lines, holes generated, aggregated height, and bumpiness (sum of height different of adjacent columns)

Change `next_piece_knowledge` under `next_move` to see how AI performs with and without the knowledge of the next piece. 
Be aware of the slower game speed due to higher computational load if `next_piece_knowledge` is turned on.

'AI' logic and implementation were partly inspired by Tetris AI of Dr. Pommes and Yiyuan Lee.

Dr. Pommes: https://levelup.gitconnected.com/tetris-ai-in-python-bd194d6326ae

Yiyuan Lee: https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/