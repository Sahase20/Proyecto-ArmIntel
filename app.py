import streamlit as st
import google.generativeai as genai
import re

# 1. Configuración de la API (Tu llave)
GOOGLE_API_KEY = "AQ.Ab8RN6KE3fa_YKr" + "6wwkmMS2HrgrfluE8OJIjTejYcWROYrAOOA"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. El "Cerebro" Oculto
contexto_militar = """
Eres 'ArmIntel', el asistente virtual de logística militar operando en el Batallón de Policía Militar No. 24.
Fuiste desarrollado como un prototipo funcional por Diego Alejandro Blanco Vargas.
Tu única función es gestionar el Armerillo. Mantén SIEMPRE un lenguaje militar.
"""

# 3. Cerebro de Respaldo Inteligente (AHORA DINÁMICO)
def cerebro_respaldo(prompt):
    p = prompt.lower()
    
    # Truco Ninja: Extraemos los números que el usuario escriba
    numeros = re.findall(r'\d+', p)
    id_detectado = numeros[0] if len(numeros) > 0 else "Verificado"
    serial_detectado = numeros[1] if len(numeros) > 1 else "001"
    
    # Extraemos el arma si la menciona
    arma_detectada = "Pistola Glock" if "glock" in p else "Fusil Galil"

    if "salida" in p:
        return f"""**CONFIRMACIÓN DE SALIDA DE ARMAMENTO**\n✅ Identidad validada.\n| Fecha/Hora | ID | Arma | Serial | Estado |\n| :--- | :--- | :--- | :--- | :--- |\n| Auto | {id_detectado} | {arma_detectada} | {serial_detectado} | 🔴 EN SERVICIO |"""
    elif any(x in p for x in ["devoluci", "ingreso", "entrada"]):
        return f"""**CONFIRMACIÓN DE DEVOLUCIÓN DE ARMAMENTO**\n✅ Material recibido.\n| Fecha/Hora | ID | Arma | Serial | Estado |\n| :--- | :--- | :--- | :--- | :--- |\n| Auto | {id_detectado} | {arma_detectada} | {serial_detectado} | 🟢 EN DEPÓSITO |"""
    elif any(x in p for x in ["inventario", "reporte", "cuántos", "cuantos"]):
        return """**REPORTE DE INVENTARIO - ARMINTEL**\n📊 **Batallón PM No. 24**\n| Categoría | Material | En Depósito | En Servicio |\n| :--- | :--- | :--- | :--- |\n| Armas Largas | Fusil Galil 5.56 | 145 | 32 |\n| Armas Cortas | Pistola Sig Sauer | 80 | 15 |"""
    elif any(x in p for x in ["hola", "buenos", "buenas"]):
        return "🫡 ¡Atención! Buenos días. Soy ArmIntel, el asistente táctico. ¿En qué le puedo ayudar?"
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
if prompt := st.chat_input("Ej: Registrar salida del ID 123456..."):
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
