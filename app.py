import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import streamlit as st
import numpy as np
import pydeck as pdk
import plotly.express as px
cases = st.sidebar.radio("Select the page",('World cases','India cases','COVID-19 and Heath care','Effect on Economy'))

if cases == 'World cases':
    st.title('Welcome👏👏❤💕 ')
    st.title('🦠🦠😷COVID-19 INDICATOR😷🦠🦠')

    #web scrapping
    #now data for the world
    ## quick hack

    from datetime import date, timedelta
    today = date.today()
    yesterday = today - timedelta(days=1)

    d1 = yesterday.strftime("%m-%d-%Y")
    st.subheader('Uptaded on '+ str(today))
    file_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' + d1 + '.csv'
    df = pd.read_csv(file_url)
    data = df[['Confirmed','Lat','Long_','Country_Region','Recovered','Deaths']]
    data.rename( columns={'Lat':'lat','Long_':'lon'},inplace = True)
    data = data.dropna()
    fig = px.scatter_mapbox(data,lat="lat", lon="lon", hover_name="Country_Region", hover_data=["Confirmed",'Recovered','Deaths'],
                        color_discrete_sequence=["firebrick"], zoom=3, height=300)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
    st.subheader('3D view of USA')
    st.write(pdk.Deck(
       map_style="mapbox://styles/mapbox/light-v9",
       initial_view_state={
          "latitude":40.353813,
          "longitude":-88.00000,
          "zoom":11,
          "pitch":50,
       },
       layers=[
          pdk.Layer(
          "HexagonLayer",
          data = data,
          get_position='[lon,lat]',
          radius=10000,
          extruded=True,
          pickable=True,
          elevation_scale=4,
          elevation_range=[20000,200000],
          ),
       ],
           tooltip =   '<li><bold>Country : '+str(data['Country_Region'])+
                        '<li><bold>Province : '+str(data['Recovered'])+
                        '<li><bold>Confirmed : '+str(data['Confirmed'])+
                        '<li><bold>Deaths : '+str(data['Deaths']),

    ))

    df.drop(columns=['FIPS','Admin2','Province_State','Last_Update','Lat','Long_','Combined_Key'],inplace=True)
    all_cases=df.groupby('Country_Region').sum()

    ##calculating mortality rate
    all_cases['Mortality Rate (per 100)'] = np.round(100*all_cases['Deaths']/all_cases['Confirmed'],2)
    ##total confirmed cases in world
    total_confirmed = all_cases['Confirmed'].sum()
    ##total death cases in world
    total_death = all_cases['Deaths'].sum()
    ##total recovered cases in world
    total_recovered = all_cases['Recovered'].sum()
    data = all_cases.nlargest(30,'Confirmed')
    x = data.index
    st.subheader('Enter country you want to know:Confirmed/Recovered/Death cases')
    country = st.text_input('Enter country')
    if country:
        st.subheader('Confirmed')
        st.info(all_cases['Confirmed'][country])
        st.subheader('Recovered')
        st.success(all_cases['Recovered'][country])
        st.subheader('Deaths')
        st.warning(all_cases['Deaths'][country])
    st.subheader('Confirmed/Recovered/Deaths in top 30 countries')
    cases = st.selectbox('select your choice',('Total cases','pie chart','Confirmed cases','Recovered cases','Deaths'))
    if cases == 'Total cases':
        @st.cache
        def total_cases():
            plt.figure(figsize = (20,15))
            plt.barh(x,data['Confirmed'],color = 'pink',label='Confirmed')
            for index, value in enumerate(data['Confirmed']):
                plt.text(value, index, str(value))
            plt.barh(x,data['Recovered'],color = 'orange',label='Recovered')
            plt.barh(x,data['Deaths'],color = 'grey',label='Death')
            plt.legend()

        st.pyplot(total_cases())

    if cases =='pie chart':
        @st.cache
        def pie_chart():
            x = [total_confirmed,total_recovered,total_death]
            labels = ['total_confirmed\n'+str(total_confirmed),'total_recovered\n'+str(total_recovered),'total_death\n'+str(total_death)]
            color = ['pink','green','red']
            explode = [0,0,0]
            plt.pie(x,labels = labels,colors = color,explode = explode)
            central_circle = plt.Circle((0,0), 0.5, color = 'white')
            fig = plt.gcf()
            #Add an Artist to the axes, and return the artist.
            fig.gca().add_artist(central_circle)

        st.pyplot(pie_chart())

    if cases == 'Confirmed cases':
        @st.cache
        def confi():
            plt.figure(figsize = (20,15))
            plt.barh(x,data['Confirmed'],color = 'pink',label='Confirmed')
            for index, value in enumerate(data['Confirmed']):
                plt.text(value, index, str(value))

        st.pyplot(confi())

    if cases == 'Recovered cases':
        @st.cache
        def recases():
            plt.figure(figsize = (20,15))
            plt.scatter(data['Recovered'],x,alpha=0.5,s = 1000,cmap="BuPu",color = 'orange',label='Recovered',edgecolors="grey", linewidth=2)
            for index, value in enumerate(data['Recovered']):
                plt.text(value, index, str(value))
        st.pyplot(recases())

    if cases == 'Deaths':
        @st.cache
        def death():
            plt.figure(figsize = (20,15))
            plt.scatter(data['Deaths'],x,alpha=0.3,s = 1000,cmap="BuPu",color = 'grey',label='Deaths',edgecolors="grey", linewidth=2)
            for index, value in enumerate(data['Deaths']):
                plt.text(value, index, str(value))
        st.pyplot(death())
    ##total confirmed cases in world
    total_confirmed = all_cases['Confirmed'].sum()
    ##total death cases in world
    total_death = all_cases['Deaths'].sum()
    ##total recovered cases in world
    total_recovered = all_cases['Recovered'].sum()
    st.sidebar.subheader('Total cases in world')
    st.sidebar.subheader('Confirmed')
    st.sidebar.info(total_confirmed)
    st.sidebar.subheader('Recovered')
    st.sidebar.success(total_recovered)
    st.sidebar.subheader('Deaths')
    st.sidebar.warning(total_death)
    option = st.selectbox('select country',('Brazil','Spain','Italy','United Kingdom','Australia','France','US','Germany','Russia','Turkey','Iran','China','Canada','India'))

    df_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    df_recovered=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    df_deaths=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

    df_confirmed.drop(columns=['Lat','Long'],inplace=True)
    df_recovered.drop(columns=['Lat','Long'],inplace=True)
    df_deaths.drop(columns=['Lat','Long'],inplace=True)

    # consolidate the data as per the country

    df_confirmed_con = df_confirmed.groupby(by='Country/Region').sum()
    df_recovered_con = df_recovered.groupby(by='Country/Region').sum()
    df_death_con = df_deaths.groupby(by='Country/Region').sum()

    df_confirmed_con = df_confirmed_con.transpose()
    df_recovered_con = df_recovered_con.transpose()
    df_death_con = df_death_con.transpose()

    # melt data and merge confirmed, death and recovered time series into one dataframe

    # add date column to the data frame
    df_confirmed_con['date'] = df_confirmed_con.index
    df_death_con['date'] = df_death_con.index
    df_recovered_con['date'] = df_recovered_con.index

    # melt data and merge confirmed, death and recovered time series into one dataframe

    # add date column to the data frame
    df_confirmed_con['date'] = df_confirmed_con.index
    df_death_con['date'] = df_death_con.index
    df_recovered_con['date'] = df_recovered_con.index

    # convert the data into long form in order to merge the data
    df_confirmed_long = df_confirmed_con.melt(id_vars=['date'],value_name='Confirmed')
    df_death_long = df_death_con.melt(id_vars=['date'],value_name='Death')
    df_recovered_long = df_recovered_con.melt(id_vars=['date'],value_name='Recovered')
    # merge the data
    full_table = df_confirmed_long.merge(right=df_death_long, how='left',
                                     on=['Country/Region', 'date'])

    full_table = full_table.merge(right=df_recovered_long, how='left',
                                     on=['Country/Region', 'date'])
    full_table=full_table[full_table['Country/Region']==option]
    date = pd.to_datetime(full_table['date'])

    def draw(option):
        plt.figure(figsize=(10,5))
        plt.plot(date,full_table['Confirmed'],color='red',linewidth = 8)


    def p1(option):
        country = option
        plt.figure(figsize=(20,15))
        t = df_confirmed_con[country] - df_confirmed_con[country].shift(1)
        df_confirmed_con['date']=pd.to_datetime(df_confirmed_con['date'])
        plt.bar(df_confirmed_con['date'],t,color='pink')
        plt.title('Per day Confirmed cases',fontsize=20)
        plt.ylabel('Confirmed',fontsize=15)
        plt.xlabel('DATE',fontsize=15)
    st.pyplot(draw(option))
    st.success('Per day analysis')
    st.title('Per day Confirmed cases')
    st.pyplot(p1(option))
    st.title('Per day Recovered cases')
    def p2(option):
        country = option
        plt.figure(figsize=(20,15))
        t = df_recovered_con[country] - df_recovered_con[country].shift(1)
        df_recovered_con['date']=pd.to_datetime(df_recovered_con['date'])
        plt.bar(df_recovered_con['date'],t,color='lightgreen')
        plt.title('Per day recovered cases',fontsize=20)
        plt.ylabel('Recovered',fontsize=15)
        plt.xlabel('DATE',fontsize=15)
    st.pyplot(p2(option))
    st.title('Per day Death cases')
    def p3(option):
        country = option
        plt.figure(figsize=(20,15))
        t = df_death_con[country] - df_death_con[country].shift(1)
        df_death_con['date']=pd.to_datetime(df_death_con['date'])
        plt.plot(df_death_con['date'],t,marker='o',markersize=10,linestyle='dashed',color='grey',linewidth=5)
        plt.title('Per day Death cases',fontsize=20)
        plt.ylabel('Death',fontsize=15)
        plt.xlabel('DATE',fontsize=15)
    st.pyplot(p3(option))




    @st.cache
    def world_pie():
        plt.figure(figsize=(13,13))
        x = [total_confirmed,total_recovered,total_death]
        labels = ['total_confirmed\n'+str(total_confirmed),'total_recovered\n'+str(total_recovered),'total_death\n'+str(total_death)]
        color = ['pink','green','red']
        explode = [0,0,0]
        plt.pie(x,labels = labels,colors = color,explode = explode)
        central_circle = plt.Circle((0,0), 0.5, color = 'white')
        fig = plt.gcf()
        #Add an Artist to the axes, and return the artist.
        fig.gca().add_artist(central_circle)

    st.sidebar.pyplot(world_pie())
    st.write(data.style.set_properties(**{'background-color': 'brown',
                            'color': 'gold',
                            'border-color': 'white'}))

