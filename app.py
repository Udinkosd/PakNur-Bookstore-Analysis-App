import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import matplotlib.ticker as mtick
import streamlit_lottie as st_lottie
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import urllib.request
import seaborn as sns
import gender_guesser.detector as gender
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import xmltodict
from pandas import json_normalize
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_lottie import st_lottie

st.set_page_config(page_title="PakNur Bookstore Analysis App", layout="wide")

df = pd.read_csv('PakNur Bookstore.csv')
with open('./styles.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.markdown(f"""
    <style>
        .lottie-player {{
            width: 200px;
            height: 200px;
            background: transparent; /* Set the background to transparent */
        }}
    </style>
""", unsafe_allow_html=True)

lottie_book = load_lottieurl("https://lottie.host/eca10532-a730-48fc-92a9-dd60ed932248/EUebA31hXI.json")
st_lottie(lottie_book, speed=1, height=200, key="initial")

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)

def display_introduction():
    if 'BARANG' in df.columns:
        total_books = df['BARANG'].count()
    else:
        total_books = "Data jumlah buku tidak tersedia"

    total_price = None

    if 'HARGA TOTAL' in df.columns:
        if df['HARGA TOTAL'].isnull().any():
            st.write("There are missing values in the 'HARGA TOTAL' column.")
        else:
            total_price = df['HARGA TOTAL'].sum()
            total_price_rp = f"Rp {total_price:,.2f}"
    else:
        st.write("Data harga total tidak tersedia")
        
    if 'PENERBIT' in df.columns:
        top_seller_publisher = df['PENERBIT'].mode()[0]
    else:
        top_seller_publisher = "Data penerbit tidak tersedia"

    col1, col2, col3 = st.columns((1, 1, 1))

    with col1:
        st.markdown(f"""
            <style>
            .box {{
                    background-color: rgba(0, 0, 0, 0.3);
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 10px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100%;
                }}
            .box h3 {{
                    margin-top: 0;
                    font-size: 24px;  /* Set font size for heading */
                }}
            .box p {{
                    font-size: 20px;  /* Set font size for content */
                }}
            </style>
            <div class="box">
                <h3>Jumlah Buku Terdaftar</h3>
                <p><b>{total_books}</b></p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <style>
            .box {{
                    background-color: rgba(0, 0, 0, 0.3);
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 10px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100%;
                }}
            .box h3 {{
                    margin-top: 0;
                    font-size: 24px;  /* Set font size for heading */
                }}
            .box p {{
                    font-size: 20px;  /* Set font size for content */
                }}
            </style>
            <div class="box">
                <h3>Harga total seluruh Buku</h3>
                <p><b>{total_price_rp}</b></p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <style>
            .box {{
                    background-color: rgba(0, 0, 0, 0.3);
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 10px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100%;
                }}
            .box h3 {{
                    margin-top: 0;
                    font-size: 24px;  /* Set font size for heading */
                }}
            .box p {{
                    font-size: 20px;  /* Set font size for content */
                }}
            </style>
            <div class="box">
                <h3>Top seller buku</h3>
                <p><b>{top_seller_publisher}</b></p>
            </div>
        """, unsafe_allow_html=True)

def scatter_plot():
    fig = px.scatter(df, x='HARGA SATUAN', y='PENERBIT')
    st.plotly_chart(fig)

    st.markdown("""
    Dengan visualisasi ini, kita dapat melihat pola hubungan antara 
    harga satuan buku dengan penerbitnya. Jika ada korelasi yang kuat 
    antara harga satuan dengan penerbit, kita akan melihat pola tertentu 
    di mana buku dari penerbit tertentu cenderung memiliki harga satuan 
    tertentu yang lebih tinggi atau lebih rendah daripada penerbit lainnya. 
    Ini bisa memberikan wawasan yang berharga tentang strategi penetapan 
    harga dan preferensi pembelian pelanggan di toko buku Pak Nur.
    """)

def relation_section(relation, selected_columns):
    if relation == "Datasets":
        st.subheader("Dataset")
        if selected_columns:
            filtered_df = df[selected_columns]
            st.dataframe(filtered_df)
        else:
            st.dataframe(df)
    elif relation == "Cluster":
        scatter_plot()

def book_summary():
    st.write("Informasi lengkap tentang dataset:")
    st.write(df.info())
    st.write()

    author_publisher_counts = df.groupby(['PENULIS/PENGARANG', 'PENERBIT']).size()
    st.write("Jumlah buku untuk setiap penulis/pengarang dan penerbit:")
    st.write(author_publisher_counts)
    st.write()

    max_price = df['HARGA SATUAN'].max()
    min_price = df['HARGA SATUAN'].min()
    avg_price = df['HARGA SATUAN'].mean()
    oldest_acquisition_date = df['TANGGAL/BULAN/TAHUN PEROLEHAN'].min()

    max_price_str = '{:,.0f}'.format(max_price)
    min_price_str = '{:,.0f}'.format(min_price)
    avg_price_str = '{:,.0f}'.format(avg_price)

    st.write("Buku dengan harga tertinggi:", max_price_str)
    st.write("Buku dengan harga terendah:", min_price_str)
    st.write("Harga rata-rata buku:", avg_price_str)
    st.write()
    st.write("Tahun perolehan buku tertua:", oldest_acquisition_date)

# def line_chart():
#     # Count the number of books for each publisher
#     publisher_counts = df['PENERBIT'].value_counts()

#     # Create a bar chart
#     fig, ax = plt.subplots()
#     ax.bar(publisher_counts.index, publisher_counts.values)
#     ax.set_xlabel('Publisher')
#     ax.set_ylabel('Number of Books')
#     ax.set_title('Number of Books by Publisher')

#     # Show the plot in Streamlit
#     st.pyplot(fig)

def display_data():
    relation_options = ["Datasets", "Cluster"]
    selected_relation = st.selectbox("Pilih Halaman", relation_options)
    
    if selected_relation == "Datasets":
        selected_columns = st.multiselect("Filter", df.columns)
    else:
        selected_columns = None

    return selected_relation, selected_columns
        
def main():
    st.sidebar.title("Selamat Datang!")

    sections = ["Statistik", "Data"]
    selected_section = st.sidebar.radio("Pilih Halaman", sections)

    st.title("PakNur Bookstore Analysis App")

    if selected_section == "Statistik":
        display_introduction()
        # line_chart()
        # book_summary()
        st.write("You are viewing the Introduction section.")
    elif selected_section == "Data":
        selected_relation, selected_columns = display_data()
        relation_section(selected_relation, selected_columns)
        st.write("You are viewing the Data section.")

if __name__ == "__main__":
    main()