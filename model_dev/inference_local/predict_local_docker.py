import os, sys, logging, pandas as pd, json, requests, time

logger = logging.getLogger(os.path.basename(__file__))

def predict(data, index):
    logger.info('============== %s ===============', index)
    logger.info('Request data: %s', data)
    url = 'http://127.0.0.1:8080/invocations'
    try:

        data = json.dumps(data)
        t0 = int(round(time.time() * 1000))
        response = requests.post(
            url=url,
            data=data,
            headers={'content-type': 'application/json'}
        )
        t1 = int(round(time.time() * 1000))

        # Check and return request
        assert response.status_code == 200, AssertionError(response.text)
        logger.info('%d ms, Response: %s', t1 - t0, response.text)
        return t1 - t0
    except:
        return data

if __name__ == '__main__':
    predict({'userid' : 101}, 1)
    for i in range(20):
        predict({'a' : i}, i+1)
        if i >= 20:
            break

    logger.info('=============== concurrent requests ===============')
    import concurrent.futures
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    futures = []
    for i in range(1000):
        futures.append(executor.submit(predict, {'a' : i-1, 'b' : i+1}, i+1))
        if i >= 1000:
            break

    tot = 0
    max_t = 0
    min_t = 1000000
    n = 0
    failed = []
    for future in concurrent.futures.as_completed(futures):
        t = future.result()
        if isinstance(t, dict):
            failed.append(t)
            continue

        logger.info('time consumed: %s', t)
        tot += t
        max_t = max(t, max_t)
        min_t = min(t, min_t)
        n += 1

    logger.info('failed requests:')
    for fail in failed:
        logger.info('\t%s', fail)
    logger.info('average time consumed over %d returned: %.2f ms', n, tot/n)
    logger.info('max time: %d ms, min time: %d ms', max_t, min_t)
