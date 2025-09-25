# enhanced_model_server.py

import onnxruntime as ort
from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import JSONResponse
import numpy as np
import uvicorn
import json
from pathlib import Path
import psutil
import time

app = FastAPI()

sessions = {}
class_names = {}
current_model = None

def load_model(weights_path, model_name):
    global sessions
    print(f"Loading model {model_name} from {weights_path}")
    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
    session = ort.InferenceSession(weights_path, providers=providers)
    print(f"Model {model_name} loaded successfully. Providers: {session.get_providers()}")
    print(f"Using device: {session.get_providers()[0]}")
    sessions[model_name] = session
    return session

def load_class_names(file_path, model_name):
    global class_names
    print(f"Loading class names for {model_name} from {file_path}")
    file_extension = Path(file_path).suffix.lower()
    if file_extension == '.json':
        with open(file_path, 'r') as f:
            class_names[model_name] = json.load(f)
    elif file_extension == '.txt':
        with open(file_path, 'r') as f:
            class_names[model_name] = [line.strip() for line in f.readlines()]
    else:
        raise ValueError("Unsupported file format. Please use .json or .txt")
    print(f"Loaded {len(class_names[model_name])} class names for {model_name}")
    return class_names[model_name]

@app.post("/predict")
async def predict(file: UploadFile = File(...), 
                  model: str = Query(None, description="Model to use for prediction"),
                  confidence: float = Query(0.5, description="Confidence threshold")):
    global sessions, class_names, current_model
    
    if model is None:
        model = current_model
    
    if model not in sessions:
        return JSONResponse(content={"error": f"Model {model} not loaded"}, status_code=400)
    
    session = sessions[model]
    
    start_time = time.time()
    
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    
    img = nparr.reshape(1, 3, 640, 640).astype(np.float32) / 255.0
    
    results = session.run([output_name], {input_name: img})
    
    inference_time = time.time() - start_time
    
    # Filter results based on confidence threshold
    filtered_results = [detection for detection in results[0][0] if detection[4] > confidence]
    
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    
    return {
        "predictions": filtered_results,
        "class_names": class_names[model],
        "performance": {
            "inference_time": inference_time,
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage
        }
    }

@app.post("/load_model")
async def load_new_model(weights_path: str, class_names_path: str, model_name: str):
    try:
        load_model(weights_path, model_name)
        load_class_names(class_names_path, model_name)
        global current_model
        current_model = model_name
        return {"message": f"Model {model_name} loaded successfully"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/models")
async def get_models():
    return {"models": list(sessions.keys())}

@app.post("/set_model")
async def set_current_model(model_name: str):
    global current_model
    if model_name in sessions:
        current_model = model_name
        return {"message": f"Current model set to {model_name}"}
    else:
        return JSONResponse(content={"error": f"Model {model_name} not found"}, status_code=400)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Run enhanced object detection server')
    parser.add_argument('--weights', required=True, help='Path to the ONNX weights file')
    parser.add_argument('--class-names', required=True, help='Path to the class names file (JSON or TXT)')
    parser.add_argument('--model-name', required=True, help='Name of the model')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on')
    args = parser.parse_args()

    load_model(args.weights, args.model_name)
    load_class_names(args.class_names, args.model_name)
    current_model = args.model_name
    
    print(f"Starting server on port {args.port}")
    uvicorn.run(app, host="0.0.0.0", port=args.port)
