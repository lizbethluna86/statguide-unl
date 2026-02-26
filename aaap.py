import streamlit as st
import graphviz

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Asistente Estadístico Posgrado", layout="wide", page_icon="🎓")

st.title("🎓 Asistente Estadístico para Estudiantes de Posgrado")
st.markdown("""
**Maestría en Restauración de Paisajes Tropicales - UNL**
Esta herramienta te guía en la selección de análisis estadísticos y visualización de datos, 
cubriendo enfoques ecológicos, socioeconómicos y de síntesis de información.
""")

# --- BARRA LATERAL: DIAGNÓSTICO ---
st.sidebar.header("1. Diagnóstico de Investigación")

categoria_principal = st.sidebar.selectbox(
    "Selecciona la categoría general de tu estudio:",
    [
        "Selecciona una opción...",
        "Enfoque Ecológico / Biofísico",
        "Enfoque Socioeconómico",
        "Revisión Sistemática de Literatura",
        "Sistematización de Experiencias"
    ]
)

# Variables globales para resultados
titulo_res = ""
definicion = ""
ejemplo = ""
diseno_res = ""
estadistica = ""
graficos = ""
supuestos_info = ""
prompt_context = ""

# ==============================================================================
# LÓGICA: ENFOQUE ECOLÓGICO
# ==============================================================================
if categoria_principal == "Enfoque Ecológico / Biofísico":
    sub_enfoque = st.sidebar.radio(
        "¿Cuál es el alcance de tu estudio ecológico?",
        ["Descriptivo", "Correlacional", "Explicativo"]
    )

    # --- 1.1 DESCRIPTIVO ---
    if sub_enfoque == "Descriptivo":
        titulo_res = "Estudio Ecológico Descriptivo"
        definicion = """
        Busca caracterizar y documentar patrones biofísicos sin analizar relaciones causales. 
        Responde principalmente a preguntas del tipo: **¿qué hay?, ¿cuánto hay?, ¿cómo es?**. 
        En estos estudios se usan inventarios forestales, mediciones de biodiversidad, análisis de cobertura, etc.
        """
        ejemplo = """
        **Pregunta:** ¿Cuál es la composición florística y la estructura diamétrica de un bosque secundario en la Amazonía ecuatoriana?
        \n**Diseño:** Parcelas temporales o permanentes, medición de DAP, identificación taxonómica, cálculo de abundancia y área basal.
        """
        estadistica = """
        **Medidas de Tendencia Central y Dispersión:**
        *   Media (promedio), Mediana (dato central), Moda.
        *   Desviación Estándar (dispersión), Error Estándar, Coeficiente de Variación.
        *   **Índices de Diversidad:** Shannon-Wiener (H'), Simpson (D), Riqueza de especies (S).
        *   **Estructura:** Distribución de frecuencias (clases diamétricas), Área Basal (m²/ha).
        """
        graficos = """
        *   Histogramas (para distribución diamétrica - J invertida).
        *   Gráficos de Barras (Abundancia por familia/especie).
        *   Curvas de Acumulación de Especies (para evaluar esfuerzo de muestreo).
        *   Diagramas de perfil de vegetación.
        """
        prompt_context = "Estudio descriptivo de estructura forestal y diversidad."

    # --- 1.2 CORRELACIONAL ---
    elif sub_enfoque == "Correlacional":
        titulo_res = "Estudio Ecológico Correlacional"
        definicion = """
        Analiza la asociación estadística entre variables ecológicas, sin establecer causalidad directa. 
        Responde a: **¿existe relación entre X e Y?**.
        """
        ejemplo = """
        **Pregunta:** ¿Cómo se relacionan la fragmentación del paisaje, la conectividad ecológica y la riqueza de aves en bosques tropicales?
        \n**Diseño:** Métricas de paisaje (p.ej., tamaño de parche, índice de conectividad), monitoreo de aves, modelos lineales generalizados.
        """
        estadistica = """
        **Análisis de Correlación:**
        1.  **Correlación de Pearson (r):** Úsala si ambas variables son cuantitativas, tienen distribución normal y la relación es lineal.
        2.  **Correlación de Spearman (rho):** Úsala si los datos no son normales (no paramétricos) o la relación es monótona pero no lineal.
        
        **Ejemplo sencillo:**
        *   *Variables:* Altura del árbol (m) vs. Diámetro (DAP en cm).
        *   *Hipótesis:* A mayor diámetro, mayor altura (correlación positiva).
        *   *Interpretación:* Un valor cercano a +1 indica una relación fuerte positiva; cercano a 0 indica que no hay relación lineal.
        """
        graficos = """
        *   **Scatterplot (Gráfico de dispersión):** Eje X = Variable 1, Eje Y = Variable 2. Añadir línea de tendencia.
        *   **Correlograma (Matriz de correlación):** Para visualizar relaciones entre múltiples variables a la vez (colores intensos = mayor correlación).
        """
        prompt_context = "Estudio correlacional entre variables ecológicas (ej. DAP vs Altura)."

    # --- 1.3 EXPLICATIVO ---
    elif sub_enfoque == "Explicativo":
        titulo_res = "Estudio Ecológico Explicativo"
        definicion = """
        Busca identificar relaciones causales o mecanismos ecológicos subyacentes. 
        Responde a: **¿por qué ocurre X?, ¿qué efecto tiene Y sobre Z?**. 
        Frecuentemente emplea diseños experimentales, cuasi-experimentales o modelación ecológica.
        """
        ejemplo = """
        **Pregunta:** ¿Qué efecto tiene la intensidad de aprovechamiento forestal sobre la tasa de crecimiento residual del bosque?
        \n**Diseño:** Comparación entre parcelas con distinta intensidad de corta; análisis de varianza o modelos mixtos.
        """
        
        # Sub-menú para detalles del diseño experimental
        st.sidebar.markdown("---")
        tipo_experimento = st.sidebar.radio("Detalle del diseño experimental:", ["Comparar 2 grupos", "Comparar más de 2 grupos"])
        
        if tipo_experimento == "Comparar 2 grupos":
            estadistica = """
            **Comparación de dos medias:**
            *   **Prueba t de Student:** Usar si se cumple normalidad y homogeneidad de varianzas.
                *   *Nota sobre la muestra:* Se recomienda n > 30 por grupo para invocar el Teorema del Límite Central, aunque la prueba es robusta. Si n < 30, la normalidad es estricta.
            *   **Prueba U de Mann-Whitney (Wilcoxon):** Alternativa no paramétrica si NO hay normalidad.
            """
        else:
            estadistica = """
            **Comparación de más de 2 medias (ANOVA):**
            *   **DCA (Diseño Completamente al Azar):** Un solo factor, unidades homogéneas. (ANOVA de una vía).
            *   **DBCA (Bloques Completos al Azar):** Si hay un gradiente de ruido (ej. pendiente), se agrupan las unidades en bloques. El bloque entra como factor en el modelo.
            *   **Cuadrado Latino:** Si hay dos gradientes de ruido perpendiculares (ej. fertilidad y luz). Se controla por filas y columnas.
            """

        graficos = """
        *   **Boxplot (Diagrama de Cajas):** Para ver medianas y dispersión.
        *   **Gráfico de Medias con Error Estándar (Barplot + Error bars):** Clásico para publicaciones.
        *   **Gráfico de Violín:** Muestra la densidad de los datos.
        """
        
        supuestos_info = """
        **1. Normalidad (Los residuos deben seguir una curva de campana):**
        *   *Prueba:* Shapiro-Wilk (n < 50) o Kolmogorov-Smirnov.
        *   *¿Qué hacer si falla?* Transformar datos (Log, Raíz cuadrada) o usar pruebas No Paramétricas (Kruskal-Wallis / Mann-Whitney).

        **2. Homocedasticidad (Varianzas iguales entre grupos):**
        *   *Prueba:* Levene o Bartlett.
        *   *¿Qué hacer si falla?* Usar **ANOVA de Welch** (no asume varianzas iguales) o Modelos Lineales Generalizados (GLS).

        **3. Independencia de los datos:**
        *   *Violación común:* Autocorrelación espacial (parcelas muy juntas se parecen más) o temporal (medidas repetidas en el mismo árbol).
        *   *Solución:* Si hay dependencia espacial, usar Estadística Espacial. Si hay medidas repetidas, usar **ANOVA de Medidas Repetidas** o Modelos Mixtos.
        """
        prompt_context = f"Diseño experimental explicativo ({tipo_experimento})."

