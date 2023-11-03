import streamlit as st
from app.map import *
from app.parameter import specializations, legend_dict_spec_colors

st.set_page_config(layout='wide', page_title="Farmer's Market App", page_icon="🇳🇬") #ng --> nigerian flag

def prepare_map_data():
    global df
    # read users into dataframe
    df = pd.read_feather("./data/user.feather")
    # drop records with invalid coordinates:
    df = df.drop(df[df.lat <= 0].index)
    df = df.drop(df[df.lng <= 0].index)

    return df


st.title("Farmer's Market App")

#set up sidebar
st.sidebar.header("Color Code")

for key, value in legend_dict_spec_colors.items():
    st.sidebar.markdown(f"**{key}:** {value}")

df = prepare_map_data()

spec_filter = st.multiselect(label="Choose one or more specializations", options=specializations, default=specializations)

#filter dataframe
df = df[df['specialization'].isin(spec_filter)]

#draw map
st.pydeck_chart(create_pydeck(df))

#display dataframe
#with st.expander(label='data'):
st.dataframe(df, hide_index=True, width=1000)
