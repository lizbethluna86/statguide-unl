import streamlit as st
import graphviz

# Configuración de la página
st.set_page_config(page_title="StatGuide: Restauración UNL", layout="wide")

# Título y Contexto
st.title("🌿 StatGuide: Asistente Estadístico para Restauración de Paisajes")
st.markdown("""
Esta herramienta basada en lógica de decisión ayuda a los estudiantes de la **Maestría en Restauración de Paisajes Tropicales (UNL)** 
a seleccionar el análisis estadístico y la visualización de datos adecuada para sus tesis.
""")

# --- BARRA LATERAL: DIAGNÓSTICO ---
st.sidebar.header("1. Diagnóstico de tu Investigación")

tipo_estudio = st.sidebar.selectbox(
    "¿Cuál es el enfoque principal de tu investigación?",
    ["Selecciona una opción", 
     "Experimental (Tratamientos/Comparación de Grupos)", 
     "Observacional / Encuestas Socioeconómicas", 
     "Revisión Sistemática de Literatura",
     "Sistematización de Experiencias"]
)

# Lógica condicional anidada (El motor de IA simbólica)
resultado = None
grafico_desc = None
grafico_adv = None
consejo = None

if tipo_estudio == "Experimental (Tratamientos/Comparación de Grupos)":
    st.sidebar.markdown("---")
    tipo_var = st.sidebar.radio("¿Tu variable respuesta (lo que mides) es:", ["Numérica Continua (ej. Altura, Biomasa)", "Conteo/Discreta (ej. Número de plántulas)", "Categórica (ej. Vivo/Muerto)"])
    
    if tipo_var == "Numérica Continua":
        grupos = st.sidebar.radio("¿Cuántos grupos estás comparando?", ["Dos grupos (ej. Control vs Tratamiento)", "Más de dos grupos (ej. 3 tipos de sustrato)"])
        distribucion = st.sidebar.radio("¿Tus datos siguen una distribución normal?", ["Sí (Paramétrico)", "No / No sé (No Paramétrico)"])
        
        if grupos == "Dos grupos":
            if distribucion == "Sí (Paramétrico)":
                resultado = "Prueba T de Student (t-test)"
                grafico_desc = "Gráfico de Barras con error estándar (clásico) o Boxplot."
                grafico_adv = "Raincloud Plot (Nube de lluvia): Combina distribución, caja y puntos crudos."
            else:
                resultado = "U de Mann-Whitney (Wilcoxon rank-sum)"
                grafico_desc = "Boxplot (Diagrama de Caja)."
                grafico_adv = "Violin Plot: Muestra la densidad de los datos mejor que la caja."
        else: # Más de 2 grupos
            if distribucion == "Sí (Paramétrico)":
                resultado = "ANOVA de una vía (o factorial si hay más factores)"
                grafico_desc = "Gráfico de Medias con Intervalos de Confianza (IC 95%)."
                grafico_adv = "Gráfico de Interacción (si hay 2 factores) o Post-hoc letter display."
            else:
                resultado = "Kruskal-Wallis"
                grafico_desc = "Boxplot agrupado."
                grafico_adv = "Ridgeline Plot: Excelente para comparar distribuciones de muchos grupos."

    elif tipo_var == "Conteo/Discreta":
        resultado = "Modelos Lineales Generalizados (GLM) - Familia Poisson o Binomial Negativa"
        grafico_desc = "Gráfico de Barras de conteos."
        grafico_adv = "Rootogram (para evaluar ajuste del modelo)."

