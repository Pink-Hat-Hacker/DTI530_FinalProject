import streamlit as st
import json
import plotly.graph_objects as go
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

# ----------------------------
# Page Setup
# ----------------------------
st.set_page_config(page_title="Naked", layout="wide")
st.title("Naked: Outdoor Brand Suggestion Dashboard")

# ----------------------------
# LOAD KNOWLEDGE FILES
# ----------------------------
with open("data/brand_profiles.json", "r") as f:
    brand_data = json.load(f)
with open("data/materials_profiles.json", "r") as f:
    material_data = json.load(f)

# ----------------------------
# UI Input Categories
# ----------------------------
activity_options = ["Hiking", "Backpacking", "Trail Running", "Camping", "Casual Outdoor"]
weather_options = ["Hot", "Cold", "Wet", "Dry", "Variable"]
material_preferences = ["Natural Fibers", "Synthetic Fibers", "Technical Materials", "Composite or Natural Materials", "Blends"]
sustainability_options = ["Very Sustainable", "Semi-Sustainable", "Doesn't Matter"]

st.header("Tell us what you need")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    selected_activities = st.multiselect("Activity Options", activity_options)

with col2:
    selected_weather = st.multiselect("Weather Options", weather_options)

with col3:
    selected_materials = st.multiselect("Material Preferences", material_preferences)

with col4:
    selected_sustainability = st.multiselect("Sustainability Options", sustainability_options)

extra_input = st.text_area("Additional Description - optional (Trip details, budget, ...)")

# ----------------------------
# LITELLM CLIENT CONFIG
# ----------------------------
token = os.getenv("LITELLM_TOKEN")
client = OpenAI(api_key=token, base_url="https://litellm.oit.duke.edu/v1")
SYSTEM_PROMPT = (
    "You are a material scientist that is an expert in outdoor gear.\n\n"
    "Knowledge sources:\n"
    "1. brand_profiles.json = " + json.dumps(brand_data) + "\n"
    "2. materials_profiles.json = " + json.dumps(material_data) + "\n\n"
    "Based on the user's input of:\n"
    "- intended activity\n"
    "- weather conditions\n"
    "- material preferences\n"
    "- sustainability preferences\n"
    "- activity description\n\n"
    "Return EXACTLY 3 suggested outdoor brands.\n\n"
    "STRICT OUTPUT FORMAT (must be valid JSON with an object at the root):\n"
    "{\n"
    "  \"suggestions\": [\n"
    "    {\n"
    "      \"brand\": \"string\",\n"
    "      \"brand_eco_score\": 0.0,\n"
    "      \"avg_price\": 0.0,\n"
    "      \"materials\": [\"material 1\", \"material 2\"],\n"
    "      \"material_eco_scores\": {\"material 1\": 0.0, \"material 2\": 0.0},\n"
    "      \"alternative_materials\": [\"alt material 1\", \"alt material 2\"],\n"
    "      \"reasoning\": \"why this brand was chosen\"\n"
    "    }\n"
    "  ]\n"
    "}\n"
)

