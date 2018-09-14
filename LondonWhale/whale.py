from multiprocessing import Process, cpu_count, active_children
import time
import logging
from order_worker import place_order

logging.basicConfig()

test_order_obj = {
    'sku_list': [
        {
            'url': '',
            'SkuCode': '',
            'size': '',
            'color': '',
            'name': '',
            'quantity': 1
         },
        {
            'url': '',
            'SkuCode': '',
            'size': '',
            'color': '',
            'name': '',
            'quantity': 1
            }
        ],
    'merchant': 'mytheresa',
    'total_paid': 100,
    'order_key': '',
    'Customer': '',
    'Address': ''
    }

if __name__ == '__main__':
    job_list = []
    # p = Process(target=place_order, args=({},))
    # p.start()
    while True:
        # check whether new order coming todo: 可能需要考虑队列情况，将code改为for循环
        if new_order:
            job_list.append(new_order)

        # check whether cpu is full  or job_list > 0
        if len(job_list) > 0 and len(active_children()) < cpu_count():
            job = job_list.pop(0)
            active_process = [pro.name for pro in active_children()]
            if job['merchant'] not in active_process:
                """
                fork a new process with the merchant name and dispatch to order_worker
                p = Process(target=place_order, name=job['merchant'], args=(job,))
                p.start()
                """
                pass
            else:
                job_list.append(job)  # send this job to the bottom of list

        time.sleep(10)