if cases == 'India cases':
    url = 'https://www.mohfw.gov.in/'
    web_content = requests.get(url).content
    # parse the html content
    soup = BeautifulSoup(web_content, "html.parser")
    # remove any newlines and extra spaces from left and right
    extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
    stats = [] # initialize stats
    all_rows = soup.find_all('tr') # find all table rows

    for row in all_rows:
        stat = extract_contents(row.find_all('td'))
        # find all data cells
        # notice that the data that we require is now a list of length 5
        if len(stat) == 5:
            stats.append(stat)

    # now convert the data into a pandas dataframe for further processing
    new_cols = ["Sr.No", "States/UT","Confirmed","Recovered","Deceased"]
    state_data = pd.DataFrame(data = stats, columns = new_cols)
    #showing the data
    st.write(state_data.style.set_properties(**{'background-color': 'black',
                            'color': 'lawngreen',
                            'border-color': 'white'}))
    state_data.drop(state_data.tail(2).index,inplace=True)
    state_data['Deceased'][24]=0
    state_data['lat']=[11.7401,15.9129,28.2180,26.244156,25.0961,30.7333,21.295132,20.1809,28.7041,15.2993,22.309425,29.065773,32.084206,33.7782,23.6102,15.317277,10.850516,34.209515,23.473324,19.663280,24.6637,25.4670,23.1645,20.940920,11.9416,31.1471,27.0238,11.1271,18.1124,23.9408,30.0668,26.8467,22.9868]
    state_data['lon']=[92.6586,79.7400,94.7278,92.537842,85.3131,76.7794,81.828232,73.0169,77.1025,74.1240,72.136230,76.040497,77.571167,76.5762,85.2799,75.713890,76.271080,77.615112,77.947998,75.300293,93.9063,91.3662,92.9376,84.803467,79.8083,75.3412,74.2179,78.6569,79.0193,91.9882,79.0193,80.9462,87.8550]
    fig = px.scatter_mapbox(state_data,lat="lat", lon="lon", hover_name="States/UT", hover_data=["Confirmed",'Recovered','Deceased'],
                            color_discrete_sequence=["firebrick"], zoom=3, height=300)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
    state_data['Confirmed'] = state_data['Confirmed'].map(int)
    state_data['Recovered'] = state_data['Recovered'].map(int)
    state_data['Deceased']  = state_data['Deceased'].map(int)
    #plotting



    def bar_graph():
        plt.figure(figsize=(24,18))
        plt.barh(state_data['States/UT'],state_data['Confirmed'] ,color=['red','blue','green','orange','yellow','pink'])
        for index, value in enumerate(state_data['Confirmed']):
            plt.text(value, index, str(value))
        plt.title('State-wise COVID-19 indicator ')
        plt.xlabel('No of Confirmed cases',fontsize=20)
        plt.ylabel('States',fontsize=20)
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=18)

    st.pyplot(bar_graph())


    #pie chart


    def pie_chart():
        plt.figure(figsize=(8,8))
        size = [sum(state_data['Confirmed']),sum(state_data['Recovered']),sum(state_data['Deceased'])]
        labels = ['Confirmed\n'+str(sum(state_data['Confirmed'])),
                'Recovered\n'+str(sum(state_data['Recovered'])),
                'Deceased\n'+str(sum(state_data['Deceased']))]
        colors = ['skyblue','green','orange']
        explode = [0,0,0.2]
        plt.pie(size,labels=labels,colors=colors,explode=explode)
        central_circle = plt.Circle((0,0), 0.5, color = 'white')
        fig = plt.gcf()
        #Add an Artist to the axes, and return the artist.
        fig.gca().add_artist(central_circle)
        plt.title('Nationwide total Confirmed, Recovered and Deceased Cases', fontsize = 16)
    st.pyplot(pie_chart())

    st.sidebar.subheader('Cases in India')
    st.sidebar.subheader('Confirmed')
    st.sidebar.info(str(sum(state_data['Confirmed'])))
    st.sidebar.subheader('Recovered')
    st.sidebar.success(str(sum(state_data['Recovered'])))
    st.sidebar.subheader('Deaths')
    st.sidebar.warning(str(sum(state_data['Deceased'])))

