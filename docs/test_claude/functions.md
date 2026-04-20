# Functions & Classes Documentation — test_claude

**Repository**: test_claude  
**Generated**: 2025-01-16  
**Total Functions**: 9  
**Total Lines**: 338  

---

## Table of Contents

- [main.py](#mainpy) · 1 function
- [src/graph.py](#srcgraphpy) · 2 functions/objects
- [src/nodes.py](#srcnodespy) · 4 functions
- [src/state.py](#srcstatepy) · 1 class
- [first_func.py](#first_funcpy) · 1 function

---

## main.py

### `main()`

**Type**: `function` | **Importance**: ████████▌ 92  
**Signature**:
```python
def main() -> None
```

**Description**:  
Entry point for the CLI application. Prompts user in a loop for task input, calls the agent, and displays final answers.

**Location**: Line 5  
**Is Public**: ✓ Entry Point  
**Has Side Effects**: ✓ (I/O: stdin/stdout)

**Used in**:
- `__main__` execution

---

## src/graph.py

### `run_agent()`

**Type**: `function` | **Importance**: ████████░ 85  
**Signature**:
```python
def run_agent(task: str) -> str
```

**Description**:  
Orchestrates the agent workflow. Initializes the state with the given task and runs the compiled LangGraph workflow through all stages (decompose → execute → synthesize). Returns the final answer string.

**Location**: Line 31  
**Is Public**: ✓ Entry Point (for agent invocation)  
**Has Side Effects**: ✓ (API calls to Claude, prints progress)

**Used in**:
- `main.py` main()

---

### `workflow` / `agent`

**Type**: `StateGraph` (LangGraph) | **Importance**: █████░░░░ 50  

**Description**:  
Compiled LangGraph workflow definition. Defines 3 nodes (decomposer, executor, synthesizer), sets entry point to decomposer, and conditional edges based on `should_continue_executing` router.

**Location**: Lines 1–26  

**Graph Structure**:
```
decomposer → [conditional edge]
    ├─ "execute" → executor → [conditional edge]
    │   ├─ "execute" → executor (loop)
    │   └─ "synthesize" → synthesizer → END
    └─ "synthesize" → synthesizer → END
```

---

## src/nodes.py

### `decomposer()`

**Type**: `function` | **Importance**: ███████▌░ 78  
**Signature**:
```python
def decomposer(state: dict) -> dict
```

**Description**:  
Node function that calls Claude to decompose the user's task into a list of clear, sequential subtasks. Parses JSON array response from Claude Opus 4.6 with extended thinking enabled.

**Location**: Line 9  
**Is Public**: ✓  
**Has Side Effects**: ✓ (API call: anthropic.messages.create)

**Model**: `claude-opus-4-6` with `thinking={"type": "adaptive"}`  
**Max Tokens**: 4096

**Used in**:
- `src/graph.py` workflow.add_node()

---

### `executor()`

**Type**: `function` | **Importance**: ███████░░ 75  
**Signature**:
```python
def executor(state: dict) -> dict
```

**Description**:  
Node function that executes the current subtask (at `state["current_index"]`). Calls Claude with context of the original task and previous subtask results. Appends the result to `subtask_results` and increments `current_index`.

**Location**: Line 38  
**Is Public**: ✓  
**Has Side Effects**: ✓ (API call: anthropic.messages.create)

**Model**: `claude-opus-4-6` with `thinking={"type": "adaptive"}`  
**Max Tokens**: 4096

**Logic**:
- Iterates through subtasks sequentially
- Each call to executor processes one subtask
- Routing (`should_continue_executing`) decides if loop continues or moves to synthesis

**Used in**:
- `src/graph.py` workflow conditional edge routing

---

### `synthesizer()`

**Type**: `function` | **Importance**: ███████░░ 72  
**Signature**:
```python
def synthesizer(state: dict) -> dict
```

**Description**:  
Final node that combines all subtask results into a single coherent answer. Calls Claude to synthesize the results, producing the `final_answer` string.

**Location**: Line 62  
**Is Public**: ✓  
**Has Side Effects**: ✓ (API call: anthropic.messages.create)

**Model**: `claude-opus-4-6` with `thinking={"type": "adaptive"}`  
**Max Tokens**: 8192 (higher for synthesis)

**Used in**:
- `src/graph.py` workflow final node

---

### `should_continue_executing()`

**Type**: `function` (router/conditional) | **Importance**: ██████░░░ 65  
**Signature**:
```python
def should_continue_executing(state: dict) -> str
```

**Returns**: `"execute"` or `"synthesize"`

**Description**:  
Routing function that determines whether to continue executing subtasks or move to synthesis. Compares `current_index` with number of subtasks.

**Location**: Line 90  
**Is Public**: ✓  
**Has Side Effects**: ✗

**Logic**:
```python
if state["current_index"] < len(state["subtasks"]):
    return "execute"
return "synthesize"
```

**Used in**:
- `src/graph.py` conditional_edges (called twice: after decomposer and executor)

---

## src/state.py

### `AgentState`

**Type**: `TypedDict` | **Importance**: ██████░░░ 60  
**Signature**:
```python
from typing import TypedDict

class AgentState(TypedDict):
    task: str                      # original user task
    subtasks: list[str]            # decomposed subtasks
    subtask_results: list[str]     # result for each subtask
    current_index: int             # which subtask is being executed
    final_answer: str              # synthesized final answer
    num_steps: int
```

**Description**:  
State schema for the LangGraph workflow. Defines all keys and their types that flow through the agent nodes. Immutable contract for the state graph.

**Location**: Lines 4–10  
**Is Public**: ✓  

**Field Descriptions**:
| Field | Type | Purpose |
|---|---|---|
| `task` | str | Original user task from CLI input |
| `subtasks` | list[str] | List of decomposed subtasks (populated by decomposer) |
| `subtask_results` | list[str] | Parallel list of results from executor |
| `current_index` | int | Pointer to current subtask being executed |
| `final_answer` | str | Final synthesized answer from synthesizer |
| `num_steps` | int | Counter for total steps completed |

**Used in**:
- `src/graph.py` StateGraph initialization
- All node functions (typed as `dict` but semantically matches AgentState)

---

## first_func.py

### `add()`

**Type**: `function` (utility) | **Importance**: ██░░░░░░░ 25  
**Signature**:
```python
def add(a: int, b: int) -> int
```

**Description**:  
Simple utility function for adding two numbers. Currently unused in the agent workflow.

**Location**: Line 1  
**Is Public**: ✓  
**Has Side Effects**: ✗

**Used in**: None (placeholder/test function)

---

## Dependency Graph

```
main.py
  └─ run_agent() [src/graph.py]
      └─ agent.invoke() [src/graph.py]
          ├─ decomposer() [src/nodes.py]
          │   └─ anthropic.Anthropic.messages.create()
          ├─ executor() [src/nodes.py] ×N
          │   └─ anthropic.Anthropic.messages.create()
          ├─ should_continue_executing() [src/nodes.py] ×N (router)
          └─ synthesizer() [src/nodes.py]
              └─ anthropic.Anthropic.messages.create()

AgentState [src/state.py] ← used by all nodes
```

---

## Summary Statistics

| Metric | Value |
|---|---|
| Total functions | 9 |
| Total classes/types | 1 |
| Entry points | 2 |
| Functions with side effects | 5 |
| API calls | 3 unique Anthropic calls |
| Lines of code | 338 |
| Avg function complexity | Low–Medium |

