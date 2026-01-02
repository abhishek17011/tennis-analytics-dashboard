import os

if not os.path.exists("tennis.db"):
    import db_setup
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Tennis Analytics Advanced", layout="wide")

st.markdown("## 🎾 Tennis Analytics – Advanced Interactive Dashboard")

conn = sqlite3.connect("tennis.db")
df = pd.read_sql("SELECT * FROM Rankings", conn)

st.sidebar.header("🎛 Filters")
year = st.sidebar.selectbox("Year", sorted(df['year'].unique()))
gender = st.sidebar.multiselect("Gender", df['gender'].unique(), default=list(df['gender'].unique()))
week = st.sidebar.slider("Week Range", int(df['week'].min()), int(df['week'].max()), (1,10))
stage = st.sidebar.multiselect("Rank Stage", df['stage'].unique(), default=list(df['stage'].unique()))

filtered = df[
    (df['year'] == year) &
    (df['gender'].isin(gender)) &
    (df['week'].between(week[0], week[1])) &
    (df['stage'].isin(stage))
]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Players", filtered['name'].nunique())
c2.metric("Countries", filtered['country'].nunique())
c3.metric("Avg Points", int(filtered['points'].mean()))
c4.metric("Top Rank", int(filtered['rank'].min()))

st.markdown("### 📊 Average Points by Player")
st.bar_chart(filtered.groupby("name")["points"].mean())

st.markdown("### 🌍 Players by Country")
st.bar_chart(filtered['country'].value_counts())

st.markdown("### 🏆 Rankings Table")
st.dataframe(filtered.sort_values("rank"))

st.markdown("### 📈 Weekly Points Trend")
st.line_chart(filtered.groupby("week")["points"].mean())

conn.close()
