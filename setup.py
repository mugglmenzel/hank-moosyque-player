from setuptools import setup

setup(
    name='iot-camera-rekognition',
    version='0.1',
    packages=[],
    url='https://github.com',
    license='',
    author='menzelmi',
    author_email='menzelmi@amazon.de',
    description='',
    install_requires=[
        'boto3',
        'AWSIoTPythonSDK',
        'pyaudio',
        'pydub',
        'mxnet',
        'opencv-python',
        'numpy',
        'picamera'
    ]
)
