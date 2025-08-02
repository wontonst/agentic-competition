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

You need to try to maximize the following reward function of the game: 
- +10 points for guessing the correct token order
- -1 point for each insert attempt
- -0.1 point for each word used in all messages

'''

game_rounds = [
    {
        "round": 0,
        "correct_order": ["White", "Blue", "Green", "Black"],
        "clues": {
        "Agent1": "The blue token should be inserted second.",
        "Agent2": "The black token should go last regardless of other rules.",
        "Agent3": "White and black tokens come before blue tokens.",
        "Agent4": "The green token comes before the black token."
        },
    },
    {
        "round": 1,
        "correct_order": ["White", "Red", "Yellow", "Blue"],
        "clues": {
            "Agent1": "Red comes after White.",
            "Agent2": "Yellow comes before Blue.",
            "Agent3": "White is not last.",
            "Agent4": "Red is before Yellow."
        }
    },
    {
        "round": 2,
        "correct_order": ["Purple", "Orange", "Green", "Black"],
        "clues": {
            "Agent1": "Green comes after Orange.",
            "Agent2": "Purple is the first token.",
            "Agent3": "Black is the last token.",
            "Agent4": "Orange comes before Green."
        }
    },
    {
        "round": 3,
        "correct_order": ["Teal", "Pink", "Cyan", "Magenta"],
        "clues": {
            "Agent1": "Teal is earlier than Magenta.",
            "Agent2": "Pink is not after Cyan.",
            "Agent3": "Magenta is after Cyan.",
            "Agent4": "Teal is first."
        }
    },
    {
        "round": 4,
        "correct_order": ["Red", "Orange", "Yellow", "Green"],
        "clues": {
            "Agent1": "Red is earlier than Green.",
            "Agent2": "Orange comes after Red.",
            "Agent3": "Yellow is between Orange and Green.",
            "Agent4": "Red is not last."
        }
    },
    {
        "round": 5,
        "correct_order": ["White", "Purple", "Teal", "Pink"],
        "clues": {
            "Agent1": "Purple comes after White.",
            "Agent2": "Teal is later than Purple.",
            "Agent3": "Pink is not before Teal.",
            "Agent4": "White is not last."
        }
    },
    {
        "round": 6,
        "correct_order": ["Magenta", "Blue", "Black", "Cyan"],
        "clues": {
            "Agent1": "Magenta comes before Blue.",
            "Agent2": "Black is later than Magenta.",
            "Agent3": "Cyan is last.",
            "Agent4": "Blue is not last."
        }
    }
]
