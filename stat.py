# with open('data/stat/continuous.pkl', 'rb') as f:
#     log = pickle.load(f)
# messages = dict(map(lambda rated: (rated, list(map(lambda x: sum(map(len, log[rated][x].values())), log[rated]))), log))

import os
import pickle


to_list = lambda x: x.strip().replace('(', '').replace(')', '').replace("'", '').split(', ')


def window_values(logs_path):
    secs_dist = {}
    logs = sorted(os.listdir(logs_path))
    for sec in logs:
        sec_path = os.path.join(logs_path, sec)
        parts = sorted(filter(lambda x: x.startswith('part'), os.listdir(sec_path)))
        timestamp = int(sec.split('-')[1])
        d = {}
        for part in parts:
            with open(os.path.join(sec_path, part)) as f:
                lists = map(to_list, f.readlines())
                d.update(dict(map(lambda x: ((x[0], x[1]), int(x[2])), lists)))
        secs_dist.update({timestamp: d})
    return secs_dist


def count_values(logs_path):
    """внутри директирий continuous"""
    secs_dist = {}
    logs = sorted(os.listdir(logs_path))
    for sec in logs:
        sec_path = os.path.join(logs_path, sec)
        parts = sorted(filter(lambda x: x.startswith('part'), os.listdir(sec_path)))
        timestamp = int(sec.split('-')[1])
        parts_dict = {}
        for part in parts:
            with open(os.path.join(sec_path, part)) as f:
                key = int(part.split('-')[1])
                lines = list(map(to_list, f.readlines()))
            parts_dict.update({key: lines})
        secs_dist.update({timestamp: parts_dict})
    return secs_dist


def process_rate_value_folder(rate_value_path):
    """внутри rate_x_values_y"""
    log_res = count_values(os.path.join(rate_value_path, 'real'))
    window_bounds = window_values(os.path.join(rate_value_path, 'window_events'))
    return log_res, window_bounds


def save_state(type_, d):
    with open(os.path.join('data', 'stat', f'{type_}.pkl'), 'wb') as out:
        pickle.dump(d, out)


base_path = os.path.join('data', 'sim')
folders = os.listdir(base_path)
stats = [{}, {}, {}]

if __name__ == '__main__':
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        _, rate = folder.split('_')
        rate = float(rate)
        res = process_rate_value_folder(folder_path)
        for d, r in zip(stats, res):
            d.update({rate: r})

    for name, d in zip(['real', 'window_events', 'pr'], stats):
        save_state(name, d)