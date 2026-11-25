**English** | [Polski](README.pl.md)

# Lesson 1.4 — A short history of AI

**Optional** · Prerequisites: 1.1 What is AI. This is a conceptual lesson without a programming task.

## Learning goals

After this lesson you will be able to:

- place the key events of AI history on a timeline;
- explain what the "AI winters" were and what caused them;
- describe how the symbolic and learning traditions took turns;
- look at today's promises about AI with some distance.

## Why history

The history of AI is several cycles of great expectations and disappointments. Methods written off as dead ends came back years later as breakthroughs. Knowing these cycles makes it easier to separate lasting ideas from fashion, and to judge more soundly what today's systems can actually do.

## Timeline

| Year | Event | Why it matters | In the course |
|---|---|---|---|
| 1943 | McCulloch and Pitts describe a mathematical model of the neuron | the first step towards neural networks | module 7 |
| 1950 | Turing publishes *Computing Machinery and Intelligence* | the question "can machines think?" and the Turing test | lesson 1.1 |
| 1956 | the Dartmouth workshop | the birth of AI as a field; the name "artificial intelligence" appears in the proposal for the workshop | — |
| 1956–1959 | Logic Theorist and General Problem Solver (Newell, Simon, Shaw) | problem solving as search | module 2 |
| 1958 | Rosenblatt's perceptron | a machine that learns from examples | module 7 |
| 1966 | ELIZA (Weizenbaum) | simple rules create the illusion of talking to a person | module 9 |
| 1969 | *Perceptrons* (Minsky, Papert) | show the limits of a single-layer perceptron, such as the XOR problem | lesson 7.3 |
| 1973 | the Lighthill report in the UK | a critical assessment of AI's results and funding cuts | — |
| 1970s and 1980s | expert systems, such as MYCIN (diagnosing infections) and XCON (configuring computers) | experts' knowledge written down as rules; a commercial boom in the 1980s | module 5 |
| 1986 | backpropagation popularized (Rumelhart, Hinton, Williams) | multi-layer networks can be trained | module 7 |
| 1990s | probabilistic methods and machine learning grow | reasoning under uncertainty, learning from data | modules 6 and 7 |
| 1997 | Deep Blue wins a match against Kasparov | game-tree search at a huge scale | module 3 |
| 2012 | AlexNet wins the ImageNet competition by a wide margin | the start of the deep learning era | module 7 |
| 2016 | AlphaGo beats Lee Sedol | neural networks combined with search | modules 3 and 8 |
| 2017 | the Transformer architecture (*Attention Is All You Need*) | the basis of today's large language models | module 9 |
| 2022 | ChatGPT released to the public | large language models reach wide use | module 9 |

## Waves of optimism and "AI winters"

After Dartmouth, optimism ran high. The first programs proved theorems and solved puzzles, and some researchers predicted machines matching people within a few decades. But methods that worked on small examples did not scale to real problems, because the state space exploded, as in lesson 1.3, and nobody knew how to write down human knowledge. Disappointment, symbolized by the Lighthill report, brought funding cuts in the 1970s. That was the first **AI winter**.

The 1980s saw a boom in expert systems. They turned out to be expensive to maintain, brittle outside their narrow domain and hard to extend. At the end of the 1980s the market collapsed and a second winter set in.

## Two traditions

- **The symbolic tradition** (search, logic, rules) dominated from the 1950s to the 1980s.
- **The learning tradition** (the perceptron, neural networks) started just as early. After the 1969 critique it faded into the background, returned in 1986 with backpropagation, and after 2012, thanks to huge amounts of data and computing power, came to dominate many applications.

The most interesting systems often combine both traditions. AlphaGo combined neural networks with game-tree search, while Deep Blue in 1997 was almost pure search.

## What history teaches

1. **Promises ran ahead of abilities.** Each winter began with disappointment over overly bold predictions.
2. **Ideas come back.** Neural networks waited decades for the data, computing power and training methods that let them reach their potential.
3. **Scale matters.** Many breakthroughs, from Deep Blue to large language models, came as much from huge growth in computing power and data as from new ideas.
4. **The traditions complement each other.** The "symbols or learning" debate rarely ends with one side winning.

## How to check

This lesson has no automated tests. After your own attempt, compare your answers to the review questions with the [model answers](../../../solutions/01_agents/04_history_of_ai/answers.md).

## Review questions

1. Why did the idea of the 1958 perceptron bring great successes only decades later?
2. How does the source of an expert system's knowledge differ from that of a large language model?
3. What led to the "AI winters"? Does a similar risk exist today?
4. Find on the timeline an example of a system that combines both traditions, and explain what each one contributes.

## What to remember

- AI as a field dates from 1956 (Dartmouth), but its ideas reach back to the 1940s and 1950s.
- The history of AI is cycles of optimism and disappointment, known as AI winters.
- The symbolic and learning traditions took turns and increasingly combine.
- Many breakthroughs depended on data and computing power, not only on new ideas.

## What next

- Module 2 begins search, one of the oldest techniques in AI. The list of lessons is in the [course map](../../../COURSE_MAP.md).

## References

- S. Russell, P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020, ch. 1.3 (the history of AI).
- A. M. Turing, *Computing Machinery and Intelligence*, Mind 59 (236), 1950, pp. 433–460.
