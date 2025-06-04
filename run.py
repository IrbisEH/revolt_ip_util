import dataclasses
import os
import pickle
from importlib.resources import open_text

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
        return pickle.load(f)

def put_data(data: dict) -> None:
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(data, f)

def search_data():
    pass

def print_data():
    pass


if __name__ == '__main__':
    try:
        item = DataItem(
            name='dpiui2_main',
            project='dpiui2',
            ip='192.168.1.100',
            ports=PORTS_SAMPLE,
        )

        data = {item.name: item.__dict__}

        put_data(data)

        # data = get_data()
        # print(data)



    except PermissionError:
        print(f'Error! Not enough access rights for data file "{DATA_FILE}".')

    except FileNotFoundError:
        print(f'Error! Data file "{DATA_FILE}" not found.')

    except Exception as e:
        print(e)