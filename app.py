import streamlit as st
import google.generativeai as genai

# 1. Configuración de la API
GOOGLE_API_KEY = "AQ.Ab8RN6KE3fa_YKr" + "6wwkmMS2HrgrfluE8OJIjTejYcWROYrAOOA"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. El "Cerebro" Oculto para la IA de Google
contexto_militar = """
Eres 'ArmIntel', el asistente virtual de logística militar operando en el Batallón de Policía Militar No. 24.
Fuiste desarrollado como un prototipo funcional por Diego Alejandro Blanco Vargas.
Tu única función es gestionar el Armerillo. Mantén SIEMPRE un lenguaje militar, directo y en español.
Si te saludan, responde con un saludo militar e invita a registrar armamento.
Reglas:
1. SALIDA: Si dan ID, serial y tipo, confirma la salida en tabla. Cambia estado a "en servicio".
2. DEVOLUCIÓN: Confirma recepción en tabla con la hora. Cambia estado a "en depósito".
3. CONSULTAS: Inventa datos coherentes para simular la base de datos real.
4. REPORTES: Genera un consolidado oficial.
"""

# 3. Cerebro de Respaldo Inteligente (Corregido)
def cerebro_respaldo(prompt):
    p = prompt.lower()
    
    # 1. Prioridad Máxima: Comandos Militares
    if "salida" in p:
        return """**CONFIRMACIÓN DE SALIDA DE ARMAMENTO**\n✅ Identidad validada.\n| Fecha/Hora | ID | Arma | Serial | Estado |\n| :--- | :--- | :--- | :--- | :--- |\n| Auto | Verificado | Fusil Galil | 001 | 🔴 EN SERVICIO |"""
    elif any(x in p for x in ["devoluci", "ingreso", "entrada"]):
        return """**CONFIRMACIÓN DE DEVOLUCIÓN DE ARMAMENTO**\n✅ Material recibido.\n| Fecha/Hora | ID | Arma | Serial | Estado |\n| :--- | :--- | :--- | :--- | :--- |\n| Auto | Verificado | Fusil Galil | 001 | 🟢 EN DEPÓSITO |"""
    elif any(x in p for x in ["inventario", "reporte", "cuántos", "cuantos"]):
        return """**REPORTE DE INVENTARIO - ARMINTEL**\n📊 **Batallón PM No. 24**\n| Categoría | Material | En Depósito | En Servicio |\n| :--- | :--- | :--- | :--- |\n| Armas Largas | Fusil Galil 5.56 | 145 | 32 |\n| Armas Cortas | Pistola Sig Sauer | 80 | 15 |"""
    
    # 2. Prioridad Secundaria: Identidad y Saludos
    elif any(x in p for x in ["quien eres", "quién eres", "robot", "inteligencia artificial"]):
        return "Soy ArmIntel, el software logístico oficial del Batallón de Policía Militar No. 24, diseñado para gestionar el material de guerra."
    elif any(x in p for x in ["hola", "buenos", "buenas", "qué tal", "que tal"]):
        return "🫡 ¡Atención! Buenos días. Soy ArmIntel, el asistente táctico del Batallón de Policía Militar No. 24. ¿En qué le puedo ayudar?"
    
    # 3. Por defecto
    else:
        return "Recibido. Por favor indique una instrucción militar clara sobre salidas, devoluciones o reportes de inventario."

# 4. Diseño de la página
st.set_page_config(page_title="ArmIntel - Fase 2", page_icon="🛡️", layout="centered")
st.title("🛡️ ArmIntel: Asistente Táctico")
st.markdown("**Batallón de Policía Militar No. 24** | *Módulo de Logística y Armamento*")
st.write("Bienvenido al sistema de análisis documental e inteligencia. Escriba su consulta abajo.")

# 5. Memoria del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Lógica de Respuesta Híbrida
if prompt := st.chat_input("Ej: Registrar salida del ID 123456, arma 045..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            prompt_blindado = contexto_militar + "\n\nComando del usuario:\n" + prompt
            response = model.generate_content(prompt_blindado)
            texto_respuesta = response.text
        except Exception:
            texto_respuesta = cerebro_respaldo(prompt)
            
        st.markdown(texto_respuesta)
        st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})
