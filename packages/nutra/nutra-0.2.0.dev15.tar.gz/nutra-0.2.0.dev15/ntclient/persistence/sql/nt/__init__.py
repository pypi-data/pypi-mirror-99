import os
import sqlite3

from .... import NT_DB_NAME, NUTRA_DIR, __db_target_nt__

con = None


def nt_ver():
    """Gets version string for nt.sqlite database"""
    query = "SELECT * FROM version;"
    if con is None:
        nt_sqlite_connect()
    cur = con.cursor()
    result = cur.execute(query).fetchall()
    cur.close()
    return result[-1][1]


def nt_sqlite_connect():
    global con
    db_path = os.path.join(NUTRA_DIR, NT_DB_NAME)
    if os.path.isfile(db_path):
        con = sqlite3.connect(db_path)
        con.row_factory = sqlite3.Row

        # Verify version
        if nt_ver() != __db_target_nt__:
            print(
                f"ERROR: usda target [{__db_target_nt__}] mismatch actual [{nt_ver()}]"
            )
            exit(1)
        return con
    else:
        print("ERROR: nt database doesn't exist, please run `nutra init`")
        exit(1)


def _sql(query, args=None, headers=False):
    """Executes a SQL command to nt.sqlite"""
    global con
    if con is None:
        con = nt_sqlite_connect()
    cur = con.cursor()

    # TODO: DEBUG flag in prefs.json ... Print off all queries
    if args:
        if type(args) == list:
            result = cur.executemany(query, args)
        else:  # tuple
            result = cur.execute(query, args)
    else:
        result = cur.execute(query)
    rows = result.fetchall()
    if headers:
        headers = [x[0] for x in result.description]
        return headers, rows
    return rows
