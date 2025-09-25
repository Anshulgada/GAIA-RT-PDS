from PIL import Image
import piexif
import cv2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, recipient_email, subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

def get_gps_from_image(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if exif_data:
            exif_dict = piexif.load(img.info["exif"])
            if piexif.GPSIFD.GPSLatitude in exif_dict["GPS"]:
                lat = exif_dict["GPS"][piexif.GPSIFD.GPSLatitude]
                lon = exif_dict["GPS"][piexif.GPSIFD.GPSLongitude]
                lat_ref = exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef]
                lon_ref = exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef]
                
                lat = sum(float(num)/float(denom) for num, denom in lat) * (-1 if lat_ref == "S" else 1)
                lon = sum(float(num)/float(denom) for num, denom in lon) * (-1 if lon_ref == "W" else 1)
                
                return lat, lon
    except Exception as e:
        print(f"Error extracting GPS data from image: {e}")
    return None

def get_gps_from_video(video_path):
    try:
        video = cv2.VideoCapture(video_path)
        if video.isOpened():
            metadata = video.get(cv2.CAP_PROP_METADATA)
            if metadata:
                # This is a simplification. Actual parsing might be more complex
                lat, lon = metadata.split('/')
                return float(lat), float(lon)
    except Exception as e:
        print(f"Error extracting GPS data from video: {e}")
    return None

def process_image(model, input_path, output_path, sender_email, sender_password, recipient_email):
    # Load the image
    img = cv2.imread(input_path)
    
    # Run inference
    results = model(img)
    
    ph_detected = False
    
    # Draw bounding boxes
    for result in results:
        if result.boxes is not None:
            for box in result.boxes.xyxy:
                x, y, x2, y2 = box
                class_id = result.boxes.cls[0]
                confidence = result.boxes.conf[0]
                class_name = model.names[int(class_id)]
                label = "{} {:.2f}".format(class_name, confidence)
                cv2.rectangle(img, (int(x), int(y)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(img, label, (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
                if class_name.lower() == "ph" or class_name.lower() == "pothole":
                    ph_detected = True
    
    # Save the output image
    cv2.imwrite(output_path, img)
    
    # Send email if PH detected
    if ph_detected:
        subject = "Pothole Detected"
        body = f"A pothole has been detected in the image: {input_path}"
        send_email(sender_email, sender_password, recipient_email, subject, body)

def process_video(model, input_path, output_path, frame_skip, sender_email, sender_password, recipient_email):
    # Load the video
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Create a video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps / frame_skip, (width, height))
    
    frame_count = 0
    ph_detected = False
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process every nth frame
        if frame_count % frame_skip == 0:
            # Run inference
            results = model(frame)
            
            # Draw bounding boxes
            for result in results:
                if result.boxes is not None:
                    for box in result.boxes.xyxy:
                        x, y, x2, y2 = box
                        class_id = result.boxes.cls[0]
                        confidence = result.boxes.conf[0]
                        class_name = model.names[int(class_id)]
                        label = "{} {:.2f}".format(class_name, confidence)
                        cv2.rectangle(frame, (int(x), int(y)), (int(x2), int(y2)), (0, 255, 0), 2)
                        cv2.putText(frame, label, (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        
                        if class_name.lower() == "ph" or class_name.lower() == "pothole":
                            ph_detected = True
            
            # Write the output frame
            out.write(frame)
        
        frame_count += 1
    
    cap.release()
    out.release()
    
    # Send email if PH detected
    if ph_detected:
        subject = "Pothole Detected"
        body = f"A pothole has been detected in the video: {input_path}"
        send_email(sender_email, sender_password, recipient_email, subject, body)


# pip install Pillow piexif