# ----------------------------
# Handle "Get Brand Suggestions"
# ----------------------------
if st.button("Get Brand Suggestions"):
    if not selected_activities:
        st.error("Please select at least one Activity.")
    else:
        user_message = {
            "activity": selected_activities,
            "weather": selected_weather,
            "materials": selected_materials,
            "sustainability": selected_sustainability,
            "description": extra_input,
        }

        try:
            response = client.chat.completions.create(
                model="gpt-5-mini",
                temperature=0.2,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": json.dumps(user_message)}
                ],
                response_format={"type": "json_object"}
            )
            print(response)
            raw = response.choices[0].message.content
            print(raw)
            obj = json.loads(raw)
            print(obj)
            suggestions = obj["suggestions"]

        except Exception as e:
            st.error(f"Model error: {e}\nShowing fallback data.")
            suggestions = [
                {
                    "brand": "Mountain Equipment",
                    "brand_eco_score": 0.45,
                    "avg_price": 99.95,
                    "materials": ["Recycled Polyester","Recycled Nylon"],
                    "material_eco_scores": {"Recycled Polyester": 0.7,"Recycled Nylon": 0.65},
                    "alternative_materials": ["Organic Cotton","Nylon"],
                    "reasoning": "Fallback display"
                },
                {
                    'brand': 'REI Co-op', 
                    'brand_eco_score': 0.292962962962963, 
                    "avg_price": 55.69109375,
                    'materials': ['REPREVE Polyester', 'COOLMAX EcoMade Polyester'], 
                    'material_eco_scores': {'REPREVE Polyester': 0.8, 'COOLMAX EcoMade Polyester': 0.7}, 
                    'alternative_materials': ['Recycled Polyester', 'Nylon'], 
                    'reasoning': 'Fallback display'
                },
                {
                    'brand': 'Fjallraven', 
                    'brand_eco_score': 0.5, 
                    "avg_price": 152.5,
                    'materials': ['Recycled Polyester', 'Cotton'], 
                    'material_eco_scores': {'Recycled Polyester': 0.7, 'Cotton': 0.25}, 
                    'alternative_materials': ['Recycled Nylon', 'Organic Cotton'], 
                    'reasoning': "Fallback display"
                },
            ]
        # Save to session state
        st.session_state["suggestions"] = suggestions
        st.session_state["selected_brand"] = None

# ----------------------------
# Render Suggestions (From State)
# ----------------------------
suggestions = st.session_state.get("suggestions")
if suggestions:
    # ---- DISPLAY RESULTS ----
    st.header("Suggested Brands")
    st.markdown("*Colors dependent on Eco-Score (Green = Very Sustainable, Yellow = Somewhat Sustainable, Red = Not Sustainable)*")

    def eco_color(score):
        if score >= 0.5:
            return "#235723"  # green
        elif 0.35 <= score < 0.5:
            return "#f7aa0f"  # yellow
        else:
            return "#b32020"  # red

    cols = st.columns(3)

    for idx, suggestion in enumerate(suggestions):
        c = cols[idx]
        # ---- CARDS ----
        with c:
            card = st.container()
            with card:
                color = eco_color(suggestion['brand_eco_score'])
                st.markdown(
                    f"""
                    <div style="
                        background-color: {color};
                        padding: 20px;
                        border-radius: 10px;
                        margin-bottom: 10px;
                    ">
                        <h3 style="color:white;">{suggestion['brand']}</h3>
                        <p style="color:white;"><b>Avg. Price:</b> ${suggestion['avg_price']}</p>
                        <p style="color:white;"><b>Eco Score:</b> {suggestion['brand_eco_score']}</p>
                        <p style="color:white;"><b>Materials:</b> {', '.join(suggestion['materials'])}</p>
                        <p style="color:white;"><b>Alternative Materials:</b> {', '.join(suggestion['alternative_materials'])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button(f"More Info - {suggestion['brand']}", key=f"info_{idx}"):
                    st.session_state["selected_brand"] = suggestion

            

    # ----------------------------
    # Brand Details View
    # ----------------------------
    selected_brand = st.session_state.get("selected_brand")

    if selected_brand:
        st.subheader(f"Details for {selected_brand['brand']}")
        detail_card = st.container(border=True)
        with detail_card:
            st.markdown(f"### Reasoning:")
            st.markdown(f"{selected_brand['reasoning']}")
            st.markdown(f"### Alternative Materials:")
            st.markdown(f"{', '.join(selected_brand['alternative_materials'])}")
        #st.json(selected_brand)

    # ----------------------------
    # Eco Score Bar Chart
    # ----------------------------

    st.subheader("Eco Score Comparison")
    brands = [s["brand"] for s in suggestions]
    scores = [s["brand_eco_score"] for s in suggestions]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=brands, y=scores))
    fig.update_layout(
        yaxis=dict(range=[0, 1]),
        xaxis_title="Brand",
        yaxis_title="Eco Score (0.0 - 1.0)",
    )

    st.plotly_chart(fig, use_container_width=True)