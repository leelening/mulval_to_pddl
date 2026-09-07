# PDDL Parser

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Planning](https://img.shields.io/badge/Planning-AI-blue)](http://www.planning.domains/)
[![PDDL](https://img.shields.io/badge/PDDL-Planning-orange)](https://en.wikipedia.org/wiki/Planning_Domain_Definition_Language)

A Python tool to create deterministic transition systems from PDDL (Planning Domain Definition Language) files.

## Overview

This parser converts classical planning problems described in PDDL format into deterministic transition systems represented as state transition graphs. It's particularly useful for:

- Converting PDDL planning problems to MDP representations
- Analyzing planning domain structures
- Generating transition systems for reinforcement learning
- Security and attack graph analysis (when combined with MulVAL)

## Features

- 🔄 **PDDL Parsing**: Parse domain and problem PDDL files
- 🗂️ **Transition System**: Generate deterministic transition systems
- 💾 **Pickle Export**: Save transition systems for later use
- 🔗 **MulVAL Integration**: Works with MulVAL attack graphs

## Tech Stack

- **Language**: Python 3.x (developed on Python 3.5+)
- **Dependencies**: none beyond the standard library (`pickle`, `re`, `itertools`)

## Installation

```bash
# Clone the repository
git clone https://github.com/leelening/pddl-parser.git
cd pddl-parser
```

No third-party packages are required.

## Usage

### Basic Usage

```bash
# Generate transition system from PDDL files
python constructor.py ./examples/domain.pddl ./examples/problem.pddl
```

This creates a `transitions.pickle` file containing the deterministic transition system.

### Input Files

The tool expects two PDDL files:

1. **domain.pddl**: Defines the planning domain (predicates, actions, effects)
2. **problem.pddl**: Defines the specific problem instance (initial state, goal)

### Example

An example is provided in the `examples/` directory:

```
examples/
├── domain.pddl     # Example planning domain
└── problem.pddl    # Example problem instance
```

These files can be generated using [mulval_to_pddl](https://github.com/leelening/mulval_to_pddl).

## Project Structure

```
.
├── constructor.py       # Main script to generate transition systems
├── examples/            # Example PDDL files
│   ├── domain.pddl
│   └── problem.pddl
└── transitions.pickle   # Generated output (after running)
```

## How It Works

### PDDL to Transition System

1. **Parse Domain**: Extract actions, preconditions, and effects
2. **Parse Problem**: Extract initial state and goal conditions
3. **Build State Space**: Breadth-first exploration of the states reachable from the initial state
4. **Generate Transitions**: For each state-action pair, determine next state
5. **Export**: Save as pickle file for later use

### Transition System Format

The output `transitions.pickle` contains a dictionary mapping:
- `transitions[state]` → dict of available action labels
- `transitions[state][action_label]` → next state

Pickled as `[transitions, initial_state]`.

## Integration with MulVAL

This parser is designed to work with [mulval_to_pddl](https://github.com/leelening/mulval_to_pddl):

1. Use MulVAL to generate attack graphs
2. Convert to PDDL using MulVAL-to-PDDL
3. Parse PDDL to transition system using this tool
4. Use transition system for security analysis or planning

## Online PDDL Editor

For testing and solving PDDL problems, use the online editor:
- [PDDL Editor](http://editor.planning.domains/)

## API Usage

```python
import pickle

# Load the transition system
with open('transitions.pickle', 'rb') as f:
    transitions, initial_state = pickle.load(f)

# A state is a canonical (sorted) tuple of ground predicates, each itself a
# tuple, e.g. (('attackerlocated', 'internet'), ('execcode', 'h1', 'someuser'))
# An action label is 'name' for a 0-ary action, otherwise 'name(arg1,arg2)'.
#
#   transitions[state][action_label] -> next_state

for action_label, next_state in transitions[initial_state].items():
    print(action_label, '->', next_state)
```

## Dependencies

- Python 3.x (standard library only)

## Limitations

- Supports deterministic planning domains only
- State space must be finite and reasonably sized
- Action effects should be deterministic

## License

MIT License - see [LICENSE.md](LICENSE.md) for details

## Acknowledgments

- [pddl-parser](https://github.com/pucrs-automated-planning/pddl-parser) - Reference implementation
- [MulVAL](http://people.cs.ksu.edu/~xou/mulval/) - For attack graph generation
- [PDDL](https://en.wikipedia.org/wiki/Planning_Domain_Definition_Language) - Planning Domain Definition Language

## Author

**Lening Li**
- GitHub: [@leelening](https://github.com/leelening)
