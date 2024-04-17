import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import seaborn as sns
import plotly.graph_objects as go
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

df = pd.read_csv("addressthamma.csv", encoding = "UTF-8")

st.set_page_config(page_title="ที่พัก", page_icon=":derelict_house_building:",layout="wide")

#title
st.title(" :derelict_house_building: ที่พัก")
st.markdown('<style>div.block-container{padding-top:1.8rem;}</style>',unsafe_allow_html=True)

colors = ['#483D8B', '#AC87C5', '#DDA0DD', '#D8BFD8', '#9370DB', '#8A2BE2',
          '#9400D3', '#9932CC', '#8B008B', '#800080', '#4B0082', '#6A5ACD',
          '#483D8B', '#8A2BE2', '#9400D3', '#9932CC', '#8B008B', '#800080',
          '#4B0082', '#6A5ACD', '#483D8B', '#8A2BE2', '#9400D3', '#9932CC',
          '#8B008B', '#800080', '#4B0082']

#sidebar
#หอนอก/ใน
st.sidebar.header("Option : ")
address = st.sidebar.multiselect("เลือกประเภทของที่อยู่", df["10. ปัจจุบันนักศึกษาอาศัยอยู่หอพักประเภทใดต่อไปนี้ (หอใน/หอนอก)"].unique(), placeholder="กรุณาเลือกประเภทของที่อยู่") 
if not address:
    df2 = df.copy()
else:
    df2 = df[df["10. ปัจจุบันนักศึกษาอาศัยอยู่หอพักประเภทใดต่อไปนี้ (หอใน/หอนอก)"].isin(address)]
#เพศ
gender = st.sidebar.multiselect("เลือกเพศ", df["2.เพศ"].unique(), placeholder="กรุณาเลือกเพศ")
if not gender:
    df2 = df.copy()
else:
    df2 = df[df["2.เพศ"].isin(gender)]
#คณะ
faculty = st.sidebar.multiselect("เลือกคณะ", df["3.คณะที่ศึกษา"].unique(), placeholder="กรุณาเลือกคณะ")
if not faculty:
    df3 = df2.copy()
else:
    df3 = df2[df2["3.คณะที่ศึกษา"].isin(faculty)]
    

# Filter the data based on Region, State and City

if not address and not gender and not faculty:
    filtered_df = df
elif not gender and not faculty:
    filtered_df = df[df["10. ปัจจุบันนักศึกษาอาศัยอยู่หอพักประเภทใดต่อไปนี้ (หอใน/หอนอก)"].isin(address)]
elif not address and not faculty:
    filtered_df = df[df["2.เพศ"].isin(gender)]
elif gender and faculty:
    filtered_df = df3[df["2.เพศ"].isin(gender) & df3["3.คณะที่ศึกษา"].isin(faculty)]
elif address and faculty:
    filtered_df = df3[df["10. ปัจจุบันนักศึกษาอาศัยอยู่หอพักประเภทใดต่อไปนี้ (หอใน/หอนอก)"].isin(address) & df3["3.คณะที่ศึกษา"].isin(faculty)]
elif address and gender:
    filtered_df = df3[df["10. ปัจจุบันนักศึกษาอาศัยอยู่หอพักประเภทใดต่อไปนี้ (หอใน/หอนอก)"].isin(address) & df3["2.เพศ"].isin(gender)]
elif faculty:
    filtered_df = df3[df3["3.คณะที่ศึกษา"].isin(faculty)]
else:
    filtered_df = df3[df3["10. ปัจจุบันนักศึกษาอาศัยอยู่หอพักประเภทใดต่อไปนี้ (หอใน/หอนอก)"].isin(address) & df3["2.เพศ"].isin(gender) & df3["3.คณะที่ศึกษา"].isin(faculty)]

col1, col2 = st.columns(2)

#คณะ
with col1:
    if 'หอใน' in address:
    # ข้อมูลประชากรของแต่ละคณะ
        x = filtered_df[filtered_df['10. ปัจจุบันนักศึกษาอาศัยอยู่หอพักประเภทใดต่อไปนี้ (หอใน/หอนอก)'] == 'หอใน']

    # สร้าง Pie Chart
        fig = px.pie(x['3.คณะที่ศึกษา'].value_counts().reset_index(name='จำนวน'),values='จำนวน',names='3.คณะที่ศึกษา',)
        fig.update_layout(title_text='คณะที่ศึกษา', title_x=0.5)

    # กำหนดสี
        fig.update_traces(marker=dict(colors=colors))

    # แสดง Pie Chart
        st.plotly_chart(fig,use_container_width=True)

