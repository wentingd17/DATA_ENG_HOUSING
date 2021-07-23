import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px
import altair as alt
import seaborn as sns

with open('df_final_all.pickle', 'rb') as read_file:
    df_final = pickle.load(read_file)
with open('map_data.pickle', 'rb') as read_file:
    map_data = pickle.load(read_file)
with open('sold_by_neig.pickle', 'rb') as read_file:
    sold_by_neig = pickle.load(read_file)
with open('sold_by_type.pickle', 'rb') as read_file:
    sold_by_type = pickle.load(read_file)



city = df_final['city'].unique()
city_choice = st.sidebar.selectbox('Select city:',city)
zipcode_input = st.sidebar.text_input('Zip','')
address_input = st.sidebar.text_input('Address','')
type = df_final['type'].unique()
type_input = st.sidebar.selectbox('Property Type',type)

features_return = ['address_sold', 'sold_date','price_sold','list_price_y',
                   'lot_sqft_sold', 'sqft_sold','bath_sold', 'beds_sold',
                   'year_built_sold','location.address.city_y']

output = df_final[(df_final['city'] == city_choice)&
                  (df_final['postal_code'] == zipcode_input)&
                  (df_final['address'] == address_input)&
                  (df_final['type'] == type_input)][features_return]

output.rename(columns = {'sold_date':'Sold Date',
                         'price_sold':'Sold Price',
                         'list_price_y':'List Price',
                         'lot_sqft_sold':'Lot SQFT',
                         'sqft_sold':'Property SQFT',
                         'bath_sold':'Number Of Bathrooms',
                         'beds_sold':'Number Of Bedrooms',
                         'year_built_sold':'Year Built',
                         'location.address.city_y':'City'},inplace = True)
#Format
output['Lot SQFT'] = output['Lot SQFT'].fillna(0)
output['Property SQFT'] = output['Property SQFT'].fillna(0)
output['Number Of Bathrooms'] = output['Number Of Bathrooms'].fillna(0)
output['Sold Price'] = output['Sold Price'].astype(float)
#output['Number Of Bedrooms'] = output['Number Of Bedrooms'].fillna(0)
features_search = ['address','list_date','list_price','lot_sqft','sqft','baths','beds',
                   'year_built','pred_price']

search = df_final[(df_final['city'] == city_choice)&
                  (df_final['postal_code'] == zipcode_input)&
                  (df_final['address'] == address_input)&
                  (df_final['type'] == type_input)][features_search]
search = search.drop_duplicates()
search.rename(columns = {'list_date':'List Date',
                         'list_price':'List Price',
                         'lot_sqft':'Lot SQFT',
                         'sqft':'Property SQFT',
                         'baths':'Number Of Bathrooms',
                         'beds':'Number Of Bedrooms',
                         'year_built':'Year Built',
                         'pred_price': 'Est Sold to Ask Ratio'},inplace = True)
search['Lot SQFT'] = search['Lot SQFT'].fillna(0)


search.set_index('address', inplace = True)
output.set_index('address_sold', inplace = True)

#Charts
#Map Chart
map_data.rename(columns = {'median_sold_price_by_city': 'Median Price'}, inplace = True)
map_data['info'] = map_data['address'] + ', ' + map_data['zipcode'].astype(str)
secret_token='pk.eyJ1IjoiY3VyZWxsYTE3IiwiYSI6ImNrcmNoc2VhbzAxaW4ycGxqaDNiendkNTkifQ.z29OPCgvUZnrmVk-moTcFg'
px.set_mapbox_access_token(secret_token)
fig = px.scatter_mapbox(map_data, lat="lat", lon="lon", text = 'city', color = 'Median Price',
                        color_continuous_scale = 'oryel', hover_name = 'info',
                   size_max=15, zoom=5)

fig.update_layout(
    title = "Properties Sold in Last 8 Months",
    legend_title = 'Median Sold Price',
    width = 800,
    height = 500,
    margin=dict(l=1, r=40, b=40, t=40)

)

#Bar Chart

line_data = sold_by_neig[sold_by_neig['zipcode'] == zipcode_input]
line_data.rename(columns = {'sold_month': 'Sold Month'}, inplace = True)
chart = (
    alt.Chart(line_data)
    .mark_bar()
    .encode(x=alt.X('city:N', axis=None), y="sold:Q", color="city:N", column="Sold Month").properties(
    title = 'Sold by Month',
    width =90
    )
)


line_data_ptype = sold_by_type[sold_by_type['zipcode'] == zipcode_input]
line_data_ptype.rename(columns = {'sold_month': 'Sold Month',
                                   'property_type': 'property type'}, inplace = True)
chart2= (
    alt.Chart(line_data_ptype)
    .mark_bar()
    .encode(x=alt.X('property type:N', axis=None), y="sold:Q", color="property type:N", column="Sold Month").properties(
    title = 'Sold by Property Type',
    width =90
    )
)

st.header("Real Estate Competitive Analysis Dashboard")
st.plotly_chart(fig)
st.write(search)
st.markdown("### Recent Sold Nearby")
st.write(output)
col1, col2 = st.beta_columns(2)
with col1:
    st.write(chart)
with col2:
    st.write(chart2)
