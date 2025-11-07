## Self-Consistency 

**Idea:** Generate multiple reasoning paths and select the most common answer.

**Example Prompt**  
Q: If Ali eats 4 apples each day for 3 days, how many apples did he eat in total?  
A: Think step by step and give your reasoning.  
(Repeat reasoning multiple times and select the most consistent answer.)

---

## Step-Back Prompting

**Idea:** Before solving, step back to identify the high-level problem type, assumptions, and strategy. Then apply it.

### 1) Basic Step-Back (prompt template)

```
Before solving, step back and identify the high-level type of problem and the general strategy to solve it. 
List the abstract steps first, then apply them to this specific question: <YOUR QUESTION>.
```

### 2) With Constraints & Risks (prompt template)

```
Step back and outline the general framework for solving problems like this. 
Name assumptions, potential pitfalls, and decision criteria. 
Then apply that framework to <YOUR QUESTION> and provide a final answer.
```

### 3) For Product/Architecture Decisions (prompt template)

```
Step back and define evaluation criteria (e.g., cost, scalability, reliability, maintainability, risk). 
Weight them briefly, then compare options against these criteria and recommend one for <YOUR CONTEXT>.
```

### 4) For Debugging (prompt template)

```
Step back and propose a general diagnostic tree for issues like this. 
State hypotheses, quick tests, and expected observations. 
Then run the tree conceptually on my case: <SYMPTOMS/LOGS>.
```

---

## Step-Back vs CoT vs Self-Consistency

* **CoT (Chain of Thought):** “Think step by step” (one clear path).
* **Self-Consistency:** “Think in multiple ways and take the majority answer.”
* **Step-Back:** “First build a high-level framework, then apply it step by step.”

**Often best:** **Step-Back → CoT**, and for tougher tasks add **Self-Consistency**.

---

## ReAct (Reasoning + Acting)

**Idea:** Alternate between **Reasoning** (“Thought”) and **Action** (using tools), observe results, and continue until you can answer.

### Real-Life Example

Imagine you’re planning a trip:

* **Reasoning:** “I should check what the weather in Stockholm is like.”
* **Action:** Open a weather app / search online.
* **Result:** “Temperature 5 °C, raining.”
* **Next reasoning:** “It’s raining → I should take an umbrella.”
* **Final action:** Pack an umbrella.

This entire process is **ReAct**—after each reasoning step, take an action; after each action, observe and reason again.

### AI Example (Prompt + Tool Use)

**Goal:** “Find current Bitcoin price and check if it’s higher than yesterday.”

1. **Thought:** “I need both the current and yesterday’s BTC price.”
2. **Action:** Fetch current BTC price → **Observation:** “$68,000.”
3. **Action:** Fetch yesterday’s BTC price → **Observation:** “$67,200.”
4. **Thought:** “$68,000 > $67,200, so price increased.”
5. **Final Answer:** ✅ “Bitcoin price increased by **$800** today.”

### ReAct Prompt Template

```
You are an intelligent agent that can both reason and act.

When given a question:
1) Think step by step (Thought).
2) Decide whether to use a tool or action (Action).
3) Observe the tool’s output (Observation).
4) Continue Thought → Action → Observation until you can answer.

Use this format:
Thought:
Action:
Observation:
Final Answer:
```

---

## Tree of Thoughts (ToT)

**Simple Definition:**
Tree of Thoughts is an advanced reasoning technique where the model explores **multiple possible reasoning branches** instead of following just one path. Each branch represents a candidate idea or plan. The model evaluates branches and selects the best one (or a combination).

### Real-Life Example (translated)

**Question:** “What should I do this weekend?”

* **Option 1: Go out**

  * **Branch A:** Park
  * **Branch B:** Cinema
* **Option 2: Stay at home**

  * **Branch C:** Movie
  * **Branch D:** Cooking

Evaluate branches:

* “Cinema is expensive → cancel.”
* “Cooking is easy and fun → select!”

This is ToT: generate multiple ideas, evaluate them, and choose the best.

### AI Example

**Question:** “How can I increase user engagement in my app?”

* **Branch 1 — Gamification:** badges, leaderboard
* **Branch 2 — Personalization:** recommendations, adaptive UI
* **Branch 3 — Notifications:** smart reminders, good timing

**Reasoning:**

* Gamification can boost fun but may distract.
* Personalization improves relevance → stronger long-term engagement.
* Notifications help but can annoy users.

**Chosen Path:** **Personalization →** implement smart recommendations.

### ToT Prompt Template

```
You are a reasoning agent that can explore multiple ideas.

For this problem:
1) Generate several distinct reasoning paths (a "tree of thoughts").
2) Evaluate each path’s strengths and weaknesses.
3) Pick the most promising path (or merge top ideas).
4) Continue reasoning along that path to reach a final conclusion.

Question: <insert your problem here>
```

---

## Quick Usage Tips

* Start with **Step-Back → CoT** for clarity.
* Add **Self-Consistency** when answers seem unstable or high-stakes.
* Use **ReAct** when tools, data lookups, or experiments are needed.
* Try **ToT** for creative, design, or strategy problems where multiple avenues exist.