# MIT License
#
# ColibriSO - a tool for organizing information of all kinds, written in Python and Streamlit.
# Copyright (C) 2022-2024 Andreas Maschke
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def fetch_all_tags(conn):
    sql = ''' SELECT id, creation_time, tag_name from tags order by tag_name'''
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def create_tag(conn, podcast):
    sql = ''' INSERT INTO tags(creation_time, tag_name)
              VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, podcast)
    return cur.lastrowid

def delete_tags(conn, tag_ids):
    conv_ids = [str(i) for i in tag_ids]

    cursor = conn.cursor()

    del_tags_sql = ''' DELETE FROM tags where id in ({ids}) '''.format(
        ids=','.join('?' for _ in conv_ids))
    cursor.execute(del_tags_sql, conv_ids)

def create_document_tag(conn, document_id, tag_id):
    sql = ''' INSERT INTO document_tags(document_id, tag_id)
              VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (int(document_id), int(tag_id)))
    return cur.lastrowid