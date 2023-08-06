""" Fibonacci calculation """


def sum(terms: int):
    """ Create an fibonacci calculation
    :param - terms - number of desired terms
    :return - last time of the sequence
    """

    previous_number = 0
    later_number = 1
    current_number = 0

    for i in range(terms):
        previous_number = later_number
        later_number = current_number
        current_number = previous_number + later_number
    
    return current_number
        