with col2 :
    if 'หอนอก' in address:
    # ข้อมูลประชากรของแต่ละคณะ
        x = filtered_df[filtered_df['10. ปัจจุบันนักศึกษาอาศัยอยู่หอพักประเภทใดต่อไปนี้ (หอใน/หอนอก)'] == 'หอนอก']

    # สร้าง Pie Chart
        fig = px.pie(x['3.คณะที่ศึกษา'].value_counts().reset_index(name='จำนวน'),values='จำนวน',names='3.คณะที่ศึกษา')
        fig.update_layout(title_text='คณะที่ศึกษา', title_x=0.5)

    # กำหนดสี
        fig.update_traces(marker=dict(colors=colors))

    # แสดง Pie Chart
        st.plotly_chart(fig,use_container_width=True)

#ชั้นปี
with col1 :
    year = filtered_df.groupby('4. ปัจจุบันกำลังศึกษาในระดับชั้นใด')
    year = year.size()
    if 'หอใน' in address:
        fig = go.Figure(go.Pie(
        values= year.values,
        labels= year.index,
        texttemplate="%{value} <br>(%{percent})",
        textposition="outside",
        marker_colors=colors
))
        fig.update_layout(
        title_text='ชั้นปีนักศึกษา', title_x=0.5,
        title={'x': 0.5},
        height=500, width=500,
        legend=dict(title="ชั้นปีนักศึกษา")
)
        st.plotly_chart(fig,use_container_width=True)

with col2 :
    year = filtered_df.groupby('4. ปัจจุบันกำลังศึกษาในระดับชั้นใด')
    year = year.size()
    if 'หอนอก' in address:
        fig = go.Figure(go.Pie(
        values= year.values,
        labels= year.index,
        texttemplate="%{value} <br>(%{percent})",
        textposition="outside",
        marker_colors=colors
))
        fig.update_layout(
        title_text='ชั้นปีนักศึกษา', title_x=0.5,
        title={'x': 0.5},
        height=500, width=500,
        legend=dict(title="ชั้นปีนักศึกษา")
)
        st.plotly_chart(fig,use_container_width=True)

#ชื่อที่พัก
with col1 :
    if 'หอใน' in address:
        x = filtered_df[filtered_df['10. ปัจจุบันนักศึกษาอาศัยอยู่หอพักประเภทใดต่อไปนี้ (หอใน/หอนอก)'] == 'หอใน']

    # สร้าง Pie Chart
        fig = px.pie(x['2. รูปแบบของห้องพักที่ผู้สัมภาษณ์อาศัยอยู่ในปัจจุบัน'].value_counts().reset_index(name='จำนวน'),values='จำนวน',names='2. รูปแบบของห้องพักที่ผู้สัมภาษณ์อาศัยอยู่ในปัจจุบัน',)
        fig.update_layout(title_text='ชื่อหอพักที่นักศึกษาอาศัยอยู่ปัจจุบัน', title_x=0.5)

    # กำหนดสี
        fig.update_traces(marker=dict(colors=colors))

    # แสดง Pie Chart
        st.plotly_chart(fig,use_container_width=True)

with col2 :
    if 'หอนอก' in address:
        x = filtered_df[filtered_df['10. ปัจจุบันนักศึกษาอาศัยอยู่หอพักประเภทใดต่อไปนี้ (หอใน/หอนอก)'] == 'หอนอก']

    # สร้าง Pie Chart
        fig = px.pie(x['1. ชื่อหอพักที่นักศึกษาอาศัยอยู่ในปัจจุบัน'].value_counts().reset_index(name='จำนวน'),values='จำนวน',names='1. ชื่อหอพักที่นักศึกษาอาศัยอยู่ในปัจจุบัน',)
        fig.update_layout(title_text='ชื่อหอพักที่นักศึกษาอาศัยอยู่ปัจจุบัน', title_x=0.5)

    # กำหนดสี
        fig.update_traces(marker=dict(colors=colors))

    # แสดง Pie Chart
        st.plotly_chart(fig,use_container_width=True)

