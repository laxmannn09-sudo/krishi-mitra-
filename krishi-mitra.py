import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Agriculture AI", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("Krishi Mitra AI")
    st.subheader("Sign In")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        if username and password:
            st.session_state.logged_in = True
            st.success("Login successful")
        else:
            st.error("Please enter valid credentials")

def overview_page():
    st.title("Overview")
    st.write(
        "Krishi Mitra AI is an integrated decision support platform designed for farmers and rural communities. "
        "It combines artificial intelligence, weather intelligence, market analysis, and expert knowledge to reduce losses, "
        "increase productivity, and support sustainable farming practices."
    )

    st.subheader("Core Capabilities")
    st.write("Crop price prediction using machine learning")
    st.write("Weather based risk alerts using real time data")
    st.write("Instant expert farming advice")
    st.write("Rural marketplace prediction tools")

    st.subheader("Impact")
    st.write(
        "This platform empowers farmers to make informed decisions, avoid exploitation by middlemen, "
        "and adapt to climate and market uncertainties."
    )

def crop_price_page():
    st.header("AI Crop Price Prediction")

    data = {
        "Year": [2018, 2019, 2020, 2021, 2022],
        "Price": [1500, 1600, 1550, 1700, 1800]
    }

    df = pd.DataFrame(data)
    st.dataframe(df)

    X = df[["Year"]]
    y = df["Price"]

    model = LinearRegression()
    model.fit(X, y)

    year_input = st.number_input(
        "Enter future year",
        min_value=2023,
        max_value=2035,
        value=2024
    )

    if st.button("Predict Crop Price"):
        future_year = np.array([[year_input]])
        prediction = model.predict(future_year)[0]

        st.success(f"Estimated crop price for {year_input} is Rupees {prediction:.2f}")

        fig, ax = plt.subplots()
        ax.scatter(df["Year"], df["Price"])
        ax.plot(df["Year"], model.predict(X))
        ax.set_xlabel("Year")
        ax.set_ylabel("Price")
        st.pyplot(fig)

def weather_page():
    st.header("Weather Based Risk Alerts")

    city = st.text_input("Enter City or Village", "Nagpur")
    country = st.text_input("Country Code", "IN")

    API_KEY = "6b087f8cac8135f6afcd5ca13a5eeab4"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric"

    if st.button("Check Weather Risk"):
        try:
            response = requests.get(url)
            data = response.json()

            if data["cod"] != 200:
                st.error("Location not found")
            else:
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                weather = data["weather"][0]["description"]

                st.write(f"Temperature {temp} degree celsius")
                st.write(f"Humidity {humidity} percent")
                st.write(f"Condition {weather}")

                if temp > 35:
                    st.warning("Heat stress risk detected")
                    st.success("Increase irrigation and provide shade")

                if humidity < 30:
                    st.warning("Drought risk detected")
                    st.success("Plan water usage carefully")

                if "rain" in weather.lower():
                    st.warning("Heavy rain risk detected")
                    st.success("Delay irrigation and protect crops")

                if temp <= 35 and humidity >= 30 and "rain" not in weather.lower():
                    st.success("No major weather risk detected")

        except:
            st.error("Weather service unavailable")

def expert_advice_page():
    st.header("AI Expert Farming Advice")

    crop = st.selectbox(
        "Select Crop",
        ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane"]
    )

    problem = st.selectbox(
        "Select Farming Problem",
        [
            "Low Yield",
            "Pest Attack",
            "Leaf Yellowing",
            "Water Stress",
            "Soil Fertility Issue"
        ]
    )

    if st.button("Get Expert Advice"):
        advice = "Follow best agricultural practices"

        if crop == "Rice" and problem == "Low Yield":
            advice = "Use quality seeds and apply nitrogen fertilizer at tillering stage"
        elif crop == "Wheat" and problem == "Pest Attack":
            advice = "Monitor aphids and use integrated pest management"
        elif crop == "Maize" and problem == "Leaf Yellowing":
            advice = "Apply urea immediately"

        st.success(advice)

def marketplace_tools_page():
    st.header("Rural Marketplace Prediction Tools")

    crop_market = st.selectbox(
        "Select Crop",
        ["Rice", "Wheat", "Maize", "Cotton"]
    )

    demand_index = st.slider(
        "Market Demand Level",
        min_value=1,
        max_value=10,
        value=5
    )

    if st.button("Analyze Market"):
        if demand_index >= 7:
            st.success("High demand expected")
            st.write("Recommendation wait and sell later")
        elif demand_index >= 4:
            st.warning("Moderate demand expected")
            st.write("Recommendation sell based on storage")
        else:
            st.error("Low demand expected")
            st.write("Recommendation sell early to avoid losses")

def support_page():
    st.header("Customer Support and Contact")

    st.write("For assistance, training, or feedback please contact us")

    name = st.text_input("Your Name")
    email = st.text_input("Email")
    message = st.text_area("Message")

    if st.button("Submit"):
        if name and email and message:
            st.success("Your message has been received. Our team will contact you")
        else:
            st.error("Please fill all fields")

if not st.session_state.logged_in:
    login_page()
else:
    st.sidebar.title("Navigation")

    page = st.sidebar.radio(
        "Go to",
        [
            "Overview",
            "Crop Price Prediction",
            "Weather Risk Alerts",
            "Expert Farming Advice",
            "Marketplace Tools",
            "Customer Support"
        ]
    )

    if page == "Overview":
        overview_page()
    elif page == "Crop Price Prediction":
        crop_price_page()
    elif page == "Weather Risk Alerts":
        weather_page()
    elif page == "Expert Farming Advice":
        expert_advice_page()
    elif page == "Marketplace Tools":
        marketplace_tools_page()
    elif page == "Customer Support":
        support_page()











