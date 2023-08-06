#  Copyright © 2020 Ingram Micro Inc. All rights reserved.

import psycopg2
import pytest

from integration_tests.tests.utils import REPLICA_TABLES

from dj_cqrs.transport import current_transport


@pytest.fixture
def replica_cursor():
    connection = psycopg2.connect(host='postgres', database='replica', user='user', password='pswd')

    # That setting is extremely important for table truncations
    connection.set_isolation_level(0)

    cursor = connection.cursor()
    for table in REPLICA_TABLES:
        cursor.execute('TRUNCATE TABLE {};'.format(table))

    yield cursor

    cursor.close()
    connection.close()


@pytest.fixture
def clean_rabbit_transport_connection():
    current_transport.clean_connection()

    yield
