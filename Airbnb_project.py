import streamlit as st
from streamlit_option_menu import option_menu
import pymongo
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import time



st.set_page_config(page_title="Airbnb Analysis",
                   layout='wide',
                   initial_sidebar_state='expanded')

st.title("Airbnb Analysis")

st.markdown("""
    <style>
        .stApp {
            background-image: url("https://wallpaper-mania.com/wp-content/uploads/2018/09/High_resolution_wallpaper_background_ID_77701309896.jpg");
            background-size: cover;
        }
        </style>
        """, unsafe_allow_html=True)

selected = option_menu(None, ['Home', 'Data', 'Explore'],
                       icons=['house-door-fill', 'printer', 'plane'],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "35px", "text-align": "centre", "margin": "0px", "--hover-color": "#6495ED"},
                               "icon": {"font-size": "35px"},
                               "container" : {"max-width": "6000px"},
                               "nav-link-selected": {"background-color": "#6495ED"}})
    

if selected == "Home":
    col1,col2 = st.columns(2,gap= 'medium')
    col1.markdown("##  Domain : <span style='color:cyan;font-weight:bold'>  Travel Industry, Property Management and Tourism </span>", unsafe_allow_html=True)
    col1.markdown("##  Technologies used : <span style='color:cyan;font-weight:bold'>  Python, Pandas, Plotly, Matplotlib, Seaborn, Streamlit, MongoDB </span>", unsafe_allow_html=True)
    col1.markdown("##  Overview : <span style='color:cyan;font-weight:bold'>   To analyze Airbnb data Extracted from MongoDB Atlas, First Preprocess the data using pandas by python scripting. Then Optimise the data for visualisation like geo maps pin pointing the location of the hotels, Price analysis and other creteria using streamlit. To create a dynamic Dashboard using PowerBI to visualise the data. </span>", unsafe_allow_html=True)
    col2.markdown("#   ")
    col2.markdown("#   ")



def connect_to_database():
    connection_string = "mongodb+srv://praks8870:Prakash9.@praksdb.obppr2u.mongodb.net/?retryWrites=true&w=majority"

    client = pymongo.MongoClient(connection_string)
    db = client['sample_airbnb']
    mycol = db['listingsAndReviews']
    return mycol




def data_extract():
    new_data = []
    with st.spinner("Please wait, The data is being extracted....."):
        time.sleep(2)
        mycol = connect_to_database()
        for i in mycol.find():
            data = dict(id = i['_id'],
                        listing_url = i['listing_url'],
                        name = i.get('name'),
                        description = i['description'],
                        house_rules = i['house_rules'],
                        property_type = i['property_type'],
                        room_type = i['room_type'],
                        bed_type =i['bed_type'],
                        min_nights = i['minimum_nights'],
                        max_nights = i['maximum_nights'],
                        cancellation = i['cancellation_policy'],
                        last_scraped = i['last_scraped'],
                        last_review = i.get('last_review'),
                        accomodates = i['accommodates'],
                        bedrooms = i.get('bedrooms'),
                        beds = i.get('beds'),
                        review_count = i['number_of_reviews'],
                        bathrooms  = i.get('bathrooms'),
                        amenities = ', '.join(i['amenities']),
                        security_deposit = i.get('security_deposit'),
                        cleaning_fee = i.get('cleaning_fee'),
                        extra_people = i['extra_people'],
                        guests = i['guests_included'],
                        image = i['images']['picture_url'],
                        host = i['host']['host_id'],
                        host_name = i['host']['host_name'],
                        host_response_rate = i['host'].get('host_response_rate'),
                        listings = i['host']['host_total_listings_count'],
                        street = i['address']['street'],
                        country = i['address']['country'],
                        country_code = i['address']['country_code'],
                        location_type = i['address']['location']['type'],
                        longitude = i['address']['location']['coordinates'][0],
                        latitude = i['address']['location']['coordinates'][1],
                        location_exact = i['address']['location']['is_location_exact'],
                        availability_30 = i['availability']['availability_30'],
                        availability_60 = i['availability']['availability_60'],
                        availability_90 = i['availability']['availability_90'],
                        availability_365 = i['availability']['availability_365'],
                        review_rating_score = i['review_scores'].get('review_scores_rating'),
                        price = i['price']
                        )
            
            new_data.append(data)

        df = pd.DataFrame(new_data)
        df.to_csv("D:\\airbnb_project\\airbnb2.csv")
        
        


