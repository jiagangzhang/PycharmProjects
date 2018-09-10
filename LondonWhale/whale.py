from multiprocessing import Process, cpu_count, active_children
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
    while True:
        # check whether new order coming or job_list >0
        if new_order:
            job_list.append(new_order)
        # check whether cpu is full, todo: 逻辑有问题，需修改
        for job in job_list:
            if len(active_children()) < cpu_count() and len(job_list) > 0:
                if job.merchant not 'already forked':  # todo: how to implement this method
                    job_list.pop
                    fork a new process and dispatch to order_worker
        else:
            time.sleep(10)
        # p = Process(target=place_order, args=({},))
        # pass

