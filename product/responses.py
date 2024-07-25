from random import choice, randint
from shared import syllabus_content  # Import shared module
import re

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'Good, thanks!'
    elif 'bye' in lowered:
        return 'See you!'
    elif 'goodbye' in lowered:
        return 'See you next time!!!!!!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1, 6)}'

    # Check for syllabus-related questions
    for key, value in syllabus_content.items():
        if 'syllabus' in lowered or 'schedule' in lowered or 'deadline' in lowered:
            if re.search(lowered, value, re.IGNORECASE):
                return value
            else:
                return "Sorry, I couldn't find any relevant information in the syllabus."

    # Default responses
    return choice(['I do not understand...',
                   'What are you talking about?',
                   'Do you mind rephrasing that?'])
