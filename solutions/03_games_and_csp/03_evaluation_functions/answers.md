**English** | [Polski](answers.pl.md)

# Lesson 3.3 — answers

Look here only after your own attempt. The tasks are in the [lesson](../../../modules/03_games_and_csp/03_evaluation_functions/README.md).

## Part A

Answer:

```python
EVAL_VALUES = [-1, 3, 1]
DEPTH_ONE_MOVE = (2, 0)
```

**The values of *e*.** There are 8 lines. For X the lines without a nought are open, for O the lines without a cross.

| Position | Open for X | Open for O | *e* |
|---|---|---|---|
| `X..` / `.O.` / `...` | 8 − 4 = 4 (the nought in the centre lies on 4 lines) | 8 − 3 = 5 (the cross in the corner lies on 3) | −1 |
| `X.O` / `.X.` / `...` | 8 − 3 = 5 | 8 − 6 = 2 (the crosses in the corner and the centre lie on 6 lines together) | 3 |
| `X..` / `.O.` / `..X` | 8 − 4 = 4 | 8 − 5 = 3 (two crosses in opposite corners: 5 lines, because they share the diagonal) | 1 |

The most common slip is leaving out the empty lines, which are open for both players, or counting twice the diagonal that holds both crosses of the third position.

**The move at depth 1.** X has five moves. *e* of the position after each of them:

| X's move | Position after the move | Open for X | Open for O | *e* |
|---|---|---|---|---|
| (0, 1) | `XX.` / `.OX` / `.O.` | 3 | 2 | 1 |
| (0, 2) | `X.X` / `.OX` / `.O.` | 3 | 2 | 1 |
| (1, 0) | `X..` / `XOX` / `.O.` | 3 | 3 | 0 |
| (2, 0) | `X..` / `.OX` / `XO.` | 3 | 1 | 2 |
| (2, 2) | `X..` / `.OX` / `.OX` | 3 | 2 | 1 |

The largest *e* = 2 comes from the move (2, 0), so that is the answer. It is not a good move, though, as review question 3 explains.

## Part B

The reference solution is the alpha-beta of lesson 3.2 with a depth parameter: first the test for the end of the game, then the test `d == 0`. The evaluation is weighted lines. Each line that holds marks of only one player is worth 10<sup>*n* − 1</sup> points, where *n* is the number of those marks: plus for the player, minus for the opponent. The sum *x* is squeezed into (−1, 1) with *x* / (1 + |*x*|).

In the match of the test this evaluation wins 11 games, draws 1 and loses none.

Alternatives:

- [negamax_h_search.py](alternatives/negamax_h_search.py) is negamax with a depth limit. At the boundary it scores the position for the player to move there, and the parent flips the sign. With a symmetric evaluation, where what is good for X is equally bad for O, the result is the same.
- [open_lines_eval.py](alternatives/open_lines_eval.py) scores by open lines, as in Part A, divided by the number of lines plus 1. It wins 7 games, draws 5 and loses none, so the test passes. It returns a `numpy.float64`, which is fine.

## Review questions

### 1. The utility of a terminal state at the boundary

A terminal state has a sure result: a win, a draw or a loss. An evaluation is only an estimate and can be wrong, and its values lie between −1 and 1, so a sure win scored at, say, 0.9 would lose to an uncertain position scored at 0.95. A search that tests the depth first can miss a win in one move.

A good answer includes:

- the difference between a sure result and an estimate;
- the consequence of testing in the other order, such as a missed win.

### 2. The range of the evaluation

A win is worth 1 and a loss −1. If an evaluation could be 50, every unfinished position with a good score would look better than a sure win, and every weak one worse than a loss. The program would rather build "promising" positions than win at once, and it could walk into a sure loss to avoid a position scored −50.

A good answer includes:

- the comparison with the values of a win and a loss;
- a concrete wrong choice that a too large evaluation leads to.

### 3. Is the move (2, 0) good?

