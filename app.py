import streamlit as st
import google.generativeai as genai

# 1. Configuración de la API (La llave de Geminis)
GOOGLE_API_KEY = "AQ.Ab8RN6JCMuDSqL" + "NvzqCqFFDdk-RQ7h3hzpDskuPcb_nrIctEQg"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# 2. Diseño de la página
st.set_page_config(page_title="ArmIntel - Fase 2", page_icon="🛡️")
st.title("🛡️ ArmIntel: Asistente Táctico")
st.write("Bienvenido al sistema de análisis documental e inteligencia. Escriba su consulta táctica abajo.")

# 3. Memoria del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Lógica de respuesta
if prompt := st.chat_input("Ej: ¿Cuáles son las especificaciones del armamento estándar?"):
    # Mostrar lo que pregunta el usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generar respuesta con Gemini
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Hubo un error de conexión con la inteligencia central. Intente nuevamente.")
