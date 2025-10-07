import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='Startup Funding Analysis')
df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')

    #total funding
    total = round(df['amount'].sum())

    # max funding
    max_funding= df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    #average funding
    avg_funding = df.groupby('startup')['amount'].sum().mean()

    #total startup funded
    num_startup = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total', str(total) + 'Cr')
    with col2:
        st.metric('Maximum Funding', str(max_funding) + 'Cr')
    with col3:
        st.metric('Average Funding', str(round(avg_funding)) + 'Cr')
    with col4:
        st.metric('Total Startups Funded',num_startup)
    st.header('Month-On-Month Funding')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df= df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis']= temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x_axis'],temp_df['amount'])
    plt.xticks(ax5.get_xticks()[::3])
    plt.xticks(rotation=90)  # 90 degree vertical

    st.pyplot(fig5)

    st.subheader('Sector Analysis')

    sector_count = df['vertical'].value_counts().head(8)

    sector_sum = df.groupby('vertical')['amount'].sum().head(8)
    col1,col2 = st.columns([1,2])

    with col1:
        st.write("Top Sectors by Count")
        fig6, ax6 = plt.subplots(figsize=(5,5))
        ax6.pie(sector_count, labels=sector_count.index, autopct='%0.1f%%')
        st.pyplot(fig6)
    with col2:
        st.write("Top Sectors by Funding Amount")
        fig7, ax7 = plt.subplots()
        ax7.pie(sector_sum, labels=sector_sum.index, autopct='%0.1f%%')
        st.pyplot(fig7)

    st.subheader('Type of Funding')
    funding_type = df.groupby('round')['amount'].sum().sort_values().head(15)
    col1,col2 = st.columns(2)

    with col1:
        fig8, ax8 = plt.subplots(figsize=(6,4))
        ax8.bar(funding_type.index, funding_type.values)
        ax8.set_ylabel("Total Amount (Cr)")
        plt.xticks(rotation=90)
        st.pyplot(fig8)
    with col2:
        st.subheader('City Wise Funding')
        city_wise = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)

        fig9, ax9 = plt.subplots(figsize=(6,4))
        ax9.bar(city_wise.index, city_wise.values)
        ax9.set_ylabel("Total Amount (Cr)")
        plt.xticks(rotation=90)
        st.pyplot(fig9)

    st.subheader('Top Startups - Year Wise')

    col1,col2 = st.columns(2)
    with col1:
        year = st.selectbox('Select Year', sorted(df['year'].dropna().unique()))
        startup_yearwise = df[df['year'] == year].groupby('startup')['amount'].sum().sort_values(ascending=False).head(
            10)
        fig10, ax10 = plt.subplots(figsize=(6, 4))
        ax10.bar(startup_yearwise.index, startup_yearwise.values)
        ax10.set_ylabel("Total Amount (Cr)")
        plt.xticks(rotation=90)
        st.pyplot(fig10)

    with col2:
        st.subheader('Top Startups - Overall')
        startup_overall = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
        fig11, ax11 = plt.subplots(figsize=(6, 4))
        ax11.bar(startup_overall.index, startup_overall.values)
        ax11.set_ylabel("Total Amount (Cr)")
        plt.xticks(rotation=90)
        st.pyplot(fig11)

    st.subheader('Top Investors')
    top_investors = df.groupby('investors')['amount'].sum().sort_values(ascending=False).head(10)

    fig12, ax12 = plt.subplots(figsize=(6, 4))
    ax12.bar(top_investors.index, top_investors.values)
    ax12.set_ylabel("Total Amount (Cr)")
    plt.xticks(rotation=90)
    st.pyplot(fig12)

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

def load_investor_details(investor):
    st.title(investor)

    st.subheader('Most Recent Investment')
    last5df = df[df['investors'].str.contains(investor, na=False)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.dataframe(last5df)

    col1,col2 = st.columns(2)
    with col1:


        big_series= df[df['investors'].str.contains(investor, na=False)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)

        st.pyplot(fig)

    with col2:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df['vertical'] = df['vertical'].fillna('0')
        vertical_series= df[df['investors'].str.contains(investor, na=False)].groupby('vertical')['amount'].sum()

        vertical_series = df[df['investors'].str.contains(investor, na=False)].groupby('startup')[
            'amount'].sum().sort_values(ascending=False).head()
        st.subheader('Sectors Invested In')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct='%0.01f%%')
        st.pyplot(fig1)

    col1, col2,col3 = st.columns(3)
    with col1:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna('0')

        round_series= df[df['investors'].str.contains(investor, na=False)].groupby('round')['amount'].sum()

        st.subheader('Stages Invested In')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct='%0.01f%%')
        st.pyplot(fig2)

    with col2:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna('0')

        city_series = df[df['investors'].str.contains(investor, na=False)].groupby('city')['amount'].sum()

        st.subheader('City Invested In')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct='%0.01f%%')
        st.pyplot(fig3)

    with col3:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        df['year'] = df['date'].dt.year
        year_series = df[df['investors'].str.contains(investor, na=False)].groupby('year')['amount'].sum()

        st.subheader('Year On Year Investment')
        fig4, ax4 = plt.subplots()
        ax4.plot(year_series.index, year_series.values)

        st.pyplot(fig4)

def load_startup_details(startup):
    startup_data = df[df['startup'] == startup]

    col1,col2 = st.columns(2)
    with col1:
        st.metric('Company Name',startup)

    with col2:
        industry = startup_data['vertical'].iloc[0]
        st.metric('Industry',industry)

    col3, col4 = st.columns(2)
    with col3:
        subindustry = startup_data['subvertical'].iloc[0]
        st.metric('Sub Industry', subindustry)

    with col4:
        city = startup_data['city'].iloc[0]
        st.metric('City', city)

    st.subheader('Funding Rounds')
    start_up = st.selectbox('Select Option',['Stage','Investors','Date'])

    if start_up == 'Stage':
        col5,col6 = st.columns(2)
        with col5:
            stage= startup_data['round'].iloc[0]
            st.metric('Stage', stage)
        with col6:
            st.info('Select a different option to see other details ')
    elif start_up == 'Investors':
        col5,col6 =st.columns(2)
        with col5:
            investor_detail = startup_data['investors'].iloc[0]
            st.metric('Investor Detail', investor_detail)
        with col6:
            st.info('Select a different option to see other details ')
    elif start_up == 'Date':
        col5, col6 = st.columns(2)
        with col5:
            latest_date = startup_data['date'].max()
            latest_date_display = latest_date.strftime('%B %Y') if pd.notnull(latest_date) else 'N/A'
            st.metric('Latest Investment Date', latest_date_display)
        with col6:
            first_date = startup_data['date'].min()
            first_date_display = first_date.strftime('%B %Y') if pd.notnull(first_date) else 'N/A'
            st.metric('First Investment Date', first_date_display)

if option == 'Overall Analysis':
    load_overall_analysis()
elif option == 'Startup':
    st.title('Startup Analysis')
    selected_startup = st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))

    load_startup_details(selected_startup)
else:
    st.title('Investor Analysis')
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
