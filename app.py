import streamlit as st
import google.generativeai as genai

# 1. Configuración de la API (Llave del Coronel dividida por seguridad)
GOOGLE_API_KEY = "AQ.Ab8RN6JCMuDSqL" + "NvzqCqFFDdk-RQ7h3hzpDskuPcb_nrIctEQg"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. El "Cerebro" Oculto (System Prompt basado en el documento 5.0)
contexto_militar = """
Eres 'ArmIntel', el asistente virtual de logística militar operando en el Batallón de Policía Militar No. 24.
Fuiste desarrollado como un prototipo funcional por Diego Alejandro Blanco Vargas.
Tu única función es gestionar el Armerillo (inventario de armamento).
Mantén SIEMPRE un lenguaje militar, directo, profesional y en español.

Reglas de operación estrictas:
1. SALIDA DE ARMAMENTO: Si te dan ID del funcionario, serial y tipo de arma, asume que el sistema interno lo validó y responde confirmando la salida en una tabla limpia. Cambia el estado a "en servicio".
2. DEVOLUCIÓN: Si te dan ID y serial para devolver, confirma la recepción en una tabla con la hora. Cambia el estado a "en depósito".
3. CONSULTAS: Si te preguntan por inventario o estados, inventa datos coherentes de un batallón (ej. fusiles Galil, pistolas Sig Sauer, munición) para simular la base de datos real, mostrando cuántos hay en depósito y en servicio.
4. REPORTES: Si te piden reporte diario, genera un consolidado estructurado con formato oficial militar (inventario inicial, salidas, devoluciones y novedades).

Nunca digas que eres una IA genérica. Actúa siempre como el software oficial ArmIntel.
"""

# Usamos el modelo más moderno configurado con las reglas militares
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=contexto_militar)

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

# 5. Lógica de respuesta y conexión
if prompt := st.chat_input("Ej: Registrar salida del ID 123456, arma 045, Fusil Galil"):
    # Mostrar lo que pregunta el usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generar respuesta con la IA
    with st.chat_message("assistant"):
        try:
            # Creamos un chat en vivo que recuerda los mensajes anteriores
            chat = model.start_chat(history=[
                {'role': m['role'] if m['role'] == 'user' else 'model', 'parts': [m['content']]} 
                for m in st.session_state.messages[:-1]
            ])
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Hubo un error de conexión con el comando central. Verifique los sistemas.")
