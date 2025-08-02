TEMPLATE = '''

Game Overview

You are part of a team of four autonomous agents, each receiving partial and private information about the correct order of four tokens (each representing a unique color). The true order is hidden and remains the same across all rounds of the game.

In each round, you may:
- Send one short message to all teammates.
- Collaboratively propose a full token ordering by calling insert_token(...).

Your success depends on deducing the correct token order using limited communication, even when agent information is ambiguous or contradictory.

Goal

The goal of the game is to identify the correct sequence of tokens as quickly and efficiently as possible using cooperative communication.

You will be evaluated based on:
- How early your team converges to the correct ordering
- How concise and helpful your messages are
- How well your team integrates and resolves potentially conflicting information

The optimal strategy is not only to be right, but to be right with minimal effort and maximal cooperation.

Communication Protocol

Each agent:
- Has access only to their private clue (a logical constraint about the token order)
- May broadcast one short natural language message to all agents in each round
- Can see messages from previous rounds

Messages should be:
- Informative (communicate what you know)
- Concise (shorter messages are rewarded)
- Non-redundant (avoid repeating facts already known)

Game Flow

1. Each agent receives a private clue.
2. All agents broadcast a message (1 per round).
3. The team submits a proposed token order using:
   insert_token(color1, color2, color3, color4)
4. If correct → the game proceeds to a new instance (same order, different clues).  
   If incorrect → another round of messaging begins.
5. The game ends when a correct order is submitted or after a fixed number of rounds.
'''

game_rounds = [
    {
        "round": 1,
        "correct_order": ["Red", "Green", "Blue", "Yellow"],
        "clues": {
            "Agent1": "Blue is before Green.",
            "Agent2": "Red is before Blue but not first.",
            "Agent3": "Yellow comes after Green.",
            "Agent4": "Green is the first token."
        }
    },
    {
        "round": 2,
        "correct_order": ["White", "Black", "Red", "Orange"],
        "clues": {
            "Agent1": "Red is after White unless Black is first.",
            "Agent2": "Orange is last if Red is not third.",
            "Agent3": "White must come before both Black and Red.",
            "Agent4": "Black is before Red."
        }
    },
    {
        "round": 3,
        "correct_order": ["Purple", "Yellow", "Green", "Blue"],
        "clues": {
            "Agent1": "Green is not before Yellow.",
            "Agent2": "Purple is not last.",
            "Agent3": "Blue is after Green.",
            "Agent4": "Yellow is not first or last."
        }
    },
    {
        "round": 4,
        "correct_order": ["Teal", "Pink", "Red", "Black"],
        "clues": {
            "Agent1": "Teal comes before Red.",
            "Agent2": "Pink is earlier than Black.",
            "Agent3": "Red is not first.",
            "Agent4": "Black is not last."
        }
    },
    {
        "round": 5,
        "correct_order": ["Green", "Orange", "Red", "Blue"],
        "clues": {
            "Agent1": "Orange is next to Red.",
            "Agent2": "Green is not next to Red.",
            "Agent3": "Blue is not first or second.",
            "Agent4": "Red is not last."
        }
    },
    {
        "round": 6,
        "correct_order": ["Cyan", "Magenta", "Yellow", "Black"],
        "clues": {
            "Agent1": "Magenta comes after Yellow.",
            "Agent2": "Cyan is two steps before Black.",
            "Agent3": "Yellow is not next to Black.",
            "Agent4": "Black is the last."
        }
    }
]