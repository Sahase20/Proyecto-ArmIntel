import streamlit as st
import requests

# 1. Configuración de la API (Tu llave nueva)
GOOGLE_API_KEY = "AQ.Ab8RN6KE3fa_YKr" + "6wwkmMS2HrgrfluE8OJIjTejYcWROYrAOOA"

# 2. El "Cerebro" Oculto
contexto_militar = """
Eres 'ArmIntel', el asistente virtual de logística militar operando en el Batallón de Policía Militar No. 24.
Fuiste desarrollado como un prototipo funcional por Diego Alejandro Blanco Vargas.
Tu única función es gestionar el Armerillo (inventario de armamento).
Mantén SIEMPRE un lenguaje militar, directo, profesional y en español.

Reglas de operación estrictas:
1. SALIDA DE ARMAMENTO: Si te dan ID del funcionario, serial y tipo de arma, responde confirmando la salida en una tabla limpia. Cambia el estado a "en servicio".
2. DEVOLUCIÓN: Si te dan ID y serial para devolver, confirma la recepción en una tabla con la hora. Cambia el estado a "en depósito".
3. CONSULTAS: Inventa datos coherentes de un batallón para simular la base de datos real, mostrando cuántos hay en depósito y en servicio.
4. REPORTES: Genera un consolidado estructurado con formato oficial militar.

Nunca digas que eres una IA genérica. Actúa siempre como el software oficial ArmIntel.
"""

# 3. Diseño de la página institucional
st.set_page_config(page_title="ArmIntel - Fase 2", page_icon="🛡️", layout="centered")
st.title("🛡️ ArmIntel: Asistente Táctico")
st.markdown("**Batallón de Policía Militar No. 24** | *Módulo de Logística y Armamento*")
st.write("Bienvenido al sistema de análisis documental e inteligencia. Escriba su consulta o instrucción táctica abajo.")

# 4. Memoria del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Lógica de respuesta (CONEXIÓN DIRECTA A GOOGLE)
if prompt := st.chat_input("Ej: Registrar salida del ID 123456, arma 045, Fusil Galil"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            # Unimos el contexto militar y la pregunta
            instruccion_completa = contexto_militar + "\n\nComando del usuario:\n" + prompt
            
            # Llamada directa al servidor (Evita el error 404 de la librería)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
            payload = {"contents": [{"parts": [{"text": instruccion_completa}]}]}
            
            respuesta_bruta = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
            
            if respuesta_bruta.status_code == 200:
                datos = respuesta_bruta.json()
                texto_final = datos['candidates'][0]['content']['parts'][0]['text']
                st.markdown(texto_final)
                st.session_state.messages.append({"role": "assistant", "content": texto_final})
            else:
                st.error(f"Error de Google: {respuesta_bruta.status_code} - {respuesta_bruta.text}")
                
        except Exception as e:
            st.error("Error del sistema:")
            st.error(e)
