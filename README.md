# UL_Tablero_2026
Ejemplo sobre cómo utilizar widgets en los tableros.

## El Mundo Gestalt
Tablero en Streamlit, con estética de bloques (pixel art), que explica los 7 principios de la Gestalt aplicados a la visualización de datos:

| # | Principio | Demo interactiva | Widget ipywidgets recomendado |
|---|-----------|------------------|-------------------------------|
| 1 | Cierre | Anillo de KPI al que se le quitan bloques | `IntSlider` |
| 2 | Proximidad | Barras agrupadas por bioma o mineral | `ToggleButtons` |
| 3 | Continuidad | Ranking de túneles ordenado, con rieles | `Dropdown` |
| 4 | Semejanza | Dispersión de vetas con color y resaltado | `ColorPicker` |
| 5 | Figura y fondo | Líneas con una mina al frente y el resto como contexto | `FloatSlider` |
| 6 | Dirección común | Animación de una manada y gráfico de pendiente | `Play` |
| 7 | Simetría | Gráfico de mariposa en espejo | `ToggleButton` |

Cada sección incluye el código del widget de **ipywidgets** para usarlo en un notebook de Jupyter, y su equivalente en Streamlit.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Referencias: [Plain Concepts · Visualización de datos](https://www.plainconcepts.com/es/visualizacion-datos-guia-ejemplos/) · [ipywidgets](https://pypi.org/project/ipywidgets/)