if cases =='COVID-19 and Heath care':
    st.title('COVID-19')
    from PIL import Image
    image = Image.open('C:\\Users\\sahib pratap\\Pictures\\95d3056d580c43bdb53c4f328155a590_18.jpg')
    st.image(image, caption='Coronavirus',
              use_column_width=True)
    st.success("The virus that causes COVID-19 is a coronavirus. Coronaviruses are a large, diverse group of viruses, and you need powerful microscopes to be able to see them. Coronavirus means crown. And as you can see on this slide, the virus looks like it has a crown around it. That's how coronaviruses got their name. There are many different types of coronaviruses, and they infect a wide range of mammals and birds. And some even cause mild respiratory disease in people every year, so coronaviruses are not new." )
    st.header('This is the third coronavirus since 2020')
    st.subheader('🦠Severe Acute Respiratory Syndrome(SARS)')
    st.subheader('🦠Middle East Respiratory Syndrome(MERS)')
    st.subheader('🦠SARS-COV-2')
    st.title('Symtoms')
    st.subheader("👉Fatigue")
    st.subheader("👉Nausea")
    st.subheader("👉Loss of taste or smell")
    st.subheader("👉Muscle ache")
    st.title('Flatening of curve')
    from PIL import Image
    image = Image.open('C:\\Users\\sahib pratap\\Pictures\\flatening the curve.gif')
    st.image(image, caption='Concept of flatening of curve',
              use_column_width=True)
    st.warning("This graph shows a tall, narrow curve and a short, wide curve. Through the graph is a line that shows how many sick people U.S. hospitals can treat. The tall curve goes above the line. That means too many people are sick at one time: We won't have enough hospital beds for all the people who will need treatment. The flatter curve shows what happens if the spread of the virus slows down. The same number of people may get sick, but the infections happen over a longer span of time, so hospitals can treat everyone.")

    def agegp():
        df = pd.read_csv('C:\\Users\\sahib pratap\\Downloads\\AgeGroupDetails.csv')
        df.drop(df.tail(1).index,inplace=True)
        df['Percentage']=df['Percentage'].str.strip('%')
        df['Percentage']=df['Percentage'].map(float)
        plt.figure(figsize=(10,5))
        plt.bar(df['AgeGroup'],df['Percentage'],color='violet')
        plt.title('Agegroup percentage of cases')
        plt.xlabel('Age group')
        plt.ylabel('Percentage')
    st.pyplot(agegp())
    st.subheader('No of beds in each state')
    def beds():
        df = pd.read_csv("C:\\Users\\sahib pratap\\Downloads\\Hospitals_and_Beds_statewise.csv")
        df.drop(df.tail(1).index,inplace=True)
        df['Unnamed: 6']=df['Unnamed: 6'].map(int)
        plt.figure(figsize=(20,15))
        plt.barh(df['Unnamed: 0'],df['Unnamed: 6'],color='green')
        plt.title('No of Beds in Each state')
        plt.ylabel('State')
        plt.xlabel('No of beds')
        for index, value in enumerate(df['Unnamed: 6']):
            plt.text(value, index, str(value))
    st.pyplot(beds())
