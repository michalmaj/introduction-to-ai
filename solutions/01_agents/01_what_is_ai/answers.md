**English** | [Polski](answers.pl.md)

# Lesson 1.1 — answers

Look here only after your own attempt. The task is in the [lesson](../../../modules/01_agents/01_what_is_ai/README.md). For questions (d) and (e), other well-argued answers are possible.

## Analysing the systems

### 1. Spam filter

- **(a) Perceives:** the content and headers of a message: the sender, words, links and attachments. Sometimes also the user's "this is spam" marks.
- **(b) Actions:** moves the message to the spam folder or leaves it in the inbox.
- **(c) Performance measure:** how much spam it catches and how rarely it mistakes an ordinary message for spam. The second error usually costs more, because an important message can be lost.
- **(d) Learning or rules:** usually both. A classifier learns from labelled messages, and rules such as lists of blocked senders are added on top.
- **(e) View:** acting rationally: maximizing the quality of the classification. Nobody expects a filter to behave like a person.

### 2. Chess program

- **(a) Perceives:** the whole position on the board and the history of moves.
- **(b) Actions:** legal moves.
- **(c) Performance measure:** the game result (win, draw, loss), and over time its rating.
- **(d) Learning or rules:** classical programs combine game-tree search with a hand-designed evaluation function. Newer ones learn the evaluation by playing against themselves. Module 3 covers the search.
- **(e) View:** acting rationally: choosing the move with the best expected outcome.

### 3. Car navigation

- **(a) Perceives:** the road map, the GPS position and traffic data.
- **(b) Actions:** proposes a route, gives instructions such as "turn right" and recomputes the route.
- **(c) Performance measure:** travel time or route length, and how accurate the predicted arrival time is.
- **(d) Learning or rules:** route finding is a search over the road graph (module 2), which is the symbolic approach. Traffic prediction is often learned from data.
- **(e) View:** acting rationally.

### 4. Warehouse robot

- **(a) Perceives:** sensor readings, meaning obstacles and parcels, and sometimes its own position.
- **(b) Actions:** drives, picks up a parcel, waits.
- **(c) Performance measure:** parcels collected in a given time, energy used and no collisions.
- **(d) Learning or rules:** it depends on the robot. It may follow written rules (lesson 1.2), plan its route (module 2) or learn to navigate (module 8).
- **(e) View:** acting rationally: what counts is effectiveness, not resemblance to a person.

### 5. Customer-service chatbot

- **(a) Perceives:** the customer's messages, and sometimes order data.
- **(b) Actions:** replies, asks questions, hands the case over to a person, and sometimes performs operations such as checking a parcel's status.
- **(c) Performance measure:** the share of cases solved correctly, customer satisfaction, no false information, and handing over to a person when that is needed.
- **(d) Learning or rules:** modern chatbots are built on language models trained on data; older ones on hand-written conversation scripts.
- **(e) View:** it behaves *humanly*, because it holds conversations, but it is worth judging *rationally*, by whether it solved the case. It is a good example that natural conversation and effectiveness are different things (module 9).

A good analysis:

- separates what the system perceives from what it does;
- gives a measurable performance measure, not a vague "works well";
- notices that many systems combine rules with learning;
- justifies the choice of view of AI.

## Review questions

### 1. "Acting humanly" versus "acting rationally"

Acting humanly means behaving so that the system cannot be told apart from a person. Acting rationally means choosing the actions with the best outcome according to the performance measure. The difference matters whenever people act suboptimally. Navigation that acted "humanly" would repeat typical human mistakes, such as choosing a familiar but slower road. Rational navigation chooses the faster one. Likewise, a chatbot can sound natural and still give false information.

A good answer contains:

- comparison with people as the criterion of the human view;
- the performance measure as the criterion of the rational view;
- an example where the two criteria lead to different behaviour.

### 2. The Turing test and the warehouse robot

The Turing test checks whether a conversation with a machine can be told apart from a conversation with a person. A warehouse robot does not converse. What counts is whether it collects parcels quickly and safely. A robot that "passed" some test of human likeness could still collect parcels slowly and with collisions. The right yardstick is the performance measure of the task.

A good answer contains:

- the fact that the test measures conversational indistinguishability from a person;
- the remark that the robot is judged by how it does its task;
- at least one concrete element of the robot's performance measure.

### 3. The thermostat

A thermostat is an agent. It perceives the temperature (a sensor) and switches the heating on or off (an actuator). It is a very simple reflex agent that follows the rule "too cold, so heat". Within its narrow performance measure, keeping the set temperature, it is rational, because given what it perceives it chooses the right action. This shows that "agent" and "rational" do not mean "as intelligent as a person".

A good answer contains:

- the thermostat's sensor and actuator;
- an assessment of rationality against a specific performance measure;
- the remark that a rational agent does not have to be complex.

### 4. Advantages and disadvantages of both approaches

- **The symbolic approach.** Advantage: transparency and explainability, because you can see the rule or plan behind a decision. Disadvantage: brittleness in unforeseen situations and the laborious work of writing knowledge down by hand.
- **The learning approach.** Advantage: it handles perception and patterns we cannot describe with rules, such as recognizing images. Disadvantage: it needs a lot of data, and its decisions are harder to explain.

A good answer contains:

- one advantage and one disadvantage for each approach;
- at least one concrete example.
