from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from time import sleep
from threading import Thread
from picamera import PiCamera

import utils
from facerecognizer import FaceRecognizer


class HankMoody:
    def __init__(self):
        self.client = self.__initialize_iot_client()
        self.mqtt = self.client.getMQTTConnection()
        self.camera = self.__initialize_camera()

    def start(self):

        self.camera.capture('camera/sample.jpg')
        t = Thread(target=self.recognize)
        t.start()

    def recognize(self):
        emotions = FaceRecognizer("camera/sample.jpg").prevalent_emotions
        for emotion in emotions:
            print('Playing music for detected prevelant emotion:\n-> %s' % emotion)
            self.mqtt.publish('actions', {
                'message': 'playing music for mood: %s' % emotion['Type'],
                'action': 'play_sound',
                'value': emotion
            }, 1)
            utils.play_sample_sound('music/%s.mp3' % emotion['Type'])

    @staticmethod
    def __initialize_iot_client():
        client = AWSIoTMQTTShadowClient("iot-camera-rekognition-device")
        client.configureCredentials("certs/root.pem.crt", "certs/private.pem.key", "certs/certificate.pem.crt")
        client.getMQTTConnection().configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        return client

    @staticmethod
    def __initialize_camera():
        camera = PiCamera()
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        sleep(2)
        return camera


if __name__ == "__main__":
    HankMoody().start()
