# 💵 Detección y Clasificación de Billetes con Flask y YOLOv8 💵

Proyecto de detección y clasificación de billetes basado en **YOLOv8**. 
Esta aplicación identifica billetes en imágenes, los clasifica por denominación y moneda, y calcula el monto total en pesos argentinos o dólares. 🚀

---
## 📋 Requisitos
- Python 3.8 o superior 🐍

---


# Pasos para desplegar la aplicación

Sigue estos pasos para ejecutar la aplicación en tu entorno local:

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/franciscoryb1/app-computer-vision.git
   cd app-computer-vision
   ```

2. **Crear un entorno virtual**
   ```bash
   python -m venv .env
   ```

3. **Activar el entorno virtual**
   - En **Windows**:
     ```bash
     .env\Scripts\activate
     ```
   - En **Linux/Mac**:
     ```bash
     source .env/bin/activate
     ```

4. **Instalar los requerimientos**
   Instala las dependencias necesarias para el proyecto:
   ```bash
   pip install -r requirements.txt
   ```

5. **Levantar el servicio**
   Ejecuta la aplicación desde la consola:
   ```bash
   python app.py
   ```

6. **Acceder a la aplicación**
   Una vez que la aplicación esté en funcionamiento, estará disponible en el enlace que aparece en la consola (generalmente algo como `http://127.0.0.1:5000`)
