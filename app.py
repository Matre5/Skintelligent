import streamlit as st
from utils import country, LANGUAGES, comedogenic_ingredients, fragrance_ingredients, store_list
from prompt_utils import home_prompt, Nig_prompt
import requests
import base64
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv('API_KEY')
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL')
INGREDIENT_MODEL = os.getenv('INGREDIENT_EXPLAINER_MODEL')

st.set_page_config(page_title="SkinTelligent", layout="wide")

tab1, tab2, tab3, tab4 = st.tabs(["🧴 Skincare Routine Generator", "🧪 Ingredient Checker", "🧴 Nigerian centered Skincare", "🛍️ Stores"])

with tab1:
    st.title("🧴Skintelligent - Your AI Skincare Buddy")

    st.write("Tell me about your skin needs and I'll suggest tailored routines for you")

    with st.form("skincare form"):
        name = st.text_input("What is your name? ")
        skin_type = st.selectbox("Skin Type", ["Oily", "Dry", "Combination", "Normal"])
        skin_tone = st.selectbox("Skin Tone", ["Fair", "Light", "Medium", "Tan", "Deep"])
        concerns = st.multiselect("Concerns", ["Acne", "Hyperpigmentation", "Dryness", "Dullness", "Redness", "Aging", "Sensitive", "Skin barrier damage"])
        expert_mode = st.checkbox("Advanced (mention actives, layering, and ingredients)", value=True)
        budget = st.selectbox("Budget", ["Low", "Medium", "High"])
        location = st.selectbox('Country', country)
        language =  st.selectbox('Preferred language', LANGUAGES)
        gender = st.radio("Gender", ["Female", "Male"])
        

        submitted = st.form_submit_button("Get Routine")
        
    if submitted:
        with st.spinner("⏳ Generating your personalized skincare routine..."):
            
            prompt = home_prompt(name, skin_type, skin_tone, concerns, budget, country, expert_mode, gender, language)

            headers = {
                "Authorization": OPENROUTER_API_KEY,
                "Content-Type": "application/json"
            }

            body = {
                "model": DEFAULT_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a licensed dermatologist"},
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
                        
                def create_download_file(text, filename="routinne.txt"):
                    b64 = base64.b64encode(text.encode()).decode()
                    href= f" <a href='data:file/txt;base64, {b64}' download='{filename}'>📥Download Your Skincare Routine </a>"
                    return href
                
                st.markdown(create_download_file(reply), unsafe_allow_html=True)
                
                # At the bottom of your try block, after displaying the reply
                st.download_button(
                    label="📥 Download Routine as TXT",
                    data=reply,
                    file_name=f"{name.lower().replace(' ', '_')}_skincare_routine.txt",
                    mime="text/plain"
                    )


            except Exception as e:
                st.error("❌ Something went wrong. Please try again.")
                st.exception(e)


with tab2:
    st.title("🧪 Products Ingredient Checker")
    st.header("Know what you are feeding your skin")
    st.markdown("Paste the list of product ingredients below:")

    ingredient_text = st.text_area("Ingredients", placeholder="E.g. Water, Stearic Acid, Isopropyl Myristate...")

    if st.button("Check Ingredients"):
        if not ingredient_text.strip():
            st.warning("Please paste some ingredients to check.")
        else:
            input_ingredients = [ing.strip().lower() for ing in ingredient_text.split(",")]

            found_comedogenic = []
            found_fragrance = []

            for ing in input_ingredients:
                if ing in comedogenic_ingredients:
                    found_comedogenic.append((ing, comedogenic_ingredients[ing]))
                if ing in fragrance_ingredients:
                    found_fragrance.append((ing, fragrance_ingredients[ing]))

            if found_comedogenic:
                st.markdown("### ❌ Pore-Clogging Ingredients Found")
                for ing, reason in found_comedogenic:
                    st.markdown(f"- **{ing.title()}** – {reason}")
            else:
                st.success("✅ No known comedogenic ingredients detected.")

            if found_fragrance:
                st.markdown("### ⚠️ Fragrance Ingredients Found")
                for ing, reason in found_fragrance:
                    st.markdown(f"- **{ing.title()}** – {reason}")
            else:
                st.success("✅ No known fragrance allergens detected.")
                
    if st.button("Explain ingredients"):
        with st.spinner("🧠 Asking the skincare expert..."):

            ingredient_text_clean = ingredient_text.strip()
            
            if not ingredient_text_clean:
                st.warning("Please paste some ingredients first.")
            else:
                ai_prompt = f"""
                    You are a dermatologist and cosmetic chemist.

                    Explain the following skincare ingredients in simple terms.

                    Tell me:
                    - What the ingredient does
                    - If it's good or risky for acne-prone, sensitive, or oily skin
                    - Any rating: ✅ Safe, ⚠️ Use with caution, ❌ Avoid

                    Respond in this format:
                    - **Ingredient Name**: Explanation (and safety tag)

                    Ingredients:
                    {ingredient_text_clean}
                    """

                headers = {
                    "Authorization": OPENROUTER_API_KEY,
                    "Content-Type": "application/json"
                }

                body = {
                    "model": INGREDIENT_MODEL,
                    "messages": [
                        {"role": "system", "content": "You are a skincare chemist."},
                        {"role": "user", "content": ai_prompt}
                    ]
                }

                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

                try:
                    reply = response.json()['choices'][0]['message']['content']
                    st.markdown("### 🤖 AI Ingredient Explanation")
                    st.markdown(reply)
                    
                    
                except Exception as e:
                    st.error("❌ Error occurred while getting explanation.")
                    st.exception(e)

with tab3:
    st.title("🧴 SkinTelligent NG")
    st.header("Nigerian Personalised skincare routine generator")
    
    st.write("You the game of skincare bots generator for african skin and markets are insufficent and not localised enough. This is tailored specifically to Nigeria and her citiziens")
    st.write("Feedbacks are highly appreciated to give you a better experience.")
    
    with st.form("Skincare form"):
        name = st.text_input("What is your name? ")
        skin_type = st.selectbox("Skin Type", ["Oily", "Dry", "Combination", "Normal"])
        skin_tone = st.selectbox("Skin Tone", ["Light skinned", "Medium Skinned", "Dark Skinned", "Very Dark Skinned"])
        concerns = st.multiselect("Concerns", ["Acne", "Hyperpigmentation", "Dryness", "Dullness", "Redness", "Aging", "Sensitive", "Skin barrier damage"])
        expert_mode = st.checkbox("Advanced (mention actives, layering, and ingredients)", value=True)
        budget = st.selectbox("Budget", ["Low", "Medium", "High"])
        # state = st.selectbox('State Resisding', country)
        # language =  st.selectbox('Preferred language', LANGUAGES)
        gender = st.radio("Gender", ['Female', 'Male'])
        
        # routine_type = st.radio( "What type of routine do you prefer?",
        # ["Simple (4 steps)", "Multi-Step (4+ steps)"])

        submitted = st.form_submit_button("Get Routine")
        
    if submitted:
        with st.spinner("⏳ Generating your personalized skincare routine..."):
            
            Ng_prompt = Nig_prompt(name, skin_type, skin_tone, concerns, budget, expert_mode, gender)
            
            headers = {
                "Authorization": OPENROUTER_API_KEY,
                "Content-Type": "application/json"
            }

            body = {
                "model": DEFAULT_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a licensed dermatologist in Nigeria"},
                    {"role": "user", "content": Ng_prompt}
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
                        # st.markdown("#### 🌞 Morning Routine")
                        st.markdown(section)
                        
                    elif "night routine" in section_lower:
                        # st.markdown("#### 🌙 Night Routine")
                        st.markdown(section)
                    elif "skin care tips" in section_lower or "skincare tips" in section_lower:
                        # st.markdown("#### 💡 Skincare Tips")
                        st.markdown(section)
                    elif "Recommended Products" in section_lower :
                        # st.markdown("#### 🛍️ Product Recommendations")
                        st.markdown(section)
                    else:
                        st.markdown(section)
                    
                if "sunscreen" not in reply.lower():
                    st.warning('Sunscreen is essential for every morning routine, especially under the Nigerian Sun. Use spf 30 or higher')   
                

            except Exception as e:
                st.error("❌ Something went wrong. Please try again.")
                st.exception(e)

with tab4:
    st.title("🛍️ Skincare Stores in Nigeria")
    st.header("")
    
    st.write("Click on any store to visit their page")
    
    for store_name, store_url in store_list:
        st.markdown(f" [{store_name}]({store_url})")
        
    df_stores = pd.DataFrame(store_list, columns=['Store Name', 'Website/Store Page'])
    
    # csv = df_stores.to_csv(index=False)
    # b64 = base64.b64encode(csv.encode()).decode()
    
    # st.markdown("### 📥 Download Store List")
    # st.markdown(f'<a href="data:file/csv;base64,{b64}, filename={"skincare_stores_nigeria.csv"}> "Download as CSV" </a>', unsafe_allow_html=True)