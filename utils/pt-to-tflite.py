from ultralytics import YOLO

model = YOLO("path/to/your/model.pt")
model.export(format="edgetpu")
