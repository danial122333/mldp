import streamlit as st
import pandas as pd
import joblib

model = joblib.load('model.pkl')

st.set_page_config(page_title='Car Price Estimator', layout='wide')
st.markdown("<div style='text-align:center;'><h1>Car Price Estimator</h1></div>", unsafe_allow_html=True)
st.markdown(
    """
    <p style="text-align:center; font-size:14px;">
    Estimate a car's price. Adjust the inputs below and click <b>Predict Price</b>.
    </p>
    """, unsafe_allow_html=True
)
st.divider()

make_to_models = {
    'Aston': ['Martin'],
    'Audi': ['R8'],
    'BMW': [],
    'Bentley': [],
    'Dodge': [],
    'Ferrari': ['812'],
    'Ford': [],
    'Lamborghini': ['Aventador'],
    'Land': ['Rover Range Rover', 'Rover Defender'],
    'Maybach': ['Pullman', 'S 650'],
    'McLaren': ['720S'],
    'Mercedes-Benz': ['G 350', 'G 500', 'G 63 AMG', 'SLS'],
    'Porsche': ['991'],
    'Volkswagen': ['T6 California', 'T6 Multivan'],
}
fuel_options = ['Diesel', 'Gasoline']
gear_options = ['Manual', 'Automatic']
offer_options = ["Employee's car", 'Used', 'New', 'Pre-registered']

st.markdown("<h3 style='text-align:center;'>Car specifications</h3>", unsafe_allow_html=True)
form_col_left, form_col_center, form_col_right = st.columns([1, 2, 1])

with form_col_center:
    mileage = st.number_input('Mileage', min_value=0, max_value=900000, value=60000, step=1000)
    hp = st.number_input('Horsepower (hp)', min_value=1, max_value=2000, value=150, step=1)
    year = st.number_input('Year', min_value=1990, max_value=2025, value=2018, step=1)
    make = st.selectbox('Make', sorted(list(make_to_models.keys())))
    models_for_make = make_to_models.get(make, [])
    model_choice = None
    if models_for_make:
        model_choice = st.selectbox('Model', models_for_make)
    fuel = st.selectbox('Fuel Type', fuel_options)
    gear = st.selectbox('Gear / Transmission', gear_options)
    offer_type = st.selectbox('Offer Type', offer_options)

st.divider()

feature_names = [
    'mileage', 'hp', 'year',
    'make_Aston', 'make_Audi', 'make_BMW', 'make_Bentley', 'make_Dodge', 'make_Ferrari', 'make_Ford',
    'make_Lamborghini', 'make_Land', 'make_Maybach', 'make_McLaren', 'make_Mercedes-Benz', 'make_Porsche', 'make_Volkswagen',
    'model_720S', 'model_812', 'model_991', 'model_Aventador', 'model_G 350', 'model_G 500', 'model_G 63 AMG',
    'model_Martin', 'model_Martin Vantage', 'model_Pullman', 'model_Rover Defender', 'model_Rover Range Rover',
    'model_SLS', 'model_T6 California', 'model_T6 Multivan',
    'fuel_Diesel', 'fuel_Gasoline', 'gear_Manual', "offerType_Employee's car", 'offerType_Used'
]
x = pd.Series(0.0, index=feature_names)
x['mileage'] = mileage
x['hp'] = hp
x['year'] = year
make_flag = f'make_{make}'
if make_flag in x.index:
    x[make_flag] = 1
if model_choice:
    name_map = {
        '720S': 'model_720S',
        '812': 'model_812',
        '991': 'model_991',
        'Aventador': 'model_Aventador',
        'G 350': 'model_G 350',
        'G 500': 'model_G 500',
        'G 63 AMG': 'model_G 63 AMG',
        'Martin': 'model_Martin',
        'Martin Vantage': 'model_Martin Vantage',
        'Pullman': 'model_Pullman',
        'Rover Defender': 'model_Rover Defender',
        'Rover Range Rover': 'model_Rover Range Rover',
        'SLS': 'model_SLS',
        'T6 California': 'model_T6 California',
        'T6 Multivan': 'model_T6 Multivan',
    }
    key = name_map.get(model_choice)
    if key and key in x.index:
        x[key] = 1
if f'fuel_{fuel}' in x.index:
    x[f'fuel_{fuel}'] = 1
x['gear_Manual'] = 1 if gear == 'Manual' else 0
if offer_type == "Employee's car":
    x["offerType_Employee's car"] = 1
elif offer_type == 'Used':
    x['offerType_Used'] = 1

left_col, center_col, right_col = st.columns([1, 2, 1])

with center_col:
    st.markdown("<h3 style='text-align:center;'>Prediction</h3>", unsafe_allow_html=True)
    predict_clicked = st.button("Predict Price")

    if predict_clicked:
        price_pred = model.predict([x.values])[0]

        st.markdown(
            f"<div style='text-align:center; font-size:24px; font-weight:bold; margin-top:10px;'>"
            f"Predicted Price : ${price_pred:,.0f}</div>",
            unsafe_allow_html=True
        )

st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("https://bmw.scene7.com/is/image/BMW/g81_cs_promotional-teaser_dsk_fb-1?wid=3840&hei=1280");
        background-size: cover;
        background-attachment: fixed;
        color: #FFFFFF;
    }
    
    .css-1d37f10 {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 20px;
        border-radius: 10px;
    }
    
    div.stButton {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)