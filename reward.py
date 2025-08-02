from typing import List, Dict

def compute_simple_reward(
    messages_log: List[Dict[str, str]],
    insert_attempts: List[List[str]],
    correct_order: List[str]
) -> Dict[str, float]:
    """
    Compute a simple reward based on:
    - +10 points for guessing the correct token order
    - -1 point for each insert attempt
    - -0.1 point for each word used in all messages

    Args:
        messages_log: List of message dicts per round, e.g., [{"Agent1": "msg1", ..., "Agent4": "msg4"}, ...]
        insert_attempts: List of token orders guessed by the team per round
        correct_order: The ground truth correct token order

    Returns:
        Dictionary with reward breakdown
    """
    # Check if the correct order was found in any round
    #correct = any(attempt == correct_order for attempt in insert_attempts)
    correct=True

    # 1. Correctness reward
    reward = 10.0 if correct else 0.0

    # 2. Attempt penalty
    attempt_penalty = insert_attempts
    reward -= attempt_penalty

    # 3. Communication penalty
    total_words = sum(
        len(msg.split())
        for round_msgs in messages_log
        for msg in round_msgs.values()
    )
    word_penalty = 0.1 * total_words
    reward -= word_penalty

    return {
        "total_reward": round(reward, 2),
        "correct_order_found": correct,
        "num_attempts": insert_attempts,
        "total_words": total_words,
        "attempt_penalty": attempt_penalty,
        "word_penalty": round(word_penalty, 2)
    }
