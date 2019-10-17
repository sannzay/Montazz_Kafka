import time
from flask import Flask, Response
from kafka import KafkaConsumer

consumer = KafkaConsumer('streams-input', group_id='view', bootstrap_servers=['127.0.0.1:9092'])
consumer1 = KafkaConsumer('streams-output', group_id='view', bootstrap_servers=['127.0.0.1:9092'])
app = Flask(__name__)
#t0 = time.time()

@app.route('/')
def index():
    return Response(kafkastream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def kafkastream():
    while(True):
	t0 = time.time()
    	for msg1 in consumer1:
		t2 = time.time()
		diff = t2-t0
		print("Hello")
		if(diff>20):
			break
        	yield (b'--frame\r\n'
                       b'Content-Type: image/png\r\n\r\n' + msg1.value + b'\r\n\r\n')

	t0 = time.time()
    	for msg in consumer:
		t1 = time.time()
		dif = t1-t0
		print(dif)
		if(dif>20):
			break
        	yield (b'--frame\r\n'
               	       b'Content-Type: image/png\r\n\r\n' + msg.value + b'\r\n\r\n')
	



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
