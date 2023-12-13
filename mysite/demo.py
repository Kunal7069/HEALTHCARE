from datetime import datetime

timestamps = ["08:30:00", "12:45:00", "23:15:00", "09:50:00"]

datetime_objects = [datetime.strptime(timestamp, "%H:%M:%S") for timestamp in timestamps]

sorted_datetime_objects = sorted(datetime_objects)

sorted_timestamps = [datetime.strftime(dt, "%H:%M:%S") for dt in sorted_datetime_objects]

print("Original Timestamps:", timestamps)
print("Sorted Timestamps:", sorted_timestamps)

# Get today's date
today_date = datetime.today().date()

# Print today's date
print("Today's date:", today_date)


<!DOCTYPE html>
<html>
<head>
    <title>Live Video Stream</title>
</head>
<body>
    
    <img id="videoFrame" src="" width="300" height="300"/>
    <img src="{% url 'video_feed' %}" alt="Video Stream" width="300" height="300">
    {% comment %} <img src="{% url 'video_feed_2' %}" alt="Video Stream" width="300" height="300"> {% endcomment %}
    <script>
        const videoSocket = new WebSocket(
            'ws://192.168.162.171:8765/ws/video_stream/'
        );
        videoSocket.onmessage = function(e) {
         document.getElementById('videoFrame').src = 'data:image/jpeg;base64,' + e.data;
        };
    </script>
</body>
</html>
