TEMPLATE = '''
Game Overview

You are part of a team of four autonomous agents, each receiving partial and private information about the correct order of four tokens. Each token is uniquely defined by four features: a color, a shape, a number, and a letter (e.g., "Red Triangle 3 A"). The true order of these composite tokens is hidden and remains fixed across all rounds of the game.

In each round, you may:
- Send one short message to all teammates.
- Collaboratively propose a full token ordering by calling insert_token(...).

Your success depends on deducing the correct order using limited communication, even when information is partial, ambiguous, or seemingly contradictory.

Goal

The goal of the game is to identify the correct ordered sequence of tokens as quickly and efficiently as possible through cooperative communication.

You will be evaluated based on:
- How early your team converges to the correct token order
- How concise and informative your messages are
- How effectively your team integrates fragmented or conflicting constraints

The optimal strategy is not just correctness, but efficient and collaborative reasoning.

Communication Protocol

Each agent:
- Has access only to their private clue (a logical constraint involving token properties or positions)
- May broadcast one short natural language message per round to all teammates
- Can see messages from previous rounds

Messages should be:
- Informative (describe constraints or hypotheses)
- Concise (shorter messages are rewarded)
- Non-redundant (avoid repeating known facts)

Game Flow

1. Each agent receives a private clue.
2. All agents broadcast one message per round.
3. The team submits a proposed token order using:
   insert_token(token1, token2, token3, token4)
   where each token is described in the format "Color Shape Number Letter"
4. If correct → the game proceeds to a new round (same order, different clues).
   If incorrect → another communication round begins.
5. The game ends when a correct order is submitted or after a maximum number of rounds.
'''




game_rounds = [
    {
        "round": 1,
        "correct_order": [
            "Red Triangle 1 A",
            "Green Circle 2 B",
            "Blue Square 3 C",
            "Yellow Hexagon 4 D"
        ],
        "clues": {
            "Agent1": "The Triangle comes before the Square.",
            "Agent2": "Token with number 2 is not last.",
            "Agent3": "The token labeled 'C' is after the Red one.",
            "Agent4": "Green token comes before the Blue one."
        }
    },
    {
        "round": 2,
        "correct_order": [
            "White Star 4 Z",
            "Black Triangle 1 X",
            "Red Circle 3 Y",
            "Orange Square 2 W"
        ],
        "clues": {
            "Agent1": "Star and Triangle must come before Square.",
            "Agent2": "Black token is not first unless it’s labeled X.",
            "Agent3": "Token labeled Z must be earlier than Y.",
            "Agent4": "Red token comes after the White one."
        }
    },
    {
        "round": 3,
        "correct_order": [
            "Purple Hexagon 2 L",
            "Yellow Triangle 1 M",
            "Green Circle 4 N",
            "Blue Star 3 P"
        ],
        "clues": {
            "Agent1": "Hexagon comes before Circle and Star.",
            "Agent2": "Token labeled L is earlier than M.",
            "Agent3": "Triangle is not last.",
            "Agent4": "Star is after Triangle."
        }
    },
    {
        "round": 4,
        "correct_order": [
            "Teal Diamond 3 K",
            "Pink Star 1 J",
            "Red Circle 2 I",
            "Black Square 4 H"
        ],
        "clues": {
            "Agent1": "Diamond comes before Circle.",
            "Agent2": "Pink token precedes the Red one.",
            "Agent3": "Token with number 4 is last.",
            "Agent4": "Star is not next to Square."
        }
    },
    {
        "round": 5,
        "correct_order": [
            "Green Triangle 2 A",
            "Orange Circle 3 B",
            "Red Star 1 C",
            "Blue Square 4 D"
        ],
        "clues": {
            "Agent1": "Red and Blue tokens are not adjacent.",
            "Agent2": "Triangle is earlier than Star.",
            "Agent3": "Square is last.",
            "Agent4": "Token labeled B comes after A."
        }
    },
    {
        "round": 6,
        "correct_order": [
            "Cyan Hexagon 1 E",
            "Magenta Circle 2 F",
            "Yellow Triangle 3 G",
            "Black Star 4 H"
        ],
        "clues": {
            "Agent1": "Circle is not adjacent to Triangle.",
            "Agent2": "Token labeled F is right after E.",
            "Agent3": "Black token comes last.",
            "Agent4": "Hexagon comes before Star."
        }
    }
]
