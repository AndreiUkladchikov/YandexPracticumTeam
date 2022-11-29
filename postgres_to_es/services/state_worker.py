import json
import logging
import datetime
from config.config_models import State, Indexes


def get_state(conn: str) -> State:
    with open(conn) as file:
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
                is_finished=False,
                index=Indexes.MOVIE.value
            )


def save_state(conn: str, state: State) -> None:
    with open(conn, 'w') as file:
        try:
            json.dump(state.json(), file)
        except FileNotFoundError:
            logging.error('Json state file not found')


# В начале нового цикла загрузки в ETL - обновляем state
def refresh_state(conn: str, state: State) -> State:
    state.is_finished = False
    state.last_row = 0
    state.index = Indexes.MOVIE.value
    save_state(conn, state)
    return state


def get_next_state(state: State) -> State:
    if state.index == Indexes.MOVIE.value:
        state.index = Indexes.GENRE.value
    elif state.index == Indexes.GENRE.value:
        state.index = Indexes.PERSONS.value
    else:
        state.is_finished = True
        state.last_update = datetime.datetime.now()
    state.last_row = 0
    return state
