from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime, timedelta


producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# end_time = datetime.now() + timedelta(minutes=2)

while True: 
    # datetime.now() < end_time
    log = {
        'timestamp': datetime.now().isoformat(),
        'level': random.choice(['INFO', 'WARNING', 'ERROR']),
        'message': 'This is a log message'
    }
    producer.send('logs', log)
    print("Sent log:", log)
    producer.flush() 
    time.sleep(1)  

producer.close()
