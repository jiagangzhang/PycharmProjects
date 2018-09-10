import logging
from mytheresa_worker import place_mytheresa_order


def place_order(order_obj):
    """
    check which merchant
    then dispatch to different merchant functions
    clean up when merchant functions return

    """
    place_mytheresa_order(order_obj)


if __name__ == '__main__':
    place_order({})
