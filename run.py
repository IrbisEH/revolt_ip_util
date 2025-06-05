import os
import pickle
import dataclasses

from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = Path(ROOT_DIR) / 'data.pkl'
load_dotenv(dotenv_path=f'{ROOT_DIR}/.env')

PORTS_SAMPLE = {
    'local_ssh': 80,
    'remote_ssh': 80,
    'ff_flow': 1700,
    'cs_flow': 1800,
    'dns_flow': 1900,
}

@dataclasses.dataclass
class DataItem:
    name: str       # uniq!
    project: str
    mac: str
    ip: str
    ports: dict

def get_data() -> dict:
    with open(DATA_FILE, 'rb') as f:
        raw_items = pickle.load(f)
    raw_items = [DataItem(**i) for i in raw_items]
    return {i.name: i for i in raw_items}

def put_data(data: dict) -> None:
    _data = [i.__dict__ for i in data.values()]
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(_data, f)

def add_data(params: dict) -> None:
    item = DataItem(**params)
    data = get_data()

    if item.name in data:
        _item = data[item.name]
        for k, v in ((k, v) for k, v in item.__dict__.items() if v):
            setattr(_item, k, v)
    else:
        data[item.name] = item

    put_data(data)

def show_data(filter_data: dict = None) -> None:
    data = get_data()
    result = list(data.values())

    if filter_data and filter_data.keys():
        func = get_filter_func(filter_data)
        result = list(filter(func, result))

    for i in result:
        print(i)

def get_filter_func(filter_data: dict):
    def filter_func(item: DataItem):
        is_valid = True
        for k, v in filter_data.items():
            val = getattr(item, k, None)
            if not val or val != v:
                is_valid = False
                break
        return is_valid
    return filter_func


if __name__ == '__main__':
    try:
        # parse args and run funcs
        pass
    except PermissionError:
        print(f'Error! Not enough access rights for data file "{DATA_FILE}".')

    except FileNotFoundError:
        print(f'Error! Data file "{DATA_FILE}" not found.')

    except Exception as e:
        print(e)