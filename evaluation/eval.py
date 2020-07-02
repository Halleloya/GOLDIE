import requests
import time
import json
from tqdm import tqdm

HEADERS = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}


def evaluate_register(itrs):
    url = 'http://192.168.1.189:5000/register'

    start = time.time()
    for i in tqdm(range(itrs)):
        payload = {
            "targetLoc": "level5",
            "td": {
                "_type": "pc",
                "id": "urn:dev:ops:54312-pc-{}".format(i)
            }
        }
        requests.post(url, data=json.dumps(payload), headers=HEADERS)

    end = time.time()
    elapsed = end - start
    avg = float(elapsed) / itrs
    print("Total of {} seconds elapsed for register {} things".format(
        elapsed, itrs))
    print("Average time: {}".format(avg))

    return (elapsed, avg)


def evaluate_searchByLocId(itrs):
    url = 'http://192.168.1.189:5000/searchByLocId?loc={}&id={}'

    start = time.time()
    for i in tqdm(range(itrs)):
        requests.get(url.format('level5', 'urn:dev:ops:54312-pc-{}'.format(i)))

    end = time.time()
    elapsed = end - start
    avg = float(elapsed) / itrs
    print("Total of {} seconds elapsed for searchByLocId {} things".format(
        elapsed, itrs))
    print("Average time: {}".format(avg))
    return (elapsed, avg)


def evaluate_searchByLocTypeRecursive(itrs):
    url = 'http://192.168.1.189:5000/searchByLocType?loc={}&type={}'.format(
        'level5', 'pc')

    start = time.time()
    for _ in tqdm(range(itrs)):
        requests.get(url)

    end = time.time()
    elapsed = end - start
    avg = float(elapsed) / itrs
    print("Total of {} seconds elapsed for searchByLocTypeRecursive {} things".
          format(elapsed, itrs))
    print("Average time: {}".format(avg))
    return (elapsed, avg)


def evaluate_searchByLocTypeIterative(itrs):
    url = 'http://192.168.1.189:5000/searchByLocTypeIterative?loc={}&type={}'.format(
        'level5', 'pc')

    start = time.time()
    for _ in tqdm(range(itrs)):
        requests.get(url)

    end = time.time()
    elapsed = end - start
    avg = float(elapsed) / itrs
    print("Total of {} seconds elapsed for searchByLocTypeIterative {} things".
          format(elapsed, itrs))
    print("Average time: {}".format(avg))
    return (elapsed, avg)


def evaluate_delete(itrs):
    url = "http://192.168.1.189:5000/delete?targetLoc={}&id={}"
    start = time.time()
    for i in tqdm(range(itrs)):
        requests.delete(
            url.format('level5', 'urn:dev:ops:54312-pc-{}'.format(i)))
    end = time.time()
    elapsed = end - start
    avg = float(elapsed) / itrs
    print("Total of {} seconds elapsed for delete {} things".format(
        elapsed, itrs))
    print("Average time: {}".format(avg))
    return (elapsed, avg)


if __name__ == '__main__':
    # warmup
    evaluate_register(50)

    sep = '-' * 50
    evaluation_ls = [
        evaluate_register, evaluate_searchByLocId,
        evaluate_searchByLocTypeRecursive, evaluate_searchByLocTypeIterative,
        evaluate_delete
    ]

    res = {}

    for num_itrs in [10, 50, 100, 200, 500]:
        res[str(num_itrs)] = []
        for evaluation in evaluation_ls:
            res[str(num_itrs)].append(evaluation(num_itrs))
            print(sep)

    print(res)


'''
0.21520845890045165     0.21815636157989501     0.2169780945777893      0.21891479611396789
0.18715918064117432     0.1796647548675537      0.177275710105896       0.17775959014892578
0.23601322174072265     0.2353415822982788      0.23670841217041017     0.2382632851600647
0.03278398513793945     0.03250162124633789     0.033439044952392576    0.033434526920318605
0.24893612861633302     0.26120203018188476     0.2650839018821716      0.26385631918907165


'''