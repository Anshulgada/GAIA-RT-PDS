import onnxruntime as ort
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import uvicorn
import json
from pathlib import Path

app = FastAPI()

session = None
class_names = None

def load_model(weights_path):
    global session
    print(f"Loading model from {weights_path}")
    
    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
    session = ort.InferenceSession(weights_path, providers=providers)
    
    print(f"Model loaded successfully. Providers: {session.get_providers()}")
    print(f"Using device: {session.get_providers()[0]}")
    
    return session

def load_class_names(file_path):
    global class_names

    print(f"Loading class names from {file_path}")
    
    file_extension = Path(file_path).suffix.lower()
    
    if file_extension == '.json':
        with open(file_path, 'r') as f:
            class_names = json.load(f)
            
    elif file_extension == '.txt':
        with open(file_path, 'r') as f:
            class_names = [line.strip() for line in f.readlines()]
            
    else:
        raise ValueError("Unsupported file format. Please use .json or .txt")
    
    print(f"Loaded {len(class_names)} class names")
    
    return class_names

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    global session, class_names
    
    if session is None:
        return JSONResponse(content={"error": "Model not loaded"}, status_code=500)
    
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    
    img = nparr.reshape(1, 3, 640, 640).astype(np.float32) / 255.0
    
    results = session.run([output_name], {input_name: img})
    
    return {"predictions": results[0].tolist(), "class_names": class_names}

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run object detection server')
    parser.add_argument('--weights', required=True, help='Path to the ONNX weights file')
    parser.add_argument('--class-names', required=True, help='Path to the class names file (JSON or TXT)')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on')
    args = parser.parse_args()

    load_model(args.weights)
    load_class_names(args.class_names)
    
    print(f"Starting server on port {args.port}")
    uvicorn.run(app, host="0.0.0.0", port=args.port)