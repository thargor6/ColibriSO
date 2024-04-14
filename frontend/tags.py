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

import streamlit as st
from backend.database import connect_to_colibri_db
from backend.db_tags import fetch_all_tags, delete_tags, create_tag
from datetime import datetime
import streamlit_antd_components as sac
import backend.constants as const
import traceback

def load_view():
    st.title('Tags')
    treeItems = createTreeItems()
    selNodeIdx = sac.tree(items=treeItems, label='tags', index=0, align='left', size='md', open_all=True, checkbox=False, return_index=True)
    print("SEL NODE IDX: ", selNodeIdx)
    """    
    selectedNode = sac.tree(items=[
        sac.TreeItem('item1', tag=[sac.Tag('Tag', color='red'), sac.Tag('Tag2', color='cyan')]),
        sac.TreeItem('item2', icon='folder', description='item description', children=[
            sac.TreeItem('tooltip', icon='github', tooltip='item tooltip'),
            sac.TreeItem('item2-2', children=[
                sac.TreeItem('item2-2-1'),
                sac.TreeItem('item2-2-2'),
                sac.TreeItem('item2-2-3'),
            ]),
        ]),
        sac.TreeItem('disabled', disabled=True),
        sac.TreeItem('item3', children=[
            sac.TreeItem('item3-1'),
            sac.TreeItem('item3-2'),
        ]),
    ], label='tags', index=0, align='left', size='md', icon='table', open_all=True, checkbox=False)
    print("NODES: ", selectedNode)
    """

    st.subheader('Create a new tag')
    tag_name = st.text_input('tag name')
    description = st.text_input('description')
    icon_name = st.selectbox('icon', const.SAC_ICONS, index=None)
    selNodeId = getNodeByIndex(treeItems, selNodeIdx)
    print("PARENT TAG ID: ", selNodeId)

    if st.button('create tag'):
        conn = connect_to_colibri_db()
        try:
            try:
                # creation_time, tag_name, description, icon_name, parent_tag_id
                tag = (datetime.now(), tag_name, description, icon_name, selNodeId)
                tag_id = create_tag(conn, tag)
            except:
                conn.rollback()
                traceback.print_exc()
                raise
            conn.commit()
        finally:
            conn.close()

    conn = connect_to_colibri_db()
    try:
        tag_rows = fetch_all_tags(conn, None)
    finally:
        conn.close()
    if st.button('Refresh'):
        st.write('Refreshing...')
        st.rerun()

    # more about data frames: # https://docs.streamlit.io/library/api-reference/data/st.dataframe
    #tags_df = pd.DataFrame(tag_rows, columns=["Id", "Creation date", "Tag name"])
    #tags_selection = dataframe_with_selections(tags_df)

    col1, col2 = st.columns(2)
    with col2:
        deleteButton = st.button('Delete tags')
        confirmDelete = st.checkbox("Confirm delete")

    """ 
    if deleteButton and confirmDelete:
        if len(tags_selection["Id"].values) > 0:
            with st.spinner('Deleting podcasts ...'):
                conn = connect_to_colibri_db()
                try:
                    delete_tags(conn, tags_selection["Id"].values)
                    conn.commit()
                finally:
                    conn.close()
            st.success("Documents successfully deleted")
            st.rerun()
    """

def fetchTags(conn, parent_node_id):
    # id, creation_time, tag_name, icon_name, description, parent_tag_id
    tag_rows = fetch_all_tags(conn, parent_node_id)
    return [NodeTreeItem(tag[2], icon=tag[3], description = tag[4], children=fetchTags(conn, tag[0]), node_id=int(tag[0])) for tag in tag_rows]


def createTreeItems():
    conn = connect_to_colibri_db()
    try:
        return [NodeTreeItem("", node_id=None)] + fetchTags(conn, None)
    finally:
        conn.close()

def iterateTreeItems(treeItems, startIdx, targetIdx, result):
    refIdx = startIdx
    for item in treeItems:
        if refIdx == targetIdx:
            if hasattr(item, "node_id"):
              result.append(item.node_id)
            else:
              print("NO SHIT: ", item)
              print("TYPE: ", type(item))
              #print("vars: ", vars(item))
              vars("dict", item.__dict__)
              result.append(None)
            return refIdx
        refIdx += 1
        if hasattr(item, 'children') and  item.children is not None and item.children != []:
            refIdx =  iterateTreeItems(item.children, refIdx, targetIdx, result)
    return refIdx

def getNodeByIndex(treeItems, parentNodeIdx):
    result = []
    iterateTreeItems(treeItems, 0, parentNodeIdx, result)
    print("SEARCHED NODE: ", result)

    return result[0] if len(result) > 0 else None


from dataclasses import dataclass

#@dataclass
class NodeTreeItem(sac.TreeItem):
    dummy: int = 42
    node_id: int = None