if cases=='Effect on Economy':
    st.title('Effect on Economy')
    df=pd.read_csv(r'C:\\Users\\sahib pratap\\Downloads\\Book 1.csv')

    def unemp():
        plt.figure(figsize=(10,5))
        plt.bar(df['Month'],df['Unemployment Rate(%)'],color='skyblue')
        plt.title('India Unemployment')
        plt.xlabel('Time')
        plt.ylabel('Unemployment Rate(%)')
    st.title('India Unemployment')
    st.pyplot(unemp())


    web_content = requests.get('https://unemploymentinindia.cmie.com/').text
    # parse the html content
    soup = BeautifulSoup(web_content, "html.parser")
    # remove any newlines and extra spaces from left and right
    extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
    stats = [] # initialize stats
    all_rows = soup.find_all('tr') # find all table rows

    for row in all_rows:
        stat = extract_contents(row.find_all('td')) # find all data cells
        # notice that the data that we require is now a list of length 5
        if len(stat) == 2:
            stats.append(stat)

    #now convert the data into a pandas dataframe for further processing
    st.title('State-wise COVID-19 unemployment in india')
    new_cols = ["States/UT", "Percentage"]
    state_data = pd.DataFrame(data = stats, columns = new_cols)
    state_data.drop(state_data.head(8).index,inplace=True)
    state_data.drop(state_data.tail(8).index,inplace=True)
    state_data['Percentage']=state_data['Percentage'].map(float)
    def state_unemp():
        plt.figure(figsize=(20,15))
        plt.barh(state_data['States/UT'],state_data['Percentage'],color=['red','blue','green','orange','yellow','pink'])
        for index, value in enumerate(state_data['Percentage']):
            plt.text(value, index, str(value))
        plt.title('State-wise COVID-19 unemployment in india')
        plt.xlabel('Percentage',fontsize=20)
        plt.ylabel('States',fontsize=20)
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=18)
    st.pyplot(state_unemp())
    w_unemp=pd.read_csv('C:\\Users\\sahib pratap\\Downloads\\quarantine time\\unemp.csv')
    st.title('World unemployment in 2020')
    def unemp():
        v_men=w_unemp[(w_unemp['SUBJECT']=='MEN') & (w_unemp['TIME']>='2020')][['TIME','Value']]
        v_women=w_unemp[(w_unemp['TIME']>='2020')&(w_unemp['SUBJECT']=='WOMEN')][['TIME','Value']]
        plt.figure(figsize=(10,8))
        plt.bar(v_men['TIME'],v_men['Value'],width= -0.6,align='edge',label='MEN')
        plt.bar(v_women['TIME'],v_women['Value'],width=0.4,label='WOMEN')
        plt.xlabel('Time')
        plt.ylabel('Unemployment Rate(%)')
        plt.title("World unemployment rate of Men and Women")
        plt.legend()

    st.pyplot(unemp())
    st.subheader('Choose the country to see unemployment')
    unemp=pd.read_csv('C:\\Users\\sahib pratap\\Downloads\\quarantine time\\unemp.csv')
    grouped=unemp.groupby('LOCATION')
    option=st.selectbox('select country',('AUS', 'AUT', 'BEL', 'CAN', 'CZE', 'DNK', 'FIN', 'FRA', 'DEU','GRC', 'HUN', 'ISL', 'IRL', 'ITA', 'JPN', 'KOR', 'LUX', 'MEX''NLD', 'NZL', 'NOR', 'POL', 'PRT', 'SVK', 'ESP', 'SWE', 'CHE''TUR', 'GBR', 'USA', 'BRA', 'CHL', 'EST', 'IDN', 'ISR', 'RUS'))
    def wemp():
        aus=grouped.get_group(option)
        y=aus.loc[aus['SUBJECT']=='MEN']['Value']
        ti=aus.loc[aus['SUBJECT']=='MEN']['TIME']
        x=pd.to_datetime(ti)
        plt.scatter(x,y,color='gold')
        plt.xlabel('Time')
        plt.ylabel('Unemployment Rate(%)')
        plt.title('Unemployment')
    st.pyplot(wemp())
    st.title('World GDP')
    def w_gdp():
        w_gdp = pd.read_csv('C:\\Users\\sahib pratap\\Downloads\\world_gdp.csv')
        w_gdp=w_gdp.transpose()
        w_gdp.drop(w_gdp.head(1).index,inplace=True)
        w_gdp.drop(w_gdp.tail(1).index,inplace=True)
        x=pd.to_datetime(w_gdp.index)
        y=w_gdp[0]
        plt.figure(figsize=(20,15))
        plt.plot(x,y,marker='o',markersize=19,linestyle='dashed',color='brown',linewidth=5)
        plt.xlabel('Year')
        plt.ylabel('Percentage%')
        plt.title('World GDP percentage')

    st.pyplot(w_gdp())
#Please note that information from this chat will be used for monitoring and management of the current health crisis and research in the fight against COVID-19.
#Are you experiencing any of the following symtoms?
#Cough
#Fever
#Difficulty in breathing
#None of the Above

#Have you ever had any of the following:
#Diabetes
#Hypertension
#Lung disease
#Heart disease
#None of the following

#Have you travelled anywhere internationally in the last 28-50 days?
#yes  ## NO

#if yes
#check from whats app

#and you can also add this
#Which of the following apply to you?
#Traveled internationally in the last 14 days.
#Recently Interacted or lived or currently live with someone who has tested positive for COVID-19
#Am a healthcare worker
