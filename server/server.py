from flask import Flask, send_from_directory, request
import random
import os
import logging
import frameconverter
import time
from webuiAPI import setting

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__, static_folder='../client/public')

class Video(object):
    defaultUploadOptions = {
        "filename": "file",
        "validation": {
            "allowedExtensions": ["mp4", "webm", "ogg"],
            "sizeLimit": 10485760
        },
    }
    @staticmethod
    def upload(request, options = None):
        if options is None:
            options = Video.defaultUploadOptions
        print(str(request))
        return File.upload(request, options)
        
@app.route("/")
def base():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def home(path):
    return send_from_directory(app.static_folder, path)

@app.route("/upv", methods=["POST"])
def upload_video():
    app.logger.info("HERE in UPLOAD VIDEO")
    fps = int(request.form['fps'])
    prompt = request.form['prompt']
    style = request.form['styles']
    type = request.form['type']
    #setting.add_prompt(prompt)
    #setting.setup_model_match(style)
    #setting.setup_type_match(type)
    #app.logger.info(f"style: {setting.setup['sd_model_checkpoint']}")
    #app.logger.info(f"type: {setting.setup['controlnet_module']}")
    samplingMethod = request.form['samplingMethod']
    file = request.files['video']
    logging.info(f"file: {file}")
    filename = file.filename
    #filename = request.form["fname"]
    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    fname = filename
    frameconverter.video2frame(os.path.join(app.config['UPLOAD_FOLDER'], fname), fps)
    dirin = os.path.join(app.config['UPLOAD_FOLDER'], fname[:-4] + "-opencv\\")
    if not os.path.isdir("outputs"):
        os.mkdir("outputs")
    dirout = "outputs/" + fname[:-4] + "-outimg"
    #frameconverter.interpolation(dirin, fps)
    #frameconverter.processframes(dirin, dirout)
    if not os.path.isdir(app.config['DOWNLOAD_FOLDER']):
        os.mkdir(app.config['DOWNLOAD_FOLDER'])
    #dirout+"/"
    frameconverter.convert_frames_to_video(dirin+"/", app.config['DOWNLOAD_FOLDER']+"/"+fname[:-4]+".mp4", fps)#frameconverter.MAX_FPS)
    return "ok"

@app.route("/dlv", methods=["GET"])
def download_video():
    dfn = str(request.args.get('dfn'))
    app.logger.debug("dfn = " + dfn)
    return send_from_directory("../downloads", "statueofliberty.mp4")#app.config['DOWNLOAD_FOLDER'], dfn)

if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['DOWNLOAD_FOLDER'] = 'downloads'
    app.run(debug=True)
    app.logger.info(os.listdir())