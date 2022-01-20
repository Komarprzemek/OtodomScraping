import psycopg2
import pgsql_config

def new_offer(link):
    conn = None
    cursor = None

    import_script = ("SELECT * FROM otodom")

    try:
        conn = psycopg2.connect(
            host=pgsql_config.hostname,
            dbname=pgsql_config.database,
            user=pgsql_config.username,
            password=pgsql_config.pwd,
            port=pgsql_config.port_id)  # connection to SQL function

        cursor = conn.cursor()

        cursor.execute(import_script)
        database = cursor.fetchall()

        for record in database:
            if link == record[0]:
                return 1

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