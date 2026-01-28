import streamlit as st
from utils import country, LANGUAGES
from prompt_utils import home_prompt
import requests

st.set_page_config(page_title= "Skintelligent Chatbot", layout=  'centered')

st.title("Skintelligent - Your AI Skincare Buddy")

st.write("Tell me about your skin needs and I'll suggest a tailored routines for you")

with st.form("skincare form"):
    skin_type = st.selectbox("Skin Type", ["Oily", "Dry", "Combination", "Normal"])
    skin_tone = st.selectbox("Skin Tone", ["Fair", "Light", "Medium", "Tan", "Deep"])
    concerns = st.multiselect("Concerns", ["Acne", "Hyperpigmentation", "Dryness", "Dullness", "Redness", "Aging", "Sensitive"])
    expert_mode = st.checkbox("Advanced (mention actives, layering, and ingredients)", value=True)
    budget = st.selectbox("Budget", ["Low", "Medium", "High"])
    location = st.selectbox('Country', country)
    language =  st.selectbox('Preferred language', LANGUAGES)
    

    submitted = st.form_submit_button("Get Routine")
    
if submitted:
    with st.spinner("⏳ Generating your personalized skincare routine..."):
        
        prompt = home_prompt(skin_type, skin_tone, concerns, budget, country, routine_type, expert_mode, language)

        headers = {
            "Authorization": f"Bearer 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",
            "Content-Type": "application/json"
        }

        body = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "You are a licensed dermatologist and expert skincare formulator.."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=body
        )

        try:
            # st.write("🔍 Raw response from LLM API:")
            # st.json(response.json())
            reply = response.json()['choices'][0]['message']['content']

            # Split by double newlines to identify sections
            sections = reply.split("\n\n")

            # Iterate through sections and add friendly headers
            for section in sections:
                section_lower = section.lower()
                
                if "welcome to your personalised skincare buddy" in section_lower:
                    st.markdown(f"### 👋 {section.strip()}")
                elif "morning routine" in section_lower:
                    st.markdown("#### 🌞 Morning Routine")
                    st.markdown(section)
                elif "night routine" in section_lower:
                    st.markdown("#### 🌙 Night Routine")
                    st.markdown(section)
                elif "skin care tips" in section_lower or "skincare tips" in section_lower:
                    st.markdown("#### 💡 Skincare Tips")
                    st.markdown(section)
                elif "product recommendation list" in section_lower or "products recommendation list" in section_lower:
                    st.markdown("#### 🛍️ Product Recommendations")
                    st.markdown(section)
                else:
                    st.markdown(section)

        except Exception as e:
            st.error("❌ Something went wrong. Please try again.")
            st.exception(e)