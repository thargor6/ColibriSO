from sqlite3 import Error
import os

SQL_CREATE_DB_CHANGELOGS_TABLE = """ CREATE TABLE IF NOT EXISTS db_change_logs (
        id integer PRIMARY KEY,
        name text NOT NULL,
        content text NOT NULL
); """

SQL_SELECT_LAST_CHANGELOG = """ SELECT name FROM db_change_logs ORDER BY id DESC LIMIT 1; """

def apply_db_changelogs(conn):
    try:
        c = conn.cursor()
        # create changelogs table if not exists
        c.execute(SQL_CREATE_DB_CHANGELOGS_TABLE)
        conn.commit()
        # get last applied changelog
        last_applied_changelog_id = fetch_last_applied_changeset_id(c)
        print("Last applied changelog id: ", last_applied_changelog_id)
        # scan for changelogs
        changelogs = sorted_directory_listing_with_os_listdir("db_changelogs")
        # apply changelogs
        for changelog in changelogs:
            if last_applied_changelog_id is None or last_applied_changelog_id < changelog:
                print("Applying changelog: ", changelog)
                with open("db_changelogs/" + changelog, "r") as file:
                    content = file.read()
                    c.execute("INSERT INTO db_change_logs (name, content) VALUES (?, ?)", (changelog, content))
                    conn.commit()
                    c.executescript(content)
                    conn.commit()
            else:
                print("Changelog already applied: ", changelog)
        print("Changelogs: ", changelogs)
    except Error as e:
        print(e)

def fetch_last_applied_changeset_id(c):
    c.execute(SQL_SELECT_LAST_CHANGELOG)
    row = c.fetchone()
    if row is None:
        last_applied_changelog_id = None
    else:
        last_applied_changelog_id = row[0]
    return last_applied_changelog_id

def sorted_directory_listing_with_os_listdir(directory):
    items = os.listdir(directory)
    sorted_items = sorted(items)
    return sorted_items