# ==============================================================================
# LÓGICA: OTROS ENFOQUES (Resumidos para mantener el foco en lo nuevo)
# ==============================================================================
elif categoria_principal == "Enfoque Socioeconómico":
    titulo_res = "Análisis Socioeconómico"
    definicion = "Análisis de encuestas y variables sociales."
    estadistica = """
    *   **Variable Cuantitativa:** Regresión Lineal Múltiple.
    *   **Variable Binaria (Sí/No):** Regresión Logística (Logit/Probit).
    *   **Variable Nominal (>2 cat):** Regresión Multinomial.
    *   **Datos Anidados:** Modelos Multinivel (Familias dentro de Comunidades).
    """
    graficos = "Scatterplots, Gráficos de Mosaico, Curvas ROC."
    prompt_context = "Análisis de encuestas socioeconómicas."

elif categoria_principal == "Revisión Sistemática de Literatura":
    titulo_res = "Revisión Sistemática"
    definicion = "Síntesis de evidencia científica existente."
    estadistica = """
    *   **PICOC:** (Población, Intervención, Comparación, Outcome, Contexto).
    *   **PCC:** (Población, Concepto, Contexto).
    *   **Marcos de reporte:** PRISMA (General) o ROSES (Medio ambiente).
    """
    graficos = "Diagrama de Flujo PRISMA, Mapas bibliométricos (VOSviewer)."
    prompt_context = "Revisión sistemática de literatura."

