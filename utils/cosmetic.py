from base64 import b64encode
import pandas as pd
import streamlit as st
from streamlit_elements import dashboard, elements, html, mui, nivo
import random as rnd

def page_config():
    st.set_page_config(
    page_title="Extract images from a PDF file",
    page_icon=":file_folder:",  #check emoji on: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
    initial_sidebar_state='expanded'
)
    
def page_navbar():
    with elements("dashboard"):
        layout = [
            # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
            dashboard.Item("first_item", 0, 0, 1, 1, isDraggable=False, isResizable=False, moved=False),
            dashboard.Item("second_item", 1, 0, 3, 1, isDraggable=False, isResizable=False, moved=False),
        ]

        with dashboard.Grid(layout):
            with elements("style_mui_logo"):
                mui.Box(
                    html.img(src="https://hips.hearstapps.com/hmg-prod/images/white-llama-in-argentina-south-america-salta-royalty-free-image-154948449-1532379487.jpg", css={"width": "100%"}),
                    sx={
                        "bgcolor": "background.paper",
                        "boxShadow": 1,
                        "borderRadius": 2,
                        "p": 1,
                        "pt": 3,	
                    }, key="first_item"
                )

            with elements("style_mui_title"):
                mui.Box(
                    html.h1("Extraxt Image from PDF"),
                    html.p("This Streamlit app is to extract images from your PDF files and upload it to IBM Cloud Object Storage, the output is a txt file that contain text and the URL of uploaded images",
                        css={"font-family":"sans-serif", "font-size": "11px"}),
                    sx={
                        "bgcolor": "background.paper",
                        "boxShadow": 1,
                        "borderRadius": 2,
                        "p": 2,
                    }, key="second_item"
                )


def image_thumbnail_grid(imgbin_list, input_list):   
    images_b64 = [b64encode(bytes).decode() for bytes in imgbin_list]
    layout = []
    len_input = len(input_list)
    grid_y = 0

    for i in range(len_input):
        if i % 4 == 0 and i > 0:
            grid_y +=1
        layout.append(dashboard.Item("item_"+str(i), i-(grid_y*4), grid_y, 1, 1))
    
    with elements("img_grids"+str(rnd.randint(0, 1000))):
        with dashboard.Grid(layout):
            for i in range(len_input):
                with elements("mui_img_"+str(i)):
                    mui.Box(
                        html.img(src=f"data:image/png;base64,{images_b64[i]}", css={"width": "100%"}),
                        html.p(f"../{input_list[i][-40:]}", css={"font-family":"sans-serif", "font-size": "11px"}),
                        sx={
                            "bgcolor": "background.paper",
                            "boxShadow": 1,
                            "borderRadius": 2,
                            "p": 1,
                            #"pt": 6,	
                        }, key="item_"+str(i)
                    )


def table_element(df):
    DATA =df.to_dict(orient="records")
    table_field = list(df.keys())
    field_list = []
    for field in table_field:
        col_schema = {}
        col_schema['field'] = field
        col_schema['headerName'] = field
        col_schema['width'] = 175
        field_list.append(col_schema)
    
    if "id" not in table_field:
        field_list.append({"field": 'id', "headerName": 'No', "width": 50, "hide": True})
    DEFAULT_COLUMNS = field_list

    if df.index[0] == 0:
        df.index +=1

    DEFAULT_ROWS = [item.update({'id': i+1}) for i, item in enumerate(DATA)]
    DEFAULT_ROWS = DATA

    with elements("table_serach"+str(rnd.randint(0, 1000))):
        layout = [
            # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
            dashboard.Item("first_item", 0, 0, 4, 4),
        ]
        with dashboard.Grid(layout):
            with elements("mui_table"):
                mui.DataGrid(
                    columns=DEFAULT_COLUMNS,
                    rows = DEFAULT_ROWS,
                    pageSize=6,
                    checkboxSelection=False,
                    key="first_item"
                )