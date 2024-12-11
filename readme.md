# 🏠📊 **ZonaProp Scraper: Análisis del mercado inmobiliario en la Costa Atlántica**  

🚀 El objetivo de este proyecto es recolectar y analizar datos de propiedades publicadas en venta en **ZonaProp**, en particulaar de la **Costa Atlántica de la Provincia de Buenos Aires**. A su vez, resulta una oportunidad perfecta para poner en práctica conceptos y herramientas aprendidos en lo que respecta al análisis de datos.

---

## 🌟 **¿Cuál es el objetivo?**  

Este proyecto tiene como objetivo principal:  

1. 🕵️**Recolectar datos**: Automatizar el proceso de recolección de información sobre propiedades en venta.  
2. 📈 **Analizar datos**: Utilizar estos datos para obtener insights sobre el mercado inmobiliario en la región.  
3. 💻 **Aprendizaje personal**: Mejorar mis habilidades de scraping, análisis de datos y visualización.  

---

## 🚀 **¿Qué tecnologías uso?**  

Este proyecto está construido con:  

- 🌐 **Beautiful Soup**: Librería de python utilizada para extraer datos HTML.  
- 🔄 **Requests**: Librería de python utilizada para manejar solicitudes HTTP. (Es utilizada de forma indirecta ya que forma parte de la librería CloudScraper)
- ☁️🚪**CloudScraper**: Es una librería de python que me permite saltar el anti-bots de cloudflare.
- 📊 **Pandas**: Una libraría de python que me permite limpiar y estructurar los datos obtenidos.  
- 🛢️ **MySQL/SQLite**: Una base de datos que cumple la función de almacenar y me permite acceder a los datos de una forma poderosa y flexible.
- 📈 **Tableau**: Para crear visualizaciones impactantes.  

---

## ⚙️ **¿Cómo funciona?**  

1. El scraper accede al sitio web de **ZonaProp** y extrae información relevante como:  
   - 🏡 **Ubicación** (generalmente es el título de la publicación)
   - 💰 **Precio de la propiedad**  
   - 📐 **Metros cuadrados** (Totales, cubiertos y no cubiertos)
   - 🛋️ **Cantidad de ambientes**
   - 🛏️ **Cantidad de habitaciones**  
   - 🚽 **Cantidad de Baños**
   - 🚗 **Espacios de cochera**  
    ⚠️ Los datos poseen errores debido a la manera en que son cargados por las personas que crean las publicaciónes y por lo tanto no se pueden tomar como 100% fidelignos.
2. Los datos extraídos se guardan en una base de datos relacional para un posterior análisis.  
3. El análisis incluye gráficos y estadísticas descriptivas para entender las tendencias del mercado.  

---

## 🛠️ **Cómo usar este proyecto**  

🚧⚠️ **El proyecto aún se encuentra en desarrollo, por lo que aún se encuentra sujeto a cambios**

1. Deben instalarse las librerías correspondientes. (Aquí debo dejar la lista y la aclaración sobre la versión de python). Además se debe contar con SQLite.
2. Una vez clonado el repositorio se puede modificar el url que se encuentra en main.py si se desea realizar para otra región o categoría de inmueble, por defecto solo recaba información sobre departamentos en la región de la Costa Atlántica de la Pcia de Buenos Aires.
3. Se puede correr el script ejecutando 'main.py' en la terminal, tal que: 'python main.py'.
4. Una vez finalizado se econtrará un documento llamado 'ZonaPropData.sqlite3' o 'ZonaPropData', dicho documento se puede acceder a travéz del SQLiteBrowser desde allí se puede generar un archivo '.csv'.

---

## 🌍 **Áreas cubiertas**  

Por ahora, el scraper se enfoca en ciudades populares de la **Costa Atlántica**, como:  

- 📍 Mar del Plata  
- 📍 Pinamar  
- 📍 Villa Gesell  
- 📍 Miramar  

¡La idea es que sea posible realizar el scraping en más regiones, dicha funcionalidad será añadida más adelante dado que el proyecto continua en desarrollo! 🚧  

---

## ⚠️ **Disclaimer legal**  

Este proyecto es únicamente con fines educativos 📚 y de análisis personal 🔬. El uso indebido de datos obtenidos puede violar los **Términos y Condiciones** del sitio web de ZonaProp. Por favor, asegúrate de respetar las normativas locales y los derechos de los propietarios del sitio.  

---

## 🤝 **Contribuciones**  

¿Tienes ideas para mejorar este proyecto? 🤔 ¡Son más que bienvenidas! Puedes abrir un **issue** o hacer un **pull request**.  

---

## 📧 **Contacto**  

Si tienes dudas o comentarios, no dudes en escribirme a:  
📩 **juancruzmarquesjcm@gmail.com**  

---

¡Gracias por pasarte! 🌊 **¡Espero que a más de alguno le sirva!** 🏘️📊  

