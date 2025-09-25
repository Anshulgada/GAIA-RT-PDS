# location_based_alerts.py
import json
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import cv2
from geopy.geocoders import Nominatim
from PIL import ExifTags, Image


class LocationBasedAlerts:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.geolocator = Nominatim(user_agent="object_detection_app")

    def extract_location(self, image_path):
        """
        Extract location data from image EXIF tags.
        Returns a tuple of (latitude, longitude) if available, else None.
        """
        try:
            with Image.open(image_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag = ExifTags.TAGS.get(tag_id, tag_id)
                        if tag == "GPSInfo":
                            gps_info = {}
                            for t in value:
                                sub_tag = ExifTags.GPSTAGS.get(t, t)
                                gps_info[sub_tag] = value[t]

                            lat = self._convert_to_degrees(gps_info["GPSLatitude"])
                            lon = self._convert_to_degrees(gps_info["GPSLongitude"])

                            if gps_info["GPSLatitudeRef"] != "N":
                                lat = -lat
                            if gps_info["GPSLongitudeRef"] != "E":
                                lon = -lon

                            return (lat, lon)
        except Exception as e:
            print(f"Error extracting location data: {e}")
        return None

    def _convert_to_degrees(self, value):
        """Helper function to convert GPS coordinates to degrees."""
        d, m, s = value
        return d + (m / 60.0) + (s / 3600.0)

    def get_address_from_coordinates(self, lat, lon):
        """
        Get address from latitude and longitude using geopy.
        """
        try:
            location = self.geolocator.reverse(f"{lat}, {lon}")
            return location.address
        except Exception as e:
            print(f"Error getting address: {e}")
            return f"Latitude: {lat}, Longitude: {lon}"

    def send_alert(self, recipient, class_name, location_data, image_data, json_data):
        """
        Send an alert via email with the detected class, location, and image/JSON data.
        """
        msg = MIMEMultipart()
        msg["Subject"] = f"Object Detection Alert: {class_name}"
        msg["From"] = self.sender_email
        msg["To"] = recipient

        body = f"Detected object: {class_name}\n"
        body += f"Coordinates: {location_data['coordinates']}\n"
        body += f"Location: {location_data['address']}\n"

        body += f"\nAdditional Data:\n{json.dumps(json_data, indent=2)}"

        msg.attach(MIMEText(body, "plain"))

        image = MIMEImage(image_data, name="detection.jpg")
        msg.attach(image)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            print(f"Alert sent to {recipient}")
        except Exception as e:
            print(f"Error sending alert: {e}")


def process_frame_with_alerts(
    frame, predictions, class_names, alerts, recipient, location_data
):
    """
    Process a frame, draw bounding boxes, and send alerts if necessary.
    """
    for detection in predictions:
        class_id = int(detection[5])
        confidence = detection[4]
        bbox = detection[:4]

        x1, y1, x2, y2 = bbox
        x1 = int(x1 * frame.shape[1])
        y1 = int(y1 * frame.shape[0])
        x2 = int(x2 * frame.shape[1])
        y2 = int(y2 * frame.shape[0])

        class_name = class_names[class_id]
        label = f"{class_name} {confidence:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(
            frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2
        )

        # Send alert
        if confidence > 0.7:  # You can adjust this threshold
            _, img_encoded = cv2.imencode(".jpg", frame)
            img_bytes = img_encoded.tobytes()

            json_data = {
                "class_name": class_name,
                "confidence": float(confidence),
                "bounding_box": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                "location": location_data,
            }

            alerts.send_alert(
                recipient, class_name, location_data, img_bytes, json_data
            )

    return frame
