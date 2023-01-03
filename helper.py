def make_something_move(origin: tuple, move: tuple):
    """ This function receives two coordinates (tuples), adds them up and returns the new coordinate
    For example, if we want to move the snake one square up, the function will receive the coordinate of the snake's head
    and the coordinate of UP as appears in constant.py, adds them up and returns the the coordinate for the snake's head
    """
    return (origin[0] + move[0], origin[1] + move[1])

def check_direction(direction: tuple, current_head: tuple, current_neck: tuple):
    """ This function receives a direction and the coordinate in which the object (snake) wants to go,
    and returns weither or not it's possible (returns False if the direction is opposite to that of the snake) """ 
    return make_something_move(direction, current_head) != current_neck