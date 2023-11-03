import pandas as pd
import pydeck as pdk
from app.parameter import color_map

def create_pydeck(df: pd.DataFrame):

    #print(df.head())
    view_state = pdk.ViewState(latitude=9.0242468, longitude=7.367466, zoom=5)

    #layer_2d_farms = pdk.Layer(
    #    type='ScatterplotLayer',
    #    data=df[['userName', 'specialization','lat','lng']],
    #    get_position='[lng, lat]',
    #    get_radius=700,
    #    get_fill_color='[217, 48, 76]',
    #    auto_highlight=True,
    #    pickable=True
    #)

    layer_tomatoes = create_layer_for_specialization(df, 'Tomatoes', color='red')
    layer_fish = create_layer_for_specialization(df, 'Fish', color='blue')
    layer_other_crops = create_layer_for_specialization(df, spec='Other Crops', color='green')
    layer_corn = create_layer_for_specialization(df, spec='Corn', color='yellow')
    layer_pigs = create_layer_for_specialization(df, spec='Pig', color='pink')
    layer_poultry = create_layer_for_specialization(df, spec='Poultry', color='light_orange')
    layer_cocoa = create_layer_for_specialization(df, spec='Cocoa', color='dark_brown')
    layer_cassava = create_layer_for_specialization(df, spec='Cassava', color='brown')
    layer_other_livestock = create_layer_for_specialization(df, spec='Other Livestock', color='violet')


    r = pdk.Deck(map_style='light', initial_view_state=view_state,
                 layers=[layer_tomatoes, layer_fish, layer_other_crops, layer_corn, layer_cassava, layer_cocoa,
                         layer_poultry, layer_pigs, layer_other_livestock]
                 )

    return r

def create_layer_for_specialization(df: pd.DataFrame, spec: str= 'Tomatoes', color='red'):

    df = df[df['specialization'] == spec]

    layer = pdk.Layer(
        type='ScatterplotLayer',
        data=df[['userName', 'specialization', 'lat', 'lng']],
        get_position='[lng, lat]',
        get_radius=5000,
        get_fill_color=color_map.get(color),
        auto_highlight=True,
        pickable=True
    )
    return layer


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df = pd.read_feather("../data/user.feather")

    # drop records with invalid coordinates:
    df = df.drop(df[df.lat <= 0].index)
    df = df.drop(df[df.lng <= 0].index)

    r = create_pydeck(df)
    r.to_html('map_demo.html', notebook_display=False)