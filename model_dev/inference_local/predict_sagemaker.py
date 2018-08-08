import os, sys, logging, time
from inference_local.api import MXSRequest

logger = logging.getLogger(os.path.basename(__file__))
model_name = 'model_1st'

def predict(data, index):
    try:
        logger.info('============== %s ===============', index)
        logger.info('Request: %s', data)
        t0 = int(round(time.time() * 1000))
        resp = mxs.request(model_name, data)
        t1 = int(round(time.time() * 1000))
        logger.info('%d ms, Response: %s', t1-t0, resp)
        return t1-t0
    except:
        return data

if __name__ == '__main__':
    global mxs
    mxs = MXSRequest('cdev')
    predict({'userid' : 101}, 1)

    logger.info('=============== concurrent requests ===============')
    import concurrent.futures
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
    futures = []
    for i in range(1000):
        data = {'a' : i-1, 'b': i+1}
        futures.append(executor.submit(predict, data, i+1))
        if i >= 1000:
            break

    tot = 0
    max_t = 0
    min_t = 1000000
    n = 0
    for future in concurrent.futures.as_completed(futures):
        t = future.result()
        if t is None:
            continue

        logger.info('time consumed: %s', t)
        tot += t
        max_t = max(t, max_t)
        min_t = min(t, min_t)
        n += 1

    logger.info('average time consumed over %d returned: %s', tot/n, n)
    logger.info('max time: %s, min time: %s', max_t, min_t)
