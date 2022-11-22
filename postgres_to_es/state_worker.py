import json
import logging
import datetime
from config_models import State
import db_config


def get_state() -> State:
    with open(db_config.STATE_CON) as file:
        try:
            data = json.load(file)
            state = State.parse_raw(data)
            return state
        except FileNotFoundError:
            logging.error('Json state file not found')
        except json.decoder.JSONDecodeError:
            return State(
                last_update=datetime.datetime(2000, 1, 1),
                last_row=0,
                is_finished=False
            )


def save_state(state: State) -> None:
    with open(db_config.STATE_CON, 'w') as file:
        try:
            json.dump(state.json(), file)
        except FileNotFoundError:
            logging.error('Json state file not found')


# В начале нового цикла загрузки в ETL - обновляем state
def refresh_state(state: State) -> State:
    state.is_finished = False
    state.last_row = 0
    save_state(state)
    return state
