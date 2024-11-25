# 🏠📊🌊**ZonaProp Scraper: Análisis de propiedades en la Costa Atlántica**  

🚀En este proyecto me propongo recolectar y analizar datos de propiedades publicadas en venta en el sitio web **ZonaProp**, específicamente para la región de la**Costa Atlántica Argentina, Provincia de Buenos Aires**.  

---

## 🌟 **¿Cuál es el objetivo?**  

Este proyecto tiene como objetivo principal:  

1. 🕵️**Recolectar datos**: Automatizar el proceso de recolección de información sobre propiedades en venta.  
2. 📦 **Almacenar datos**: Mediante el uso de SQL, que posteriormente permitira una forma rapida y flexible de retirar información a la hora del análisis.
3. 📈 **Analizar datos**: Utilizar estos datos para obtener insights sobre el mercado inmobiliario en la región.  
4. 💻 **Aprendizaje personal**: Mejorar mis habilidades poniendo en práctica mis conocimientos sobre scraping, análisis de datos y visualización.  

---

## 🚀 **¿Qué tecnologías uso?**  

- 🌐 **Beautiful Soup**: Librería de python utilizada para extraer datos HTML fácilmente.  
- 🔄 **Requests**: Librería de python utiliazada para realizar solicitudes HTTP, aunque solo se usa para extraer las IPs rotativas que se usan para evitar un posible bloqueo de IP.  
- ☁️🚪**CloudScraper**: Me permite saltar el anti-bots de cloudflare.
- 📊 **Pandas**: Para limpiar y estructurar los datos obtenidos.  
- 🗄️ **SQL**: Para extraer y filtrar la gran cantidad de datos, una vez que se encuentren en la base de datos.
- 📊  **Tableau**: Para crear visualizaciones impactantes.  

---

## ⚙️ **¿Cómo funciona?**  

1. El scraper accede al sitio web de **ZonaProp** y extrae información relevante como:  
   - 🏡 **Ubicación** (generalmente es el título de la publicación)
   - 💰 **Precio de la propiedad**  
   - 📐 **Metros cuadrados** (Totales, cubiertos y no cubiertos)
   - 🛋️ **Cantidad de ambientes**
   - 🛏️ **Cantidad de habitaciones**  
   - 🚽 **Cantidad de Baños**
   - 🚗 **Espacios de cochera** (Si incluyen) 
* ⚠️ Es **importante** aclarar que parte de las publicaciones que la gente realiza en ZonaProp no incluyen información detallada o toda la información, con lo cual hay que destacar que la información no es 100% fideligna ya que hay ciertos errores y omisiones.
2. Los datos extraídos se guardan en una base de datos para un posterior análisis.  
3. El análisis incluye gráficos y estadísticas descriptivas para entender las tendencias del mercado.  

---

## 🛠️ **Cómo usar este proyecto**  

El proyecto aún se encuentra en desarrollo, al ser finalizado dejaré las instrucciones aquí.

---

## 🌍 **Áreas cubiertas**  

Por ahora, el scraper se recolecta datos en ciudades populares de la **Costa Atlántica**, como:  

- 📍 Mar del Plata  
- 📍 Pinamar  
- 📍 Villa Gesell  
- 📍 Miramar  

¡La idea es hacer lo mismo para más regiones! 🚧  

---

## ⚠️ **Disclaimer legal**  

Este proyecto es únicamente con fines educativos 📚 y de análisis personal 🔬. El uso indebido de datos obtenidos puede violar los **Términos y Condiciones** del sitio web de ZonaProp. Por favor, asegúrate de respetar las normativas locales y los derechos de los propietarios del sitio.  

---

## 🤝 **Contribuciones**  

¿Tenés ideas para mejorar este proyecto? 🤔 ¡Son más que bienvenidas! Podes abrir un **issue** o hacer un **pull request**.  

---

## 📧 **Contacto**  

Si tienes dudas o comentarios, no dudes en escribirme a:  
📩 **juancruzmarquesjcm@gmail.com**  

---

¡Gracias por pasarte! 🌊 ¡Espero que a más de uno le sirva! 
