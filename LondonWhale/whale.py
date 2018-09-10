from multiprocessing import Process, cpu_count
import time
import logging
from order_worker import place_order

logging.basicConfig()

test_order_obj = {
    'sku_list': [
        {
            'url': '',
            'size': '',
            'color': '',
            'name': ''
         },
        {
            'url': '',
            'size': '',
            'color': '',
            'name': ''
            }
        ],
    'merchant': 'mytheresa',
    'total_paid': 100,
    }

if __name__ == '__main__':
    job_list = []
    p = Process(target=place_order, args=({},))
    p.start()
    # while True:
    #     # check whether new order coming
    #     # if new_order:
    #     #     add new_order to job_list
    #     #     check whether cpu is full:
    #     #     if cpu_not_full:
    #     #         job_list.pop
    #     #         fork a new process and dispatch to order_worker
    #     #     else:
    #     #         time.sleep(10)
    #     # else:
    #     #     time.sleep(10)
    #     p = Process(target=place_order, args=({},))
    #     pass

