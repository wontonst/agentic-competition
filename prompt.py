TEMPLATE = '''
You are AgentX.

Your private information:
<info>

Your actions:
- You can send a one-sentence message to all other agents each round.
- Based on all messages so far, you may propose an insertion using `insert_token(color)`.

Remember:
- Your message should be as short and informative as possible.
- The correct token order is the same across all rounds. You may learn from previous failures.

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