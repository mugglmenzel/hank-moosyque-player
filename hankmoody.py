from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

import utils
from facerecognizer import FaceRecognizer


class HankMoody:
    def __init__(self):
        self.client = self.__initialize_iot_client()
        self.mqtt = self.client.getMQTTConnection()

    def start(self):
        emotions = FaceRecognizer("samples/image3.jpg").prevalent_emotions
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


if __name__ == "__main__":
    HankMoody().start()
