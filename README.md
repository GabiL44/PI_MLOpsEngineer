![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
![Numpy](https://img.shields.io/badge/-Numpy-333333?style=flat&logo=numpy)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-333333?style=flat&logo=matplotlib)
![Seaborn](https://img.shields.io/badge/-Seaborn-333333?style=flat&logo=seaborn)
![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-333333?style=flat&logo=scikitlearn)
![FastAPI](https://img.shields.io/badge/-FastAPI-333333?style=flat&logo=fastapi)
![Render](https://img.shields.io/badge/-Render-333333?style=flat&logo=render)

# Proyecto Individual: Machine Learning Operations (MLOps)

## Introducción

Desde Henry se nos planteó desarrolar un sistema de recomendación de videojuegos basado en datos de la plataforma Steam. Nuestro trabajo es simular el rol de un MLOps Engineer. 
Para este proyecto se nos facilitaron datos y se nos solicitó la creación de una API deployada en un servicio en la nube y la aplicación de dos modelos de Machine Learning, por un lado la recomendación de juegos a partir de la simulitud que pudieran presentar con otros juegos y/o a partir de los gustos de un usuario en particular, por otro lado un análisis de sentimiento a partir de las reviews de los usuarios.

## Sobre Steam

Steam es una plataforma de distribución digital de videojuegos desarrollada por Valve Corporation. Fue lanzada en septiembre de 2003 como una forma para Valve de proveer actualizaciones automáticas a sus juegos, pero finalmente se amplió para incluir juegos de terceros. Cuenta con más de 325 millones de usuarios y más de 25.000 juegos en su catálogo. Es importante tener en cuenta que las cifras publicadas por SteamSpy son hasta el año 2017, porque a principios de 2018 Steam limitó la forma de obtener estadísticas, por eso no hay datos tan precisos.

## Datos

Para este proyecto se proporcionaron tres archivos JSON:

* **australian_user_reviews.json** es un dataset que contiene los comentarios que los usuarios realizaron sobre los juegos que consumen, además de datos adicionales como si recomiendan o no ese juego, emoticones de gracioso y estadísticas de si el comentario fue útil o no para otros usuarios. También presenta el id del usuario que comenta con su url del perfil y el id del juego que comenta.

* **australian_users_items.json** es un dataset que contiene información sobre los juegos que juegan todos los usuarios, así como el tiempo acumulado que cada usuario jugó a un determinado juego.

* **output_steam_games.json** es un dataset que contiene datos relacionados con los juegos en sí, como los título, el desarrollador, los precios, características técnicas, etiquetas, entre otros datos.

Dentro de la carpeta [notebooks] podrán encontrar un diccionario de datos en donde se encuetran los detalles de cada una de las variables de los conjuntos de datos.

## Tareas llevadas a cabo

### Transformaciones

Se realizó la extracción, transformación y carga (ETL) de los tres conjuntos de datos entregados. Para las transformaciones se utilizó la librería Pandas.

El proceso de ETL pueden visualizarlo en [ETL_steam_games](https://github.com/GabiL44/PI_MLOpsEngineer/blob/main/notebooks/ETL_steam_games.ipynb), [ETL_user_item](https://github.com/GabiL44/PI_MLOpsEngineer/blob/main/notebooks/ETL_user_item.ipynb), [ETL_users_review](https://github.com/GabiL44/PI_MLOpsEngineer/blob/main/notebooks/ETL_users_review.ipynb)


### Feature engineering

Uno de los pedidos para este proyecto fue aplicar un análisis de sentimiento a los reviews de los usuarios. Para ello se creó una nueva columna llamada 'sentiment_analysis' que reemplaza a la columna que contiene los reviews donde clasifica los sentimientos de los comentarios con la siguiente escala:

* 0 si es malo,
* 1 si es neutral o esta sin review
* 2 si es positivo.

Se realizó un análisis de sentimiento básico utilizando TextBlob que es una biblioteca de procesamiento de lenguaje natural (NLP) en Python. El objetivo de esta metodología es asignar un valor numérico a un texto, en este caso a los comentarios que los usuarios dejaron para un juego determinado, para representar si el sentimiento expresado en el texto es negativo, neutral o positivo. 

Por otra parte, y bajo el mismo criterio de optimizar los tiempos de respuesta de las consultas en la API y teniendo en cuenta las limitaciones de almacenamiento en el servicio de nube para deployar la API, se realizaron dataframes auxiliares para cada una de las funciones solicitadas. En el mismo sentido, se guardaron estos dataframes en formato *parquet* que permite una compresión y codificación eficiente de los datos.

El proceso realizado pueden verlo en [Feature engineering](https://github.com/GabiL44/PI_MLOpsEngineer/blob/main/notebooks/Feature_Engineering.ipynb)

### Análisis exploratorio de los datos

Se realizó el EDA a los tres conjuntos de datos sometidos a ETL con el objetivo de identificar las variables que se pueden utilizar en la creación del modelo de recomendación. Para ello se utilizó la librería Pandas para la manipulación de los datos y las librerías Matplotlib y Seaborn para la visualización.

El proceso de EDA puede visualizarse en [EDA](https://github.com/GabiL44/PI_MLOpsEngineer/blob/main/notebooks/EDA.ipynb)

### Modelo de aprendizaje automático

Se crearon dos modelos de recomendación, que generan cada uno, una lista de 5 juegos ya sea ingresando el nombre de un juego o el id de un usuario.

En el primer caso, el modelo tiene una relación ítem-ítem, esto es, se toma un juego y en base a que tan similar es ese juego con el resto de los juegos se recomiendan similares. En el segundo caso, el modelo aplicar un filtro usuario-juego, es decir, toma un usuario, encuentra usuarios similares y se recomiendan ítems que a esos usuarios similares les gustaron.

El desarrollo de estos modelos pueden verlo en [Modelo_de_recomendacion](https://github.com/GabiL44/PI_MLOpsEngineer/blob/main/notebooks/Modelo_recomendacion.ipynb)

### Desarrollo de API

Para el desarrolo de la API se decidió utilizar el framework FastAPI, creando las siguientes funciones:

* **userdata**: Esta función tiene por parámentro 'user_id' y devulve la cantidad de dinero gastado por el usuario, el porcentaje de recomendaciones que realizó sobre la cantidad de reviews que se analizan y la cantidad de items que consume el mismo.

* **countreviews**: En esta función se ingresan dos fechas entre las que se quiere hacer una consulta y devuelve la cantidad de usuarios que realizaron reviews entre dichas fechas y el porcentaje de las recomendaciones positivas (True) que los mismos hicieron.

* **genre**: Esta función recibe como parámetro un género de videojuego y devuelve el puesto en el que se encuentra dicho género sobre un ranking de los mismos analizando la cantidad de horas jugadas para cada uno.

* **userforgenre**: Esta función recibe como parámetro el género de un videojuego y devuelve el top 5 de los usuarios con más horas de juego en el género ingresado, indicando el id del usuario y el url de su perfil.

* **developer**: Esta función recibe como parámetro 'developer', que es la empresa desarrolladora del juego, y devuelve la cantidad de items que desarrolla dicha empresa y el porcentaje de contenido Free por año por sobre el total que desarrolla.

* **sentiment_analysis**: Esta función recibe como parámetro el año de lanzamiento de un juego y según ese año devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento, como Negativo, Neutral y Positivo.

* **recomendacion_juego**: Esta función recibe como parámetro el nombre de un juego y devuelve una lista con 5 juegos recomendados similares al ingresado.

* **recomendacion_usuario**: Esta función recibe como parámetro el id de un usuario y devuelve una lista con 5 juegos recomendados para dicho usuario teniendo en cuenta las similitudes entre los usuarios.

> *NOTA: ambas funciones, recomendacion_juego y recomendacion_usuario se agregaron a la API, pero sólo recomendacion_juego se pudo deployar en Render dado que el conjunto de datos que requiere para hacer la predicción excedía la capacidad de almacenamiento disponible. Por lo tanto, para utilizarla se puede ejecutar la API en local.*


En caso de querer ejecutar la API desde localHost se deben seguir los siguientes pasos:

- Clonar el proyecto haciendo `git clone https://github.com/GabiL44/PI_MLOpsEngineer.git`.
- Preparación del entorno de trabajo en Visual Studio Code:
    * Crear entorno `Python -m venv env`
    * Ingresar al entorno haciendo `venv\Scripts\activate`
    * Instalar dependencias con `pip install -r requirements.txt`
- Ejecutar el archivo main.py desde consola activando uvicorn. Para ello, hacer `uvicorn main:app --reload`
- Hacer Ctrl + clic sobre la dirección `http://XXX.X.X.X:XXXX` (se muestra en la consola).
- Una vez en el navegador, agregar `/docs` para acceder a ReDoc.
- En cada una de las funciones hacer clic en *Try it out* y luego introducir el dato que requiera o utilizar los ejemplos por defecto. Finalmente Ejecutar y observar la respuesta.

### Deployment

Para el deploy de la API se seleccionó la plataforma Render que es una nube unificada para crear y ejecutar aplicaciones y sitios web, permitiendo el despliegue automático desde GitHub. Para esto se siguieron estos pasos:

- Se generó un servicio nuevo  en `render.com`, conectado al presente repositorio y utilizando Python 3 como Runtime.
- Finalmente, el servicio queda corriendo en [https://pi-mlops-engineer-d4uh.onrender.com](https://pi-mlops-engineer-jvwx.onrender.com).

Como se indicó anteriormente, para el despliegue automático, Render utiliza GitHub y dado que el servicio gratuito cuenta con una limitada capacidad de almacenamiento, se realizó un repositorio exclusivo para el deploy, el cual se encuenta [aqui](https://github.com/GabiL44/PI_MLOps_render_deploy).


### Video
Para finalizar les dejo un [video](https://drive.google.com/file/d/1FWyGBzr3Cb9St8XRSLnHJidjx3EzYiza/view?usp=sharing), donde muestro el desarrollo del proyecto y su deploy en render y LocalHost.

