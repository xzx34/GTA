from typing import List, Literal

def select_prompt(question=None):
    return f"""
**Your Task: Optimal Graph Representation Selection**

You will be given a graph theory problem description. Your sole responsibility is to analyze this problem and select the **single best representation format** that would make it easiest for a system to process and solve the problem algorithmically.

**Available Representation Formats:**
*   `NL` (Natural Language: a descriptive text-based format)
*   `SL` (Structured Language: a templated, keyword-based text format)
*   `AM` (Adjacency Matrix: a matrix showing connections and/or weights)
*   `AL` (Adjacency List: lists neighbors and/or weights for each vertex)

**Considerations for your selection:**
*   **Problem Type:** What kind of graph question is being asked (e.g., finding paths, checking properties, calculating flows)?
*   **Graph Characteristics (infer from description):**
    *   Approximate size (number of nodes/edges).
    *   Is it likely sparse (few edges) or dense (many edges)?
    *   Are edge weights/capacities involved?
    *   Is it directed or undirected?
*   **Processing Efficiency:**
    *   `AM` can be good for dense graphs or when checking non-connections is important.
    *   `AL` is often efficient for sparse graphs and algorithms that traverse edges.
    *   `NL` and `SL` might be suitable for smaller graphs or problems where the structure is simpler to describe textually, but could be harder to parse for complex algorithms.

**Input Problem:**
{question}

**Instruction:**
Review the input problem. Based on your analysis and the considerations above, output **only one** of the following four representation format codes: `NL`, `SL`, `AM`, or `AL`.

**Your Output (must be one of NL, SL, AM, AL):**

    """

def algorithm_planner(question=None):
    return f"""
**You are an Expert Algorithm Planner for Graph Theory Problems.**

**Your Task:**
You will be provided with a graph theory problem description. Your objective is to devise a **high-level strategic plan** or the **main algorithmic approach** that would be used to solve this problem.

**Crucial Instructions:**
*   **DO NOT solve the problem.**
*   **DO NOT derive the final answer.**
*   **DO NOT write code.**

Your output should be a **conceptual outline** of the algorithm or the logical phases involved. Think of it as describing the *methodology* at a high level.

**For example, if the problem were "Find the shortest path between node A and node B":**
*   A good high-level plan might be: "Utilize a breadth-first search (BFS) starting from node A, keeping track of distances, until node B is reached. Alternatively, if edges have weights, apply Dijkstra's algorithm."
*   A bad (too detailed/executing) response would be: "1. Initialize distance to A as 0, all others as infinity. 2. Add A to queue. 3. While queue not empty..."

**Considerations for your plan:**
*   Identify the core objective of the problem (e.g., finding a path, counting components, optimizing a value).
*   What general class of graph algorithms is typically used for such a problem?
*   What are the main conceptual stages of that algorithm?

**Input Problem Description:**
{question}

**Instruction:**
Based on the problem description, provide a concise, high-level algorithmic plan or strategy. Focus on the "what" and "why" of the approach, not the detailed "how."

**Your High-Level Algorithmic Plan:**

    """

def algorithm_decomposer(question=None, plan=None):
    return f"""
**You are an Expert Algorithm Decomposer.**

**Your Task:**
You will be given an original graph theory problem description (`question`) and a high-level algorithmic plan (`plan`) designed to solve it. Your responsibility is to decompose this `plan` into a sequence of **2 or 3 highly detailed, specific, and actionable sub-steps**. These sub-steps should guide another system (an "Executor") to carry out the plan and solve the original `question`.

**Crucial Instructions:**
*   **Extreme Detail Required:** Each sub-step must be very specific. Think about what data structures are needed, what values to initialize, what to iterate over, what conditions to check, what information to maintain or update at each stage.
*   **Actionable by an LLM:** Phrase each sub-step as a clear instruction that an LLM could follow to perform a part of the algorithm.
*   **Logical Sequence:** The sub-steps must follow a logical order that reflects the progression of the `plan`.
*   **Coverage:** Together, the sub-steps should comprehensively cover the entire `plan`.
*   **DO NOT solve the original problem or provide the final answer.** You are only creating the detailed execution blueprint.
*   **You MUST generate EITHER 2 OR 3 sub-steps.** No more, no less.

**Input:**

1.  **Original Problem (`question`):**
    ```
    {question}
    ```

2.  **High-Level Algorithmic Plan (`plan`):**
    ```
    {plan}
    ```

**Output Format (Strictly Adhere to This):**
You MUST output the decomposed sub-steps in the following exact format. Use `### Sub-step X:` for each step.

```
### Sub-step 1:
[Provide an extremely detailed instruction for the first phase of the algorithm based on the plan. Be specific about:
- Initializing any necessary data structures (e.g., distance arrays, visited sets, queues, stacks, flow matrices).
- Setting initial values for variables or nodes (e.g., source node distance to 0, all others to infinity).
- The very first set of operations to perform.]

### Sub-step 2:
[Provide an extremely detailed instruction for the second phase, logically following Sub-step 1. Be specific about:
- Iterative processes (e.g., "While the queue is not empty..." or "For each neighbor of the current node...").
- Conditions for updates or state changes (e.g., "If a shorter path is found..." or "If the capacity is greater than zero...").
- How to update data structures or values based on operations.
- What to do if a certain condition is met (e.g., target node reached, no more augmenting paths found).]

(Include this section ONLY if you are generating 3 sub-steps)
### Sub-step 3:
[Provide an extremely detailed instruction for the third and final phase, if necessary to complete the plan. Be specific about:
- Continuation of iterative processes.
- Termination conditions for the algorithm.
- How to derive any intermediate results needed for the final answer (e.g., "Sum the capacities of edges in the minimum cut set" or "Backtrack from the target node to reconstruct the path").
- Final checks or operations before the overall algorithm concludes.]
```

**Instruction:**
Based on the provided `question` and `plan`, generate 2 or 3 highly detailed sub-steps strictly following the output format above.

    """