#สร้างchartปัจจัยที่มีความสำคัญในการเลือกหอพัก
colors = ['#483D8B', '#AC87C5', '#DDA0DD', '#D8BFD8', '#9370DB']
with col1:
    if 'หอใน' in address:    
        count_location = len(filtered_df[filtered_df['1.ปัจจัยในการเลือกหอพักของนักศึกษา [ทำเลที่ตั้งของหอพักใกล้มหาวิทยาลัย]'] == "มากที่สุด"])
        count_travel_convenience = len(filtered_df[filtered_df['1.ปัจจัยในการเลือกหอพักของนักศึกษา [มีความสะดวกในการเดินทาง]'] == "มากที่สุด"])
        count_reasonable_price = len(filtered_df[filtered_df['1.ปัจจัยในการเลือกหอพักของนักศึกษา [ราคามีความเหมาะสม]'] == "มากที่สุด"])
        count_near_res = len(filtered_df[filtered_df['1.ปัจจัยในการเลือกหอพักของนักศึกษา [มีร้านอาหารใกล้หอพัก]'] == "มากที่สุด"])
        count_environment = len(filtered_df[filtered_df['1.ปัจจัยในการเลือกหอพักของนักศึกษา [สิ่งเเวดล้อม (บรรยากาศรอบที่พัก)]'] == "มากที่สุด"])
        
        fig = go.Figure(go.Bar(
            x=['ทำเลที่ตั้งของหอพักใกล้มหาวิทยาลัย', 'มีความสะดวกในการเดินทาง', 'ราคามีความเหมาะสม', 'มีร้านอาหารใกล้หอพัก', 'บรรยากาศรอบที่พัก'],
            y=[count_location, count_travel_convenience, count_reasonable_price, count_near_res, count_environment],
            text=[f"{count} คน" for count in [count_location, count_travel_convenience, count_reasonable_price, count_near_res, count_environment]],
            textposition='auto',
            marker_color=colors,
        ))

        fig.update_layout(
            title={'text': 'ปัจจัยที่มีความสำคัญในการเลือกหอพัก(หอใน) 5 อันดับแรก', 'x': 0.5},
            xaxis_title='ปัจจัย',
            yaxis_title='จำนวนนักศึกษา',
            height=600, width=600,
        )
        st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    if 'หอนอก' in address:
        count_comfort = len(filtered_df[filtered_df['2.ปัจจัยในการเลือกหอพัก [ความสะดวกสบายของห้องพัก]'] == "มากที่สุด"])
        count_facilities = len(filtered_df[filtered_df['2.ปัจจัยในการเลือกหอพัก [สิ่งอำนวยความสะดวกภายในหอพัก]'] == "มากที่สุด"])
        count_security = len(filtered_df[filtered_df['2.ปัจจัยในการเลือกหอพัก [ความปลอดภัยของหอพัก]'] == "มากที่สุด"])
        count_environments = len(filtered_df[filtered_df['2.ปัจจัยในการเลือกหอพัก [สิ่งเเวดล้อม (บรรยากาศรอบที่พัก)]'] == "มากที่สุด"])
        count_cleanliness = len(filtered_df[filtered_df['2.ปัจจัยในการเลือกหอพัก [ความสะอาดภายในหอพัก และบริเวณโดยรอบหอพัก]'] == "มากที่สุด"])

        fig = go.Figure(go.Bar(
        x=['ความสะดวกสบายของห้องพัก', 'สิ่งอำนวยความสะดวกภายในหอพัก', 'ความปลอดภัยของหอพัก', 'บรรยากาศรอบที่พัก', 'ความสะอาดภายในหอพัก และบริเวณโดยรอบหอพัก'],
        y=[count_comfort, count_facilities, count_security, count_environments, count_cleanliness],
        text=[f"{count} คน" for count in [count_comfort, count_facilities, count_security, count_environments, count_cleanliness]],
        textposition='auto',
        marker_color=colors,
))

        fig.update_layout(
        title={'text': 'ปัจจัยที่มีความสำคัญในการเลือกหอพัก(หอนอก) 5 อันดับแรก', 'x': 0.5},
        xaxis_title='ปัจจัย',
        yaxis_title='จำนวนนักศึกษา',
        height=600, width=600,
)
        st.plotly_chart(fig,use_container_width=True, height = 200)

#รูปแบบการเดินทาง
with col1:
    if 'หอใน' in address:
        x = filtered_df[filtered_df['10. ปัจจุบันนักศึกษาอาศัยอยู่หอพักประเภทใดต่อไปนี้ (หอใน/หอนอก)'] == 'หอใน']

    # สร้าง Pie Chart
        fig = px.bar(x['1. รูปแบบการเดินทางไปมหาวิทยาลัยของนักศึกษา'].value_counts().reset_index(name='จำนวน').head(5),y ='จำนวน', x ='1. รูปแบบการเดินทางไปมหาวิทยาลัยของนักศึกษา',)
        fig.update_traces(marker=dict(color=colors))
        fig.update_layout(title_text='รูปแบบการเดินทางไปมหาวิทยาลัยของนักศึกษาหอใน', title_x=0.5)

    # แสดง Pie Chart
        st.plotly_chart(fig,use_container_width=True)

with col2:
    if 'หอนอก' in address:
        x = filtered_df[filtered_df['10. ปัจจุบันนักศึกษาอาศัยอยู่หอพักประเภทใดต่อไปนี้ (หอใน/หอนอก)'] == 'หอนอก']

    # สร้าง Pie Chart
        fig = px.bar(x['1.1 รูปแบบการเดินทางไปมหาวิทยาลัยของนักศึกษา'].value_counts().reset_index(name='จำนวน').head(5),y ='จำนวน', x ='1.1 รูปแบบการเดินทางไปมหาวิทยาลัยของนักศึกษา',)
        fig.update_traces(marker=dict(color=colors))
        fig.update_layout(title_text='รูปแบบการเดินทางไปมหาวิทยาลัยของนักศึกษาหอนอก', title_x=0.5)

    # แสดง Pie Chart
        st.plotly_chart(fig,use_container_width=True)
