import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta, datetime
from streamlit_option_menu import option_menu

    
# Set page config
st.set_page_config(page_title="Service Type Based Network Slice Optimization", layout="wide")
st.sidebar.title("Service Type Based Network Slice Optimization")

st.logo(image="images/5Glogo.jpg", 
        icon_image="images/5Glogo.jpg")

# Define custom CSS for table styling
table_style = """
<style>
    table {
        width: 100%;
        border-collapse: collapse;
        font-family: Arial, sans-serif;
        font-size: 16px;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
    }
        th {
        background-color: #000000;
        color: white;
    }
    tr:hover {
        background-color: #ddd;
    }
    .bottom-subheader {
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-top: 15px;
    }
</style>
"""

with st.sidebar:
    main_menu = option_menu(
        "",
        ["Deployment Config","Service Type CellWise", "Trends"],
        icons=["house","bar-chart","gear"], 
        menu_icon="cast",
        default_index=0
    )

if main_menu == "Deployment Config":
    # Sample data
    st.title("Deployment Network Slice Config")
    data = {
        'Slice ID': ['001','002','003','004','005'],
        'Service': ['UHD Streaming', 'AR/VR','e-health','Smart City/Grid', 'Connected Cars'],
        'Slice Type': ['eMBB', 'eMBB', 'URLLC','mMTC','URLLC'],
        'Latency(ms)':['<20','<10','<1','<100','<5'],
        'Bandwidth':['200Mbps','300Mbps','100Mbps','5Mbps','200Mbps'],
        'Concurrent Users':[10000,2000,500,20000,10000]
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    
    # Convert DataFrame to HTML without index
    table_html = df.to_html(index=False)

    # Render the HTML table in Streamlit
    bottom_subheader = '<div class="bottom-subheader">High Capacity Urban Network Deployment</div>'
    st.markdown(table_style + table_html+bottom_subheader, unsafe_allow_html=True)

    # Title
    #st.title("Simple Table Display in Streamlit")

    # Display table using st.table (static table)
    #st.subheader("Static Table:")
    #st.table(df_reset)



if main_menu == "Service Type CellWise":
    data = pd.read_csv("ServiceType.csv")
    #data['DATE'] = pd.to_datetime(data['DATE'])

    sub_menu = st.sidebar.selectbox(
        "Select Cell",
        ["All","CellID-1","CellID-2","CellID-3"]
    )

    sub_menu1 = st.sidebar.selectbox(
        "Select chart type",
        ["Pie","Bar"]
    )

    a, b, c = st.columns(3)
    a.metric("Total Services", data['Number of Users in (in thousands)'].sum(), border=True)
    b.metric("Total Cells", 4, border=True)
    with c:
        #Display CellID<-> Total Service Type Data
        # Sample data
        data10 = {
            "CellID": ["Cell_001", "Cell_002", "Cell_003"],
            "Total Services": [120, 95, 150]
        }

        # Create DataFrame
        df4 = pd.DataFrame(data10)

        # Display dataframe with progress bar on 'Total Services'
        st.dataframe(
            df4,
            hide_index=True,
            column_config={
                "Total Services": st.column_config.ProgressColumn(
                    "Total Services",
                    help="Number of services running on the cell",
                   format="%d",
                    min_value=0,
                    max_value=200,  # You can adjust this based on your expected range
                )
            },
            use_container_width=True,
        )


    cols = st.columns(1)
    with cols[0]:
        with st.container(border=True):
            if sub_menu1 == "Bar":
                st.bar_chart(data,x="Service Type", y="Number of Users in (in thousands)",color="#29b5e8", horizontal=True)

            if sub_menu1 == "Pie":
                # Plot pie chart
                #fig = px.pie(data, names='Service Type', values='Number of Users in (in thousands)', title='Service Types')
                st.write("Service type distribution for all Cells")
                # Create pie chart with Labels Inside 
                fig = go.Figure(data=[go.Pie(
                    labels=data['Service Type'],
                    values=data['Number of Users in (in thousands)'],
                    textinfo='label+percent',
                    textposition='inside',  # Places labels inside slices
                    insidetextorientation='radial'  # Optional: makes text follow the pie slice direction
                )])

                # Display in Streamlit
                st.plotly_chart(fig)

    

if main_menu == "Trends":
    st.title("Trends")
    st.sidebar.markdown("")
    sub_menu2 = st.sidebar.selectbox(
        "Select time frame",
        ["Today","Last Week"]
    )

    cols = st.columns(1)
    with cols[0]:
        with st.container(border=True):
            if sub_menu2 == "Today":
                #st.image("images\Today.png")
                df = pd.read_csv("Trends.csv")
                df_melted = df.melt(id_vars='Time', var_name='Service', value_name='Value')
                # Plot using Plotly Express
                fig1 = px.line(
                    df_melted,
                    x='Time',
                    y='Value',
                    color='Service',
                    labels={'Time':'Time of day (HH:MM)', 'Value':'No. of Users (in thousands)','Service':''},
                    title=""
                )

                fig1.update_layout(
                    yaxis=dict(
                        range=[0,200],
                        dtick=25,
                        title='No. of Users (in thousands)'
                    ),
                    xaxis_title='Time of day (HH:MM)'

                )
                st.plotly_chart(fig1, use_container_width=True)

            if sub_menu2 == "Last Week":
                st.image("images\weekend.png")

