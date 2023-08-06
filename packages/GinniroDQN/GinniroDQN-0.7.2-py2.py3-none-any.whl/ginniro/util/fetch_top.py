import os
import json


def fetch_top(filepath, filename, start, end, k=10):

    init_dict = {}
    data_dict = {}

    for subpath in os.listdir(filepath):
        init_dict[subpath] = 0
        fn = os.path.join(filepath, subpath, filename)

        data = json.load(open(fn, 'r'))
        keylist = [int(key) for key in data['success_rate'].keys()]
        keylist.sort()

        for key in keylist:
            if int(key) >= start and int(key) <= end:
                if int(key) in data_dict.keys():
                    data_dict[int(key)].append((subpath, data['success_rate'][str(key)]))
                else:
                    data_dict[int(key)] = [(subpath, data['success_rate'][str(key)])]

    for key, value in data_dict.items():
        st = sorted(value, key=lambda x: x[1], reverse=True)
        for i in range(k):
            init_dict[st[i][0]] += 1

    sorted_idx = sorted(init_dict.items(), key=lambda x: x[1], reverse=True)

    print(sorted_idx[:k])

    return sorted_idx[:k]
