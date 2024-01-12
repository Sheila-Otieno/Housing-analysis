import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import pydeck as pdk
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
st.set_option('deprecation.showPyplotGlobalUse', False)
import plotly.graph_objs as go
warnings.filterwarnings('ignore')

#import sql connection function to retrieve data
#from sql__connection import *

st.set_page_config(page_title="American Housing Data", page_icon=":house_with_garden:",layout="wide")

st.title(" :chart: Analysis of American houses")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

#result = view_all_data()
#df=pd.DataFrame(result,columns=["Zip Code","Price","Beds","Baths","Living Space","Address",
                                #"City","State","Zip Code Population","Zip Code Density","County",
                                #"Median Household Income","Latitude","Longitude"])

##read csv file
df = pd.read_csv("American_Housing_Data.csv", encoding = "ISO-8859-1")



##sidebar section

st.sidebar.header("Choose your filter: ")
#Filter for the state    
state = st.sidebar.multiselect("Pick the state", df["State"].unique())
if not state:
    df2 = df.copy()
else:
    df2 = df[df["State"].isin(state)]

##Filter for the city
city = st.sidebar.multiselect("Pick the city", df2["City"].unique())
if not city:
    df3 = df2.copy()
else:
    df3 = df2[df2["City"].isin(city)]

# Filter for experience level
address = st.sidebar.multiselect("Pick an address",df3["Address"].unique())

# Filter the data based on State, city, and level

if not state and not city and not address:
    filtered_df = df
elif not city and not address:
    filtered_df = df[df["State"].isin(state)]
elif not state and not address:
    filtered_df = df[df["City"].isin(city)]
elif state and city:
    filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
elif state and address:
    filtered_df = df3[df["State"].isin(state) & df3["Address"].isin(address)]
elif city and address:
    filtered_df = df3[df["City"].isin(city) & df3["Address"].isin(address)]
elif address:
    filtered_df = df3[df3["Address"].isin(address)]
else:
    filtered_df = df3[df3["State"].isin(state) & df3["City"].isin(city) & df3["Address"].isin(address)]

#create a home page view
def home():
    #view data in table format
    with st.expander("VIEW EXCEL DATASET"):
        showData=st.multiselect('Filter: ',df.columns,default=["Zip Code","Price","Beds","Baths","Living Space","Address",
                                "City","State","Zip Code Population","Zip Code Density","County",
                                "Median Household Income","Latitude","Longitude"])
        st.dataframe(df[showData],use_container_width=True)

    #calculate metrics 
    total_population = float(pd.Series(filtered_df['Zip Code Population']).sum())
    median_income = float(pd.Series(filtered_df['Median Household Income']).median())
    average_density = float(pd.Series(filtered_df['Zip Code Density']).mean())

    ##columns for displaying the metrics
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.info('Total population')
        st.metric(label="Population :man-woman-girl-boy:",value=f"{total_population}")
    with col2:
        st.info('Median Income')
        st.metric(label="Income :dollar:",value=f"{median_income:,.0f}")
    with col3:
        st.info('Average density')
        st.metric(label="Density :man-woman-girl-boy:",value=f"{average_density:,.0f}")
    
    style_metric_cards(background_color="#FFFFFF",border_left_color="#686664",
                       border_color="#000000",box_shadow="#F71938")



def plot_graphs():
    # Create a scatter plot
    data1 = px.scatter(filtered_df, x = "Price", y = "Living Space", size = "Zip Code Population")
    data1['layout'].update(title="Relationship between Price and Living Space.",
                       titlefont = dict(size=20),xaxis = dict(title="Price",titlefont=dict(size=19)),
                       yaxis = dict(title = "Living Space", titlefont = dict(size=19)))
    st.plotly_chart(data1,use_container_width=True)

    population_df = filtered_df.groupby(by = ["City"], as_index = False)[["Zip Code Density"]].sum()
    st.subheader("Density Population of each city")
    fig = px.bar(population_df, x = "City", y = "Zip Code Density", text = ['${:,.2f}'.format(x) for x in population_df["Zip Code Density"]],
            template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

    population_df2 = filtered_df.groupby(by = ["Address"], as_index = False)[["Zip Code Density"]].sum()
    st.subheader("Density Population of each address")
    fig2 = px.bar(population_df2, x = "Address", y = "Zip Code Density", text = ['${:,.2f}'.format(x) for x in population_df2["Zip Code Density"]],
            template = "seaborn")
    st.plotly_chart(fig2,use_container_width=True, height = 200)

def plot_maps():
    st.map(data=filtered_df, latitude="Latitude", 
            longitude="Longitude", color="#0044ff", size="Zip Code Density", zoom=5, use_container_width=True)


def sideBar():
 with st.sidebar:
    selected=option_menu(
        menu_title="Main Menu",
        options=["Home","Map Layout"],
        icons=["house","map"],
        menu_icon="cast",
        default_index=0
    )
 if selected=="Home":
    #st.subheader(f"Page: {selected}")
    home()
    plot_graphs()
 if selected=="Map Layout":
    #st.subheader(f"Page: {selected}")
    plot_maps()

sideBar()
st.sidebar.image("data/house.jpg",caption="")


