from flask import Flask, request, jsonify, send_file, render_template
from ultralytics import YOLO
import cv2
import os
from collections import Counter

# Configuración inicial
app = Flask(__name__, static_folder="static", template_folder="templates")

model_path = "models/yolov8n_trained.pt"
model = YOLO(model_path)

class_to_value = {
    "100_pesos": 100,
    "10_pesos": 10,
    "200_pesos": 200,
    "20_pesos": 20,
    "500_pesos": 500,
    "50_pesos": 50
}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/detect', methods=['POST'])
def detect_money():
    # Recibir la imagen cargada
    image_file = request.files['image']
    if not image_file:
        return jsonify({"error": "No se envió ninguna imagen."}), 400

    # Guardar la imagen cargada temporalmente
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, "temp_image.jpg")
    image_file.save(file_path)

    # Realizar predicción
    results = model.predict(source=file_path, save=False)
    
    # Extraer las clases detectadas
    classes_detected = results[0].boxes.cls.cpu().numpy()
    class_names = results[0].names
    class_counts = Counter(class_names[int(cls)] for cls in classes_detected)
    
    # Calcular el total
    total_amount = 0
    breakdown = []
    for cls, count in class_counts.items():
        denomination = class_to_value.get(cls, 0)
        total_amount += denomination * count
        breakdown.append({"denomination": cls, "count": count})
    
    # Dibujar los bounding boxes en la imagen
    annotated_frame = results[0].plot()
    output_path = "static/result_image.jpg"
    cv2.imwrite(output_path, annotated_frame)

    # Responder con la imagen y los resultados
    return jsonify({
        "breakdown": breakdown,
        "total": total_amount,
        "image_url": "/static/result_image.jpg"
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

