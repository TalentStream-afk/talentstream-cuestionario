import streamlit as st
from supabase import create_client
import os

st.set_page_config(page_title="Evaluación Conductual - TalentStream", page_icon="🧠", layout="centered")
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

if "evaluacion_enviada" not in st.session_state:
    st.session_state.evaluacion_enviada = False

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

        res = supabase.table("candidatos").select("Nombre", "Vacante", "disc_veredicto").eq("Cédula", str(cedula_url)).execute()
        
        if not res.data:
            st.error("❌ El documento de identidad en este enlace no coincide con ningún candidato activo.")
        else:
            candidato = res.data[0]
            veredicto_existente = candidato.get("disc_veredicto")

            if veredicto_existente and str(veredicto_existente).strip() != "" and veredicto_existente != "NULL":
                st.warning(f"⚠️ **Acceso Restringido:** Hola {candidato['Nombre']}, el sistema detecta que ya completaste esta evaluación conductual previamente.")
                st.info("Solo se permite un intento por candidato. Tus respuestas ya están a salvo en nuestro sistema de selección de TalentStream.")
            else:
                st.success(f"👤 **Candidato:** {candidato['Nombre']}  \n💼 **Cargo al que postula:** {candidato['Vacante']}")
                st.write("Selecciona la opción con la que **más te identifiques** en tu entorno de trabajo:")
                
                respuestas_lista = []

                if tipo_cargo == "operativo":
                    st.markdown("### 🛠️ Cuestionario de Enfoque Técnico y Operativo")
                    ans_o1 = st.radio("1. Al iniciar tus tareas diarias en tu puesto de trabajo, lo que más te interesa es:", [
                        "🔴 Cumplir mis metas individuales lo más rápido posible para destacar.",
                        "🟡 Saludar a mis compañeros y mantener una comunicación alegre durante el turno.",
                        "🟢 Que el ritmo de trabajo sea constante, predecible y seguro.",
                        "🔵 Asegurarme de que las herramientas y el proceso cumplan estrictamente las normas."
                    ], index=None, key="ope_1")

                    ans_o2 = st.radio("2. Si una máquina o un proceso presenta una falla imprevista en plena operación:", [
                        "🔴 Busco resolverlo rápido por mi cuenta para no frenar la producción.",
                        "🟡 Le aviso a mis compañeros de zona y busco ayuda en equipo de forma de entusiasmo.",
                        "🟢 Mantengo la calma completa y espero las instrucciones directas de mi supervisor.",
                        "🔵 Detengo el trabajo de inmediato siguiendo los protocolos y reporto la falla exacta."
                    ], index=None, key="ope_2")

                    ans_o3 = st.radio("3. Cuando te asignan una tarea operativa muy monótona o repetitiva:", [
                        "🔴 Busco formas de agilizarla para romper récords de velocidad.",
                        "🟡 Aprovecho para conversar con mis compañeros sanamente sin descuidar el trabajo.",
                        "🟢 La realizo con total paciencia y concentración, manteniendo un ritmo estable.",
                        "🔵 Sigo el paso a paso exacto del manual técnico de principio a fin."
                    ], index=None, key="ope_3")

                    ans_o4 = st.radio("4. Ante un cambio imprevisto de turnos, horarios o funciones asignadas:", [
                        "🔴 Me adapto rápido pensando en que es un reto que superaré fácilmente.",
                        "🟡 Lo tomo con buena actitud y humor, conversando los detalles con el equipo.",
                        "🟢 Prefiero que me avisen con tiempo para asimilarlo con calma y sin prisas.",
                        "🔵 Solicito que me expliquen formalmente cuáles serán las nuevas reglas y tareas."
                    ], index=None, key="ope_4")

                    ans_o5 = st.radio("5. Si se presenta una situación que puede retrasar su llegada al trabajo, usted:", [
                        "🔵 Informa inmediatamente a su jefe y busca una alternativa para llegar lo antes posible.",
                        "🔴 Espera a ver si logra llegar a tiempo antes de informar.",
                        "🟡 Informa cuando ya está retrasado.",
                        "🟢 Considera que no es necesario informar."
                    ], index=None, key="ope_5")

                    ans_o6 = st.radio("6. Si debe presentarse a una capacitación programada por la empresa, usted:", [
                        "🔵 Llega con anticipación y preparado para participar.",
                        "🟢 Llega a la hora exacta de inicio.",
                        "🟡 Llega cuando le sea posible durante la actividad.",
                        "🔴 Solo asiste si considera que el tema es importante."
                    ], index=None, key="ope_6")

                    ans_o7 = st.radio("7. ¿Cómo organiza sus actividades personales respecto a su horario laboral?", [
                        "🔵 Planifico mis actividades para evitar afectar mi asistencia y puntualidad.",
                        "🟢 Generalmente me organizo, aunque algunas veces se presentan inconvenientes.",
                        "🟡 Atiendo primero mis asuntos personales y luego el trabajo.",
                        "🔴 No realizo una planificación específica."
                    ], index=None, key="ope_7")

                    respuestas_lista = [ans_o1, ans_o2, ans_o3, ans_o4, ans_o5, ans_o6, ans_o7]

                elif tipo_cargo == "administrativo":
                    st.markdown("### 📝 Cuestionario de Enfoque Profesional")
                    ans_a1 = st.radio("1. Al liderar o participar en una reunión de planeación, tú prefieres:", [
                        "🔴 Enfocarme directo en las metas de productividad y tomar decisiones rápidas.",
                        "🟡 Motivar al equipo, proponer ideas creativas and mantener un ambiente alegre.",
                        "🟢 Escuchar la opinión de todos para llegar a un acuerdo armónico y sin conflictos.",
                        "🔵 Evaluar los datos históricos, riesgos técnicos y basarme en reportes exactos."
                    ], index=None, key="adm_1")

                    ans_a2 = st.radio("2. Cuando te enfrentas a un cambio de estrategia imprevisto y de alta urgencia, tú:", [
                        "🔴 Actúo de inmediato asumiendo el control de la situación y delegando tareas.",
                        "🟡 Busco aliados estratégicos rápidamente apoyándome en mi red de contactos.",
                        "🟢 Analizo cómo afectará el cambio al equipo para mantener la calma y estabilidad.",
                        "🔵 Reviso las políticas corporativas y manuales antes de dar un paso en falso."
                    ], index=None, key="adm_2")

                    ans_a3 = st.radio("3. En la entrega de reportes o gestión de proyectos, tu prioridad es:", [
                        "🔴 Entregar resultados contundentes que demuestren un alto retorno o eficiencia.",
                        "🟡 Presentar la idea de forma impactante y persuasiva ante los comités.",
                        "🟢 Asegurarme de que el proceso sea coordinado de manera pacífica y equitativa.",
                        "🔵 Garantizar que la información tenga cero errores y máxima precisión técnica."
                    ], index=None, key="adm_3")

                    ans_a4 = st.radio("4. Si alguien del equipo comete un error grave en la operación administrativa:", [
                        "🔴 Le exijo corregirlo inmediatamente enfocándome en solucionar el problema.",
                        "🟡 Converso con la persona amigablemente para entender la situación y animarla.",
                        "🟢 Le brindo mi apoyo total con paciencia para resolverlo juntos paso a paso.",
                        "🔵 Evalúo minuciosamente en qué parte del proceso o manual falló la regla."
                    ], index=None, key="adm_4")

                    ans_a5 = st.radio("5. ¿Qué característica considera más importante en su trabajo?", [
                        "🔵 Precisión y calidad.",
                        "🔴 Resultados y cumplimiento de metas.",
                        "🟢 Cooperación y estabilidad.",
                        "🟡 Comunicación y relaciones interpersonales."
                    ], index=None, key="adm_5")

                    ans_a6 = st.radio("6. Cuando recibe instrucciones de un superior, usted:", [
                        "🔵 Toma nota y verifica que haya entendido correctamente.",
                        "🔴 Busca la manera más eficiente de ejecutarlas.",
                        "🟢 Las sigue paso a paso como fueron indicadas.",
                        "🟡 Hace preguntas y conversa para aclarar el contexto."
                    ], index=None, key="adm_6")

                    ans_a7 = st.radio("7. Si un compañero le solicita ayuda mientras está ocupado, usted:", [
                        "🔵 Le ayuda después de terminar la tarea prioritaria.",
                        "🔴 Resuelve rápidamente ambas situaciones.",
                        "🟢 Busca apoyarlo sin afectar el trabajo del equipo.",
                        "🟡 Le brinda apoyo inmediato para mantener una buena relación."
                    ], index=None, key="adm_7")

                    ans_a8 = st.radio("8. Al recibir instrucciones poco claras, usted:", [
                        "🔵 Solicita detalles y confirma los criterios de trabajo.",
                        "🔴 Toma la iniciativa y avanza con la información disponible.",
                        "🟢 Consulta con el responsable para evitar errores.",
                        "🟡 Conversar con varias personas para entender el contexto."
                    ], index=None, key="adm_8")

                    ans_a9 = st.radio("9. ¿Cómo prefiere trabajar?", [
                        "🔵 Con procesos claros y objetivos definidos.",
                        "🔴 Con autonomía para tomar decisiones.",
                        "🟢 En un ambiente estable y colaborativo.",
                        "🟡 En interacción constante con otras personas."
                    ], index=None, key="adm_9")

                    ans_a10 = st.radio("10. Si debe aprender un nuevo sistema administrativo, usted:", [
                        "🔵 Estuda el manual y practica hasta dominarlo.",
                        "🔴 Explora el sistema y aprende haciendo.",
                        "🟢 Prefiere capacitación guiada y apoyo continuo.",
                        "🟡 Aprende interactuando con otros usuarios."
                    ], index=None, key="adm_10")

                    respuestas_lista = [ans_a1, ans_a2, ans_a3, ans_a4, ans_a5, ans_a6, ans_a7, ans_a8, ans_a9, ans_a10]

                else:
                    st.markdown("### 🎯 Cuestionario Estratégico y de Alta Dirección")
                    ans_e1 = st.radio("1. Cuando debe tomar una decisión que impacta a toda el área, usted:", [
                        "🔴 Decide rápidamente con la información disponible.",
                        "🟡 Busca alinear a las personas involucradas antes de decidir.",
                        "🟢 Analiza cómo afectará al equipo a largo plazo.",
                        "🔵 Revisa datos, riesgos y escenarios antes de actuar."
                    ], index=None, key="est_1")

                    ans_e2 = st.radio("2. Ante una meta corporativa muy desafiante, usted:", [
                        "🔴 Asume el reto y establece acciones inmediatas.",
                        "🟡 Motiva al equipo para lograr el objetivo.",
                        "🟢 Organiza al equipo para mantener el enfoque.",
                        "🔵 Diseña un plan detallado con indicadores de seguimiento."
                    ], index=None, key="est_2")

                    ans_e3 = st.radio("3. Cuando una estrategia no está dando resultados, usted:", [
                        "🔴 Cambia el rumbo rápidamente.",
                        "🟡 Busca nuevas ideas con el equipo.",
                        "🟢 Evalúa el impacto sobre las personas antes de actuar.",
                        "🔵 Analiza las causas y ajusta el plan."
                    ], index=None, key="est_3")

                    ans_e4 = st.radio("4. ¿Qué considera más importante en un líder?", [
                        "🔴 Capacidad de decisión.",
                        "🟡 Capacidad de inspirar.",
                        "🟢 Capacidad de apoyar al equipo.",
                        "🔵 Capacidad de planificar y controlar."
                    ], index=None, key="est_4")

                    ans_e5 = st.radio("5. Cuando surge un conflicto entre dos líderes de su equipo:", [
                        "🔴 Intervengo y tomo una decisión.",
                        "🟡 Facilito una conversación para lograr acuerdos.",
                        "🟢 Busco preservar la armonía del equipo.",
                        "🔵 Analizo objetivamente los hechos antes de actuar."
                    ], index=None, key="est_5")

                    ans_e6 = st.radio("6. Frente a un cambio organizacional importante:", [
                        "🔴 Lo impulso rápidamente.",
                        "🟡 Comunico los beneficios para generar compromiso.",
                        "🟢 Acompaño al equipo durante la transición.",
                        "🔵 Desarrollo un plan estructurado de implementación."
                    ], index=None, key="est_6")

                    ans_e7 = st.radio("7. Cuando tiene que presentar una propuesta a la alta dirección:", [
                        "🔴 Destaco el impacto en los resultados.",
                        "🟡 Me enfoco en persuadir y generar aceptación.",
                        "🟢 Explico cómo beneficiará a las personas.",
                        "🔵 Presento indicadores, análisis y evidencias."
                    ], index=None, key="est_7")

                    ans_e8 = st.radio("8. Si debe elegir entre rapidez y precisión:", [
                        "🔴 Priorizo la rapidez para aprovechar oportunidades.",
                        "🟡 Busco un equilibrio mediante la colaboración.",
                        "🟢 Priorizo la estabilidad y continuidad.",
                        "🔵 Priorizo la precisión para minimizar riesgos."
                    ], index=None, key="est_8")

                    ans_e9 = st.radio("9. ¿Qué lo motiva más profesionalmente?", [
                        "🔴 Alcanzar resultados superiores.",
                        "🟡 Influir y generar impacto en otros.",
                        "🟢 Construir equipos sólidos y estables.",
                        "🔵 Mejorar procesos y garantizar calidad."
                    ], index=None, key="est_9")

                    ans_e10 = st.radio("10. Si un proyecto estratégico está en riesgo de incumplimiento:", [
                        "🔴 Tomo control directo del proyecto.",
                        "🟡 Reúno a los involucrados para encontrar soluciones.",
                        "🟢 Refuerzo el apoyo y seguimiento al equipo.",
                        "🔵 Reviso indicadores y causas para ajustar el plan."
                    ], index=None, key="est_10")

                    ans_e11 = st.radio("11. Cuando recibe una meta corporativa ambiciosa, su primera reacción es:", [
                        "🔴 Definir acciones inmediatas para alcanzarla.",
                        "🟡 Reunir al equipo para transmitir entusiasmo y compromiso.",
                        "🟢 Evaluar cómo impactará al equipo y los recursos disponibles.",
                        "🔵 Analizar indicadores, riesgos y viabilidad antes de actuar."
                    ], index=None, key="est_11")

                    ans_e12 = st.radio("12. Si un colaborador de alto desempeño tiene problemas de actitud, usted:", [
                        "🔴 Lo confronta directamente para corregir la situación.",
                        "🟡 Conversa con él para influir positivamente en su comportamiento.",
                        "🟢 Busca comprender las causas y apoyarlo.",
                        "🔵 Documenta los hechos y aplica el procedimiento correspondiente."
                    ], index=None, key="est_12")

                    ans_e13 = st.radio("13. Frente a un proyecto con información incompleta:", [
                        "🔴 Avanza con los datos disponibles y ajusta en el camino.",
                        "🟡 Consulta diferentes opiniones para construir una visión más amplia.",
                        "🟢 Espera información adicional para reducir incertidumbre.",
                        "🔵 Solicita información técnica antes de tomar decisiones."
                    ], index=None, key="est_13")

                    ans_e14 = st.radio("14. Cuando lidera reuniones estratégicas, normalmente:", [
                        "🔴 Mantiene el enfoque en decisiones y resultados.",
                        "🟡 Promueve la participación activa de todos.",
                        "🟢 Busca consenso antes de avanzar.",
                        "🔵 Se enfoca en datos, análisis y seguimiento."
                    ], index=None, key="est_14")

                    ans_e15 = st.radio("15. Si la alta dirección cambia una estrategia ya aprobada:", [
                        "🔴 Reorganiza rápidamente las acciones del equipo.",
                        "🟡 Comunica el cambio de forma positiva y motivadora.",
                        "🟢 Acompaño al equipo para facilitar la adaptación.",
                        "🔵 Revisa el impacto y redefine el plan de ejecución."
                    ], index=None, key="est_15")

                    ans_e16 = st.radio("16. ¿Qué considera más importante para alcanzar resultados sostenibles?", [
                        "🔴 La velocidad de ejecución.",
                        "🟡 El compromiso de las personas.",
                        "🟢 La estabilidad de los procesos.",
                        "🔵 La planificación y el control."
                    ], index=None, key="est_16")

                    ans_e17 = st.radio("17. Cuando identifica una oportunidad de mejora importante:", [
                        "🔴 La implementa cuanto antes.",
                        "🟡 Busca apoyo y aceptación de los involucrados.",
                        "🟢 Evalúa cómo afectará la dinámica actual.",
                        "🔵 Realiza un análisis previo de impacto y riesgos."
                    ], index=None, key="est_17")

                    ans_e18 = st.radio("18. Ante un desacuerdo con otro líder de la organización:", [
                        "🔴 Defiende firmemente su posición.",
                        "🟡 Busca persuadir mediante el diálogo.",
                        "🟢 Procura mantener una relación armoniosa.",
                        "🔵 Basa su posición en hechos y evidencias."
                    ], index=None, key="est_18")

                    ans_e19 = st.radio("19. ¿Cómo mide el éxito de su gestión?", [
                        "🔴 Por el cumplimiento de metas y resultados.",
                        "🟡 Por la influencia positiva que genera en otros.",
                        "🟢 Por la estabilidad y compromiso del equipo.",
                        "🔵 Por la eficiencia y calidad de los procesos."
                    ], index=None, key="est_19")

                    ans_e20 = st.radio("20. Si debe elegir a un sucesor para su cargo, valoraría principalmente:", [
                        "🔴 Su capacidad para asumir retos y tomar decisiones.",
                        "🟡 Su habilidad para liderar personas.",
                        "🟢 Su compromiso y confiabilidad.",
                        "🔵 Su capacidad analítica y organización."
                    ], index=None, key="est_20")

                    ans_e21 = st.radio("21. En una crisis organizacional, usted suele:", [
                        "🔴 Tomar decisiones rápidas y asumir el liderazgo.",
                        "🟡 Mantener al equipo informado y motivado.",
                        "🟢 Brindar estabilidad y apoyo al equipo.",
                        "🔵 Analizar información para minimizar riesgos."
                    ], index=None, key="est_21")

                    ans_e22 = st.radio("22. ¿Qué describe mejor su estilo de liderazgo?", [
                        "🔴 Exigente y orientado a resultados.",
                        "🟡 Inspirador y comunicativo.",
                        "🟢 Cercano y colaborativo.",
                        "🔵 Metódico y orientado a procesos."
                    ], index=None, key="est_22")

                    respuestas_lista = [ans_e1, ans_e2, ans_e3, ans_e4, ans_e5, ans_e6, ans_e7, ans_e8, ans_e9, ans_e10, ans_e11, ans_e12, ans_e13, ans_e14, ans_e15, ans_e16, ans_e17, ans_e18, ans_e19, ans_e20, ans_e21, ans_e22]

                st.markdown("---")
                
                if st.button("📤 Finalizar y Enviar Evaluación", type="primary", use_container_width=True):
                    if not all(x is not None for x in respuestas_lista):
                        st.warning("⚠️ Debes seleccionar una respuesta para cada una de las preguntas antes de enviar.")
                    else:
                        puntos_finales = {"D": 0.0, "I": 0.0, "S": 0.0, "C": 0.0}
                        total_preguntas = len(respuestas_lista)
                        peso_pregunta = 100.0 / total_preguntas

                        for r in respuestas_lista:
                            if "🔴" in r: puntos_finales["D"] += peso_pregunta
                            elif "🟡" in r: puntos_finales["I"] += peso_pregunta
                            elif "🟢" in r: puntos_finales["S"] += peso_pregunta
                            elif "🔵" in r: puntos_finales["C"] += peso_pregunta

                        puntos_finales = {k: int(round(v)) for k, v in puntos_finales.items()}
                        suma_comprobacion = sum(puntos_finales.values())
                        if suma_comprobacion != 100 and suma_comprobacion > 0:
                            factor_max = max(puntos_finales, key=puntos_finales.get)
                            puntos_finales[factor_max] += (100 - suma_comprobacion)
                        
                        factor_dominant = max(puntos_finales, key=puntos_finales.get)
                        textos_disc = {
                            "D": ("🔴 Perfil Directo, Conductor y Competitivo.", "Posee una altísima orientación a resultados y resolución de problemas bajo presión. No teme asumir riesgos estratégicos y empujará al equipo a cumplir metas exigentes de inmediato."),
                            "I": ("🟡 Perfil Persuasivo, Comunicativo y Relacional.", "Tiene una capacidad nata para conectar con personas, liderar equipos mediante la motivación y articular relaciones humanas fluidas, asegurando un clima de entusiasmo."),
                            "S": ("🟢 Perfil Confiable, Paciente y Estable.", "Aporta lealtad, consistencia y un alto sentido del orden a procesos a largo plazo. Trabaja con serenidad en situaciones críticas y garantiza que las tareas rutinarias se completen con total constancia."),
                            "C": ("🔵 Perfil Analítico, Riguroso y Preciso.", "Su enfoque se basa en la calidad, la exactitud y el cumplimiento normativo. Minimiza los márgenes de error a cero, siendo excelente para la planeación técnica estructurada.")
                        }
                        
                        titulo_v, porque_v = textos_disc[factor_dominant]
                        veredicto_completo = f"{titulo_v} | {porque_v}"
                        supabase.table("candidatos").update({
                            "disc_d": puntos_finales["D"],
                            "disc_i": puntos_finales["I"],
                            "disc_s": puntos_finales["S"],
                            "disc_c": puntos_finales["C"],
                            "disc_veredicto": veredicto_completo
                        }).eq("Cédula", str(cedula_url)).execute()
                        
                        st.session_state.evaluacion_enviada = True
                        st.rerun()