elif tipo_estudio == "Observacional / Encuestas Socioeconómicas":
    st.sidebar.markdown("---")
    objetivo = st.sidebar.selectbox("¿Qué buscas hacer?", ["Predecir una variable numérica", "Predecir una categoría (Sí/No)", "Agrupar encuestados/sitios por similitud"])
    
    if objetivo == "Predecir una variable numérica":
        resultado = "Regresión Lineal Múltiple"
        grafico_desc = "Scatterplot (Gráfico de dispersión)."
        grafico_adv = "Matriz de Correlación (Heatmap) o Gráfico de Residuos."
    elif objetivo == "Predecir una categoría (Sí/No)":
        resultado = "Regresión Logística Binaria"
        grafico_desc = "Gráfico de Mosaico (Mosaic Plot)."
        grafico_adv = "Curva ROC o Gráfico de Efectos Marginales."
    elif objetivo == "Agrupar encuestados/sitios por similitud":
        resultado = "Análisis Multivariado: PCA (Componentes Principales) o Cluster Analysis"
        grafico_desc = "Dendrograma."
        grafico_adv = "Biplot (PCA) mostrando vectores de variables y puntos de sitios."

elif tipo_estudio == "Revisión Sistemática de Literatura":
    resultado = "Meta-análisis (si hay datos) o Síntesis Narrativa"
    grafico_desc = "Diagrama de Flujo PRISMA (Obligatorio)."
    grafico_adv = "VOSviewer (Redes bibliométricas) o Nube de Palabras estructurada."

elif tipo_estudio == "Sistematización de Experiencias":
    resultado = "Análisis Cualitativo de Contenido / Triangulación"
    grafico_desc = "Línea de Tiempo (Timeline) de hitos."
    grafico_adv = "Mapas Mentales o Diagramas de Sankey (Flujo de procesos)."

# --- ÁREA PRINCIPAL: RESULTADOS ---

if tipo_estudio != "Selecciona una opción":
    st.header(f"🔍 Recomendación para: {tipo_estudio}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Análisis Sugerido")
        st.info(f"**{resultado}**")
        st.markdown(f"**¿Por qué?** Basado en tus selecciones, este análisis es el estándar para responder a tu pregunta de investigación.")
        
    with col2:
        st.subheader("📈 Visualización Recomendada")
        st.success(f"**Descriptiva:** {grafico_desc}")
        st.warning(f"**Avanzada (Publicación):** {grafico_adv}")

    # --- VISUALIZACIÓN DEL FLUJO ---
    st.markdown("---")
    st.subheader("🗺️ Tu Mapa de Decisión")
    # Creamos un grafo visual simple
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR')
    graph.node('A', 'Inicio')
    graph.node('B', tipo_estudio)
    graph.edge('A', 'B')
    if resultado:
        graph.node('C', resultado)
        graph.edge('B', 'C')
        graph.node('D', 'Gráfica: ' + grafico_adv)
        graph.edge('C', 'D')
    st.graphviz_chart(graph)

    # --- ASISTENTE DE CÓDIGO (PROMPT GENERATOR) ---
    st.markdown("---")
    st.subheader("🤖 Generador de Prompt para IA")
    st.markdown("Copia este texto y pégalo en ChatGPT, Claude o Copilot para obtener tu código en R o Python:")
    
    prompt = f"""
    Actúa como un experto en estadística ecológica. Estoy haciendo una tesis de maestría en restauración de paisajes.
    Mi diseño es: {tipo_estudio}.
    Quiero realizar un análisis de tipo: {resultado}.
    Mis datos tienen estas características: Variable respuesta numérica/categórica, comparando grupos o variables.
    Por favor, genera el código en R (usando ggplot2 y tidyverse) para:
    1. Realizar el análisis estadístico ({resultado}).
    2. Verificar supuestos (si aplica).
    3. Crear un gráfico de publicación de alta calidad tipo: {grafico_adv}.
    Usa un dataset simulado de ejemplo.
    """
    st.code(prompt, language='text')

else:
    st.info("👈 Por favor, utiliza el menú de la izquierda para configurar los parámetros de tu investigación.")
    
    # Mostrar ejemplos visuales generales
    st.markdown("### Ejemplos de lo que puedes lograr")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Experimental**")
        st.caption("Comparación de medias, supervivencia, crecimiento.")
    with col2:
        st.markdown("**Socioeconómico**")
        st.caption("Regresiones, análisis de encuestas, PCA.")
    with col3:
        st.markdown("**Revisiones**")
        st.caption("Diagramas PRISMA, mapas bibliométricos.")
