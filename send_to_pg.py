import psycopg2

import pgsql_config


def send(link, title, localization, price, area, price_per_sqm, room, rent, heat, floor):
    conn = None
    cursor = None

    create_script = '''CREATE TABLE IF NOT EXISTS otodom(
                                       link varchar(100) PRIMARY KEY,
                                       title varchar(200) NOT NULL,
                                       localization varchar(100) NOT NULL,
                                       price varchar(40) NOT NULL,
                                       area varchar(40) NOT NULL,
                                       price_per_sqm varchar(10) NOT NULL,
                                       room varchar(2) NOT NULL,
                                       rent varchar(40) NOT NULL,
                                       heat varchar(40) NOT NULL,
                                       floor varchar(40) NOT NULL)'''

    insert_script = "INSERT INTO otodom(link, title, localization, price, area, price_per_sqm, room, rent, heat, floor) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    insert_value = (link, title, localization, price, area, price_per_sqm, room, rent, heat, floor)

    try:
        conn = psycopg2.connect(
            host=pgsql_config.hostname,
            dbname=pgsql_config.database,
            user=pgsql_config.username,
            password=pgsql_config.pwd,
            port=pgsql_config.port_id)  # connection to SQL function

        cursor = conn.cursor()
        cursor.execute(create_script)
        cursor.execute(insert_script, insert_value)

        conn.commit()

    except Exception as error:
        print("Connection Error: ")
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if cursor is not None:
            conn.close()

    return 0