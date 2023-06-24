import cv2
import time
import os
import sys, getopt
from edge_impulse_linux.image import ImageImpulseRunner
from flask import Flask, jsonify
import threading

app = Flask(__name__)
runner = None
results = []

def get_webcams():
    port_ids = []
    for port in range(32):
        camera = cv2.VideoCapture(port)
        if camera.isOpened():
            ret = camera.read()[0]
            if ret:
                backendName = camera.getBackendName()
                w = camera.get(30)
                h = camera.get(31)
                port_ids.append(port)
            camera.release()
    return port_ids

def now():
    return round(time.time() * 1000)

def main(argv):
    global runner
    global results
    try:
        opts, args = getopt.getopt(argv, "h", ["--help"])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            sys.exit()

    if len(args) == 0:
        sys.exit(2)

    model = args[0]
    dir_path = os.path.dirname(os.path.realpath(__file__))
    modelfile = os.path.join(dir_path, model)

    print('MODEL: ' + modelfile)

    with ImageImpulseRunner(modelfile) as runner:
        try:
            model_info = runner.init()
            print('Loaded runner for "' + model_info['project']['owner'] + ' / ' + model_info['project']['name'] + '"')
            labels = model_info['model_parameters']['labels']

            port_ids = get_webcams()
            if len(port_ids) == 0:
                raise Exception('Cannot find any webcams')
            videoCaptureDeviceId = int(port_ids[0])

            next_frame = 0 

            for res, img in runner.classifier(videoCaptureDeviceId):
                if (next_frame > now()):
                    time.sleep((next_frame - now()) / 1000)

                if "bounding_boxes" in res["result"].keys():
                    print('Result (%d ms.) ' % (res['timing']['dsp'] + res['timing']['classification']), end='')
                    results = []
                    for bbox in res['result']['bounding_boxes']:
                        results.append(bbox)
                    print('', flush=True)
                next_frame = now() + 100
        finally:
            if (runner):
                runner.stop()

def classification_thread():
    global runner
    global results
    # replace 'modelfile.eim' with your actual model file path
    main(['modelfile.eim'])

@app.route('/')
def get_classification():
    global results
    return jsonify(results)

if __name__ == "__main__":
    threading.Thread(target=classification_thread).start()
    app.run(host='0.0.0.0', port=5050)
