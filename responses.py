import random

def get_response(message:str) -> str:
    p_message = message.lower()
    
    if p_message == 'hello':
        return 'hello'
    
    if p_message == 'roll':
        return str(random.randint(1, 6))
    
    return 'I didn\'t understand what you wrote'