import streamlit as st
from supabase import create_client
import os

# Configuración de pantalla limpia
st.set_page_config(page_title="Evaluación Conductual - TalentStream", page_icon="🧠", layout="centered")

# Ocultar menús por defecto de Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Conexión a tu Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

if "evaluacion_enviada" not in st.session_state:
    st.session_state.evaluacion_enviada = False

# Leer parámetros de la URL
query_params = st.query_params
cedula_url = query_params.get("cedula", "")
tipo_cargo = query_params.get("tipo", "administrativo").lower()

st.markdown('<h2 style="text-align:center; color:#6366f1; font-weight:bold;">🧠 Evaluación de Perfil Conductual</h2>', unsafe_allow_html=True)
st.markdown("---")

if st.session_state.evaluacion_enviada:
    st.balloons()
    st.success("🎉 ¡Tu prueba ha sido registrada con éxito! Ya puedes cerrar esta pestaña. Muchas gracias.")
else:
    if not cedula_url:
        st.error("🛑 Enlace no válido. Por favor, solicita un link personalizado a tu reclutador.")
    else:
        # 🔍 CONSULTA DE VALIDACIÓN: Traemos también el veredicto para verificar si ya respondió antes
        res = supabase.table("candidatos").select("Nombre", "Vacante", "disc_veredicto").eq("Cédula", str(cedula_url)).execute()
        
        if not res.data:
            st.error("❌ El documento de identidad en este enlace no coincide con ningún candidato activo.")
        else:
            candidato = res.data[0]
            veredicto_existente = candidato.get("disc_veredicto")
            
            # 🛑 TRABA DE SEGURIDAD: Si ya tiene veredicto en la base de datos, BLOQUEAMOS el acceso
            if veredicto_existente and str(veredicto_existente).strip() != "" and veredicto_existente != "NULL":
                st.warning(f"⚠️ **Acceso Restringido:** Hola {candidato['Nombre']}, el sistema detecta que ya completaste esta evaluación conductual previamente.")
                st.info("Solo se permite un intento por candidato. Tus respuestas ya están a salvo en nuestro sistema de selección de TalentStream.")
            else:
                # Si está limpio, procedemos a mostrar el cuestionario con normalidad
                st.success(f"👤 **Candidato:** {candidato['Nombre']}  \n💼 **Cargo al que postula:** {candidato['Vacante']}")
                st.write("Selecciona la opción con la que **más te identifiques** en tu entorno de trabajo:")
                
                ans_1, ans_2, ans_3, ans_4 = None, None, None, None
                
                # =========================================================
                # 💼 BLOQUE 1: PREGUNTAS PARA CARGOS ADMINISTRATIVOS
                # =========================================================
                if tipo_cargo == "administrativo":
                    st.markdown("### 📝 Cuestionario de Enfoque Profesional")
                    ans_1 = st.radio("1. Al liderar o participar en una reunión de planeación, tú prefieres:", [
                        "🔴 Enfocarme directo en las metas de productividad y tomar decisiones rápidas.",
                        "🟡 Motivar al equipo, proponer ideas creativas y mantener un ambiente alegre.",
                        "🟢 Escuchar la opinión de todos para llegar a un acuerdo armónico y sin conflictos.",
                        "🔵 Evaluar los datos históricos, riesgos técnicos y basarme en reportes exactos."
                    ], index=None, key="adm_1")

                    ans_2 = st.radio("2. Cuando te enfrentas a un cambio de estrategia imprevisto y de alta urgencia, tú:", [
                        "🔴 Actúo de inmediato asumiendo el control de la situación y delegando tareas.",
                        "🟡 Busco aliados estratégicos rápidamente apoyándome en mi red de contactos.",
                        "🟢 Analizo cómo afectará el cambio al equipo para mantener la calma y estabilidad.",
                        "🔵 Reviso las políticas corporativas y manuales antes de dar un paso en falso."
                    ], index=None, key="adm_2")

                    ans_3 = st.radio("3. En la entrega de reportes o gestión de proyectos, tu prioridad es:", [
                        "🔴 Entregar resultados contundentes que demuestren un alto retorno o eficiencia.",
                        "🟡 Presentar la idea de forma impactante y persuasiva ante los comités.",
                        "🟢 Asegurarme de que el proceso sea coordinated de manera pacífica y equitativa.",
                        "🔵 Garantizar que la información tenga cero errores y máxima precisión técnica."
                    ], index=None, key="adm_3")

                    ans_4 = st.radio("4. Si alguien del equipo comete un error grave en la operación administrativa:", [
                        "🔴 Le exijo corregirlo inmediatamente enfocándome en solucionar el problema.",
                        "🟡 Converso con la persona amigablemente para entender la situación y animarla.",
                        "🟢 Le brindo mi apoyo total con paciencia para resolverlo juntos paso a paso.",
                        "🔵 Evalúo minuciosamente en qué parte del proceso o manual falló la regla."
                    ], index=None, key="adm_4")

                # ========================================================
                # ⚙️ BLOQUE 2: PREGUNTAS PARA CARGOS OPERATIVOS
                # ========================================================
                else:
                    st.markdown("### 🛠️ Cuestionario de Enfoque Técnico y Operativo")
                    ans_1 = st.radio("1. Al iniciar tus tareas diarias en tu puesto de trabajo, lo que más te interesa es:", [
                        "🔴 Cumplir mis metas individuales lo más rápido posible para destacar.",
                        "🟡 Saludar a mis compañeros y mantener una comunicación alegre durante el turno.",
                        "🟢 Que el ritmo de trabajo sea constante, predecible y seguro.",
                        "🔵 Asegurarme de que las herramientas y el proceso cumplan estrictamente las normas."
                    ], index=None, key="ope_1")

                    ans_2 = st.radio("2. Si una máquina o un proceso presenta una falla imprevista en plena operación:", [
                        "🔴 Busco resolverlo rápido por mi cuenta para no frenar la producción.",
                        "🟡 Le aviso a mis compañeros de zona y busco ayuda en equipo de forma de entusiasmo.",
                        "🟢 Mantengo la calma completa y espero las instrucciones directas de mi supervisor.",
                        "🔵 Detengo el trabajo de inmediato siguiendo los protocolos y reporto la falla exacta."
                    ], index=None, key="ope_2")

                    ans_3 = st.radio("3. Cuando te asignan una tarea operativa muy monótona o repetitiva:", [
                        "🔴 Busco formas de agilizarla para romper récords de velocidad.",
                        "🟡 Aprovecho para conversar con mis compañeros sanamente sin descuidar el trabajo.",
                        "🟢 La realizo con total paciencia y concentración, manteniendo un ritmo estable.",
                        "🔵 Sigo el paso a paso exacto del manual técnico de principio a fin."
                    ], index=None, key="ope_3")

                    ans_4 = st.radio("4. Ante un cambio imprevisto de turnos, horarios o funciones asignadas:", [
                        "🔴 Me adapto rápido pensando en que es un reto que superaré fácilmente.",
                        "🟡 Lo tomo con buena actitud y humor, conversando los detalles con el equipo.",
                        "🟢 Prefiero que me avisen con tiempo para asimilarlo con calma y sin prisas.",
                        "🔵 Solicito que me expliquen formalmente cuáles serán las nuevas reglas y tareas."
                    ], index=None, key="ope_4")

                st.markdown("---")
                
                if st.button("📤 Finalizar y Enviar Evaluación", type="primary", use_container_width=True):
                    if not all([ans_1, ans_2, ans_3, ans_4]):
                        st.warning("⚠️ Debes seleccionar una respuesta para cada una de las 4 preguntas antes de enviar.")
                    else:
                        puntos_finales = {"D": 0, "I": 0, "S": 0, "C": 0}
                        respuestas_candidato = [ans_1, ans_2, ans_3, ans_4]
                        
                        for r in respuestas_candidato:
                            if "🔴" in r: puntos_finales["D"] += 25
                            elif "🟡" in r: puntos_finales["I"] += 25
                            elif "🟢" in r: puntos_finales["S"] += 25
                            elif "🔵" in r: puntos_finales["C"] += 25
                        
                        factor_dominante = max(puntos_finales, key=puntos_finales.get)
                        
                        textos_disc = {
                            "D": ("🔴 Perfil Directo, Conductor y Competitivo.", "Posee una altísima orientación a resultados y resolución de problemas bajo presión. No teme asumir riesgos estratégicos y empujará al equipo a cumplir metas exigentes de inmediato."),
                            "I": ("🟡 Perfil Persuasivo, Comunicativo y Relacional.", "Tiene una capacidad nata para conectar con personas, liderar equipos mediante la motivación y articular relaciones humanas fluidas, asegurando un clima de entusiasmo."),
                            "S": ("🟢 Perfil Confiable, Paciente y Estable.", "Aporta lealtad, consistencia y un alto sentido del orden a procesos a largo plazo. Trabaja con serenidad en situaciones críticas y garantiza que las tareas rutinarias se completen con total constancia."),
                            "C": ("🔵 Perfil Analítico, Riguroso y Preciso.", "Su enfoque se basa en la calidad, la exactitud y el cumplimiento normativo. Minimiza los márgenes de error a cero, siendo excelente para la planeación técnica estructurada.")
                        }
                        
                        titulo_v, porque_v = textos_disc[factor_dominante]
                        veredicto_completo = f"{titulo_v} | {porque_v}"
                        
                        # Guardamos de manera exacta los puntajes
                        supabase.table("candidatos").update({
                            "disc_d": puntos_finales["D"],
                            "disc_i": puntos_finales["I"],
                            "disc_s": puntos_finales["S"],
                            "disc_c": puntos_finales["C"],
                            "disc_veredicto": veredicto_completo
                        }).eq("Cédula", str(cedula_url)).execute()
                        
                        st.session_state.evaluacion_enviada = True
                        st.rerun()