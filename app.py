from flask import Flask, render_template, url_for, request, jsonify
import threading
from pyngrok import ngrok
from text_sentiment_prediction import *

#libreria para exponer la api a una url publica


app = Flask(__name__)
port = "5000"

public_url = ngrok.connect(port).public_url
print(public_url)

app.config["BASE_URL"] = public_url

# correr la api en url publica
#run_with_ngrok(app)

@app.route('/')
#cambiar nombre de index a home
def home():
    #agregar una variable para que reciba los datos de una funcion
    entries = show_entry()
    #le pasamos la variable a la plantilla index.html
    return render_template("index.html", entries=entries)
 
@app.route('/predict-emotion', methods=["POST"])
def predict_emotion():
    
    # Obtener el texto ingresado del requerimiento POST.
    input_text = request.json.get("text")  
    
    if not input_text:
        # Respuesta para enviar si input_text está indefinido.
        response = {
                    "status": "error",
                    "message": "¡Por favor, ingresa algún texto para predecir la emoción!"
                  }
        return jsonify(response)
    else:  
        predicted_emotion,predicted_emotion_img_url = predict(input_text)
        
        # Respuesta para enviar si input_text no está indefinido.
        response = {
                    "status": "success",
                    "data": {
                            "predicted_emotion": predicted_emotion,
                            "predicted_emotion_img_url": predicted_emotion_img_url
                            }  
                   }

        # Enviar respuesta.         
        return jsonify(response)
#funcion que lee el archivo csv con el hsitorial de predicciones y lo devuelve en un arreglo
def show_entry():
    day_entry_list = pd.read_csv("/content/Clase135/static/assets/data_files/data_entry.csv")
    day_entry_list = day_entry_list.iloc[::-1]

    
    
threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()




    
