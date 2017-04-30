import sqlite3

TABLE_NAME = "reports"
ID = "_id"
LAT_LONG_COLUMN = "lat_long"
PAST_IMG_COLUMN = "past_img"
PRESENT_IMG_COLUMN = "present_img"
FUTURE_IMG_COLUMN = "future"

#
# with sqlite3.connect("sample.db") as connection:
#     c = connection.cursor()
#     c.execute("""DROP TABLE IF EXISTS {} """.format(TABLE_NAME))
#     cursor = c.execute("""CREATE TABLE {} ({} INTEGER PRIMARY KEY autoincrement ,{} TEXT, {} TEXT, {} TEXT, {} TEXT)"""
#                        .format(TABLE_NAME, ID, LAT_LONG_COLUMN, PRESENT_IMG_COLUMN, PAST_IMG_COLUMN, FUTURE_IMG_COLUMN))
#

def insert(future, present, past):
    conn = sqlite3.connect("sample.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO {} ({},{},{}) VALUES (?, ?, ?)".format(TABLE_NAME,
                                                                    FUTURE_IMG_COLUMN,
                                                                    PRESENT_IMG_COLUMN,
                                                                    PAST_IMG_COLUMN), (future, present, past))
    conn.commit()
    conn.close()


def get_data():
    conn = sqlite3.connect("sample.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM {}" .format(TABLE_NAME))
    data = cur.fetchall()
    conn.close()
    return data



if __name__ == '__main__':
    insert("akdf" ,"jaibfk", "aklndbi")
    insert("akdf" ,"jaibfk", "aklndbi")
    insert("akdf", "jaibfk", "aklndbi")
    insert("akdf", "jaibfk", "aklndbi")
    insert("akdf", "jaibfk", "aklndbi")
    insert("akdf", "jaibfk", "aklndbi")
    data = get_data()
    print data


