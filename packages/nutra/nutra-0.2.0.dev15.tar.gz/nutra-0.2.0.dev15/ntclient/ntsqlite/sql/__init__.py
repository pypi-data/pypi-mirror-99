#!/usr/bin/env python3
import csv
import os
import sqlite3

NT_DB_NAME = "nt.sqlite"


def build_ntsqlite(verbose=False):
    # cd into this script's directory
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    os.chdir(SCRIPT_DIR)

    if verbose:
        print("Cleanup...")
    if os.path.isfile(NT_DB_NAME):
        os.remove(NT_DB_NAME)

    if verbose:
        print(f"\nPack {NT_DB_NAME}")
    con = sqlite3.connect(NT_DB_NAME)
    cur = con.cursor()

    if verbose:
        print("\n-> Create tables")
    with open("tables.sql") as tables:
        cur.executescript(tables.read())

    if verbose:
        print("-> Populate data")
    for p in os.listdir("data"):
        if not p.endswith(".csv"):
            continue
        t = os.path.splitext(os.path.basename(p))[0]
        p = os.path.join("data", p)

        # Loop over CSV files
        with open(p) as f:
            reader = csv.DictReader(f)
            q = ",".join("?" * len(reader.fieldnames))
            reader = csv.reader(f)
            cur.executemany(f"INSERT INTO {t} VALUES ({q});", reader)

    cur.close()
    con.commit()
    con.close()
    if verbose:
        print("\nDone!")
    return True


if __name__ == "__main__":
    build_ntsqlite()
