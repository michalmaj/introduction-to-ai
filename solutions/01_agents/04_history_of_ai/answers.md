**English** | [Polski](answers.pl.md)

# Lesson 1.4 — answers

Look here only after your own attempt. The questions are in the [lesson](../../../modules/01_agents/04_history_of_ai/README.md).

## 1. Why the perceptron waited decades

A single-layer perceptron has serious limits: it cannot even solve the XOR problem. Minsky and Papert showed this in 1969, and interest in networks dropped. Multi-layer networks do not have that limit, but there was no effective way to train them. That way, backpropagation, was popularized only in 1986. Their full potential appeared even later, around 2012, when huge datasets and enough computing power, including graphics cards, became available.

A good answer contains:

- the limit of the single-layer perceptron (XOR, 1969);
- backpropagation as the way to train multi-layer networks;
- the role of data and computing power in the breakthrough after 2012.

## 2. The source of knowledge: expert system versus language model

An expert system's knowledge was written down by hand, by knowledge engineers and experts, as explicit rules. Every rule can be read and checked. A large language model acquires its knowledge by training on huge amounts of text and stores it in millions or billions of parameters that cannot be read like rules. The first approach is transparent but demands laborious manual work and is brittle. The second scales without writing knowledge down by hand, but it is harder to explain and to verify.

A good answer contains:

- hand-written rules in the expert system;
- knowledge learned from data and hidden in the language model's parameters;
- the consequences: transparency versus scalability.

## 3. The causes of the "AI winters"

Both winters began with disappointment. Promises ran ahead of abilities. Methods that worked on small examples did not scale (the state-space explosion), and expert systems turned out to be expensive to maintain and brittle. When results fell short of expectations, funding and interest dropped. A similar risk exists today: when expectations of AI grow faster than its real abilities and reliability, disappointment could again cut investment. The difference is that today's systems are already widely used in practice.

A good answer contains:

- the gap between promises and abilities;
- at least one technical cause: failure to scale or brittleness;
- a reasoned opinion about today's risk.

## 4. A system combining both traditions

AlphaGo (2016). Neural networks, the learning tradition, evaluated positions and suggested promising moves, which for Go could not be captured well by hand-written rules. Game-tree search, the symbolic tradition, planned the next moves using those evaluations. Each part does what it is good at: the network supplies "intuition", and the search systematically checks the consequences.

A good answer contains:

- a concrete system from the timeline;
- the roles of the learning part and the symbolic part;
- a reason why the combination works better than either part alone.
