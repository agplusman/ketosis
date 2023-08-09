import streamlit as st
import pandas as pd

def calculate_fat_consumption(age, weight_lbs, height_ft, height_in, gender, activity_level_description, calories_burned, hours_05_15, hours_15_30, hours_30_up):
    # Converting weight and height
    weight_kg = weight_lbs * 0.453592
    height_cm = (height_ft * 12 + height_in) * 2.54

    # Calculating BMR
    if gender == "Male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    # Adjusting for activity level
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }
    tdee = bmr * activity_multipliers[activity_level_description]

    # Defining multipliers for ketosis levels
    ketosis_multipliers = [1.1, 1.2, 1.3] # Adjust these values based on how you want to scale the effect of different ketosis levels

    # Calculating total calories burned
    total_calories_burned = ((tdee / 24 * hours_05_15) * ketosis_multipliers[0] +
                            (tdee / 24 * hours_15_30) * ketosis_multipliers[1] +
                            (tdee / 24 * hours_30_up) * ketosis_multipliers[2] +
                            calories_burned)

    # Converting calories to fat in grams
    fat_consumed_grams = total_calories_burned / 9

    # Converting fat consumed to pounds
    fat_consumed_lbs = fat_consumed_grams * 0.00220462

    return bmr, total_calories_burned, fat_consumed_lbs

# Streamlit app interface
st.title("Fat Consumption Calculator during Fasting in Ketosis")
age = st.slider("Age", 18, 99)
weight_lbs = st.slider("Weight (lbs)", 100, 400)
height_ft = st.slider("Height (feet)", 4, 7)
height_in = st.slider("Height (inches)", 0, 11)
gender = st.selectbox("Gender", options=["Male", "Female"])
activity_level = st.selectbox("Activity Level", options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
calories_burned = st.slider("Calories Burned through Exercise", 0, 5000)
hours_05_15 = st.slider("Hours in Ketosis (0.5-1.5 mmol/L)", 0.0, 48.0, step=0.5)
hours_15_30 = st.slider("Hours in Ketosis (1.5-3.0 mmol/L)", 0.0, 48.0, step=0.5)
hours_30_up = st.slider("Hours in Ketosis (>3.0 mmol/L)", 0.0, 48.0, step=0.5)

if st.button("Calculate"):
    bmr, total_calories_burned, result = calculate_fat_consumption(age, weight_lbs, height_ft, height_in, gender, activity_level, calories_burned, hours_05_15, hours_15_30, hours_30_up)
    st.success(f"The estimated fat consumption during your fasting period is approximately {result:.2f} pounds.")
    
    # Creating and displaying a table with key calculations
    df = pd.DataFrame({
        'Metric': ['BMR (Basal Metabolic Rate)', 'Total Calories Burned'],
        'Value': [f"{bmr:.2f} kcal/day", f"{total_calories_burned:.2f} kcal"],
        'Explanation': ['Energy expended at rest to maintain vital functions', 'Total energy burned including BMR and physical activity, adjusted for ketosis levels']
    })
    st.table(df)

st.write("Note: This calculator provides a theoretical estimation and may not fully represent individual variations or the complex physiological processes involved in metabolism. Consulting with a healthcare or nutrition professional can provide more accurate and personalized information.")
