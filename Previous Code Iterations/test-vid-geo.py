import subprocess
import json

# def get_gps_from_video(video_path):
#     try:
#         cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format_tags=location', '-of', 'json', video_path]
#         result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
#         metadata = json.loads(result.stdout)
#         if 'format' in metadata and 'tags' in metadata['format']:
#             tags = metadata['format']['tags']
#             if 'location' in tags:
#                 lat_lon = tags['location'].split(',')
#                 if len(lat_lon) == 2:
#                     return float(lat_lon[0]), float(lat_lon[1])
#     except Exception as e:
#         print(f"Error extracting GPS data from video: {e}")
#     return None

# # Example video path
# video_path = 'test-vid-with-gps.mp4'  # Replace with your video path
# gps_data = get_gps_from_video(video_path)

# if gps_data:
#     print(f"GPS Coordinates: Latitude: {gps_data[0]}, Longitude: {gps_data[1]}")
# else:
#     print("No GPS data found in the video.")


def get_gps_from_video(video_path):
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format_tags=latitude,longitude', '-of', 'json', video_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        metadata = json.loads(result.stdout)
        if 'format' in metadata and 'tags' in metadata['format']:
            tags = metadata['format']['tags']
            lat = tags.get('latitude')
            lon = tags.get('longitude')
            if lat and lon:
                return float(lat), float(lon)
    except Exception as e:
        print(f"Error extracting GPS data from video: {e}")
    return None
