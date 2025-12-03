import streamlit as st
import json
import requests

# -------------------------
# Load the JSON files
# -------------------------
with open("data/materials_profiles.json") as f:
    materials_profiles = json.load(f)

with open("data/brand_profiles.json") as f:
    brand_profiles = json.load(f)

# -------------------------
# Streamlit Page Setup
# -------------------------
st.set_page_config(page_title="Naked", layout="wide")
st.title("Naked: The Outdoor Gear Brand and Material Advisor")

st.write("Use the selectors below to get material + brand recommendations via **Duke AI Gateway MyGPT Builder**.")

# -------------------------
# Horizontal Button Helpers
# -------------------------
def horizontal_buttons(label, options_with_emojis, key):
    st.write(f"### {label}")
    cols = st.columns(len(options_with_emojis))
    selections = st.session_state.get(key)

    for i, (opt, emoji) in enumerate(options_with_emojis.items()):
        if cols[i].button(f"{emoji} {opt}", key=f"{key}-{i}"):
            st.session_state[key] = opt

    # Display current selection
    if selections:
        st.success(f"Selected: **{selections}**")

# -------------------------
# Category Button Definitions
# -------------------------
activity_options = {
    "hiking": "🥾",
    "mountain trekking": "⛰️",
    "biking": "🚴",
    "action sports": "🏂",
}

weather_options = {
    "hot & sunny": "☀️",
    "cold & precipitation": "❄️🌧️",
    "combination": "🌦️",
}

material_pref_options = {
    "natural fibers": "🌾",
    "synthetic fibers": "🧪",
    "combination": "🔀",
}

sustainability_options = {
    "very sustainable": "🌍",
    "somewhat sustainable": "♻️",
    "doesn't matter": "🤷",
}

# -------------------------
# Render Buttons
# -------------------------
horizontal_buttons("Activity Type", activity_options, "activity")
horizontal_buttons("Weather", weather_options, "weather")
horizontal_buttons("Material Preference", material_pref_options, "material_pref")
horizontal_buttons("Sustainability", sustainability_options, "sustainability")

st.write("---")

# -------------------------
# Validate & Submit
# -------------------------
all_selected = all(
    st.session_state.get(k) 
    for k in ["activity", "weather", "material_pref", "sustainability"]
)

if not all_selected:
    st.warning("Please make a selection in all four categories above.")
else:
    if st.button("🔍 Get Recommendations"):
        # Prepare payload for Duke AI Gateway MyGPT Builder
        payload = {
            "activity": st.session_state["activity"],
            "weather": st.session_state["weather"],
            "material_preference": st.session_state["material_pref"],
            "sustainability": st.session_state["sustainability"],
        }

        st.write("### 🔄 Querying Duke AI Gateway...")
        st.json(payload)

        # -------------------------
        # CALL YOUR DUKE GPT BUILDER ENDPOINT
        # -------------------------
        # Replace with your MyGPT Builder endpoint
        API_URL = "YOUR_DUKE_GATEWAY_ENDPOINT_HERE"

        try:
            response = requests.post(API_URL, json=payload)
            result = response.json()
        except Exception as e:
            st.error(f"Error contacting Duke Gateway: {e}")
            st.stop()

        # -------------------------
        # Display Results
        # -------------------------
        st.write("## 🎯 Suggested Brand & Materials")

        if "brand" in result:
            st.subheader(f"🏷️ Brand: **{result['brand']}**")

        if "materials" in result:
            st.write("### Materials Recommended")
            st.json(result["materials"])

        if "eco_scores" in result:
            st.write("### 🌱 Eco Scores")
            st.json(result["eco_scores"])

        if "alternative_materials" in result:
            st.write("### 🔁 Alternative Materials")
            st.json(result["alternative_materials"])
