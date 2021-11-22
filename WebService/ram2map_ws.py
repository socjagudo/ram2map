import os
import subprocess
from flask import Flask
from flask import request, redirect, url_for, render_template, current_app
from werkzeug.utils import secure_filename


#========================================
# THIS SECTION SHOULD BE IN A CONFIG FILE
#========================================

from os.path import abspath, dirname, join

# Define the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))

# Media dir
MEDIA_DIR = join(BASE_DIR, 'media')
POSTS_ADIF_DIR = join(MEDIA_DIR, 'adif')

SECRET_KEY = '...'

#========================================

app = Flask(__name__)

@app.route("/",methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/ram2map/",methods=["GET", "POST"])
def ram2map():
    if request.method == 'POST':
        callsign = request.form['callsign']
        email = request.form['email']
        mapcenter = request.form['mapcenter']

        # Check if file has been sent
        if 'adif_data_file' in request.files:
            file = request.files['adif_data_file']
            # Si el usuario no selecciona un fichero, el navegador
            # enviará una parte vacía sin nombre de fichero
            if file.filename:
                image_name = secure_filename(file.filename)
                images_dir = current_app.config['POSTS_ADIF_DIR']
                os.makedirs(images_dir, exist_ok=True)
                file_path = os.path.join(images_dir, image_name)
                file.save(file_path)
        
        # Check if next was passed as an argument for re-direction
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('index'))
        
    # Return
    return render_template("map2ram_form.html")


@app.route("/p/<string:slug>/")
def show_post(slug):
    return render_template("post_view.html", slug_title=slug)


@app.route("/admin/post/")
@app.route("/admin/post/<int:post_id>/")
def post_form(post_id=None):
    return render_template("admin/post_form.html", post_id=post_id)

#if __name__ == '__main__':
#    os.environ['FLASK_APP'] = 'ram2map_ws.py'
#    subprocess.run(['flask', 'run'])

if __name__ == '__main__':
    app.run(debug = True,
            host  = '0.0.0.0')