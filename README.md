# Como influyo el tiempo de posesion en el rendimiento de los equipos en las 5 grandes ligas europeas de futbol durante la temporada 2017/2018

En este veremos como influyo la posesion en el rendimiento de los equipos de la primera division española, alemana, italiana, y francesa

## Objetivo general
Determinar la relación entre el porcentaje de tiempo de posesión del balón y la cantidad de puntos obtenidos por los equipos de las 5 grandes ligas europeas durante la temporada 2017/2018.


### Objetivos espeficicos 
-Recopilar y organizar los datos correspondientes al porcentaje promedio de posesión y los puntos totales acumulados al final de la temporada por cada equipo involucrado.

-Calcular las medidas de tendencia central y de dispersión tanto para la posesión de balón como para los puntos, con el fin de entender cómo se distribuyen los datos en cada competición.

-Analizar la correlación entre la variable independiente (posesión) y la variable dependiente (puntos) utilizando coeficientes estadísticos (como el coeficiente de correlación de Pearson).

-Comparar los resultados de dicha correlación entre la Premier League, La Liga, Serie A, Bundesliga y Ligue 1 para identificar en cuál de estas competiciones la posesión se tradujo en una mayor rentabilidad de puntos.

# Stack tecnologico
- Python / pandas
- Duckdb
- Sqlite3
- Streamlit
- PowerBI

# Fuente de datos
El dataset original se encuentra alojado en [Kaggle](https://www.kaggle.com/datasets/aleespinosa/soccer-match-event-dataset/data) en formato .csv. Como parte de las buenas prácticas del proyecto y para reducir significativamente la huella de almacenamiento, los datos han sido procesados y exportados a formato .parquet.

# Alojamiento de datos
Los archivos resultantes están centralizados y pueden ser accedidos a través del siguiente directorio de [Google Drive]().

## Uso local del proyecto
Preinicializacion del proyecto
```bash
py ./preinitialize.py
```
### Dashboard
1. Clonar el repositorio
```bash
git clone https://github.com/DosiDeveloper/perfomance-by-posession-5bigfive-europeansleague.git
cd  perfomance-by-posession-5bigfive-europeansleague
```
2. Instalar dependencias
```bash
pip install -r requirements.txt
```
3. Correr el dashboard
```bash
py ./app.py
```
### PowerBI

> En desarrollo