No. O has noughts on (1, 1) and (2, 1), and the cell (0, 1) is empty, so O threatens to complete the middle column. X's only good move is the block (0, 1). After any other move O wins. The evaluation *e* does not see this threat, because it only counts open lines, not how close they are to completion. A depth-2 search sees O's reply: after (2, 0) O places a nought on (0, 1) and wins, which gives the utility −1. That is why at depths 2 and 3 the search chooses (0, 1).

A good answer includes:

- O's threat in the middle column;
- an explanation of why *e* does not see it;
- the observation that depth 2 reaches O's win and changes the choice to (0, 1).

### 4. The horizon effect

A search sees nothing beyond its depth boundary. If a threat appears just beyond it, the position looks safe. An example from the notebook: in the position with two noughts in the first column, the depth-1 search develops its own lines, because it does not see that O will add a third nought and have two open ends. In chess the classic example is delaying the inevitable loss of a piece with a series of checks.

A good answer includes:

- the definition: the search sees nothing beyond its depth boundary;
- an example where a threat or a loss lies just past the horizon.

### 5. Depth under a time limit

Better not to choose it in advance, but to use iterative deepening: search to depth 1, 2, 3 and so on until the time runs out, and play the best move of the last completed search. Each further ply costs several to a dozen times more than the previous one, so the last, unfinished search would take most of the time anyway. The repeated work is cheap, and the shallower search suggests the move order for the deeper one.

A good answer includes:

- iterative deepening with a time limit;
- the argument that the repeated work is cheap (as in lesson 2.6);
- the remark about the move order from the shallower search.

## Experiments

Results of the reference implementation. In `"mine"` mode the row "yours" depends on your evaluation, and the other rows should come out the same if your search cuts off at ≥ and visits the moves in the order of `game.actions`.

| Evaluation | Depth 1 | Depth 2 | Depth 3 |
|---|---|---|---|
| zero | 1 / 2 / 9 | 3 / 6 / 3 | 9 / 1 / 2 |
| open lines | 4 / 4 / 4 | 7 / 5 / 0 | 11 / 1 / 0 |
| weighted lines | 11 / 0 / 1 | 11 / 1 / 0 | 12 / 0 / 0 |

The numbers are wins / draws / losses in 12 games against an opponent who searches to depth 2 with the zero evaluation.

| Depth | Move | Score | Positions (empty board) | Time per move (empty board) |
|---|---|---|---|---|
| 1 | (1, 3) | +0.964 | 26 | < 0.001 s |
| 2 | (3, 0) | −0.800 | 236 | about 0.002 s |
| 3 | (3, 0) | +0.976 | 2,360 | about 0.02 s |
| 4 | (3, 0) | +0.750 | 21,788 | about 0.18 s |

The columns "Move" and "Score" are for the position with a threat of experiment 2, and the columns "Positions" and "Time" for the first move on the empty board of experiment 3.

- **Experiment 1.** The zero evaluation at depth 1 loses 9 games, because it simply plays the first free move. At depth 3 it wins 9, because it sees wins and threats that the depth-2 opponent does not. A good evaluation gives more than extra depth: weighted lines win 11 games already at depth 1. Best of all is both together: weighted lines at depth 3 win every game.
- **Experiment 2.** If O adds a nought on (3, 0), it will have three in the column with two open ends, and X can block only one. Only the move (3, 0) closes both lines where O can still make four. The depth-1 search sees only the position after its own move, so it chooses the move that best develops X's lines. From depth 2 on it sees O's reply and blocks. The scores jump with the parity of the depth. At an odd depth the last move before the horizon is X's, so the score is optimistic. At an even depth O has the last move, so the score is pessimistic. That is the horizon effect too.
- **Experiment 3.** Every further ply costs about 10 times more positions and time. That is less than the number of moves on the board (about 24) but more than its square root (about 5), so the move order is far from perfect. A move at depth 8 would cost about 10<sup>4</sup> times more than at depth 4, around half an hour. Within a second the search gets to depth 4. Depth 5 already takes almost 2 seconds.
