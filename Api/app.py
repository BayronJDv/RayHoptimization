from flask import Flask, jsonify, request
from flask_cors import CORS
from SequencialSearch import sequential_grid_search
from Ray.ParalelDisSearch import run_ray_parallel_grid_search
import ray
import time
import subprocess
import numpy as np
from Ray.ConnectRay import initialize_ray_cluster

# Inicializar Ray antes de cualquier operación
initialize_ray_cluster()

#hiperparametros para el grid search de prueba
param_grid_mlp = {
    'hidden_layer_sizes': [(12, 7), (15, 10, 5)], # Diferentes arquitecturas de capas ocultas
    'activation': ['relu', 'tanh'],                          # Función de activación
    'solver': ['adam', 'sgd'],                               # Algoritmo para optimización de pesos
    'alpha': [ 0.001, 0.01],                          # Parámetro de regularización L2
    'max_iter': [50,100,200]                                   # Número máximo de iteraciones
}

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello():
    return "Api en funcionamiento consulta la documentacion para su uso."

# Ruta para ejecutar la búsqueda secuencial
@app.route('/sequential-search', methods=['GET', 'POST'])
def sequential_search():
    # Recibir hiperparámetros y datos de predicción
    data = request.get_json() if request.is_json else {}
    param_grid = data.get('param_grid', param_grid_mlp)
    features = [
        'age', 'gender', 'education', 'country', 'ethnicity',
        'nscore', 'escore', 'oscore', 'ascore', 'cscore', 'impulsive', 'ss'
    ]
    input_ok = all(f in data for f in features)
    if not param_grid or not input_ok:
        return jsonify({'error': 'param_grid y datos de predicción requeridos'}), 400
    X_input = [[data[f] for f in features]]

    start = time.time()
    best_params, best_score, best_model = sequential_grid_search(param_grid)
    elapsed = time.time() - start
    pred = best_model.predict(X_input)
    return jsonify({    
        'best_params': best_params,
        'best_score': best_score,
        'search_time': elapsed,
        'prediction': int(pred[0])
    })

# Ruta para ejecutar la búsqueda paralela
@app.route('/parallel-search', methods=['GET', 'POST'])
def parallel_search():
    # Recibir hiperparámetros y datos de predicción
    data = request.get_json() if request.is_json else {}
    param_grid = data.get('param_grid', param_grid_mlp)
    features = [
        'age', 'gender', 'education', 'country', 'ethnicity',
        'nscore', 'escore', 'oscore', 'ascore', 'cscore', 'impulsive', 'ss'
    ]
    input_ok = all(f in data for f in features)
    if not param_grid or not input_ok:
        return jsonify({'error': 'param_grid y datos de predicción requeridos'}), 400
    X_input = [[data[f] for f in features]]
    #imprimir el estado de ray
    ray.init(address="auto",ignore_reinit_error=True)
    status = len(ray.nodes())
    start = time.time()
    best_params, best_score, best_model = run_ray_parallel_grid_search(param_grid)
    elapsed = time.time() - start
    pred = best_model.predict(X_input)
    return jsonify({ 
        'best_params': best_params,
        'best_score': best_score,
        'search_time': elapsed,
        'prediction': int(pred[0]),
        'nodes_used': status,
    })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)