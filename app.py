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

lottie_book = load_lottieurl("https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json")
st_lottie(lottie_book, speed=1, height=200, key="initial")

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)

def display_introduction():
    st.subheader("Apakah ini?")

    st.markdown("""
    Dengan mengidentifikasi kelompok pelanggan yang memiliki perilaku 
    pembelian yang serupa, diharapkan dapat menyusun strategi pemasaran yang lebih 
    terarah dan menyesuaikan stok barang dengan lebih baik, sehingga meningkatkan kinerja 
    bisnis mereka secara keseluruhan.
    """)
    
def display_data():
    relation_options = ["Datasets", "Harga Satuan x Penerbit"]
    selected_relation = st.selectbox("Pilih Relasi", relation_options)

    return selected_relation

def relation_section(relation):
    if relation == "Datasets":
        st.subheader("Dataset")
        st.dataframe(df)
    elif relation == "Harga Satuan x Penerbit":
        fig = px.scatter(df, x='HARGA SATUAN', y='PENERBIT')
        st.plotly_chart(fig)

    st.markdown("""
        ---------------------------------------
        Dalam scatter plot di atas, terlihat bahwa usia 23 tahun adalah yang paling muda, 
        sementara usia 53 tahun adalah yang tertua. Di rentang usia 23 hingga 25 tahun, 
        terdapat 5 responden dengan gaji di bawah 50 ribu USD per tahun. Salah satu dari responden 
        berusia 25 tahun memiliki gaji paling rendah di rentang tersebut, yaitu sebesar 30 ribu USD. 
        Di rentang usia di atas 50 tahun hingga 53 tahun, terdapat 9 responden. 
        Gaji terendah adalah 140 ribu USD dan yang tertinggi adalah 250 ribu USD, 
        dengan salah satu responden berusia 52 tahun.        
        """)

def main():
    st.sidebar.title("Selamat Datang!")

    sections = ["Pengenalan", "Data"]
    selected_section = st.sidebar.radio("Pilih Halaman", sections)

    st.title("PakNur Bookstore Analysis App")

    if selected_section == "Pengenalan":
        display_introduction()
        st.write("You are viewing the Data section.")
    elif selected_section == "Data":
        selected_relation = display_data()
        relation_section(selected_relation)
        st.write("You are viewing the Relation section.")

if __name__ == "__main__":
    main()