def prepocess_data():
    data = pd.read_csv("D:\\airbnb_project\\airbnb2.csv")
    df = pd.DataFrame(data)

    df.security_deposit = df.security_deposit[~df.security_deposit.isna()].astype(str).astype(float)
    df.min_nights = df.min_nights.astype(str).astype(float)
    df.max_nights = df.max_nights.astype(str).astype(float)
    df.price = df.price.astype(str).astype(float)
    df.cleaning_fee = df.cleaning_fee[~df.cleaning_fee.isna()].astype(str).astype(float)
    df.extra_people = df.extra_people.astype(str).astype(float)
    df.guests = df.guests.astype(str).astype(float)

    df.bedrooms.fillna(df.bedrooms.mode()[0], inplace = True)
    df.beds.fillna(df.beds.median(), inplace= True)
    df.security_deposit.fillna(df.security_deposit.median(), inplace= True)
    df.min_nights.fillna(df.min_nights.median(), inplace= True)
    df.cleaning_fee.fillna(df.cleaning_fee.median(), inplace= True)
    df.host_response_rate.fillna(df.host_response_rate.median(), inplace= True)
    df.review_rating_score.fillna(df.review_rating_score.median(), inplace= True)
    df.bathrooms.fillna('', inplace= True)
    df.last_review.fillna(0, inplace= True)
    df.last_review.replace(to_replace= 0, value = 'No Reviews', inplace= True)
    df.description.replace(to_replace= '', value = 'No description provided', inplace= True)
    df.house_rules.replace(to_replace= '', value= 'No details', inplace= True)
    df['location_exact'] = df['location_exact'].replace({True: 'yes', False: 'no'})
    df['max_nights'] = df.max_nights.astype(float).astype(int)
    
    return df



def show_data(df):
    
    n_cols = df.select_dtypes(include= ['int64', 'float64']).columns
    n_cols = n_cols[n_cols != 'price']

    num_cols = len(n_cols)
    num_rows = (num_cols // 3) + (num_cols % 3 > 0)

    fig, axes = plt.subplots(nrows = num_rows, ncols = 3, figsize =  (15, num_rows * 5))

    axes = axes.flatten()

    for i, col in enumerate(n_cols):
        axes[i].scatter(df[col], df['price'], alpha=0.5)
        axes[i].set_xlabel(col)
        axes[i].set_ylabel('price')


    plt.tight_layout()

    st.pyplot(fig)


def Optimise_the_data():
    from scipy import stats

    df = prepocess_data()

    z_scores = stats.zscore(df['price'])

    threshold = 3

    outliers = df[abs(z_scores) > threshold]
    df1 = df[abs(z_scores) <= threshold]

    return df1



if selected == 'Data':
    if st.button("Coneect To DataBase"):
        connect_to_database()
        st.success("The connection to your DataBase made Successfully")
        st.balloons()

    if st.button("Extract And Preprocess Data"):
        data_extract()
        prepocess_data()
        st.success("The Data is ready to be used now")
        st.balloons()

    if st.button("Examine the Data"):
        df = prepocess_data()
        st.title("Sample Data from the data extracted from the DataBase")
        st.write(df.head())
        st.title("Scatter Plot of Price vs Other Data")
        show_data(df)
        st.balloons()

    if st.button("Optimse The Data"):
        df2 = Optimise_the_data()
        st.title("Scatter Plt of Price vs Other Data")
        show_data(df2)
        st.balloons()


if selected == "Explore":
    df2 = Optimise_the_data()

    df_host = df2.sort_values(by='listings', ascending=False)

    df_host = df_host[['host', 'host_name', 'listings']].drop_duplicates().head(10)

    fig = px.bar(df_host,
                    x='host_name',
                    y= 'listings',
                    labels={'y': 'Number of Listings'},
                    title='Top 10 Hosts by the Number of Listings',
                    color = 'host_name',
                    category_orders={"listings": df_host['listings'].tolist()},
             )
    # fig.update_layout(xaxis=dict(tickangle=45))
    
    st.plotly_chart(fig, use_container_width= True)


    col1, col2 = st.columns(2, gap = 'medium')

    with col1:
        df_prop = df2['property_type'].value_counts().head(10).reset_index()
        df_prop.columns = ['property_type', 'count']
        fig = px.pie(df_prop,
                names='property_type',
                values='count',
                title="Top 10 Property Types",
                color_discrete_sequence=px.colors.sequential.Rainbow
                )

        fig.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_prop = df2['room_type'].value_counts().head(10).reset_index()
        df_prop.columns = ['room_type', 'count']
        fig = px.pie(df_prop,
                names='room_type',
                values='count',
                title="Pie Chart Of Room Types",
                color_discrete_sequence=px.colors.sequential.Rainbow
                )

        fig.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    c1, c2= st.columns(2, gap = 'medium')

    with c1:
        fig = px.scatter_geo(df2,
                            locations='country',
                            color= 'price', 
                            hover_data=['price'],
                            locationmode='country names',
                            size='price',
                            title= 'Avg Price in each Country',
                            color_continuous_scale='agsunset'
                                )
        st.plotly_chart(fig,use_container_width=True)


    with c2:

        fig = px.scatter_geo(df2,
                        lat='latitude',
                        lon='longitude',
                        color='availability_365',
                        hover_data=['availability_365'],
                        size='availability_365',
                        title='Avg Availability at each Location',
                        color_continuous_scale='agsunset',
                        projection='natural earth'
                        )

        st.plotly_chart(fig, use_container_width=True)
            
        df2['custom_text'] = '📍'



    fig = px.scatter_geo(df2,
                    lat='latitude',
                    lon='longitude',
                    text='custom_text',
                    custom_data=['name', 'property_type', 'price'],
                    title='Location Pins',
                    projection='natural earth',
                    )
    fig.update_geos(showcountries=True, countrycolor="lightgray", showcoastlines=True, coastlinecolor="darkgray")

    fig.update_traces(
        hovertemplate='Property Type: %{customdata[1]}<br>Name: %{customdata[0]}<br>Price: %{customdata[2]}'
    )

    st.plotly_chart(fig, use_container_width=True)