elif categoria_principal == "Sistematización de Experiencias":
    titulo_res = "Sistematización de Experiencias"
    definicion = "Interpretación crítica de procesos vividos."
    estadistica = "Metodologías cualitativas: Oscar Jara (5 tiempos), Acosta & Glaser."
    graficos = "Líneas de tiempo, Mapas de actores, Diagramas de flujo."
    prompt_context = "Sistematización de experiencias cualitativa."

# ==============================================================================
# VISUALIZACIÓN DE RESULTADOS
# ==============================================================================

if categoria_principal != "Selecciona una opción...":
    st.header(f"📌 {titulo_res}")
    
    # Definición y Ejemplo
    with st.container():
        col_def, col_ex = st.columns(2)
        with col_def:
            st.info(f"**Definición:**\n{definicion}")
        with col_ex:
            if ejemplo:
                st.success(f"**Ejemplo en Restauración:**\n{ejemplo}")

    st.markdown("---")

    # Estadística y Gráficos
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("🧮 Herramientas Estadísticas")
        st.markdown(estadistica)
        
        # Mostrar supuestos solo si existen (Caso Explicativo)
        if supuestos_info:
            with st.expander("⚠️ Verificación de Supuestos y Soluciones (Importante)", expanded=True):
                st.markdown(supuestos_info)
    
    with col2:
        st.subheader("📊 Gráficos Recomendados")
        st.warning(graficos)

    # Diagrama de flujo
    st.markdown("---")
    st.subheader("🗺️ Mapa de Decisión")
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR')
    graph.node('A', 'Inicio')
    graph.node('B', categoria_principal)
    graph.edge('A', 'B')
    if categoria_principal == "Enfoque Ecológico / Biofísico":
        graph.node('C', sub_enfoque)
        graph.edge('B', 'C')
    st.graphviz_chart(graph)

    # Prompt Generator
    st.markdown("---")
    st.subheader("🤖 Generador de Prompt para IA")
    st.markdown("Copia este texto en ChatGPT/Claude para obtener tu código en R:")
    
    final_prompt = f"""
    Actúa como un estadístico experto en ecología forestal y restauración.
    Estoy realizando un {titulo_res}.
    Contexto: {prompt_context}.
    
    Por favor genera código en R (usando tidyverse y ggplot2) para:
    1. Generar un dataset simulado que sirva de ejemplo.
    2. Realizar el análisis estadístico sugerido: {estadistica.split(':')[0] if ':' in estadistica else 'Análisis pertinente'}.
    3. Si es explicativo, incluye código para verificar supuestos (Shapiro, Levene) y qué hacer si fallan.
    4. Crear gráficos de alta calidad tipo: {graficos.replace('*', '').split(',')[0]}.
    """
    st.code(final_prompt, language='text')

else:
    st.info("👈 Por favor, selecciona una categoría en el menú de la izquierda para comenzar.")
