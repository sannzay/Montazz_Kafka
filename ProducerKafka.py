import time
import cv2
from kafka import SimpleProducer, KafkaClient
kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)
# Assign a topic
topic = 'streams-input'

def video_emitter():
    # Open the video
    video = cv2.VideoCapture(0)
    print(' emitting.....')

    t0 = time.time()

    # read the file
    while (video.isOpened):
        # read the image in each frame
        success, image = video.read()
        # check if the file has read to the end
        if not success:
            break
        # convert the image png
        ret, jpeg = cv2.imencode('.png', image)
        # Convert the image to bytes and send to kafka
	t1 = time.time()
        future=producer.send_messages(topic, jpeg.tobytes())

        # To reduce CPU usage create sleep time of 0.2sec
        #time.sleep(0.10)

        
        diff = t1-t0
        if diff > 60:
            break


    # clear the capture
    video.release()
    print('done emitting')

#if __name__ == '__main__':
#    video_emitter('')
