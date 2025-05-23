# Faculty Network Analysis & Visualization

Una visualización interactiva de red que revela los patrones de colaboración, influencia y conectividad entre los miembros del cuerpo docente universitario mediante técnicas avanzadas de web scraping y análisis de redes sociales.

![Network Preview](https://img.shields.io/badge/D3.js-Interactive-orange) ![Data Source](https://img.shields.io/badge/Data-Web%20Scraped-blue) ![Status](https://img.shields.io/badge/Status-Active-green)

## Características Principales

- **Visualización Interactiva**: Red de fuerza dirigida con zoom, pan y drag
- **Análisis Multi-dimensional**: Métricas de centralidad, clustering y PageRank
- **Identificación de Patrones**: Detección automática de colaboradores clave y puentes departamentales
- **Datos en Tiempo Real**: Web scraping automatizado para datos actualizados
- **Interfaz Intuitiva**: Dashboard con estadísticas y insights expandibles

## Preguntas de Investigación

Este proyecto está diseñado para responder **4 preguntas fundamentales** sobre la estructura de colaboración académica:

### 1. **¿Quiénes son los colaboradores más prolíficos?**
- **Métrica**: Grado de centralidad (degree centrality)
- **Insight**: Identifica profesores con el mayor número de conexiones directas
- **Aplicación**: Localizar hubs de colaboración y mentores potenciales

### 2. **¿Qué profesores actúan como puentes entre departamentos?**
- **Métrica**: Centralidad de intermediación (betweenness centrality)
- **Insight**: Revela académicos que conectan grupos departamentales aislados
- **Aplicación**: Identificar facilitadores de colaboración interdisciplinaria

### 3. **¿Quiénes son los miembros más influyentes del cuerpo docente?**
- **Métrica**: Combinación de PageRank y H-index
- **Insight**: Equilibra conectividad de red con impacto académico
- **Aplicación**: Reconocer líderes de opinión y investigadores de elite

### 4. **¿Qué departamentos tienen la colaboración interna más fuerte?**
- **Métrica**: Coeficiente de clustering promedio
- **Insight**: Mide la densidad de conexiones dentro de cada departamento
- **Aplicación**: Evaluar cohesión departamental y cultura colaborativa

## Arquitectura Técnica

### Stack Tecnológico
```
Frontend:  D3.js + Vanilla JavaScript
Backend:   Python (Web Scraping)
Data:      JSON API endpoint
Análisis:  NetworkX + Custom algorithms
```

### Componentes Principales

#### **Visualización de Red** (`network-viz.js`)
- **Force-directed layout** con simulación física
- **Nodos escalables** basados en métricas de centralidad
- **Enlaces ponderados** por frecuencia de colaboración
- **Colores departamentales** para identificación visual
- **Imágenes de perfil** integradas cuando están disponibles

#### **Panel de Análisis** (`analysis-panel.js`)
- **Cálculos en tiempo real** de métricas de red
- **Rankings dinámicos** para cada pregunta de investigación
- **Tablas interactivas** con datos expandibles
- **Estadísticas globales** de la red

#### **Web Scraping Engine**
- **Extracción automatizada** de perfiles docentes
- **Detección de colaboraciones** via publicaciones conjuntas
- **Enriquecimiento de datos** con métricas académicas
- **Actualización programada** de datasets

## Métricas Implementadas

| Métrica | Descripción | Aplicación |
|---------|-------------|------------|
| **Degree Centrality** | Número de conexiones directas | Identificar super-conectores |
| **Betweenness Centrality** | Posición como intermediario | Localizar brokers de conocimiento |
| **PageRank** | Influencia basada en la calidad de conexiones | Medir prestigio académico |
| **Clustering Coefficient** | Densidad de conexiones locales | Evaluar cohesión departamental |
| **H-Index** | Impacto de publicaciones | Complementar métricas de red |

## Diseño Visual

### Codificación de Información
- **Tamaño de nodo**: Proporcional al grado de centralidad
- **Color de nodo**: Departamento de afiliación
- **Grosor de enlace**: Fuerza de colaboración
- **Transparencia**: Peso de la conexión

### Interactividad
- **Zoom/Pan**: Navegación fluida por la red
- **Drag & Drop**: Reposicionamiento manual de nodos
- **Hover tooltips**: Información detallada instantánea
- **Click panels**: Expansión de análisis específicos

## 🔍 Insights Descubiertos

### Patrones Emergentes
1. **Colaboración Interdisciplinaria**: Los puentes departamentales tienden a ser profesores senior con múltiples afiliaciones
2. **Clusters de Investigación**: Formación natural de grupos de investigación visibles en la topología de red
3. **Influencia vs Conectividad**: No siempre coinciden los académicos más conectados con los más influyentes
4. **Jerarquías Implícitas**: La estructura de red revela jerarquías no oficiales en la institución

### Casos de Uso
- **Planificación Estratégica**: Identificar oportunidades de colaboración
- **Desarrollo de Talento**: Localizar mentores y colaboradores ideales
- **Evaluación Institucional**: Medir salud de la colaboración académica
- **Networking Académico**: Facilitar conexiones estratégicas

### Estructura de Archivos
```
📁 app/
├── 📁 static
    └── 📄 script.js
    └── 📄 tasks.js 
    └── 🖼️ uteclogo.png
├── 📁 templates
    └── 📄 index.html
├── 📄 app.py
├── 📄 faculty_network.json
```
