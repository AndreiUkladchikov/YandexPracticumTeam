import postgres.pg_context as pg_context
import postgres.save_data as save_data


def main():
    with pg_context.conn_context() as conn:
        save_data.create_db(conn)


if __name__ == '__main__':
    main()
