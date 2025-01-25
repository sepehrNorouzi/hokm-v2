from os import environ as env

from redis import Redis


def get_redis_client(is_test: bool = False) -> Redis:
    test = 'TEST_' if is_test else ''

    # REDIS CONFIG
    r_host = f'{test}REDIS_HOST'
    r_port = f'{test}REDIS_PORT'
    r_password = f'{test}REDIS_PASSWORD'
    r_db = f'{test}REDIS_DB'

    db = env.get(r_db, '0')

    host = env.get(r_host)
    port = env.get(r_port, '6379')
    db = db,
    password = env.get(r_password, '1')
    print(host, port, db, password)
    return Redis()
