from flask import Flask, request, jsonify, send_file, render_template
from ultralytics import YOLO
import cv2
import os
from collections import Counter
import requests

app = Flask(__name__, static_folder="static", template_folder="templates")

model_path = "models/yolov8n_trained-3.pt"
model = YOLO(model_path)

class_to_value = {
    "100_pesos": 100,
    "10_pesos": 10,
    "200_pesos": 200,
    "20_pesos": 20,
    "500_pesos": 500,
    "50_pesos": 50,
    "1_dolares": 1,
    "5_dolares": 5,
    "10_dolares": 10,
    "20_dolares": 20,
    "50_dolares": 50,
    "100_dolares": 100
}

# Función para obtener el valor del dólar blue desde la API
def obtener_valor_dolar_blue():
    url = "https://dolarapi.com/v1/dolares"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        for item in data:
            if item["casa"] == "blue":
                valor_blue = item["venta"]
                return int(valor_blue)
    except requests.exceptions.RequestException as e:
        return 1050




@app.route('/')
def home():
    return render_template("index.html")

@app.route('/detect', methods=['POST'])
def detect_money():
    image_file = request.files['image']
    if not image_file:
        return jsonify({"error": "No se envió ninguna imagen."}), 400

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, "temp_image.jpg")
    image_file.save(file_path)

    cotizacion_dolar = obtener_valor_dolar_blue()

    results = model.predict(source=file_path, save=False)

    # Extraer las clases detectadas
    classes_detected = results[0].boxes.cls.cpu().numpy()
    class_names = results[0].names
    class_counts = Counter(class_names[int(cls)] for cls in classes_detected)

    total_pesos = 0
    total_dolares = 0
    total_homogeneo = 0
    breakdown_pesos = []
    breakdown_dolares = []

    for cls, count in class_counts.items():
        denomination = class_to_value.get(cls, 0)
        if "_dolares" in cls:
            total_dolares += denomination * count
            total_homogeneo += denomination * count * cotizacion_dolar
            breakdown_dolares.append({"denomination": cls, "count": count})
        else:
            total_pesos += denomination * count
            total_homogeneo += denomination * count
            breakdown_pesos.append({"denomination": cls, "count": count})

    # Dibujar los bounding boxes 
    annotated_frame = results[0].plot()
    output_path = "static/result_image.jpg"
    cv2.imwrite(output_path, annotated_frame)

    return jsonify({
        "breakdown_pesos": breakdown_pesos,
        "breakdown_dolares": breakdown_dolares,
        "total_pesos": total_pesos,
        "total_dolares": total_dolares,
        "total_homogeneo": total_homogeneo,
        "cotizacion_dolar": cotizacion_dolar,
        "image_url": "/static/result_image.jpg"
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
