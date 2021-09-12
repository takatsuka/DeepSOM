from flask import Flask, render_template, request, url_for, \
                  send_file, jsonify, send_from_directory
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
import os, io, sys, json
from ast import literal_eval
from frontend.src.inputform import InputForm, get_err_messages
import celery_worker
from backend import supported_file, read_to_vec, read_to_vec_with_class

# Setting file paths
frontend_src = os.path.abspath('frontend/src/')
static_src = os.path.abspath('frontend/static/')

# Setting up flask server and celery worker
app = Flask(__name__, template_folder=frontend_src, static_folder=static_src)
app.config["SECRET_KEY"] = "F9p_ARlUGGQTjnxQz86qjQ"
celery = celery_worker.get_worker(app)

# Making upload directory
upload_dir = os.path.join(app.instance_path,"uploads")
os.makedirs(upload_dir,exist_ok=True)

@celery.task(bind=True)
def train_model(self, data, dim, graph, shape, iters, lvq_data, classifiers):
    return celery_worker.train_model(self, data, dim, graph, shape, iters, 
                                     lvq_data, classifiers)

@app.route("/", methods=['GET', 'POST'])
def index():
    """
    Renders the HTML page.
    GET requests will return the standard page.
    """
    form = InputForm(CombinedMultiDict((request.form, request.files)))

    if request.method == "POST":
        print("Received Build Request")
        # Validating file input
        if not form.validate():
            return jsonify({'result': get_err_messages(form)})
        if not supported_file(form.user_file.data.filename):
            return jsonify({'result': "File type not supported"})
        # Validating graph input
        graph = request.form['graph']
        if graph == "false":
            return jsonify({'result': "Invalid graph structure provided"})
        # Reading in data file
        user_data = form.user_file.data
        try:
            use_lvq = (form.test_split.data > 0)
            # Grabbing classes for LVQ
            if use_lvq:
                data, dim, num_classes = read_to_vec_with_class(user_data)
                lvq_data = (num_classes, form.test_split.data)
            else:
                data, dim = read_to_vec(user_data)
                lvq_data = None
            user_data.close()
        except IOError:
            user_data.close()
            return jsonify({'result': "Error reading data file"})
        # Reading in graph structure and parameters
        graph = json.loads(graph)
        # Verifying graph dimensions
        for node in graph:
            if node == "input-node":
                continue
            dims = graph[node]["parameters"]["Input Dimensions"]
            if dims is None:
                continue
            for d in dims:
                if d > dim:
                    return jsonify({'result': "Invalid input dimensions specified"})
        print("======\n Form Data ---------")
        print(form.classifiers.data)
        print("+++++++++++++")
        task = train_model.apply_async((data, dim, graph, form.som_shape.data, 
                                            form.iters.data, lvq_data, 
                                            form.classifiers.data), 
                                        serializer = 'pickle', expires = 60)
        print("Created Build Request")
        return jsonify({'result': 42, 
                        'status_url': url_for('task_status', 
                         task_id=task.id, graph=graph), 'task_id': task.id})

    return render_template("index.html", form = form)

@app.route("/status/<task_id>")
def task_status(task_id):
    task = train_model.AsyncResult(task_id)
    graph = request.args.get('graph', None)
    if isinstance(task.info, Exception):
        return jsonify({"state":task.state, 
                        "display_url": url_for('return_visualisation', task_id = task_id, 
                         graph=graph, build_status="Build Failed: "+ str(task.info))})
    if task.state == "PENDING":
        return jsonify({"state":task.state, 
                        "display_url": url_for('return_visualisation', 
                         task_id = task_id, graph=graph, 
                         build_status="Build Request Pending...")})
    elif task.state == "FAILURE":
        return jsonify({"state":task.state, 
                        "display_url": url_for('return_visualisation', 
                         task_id = task_id, graph=graph, 
                         build_status="Build Failed: "+str(task.info))})
    elif task.state == "WORKING":
        saved_info = task.info
        if isinstance(saved_info, tuple):
            return jsonify({"state":"WORKING", 
                            "display_url": url_for('return_visualisation', 
                             task_id = task_id, graph=graph, 
                             build_status="Finishing Up...")})
        if isinstance(saved_info['current'], str):
            return jsonify({"state":"WORKING", 
                            "display_url": url_for('return_visualisation', 
                             task_id = task_id, graph=graph, 
                             build_status=saved_info['current'])})
    elif task.state == "SUCCESS":
        visualisations, lvq_metrics = task.info
        # UMatrix visualisation
        umatrix_visualisation = visualisations[0]
        umatrix_filenames = {}
        i=0
        for name, plot in umatrix_visualisation.items():
            filename = task.id + "_" + str(i) + ".png"
            i += 1
            filepath = os.path.join(upload_dir,filename)
            umatrix_filenames[name]=filename
            with open(filepath, 'wb') as f:
                f.write(plot.getvalue())
        print(len(visualisations))
        # Other visualisations
        visNames = visualisations[len(visualisations) - 1]
        misc_vis = []
        print(visNames)
        if "genHTMLPlot" in visNames:
            filepath = os.path.join(upload_dir,task.id + "3d.html")
            visualisations[visNames["genHTMLPlot"]].write_html(filepath)
            plot_3d_url = url_for('uploaded_file', filename = task.id+"3d.html", 
                                  filetype = "text/html")
            misc_vis.append(("3D SOM Plot", plot_3d_url))
        if "errorColorPlot" in visNames:
            filepath = os.path.join(upload_dir,task.id + "error.html")
            visualisations[visNames["errorColorPlot"]].write_html(filepath)
            plot_error_url = url_for('uploaded_file', filename = task.id+"error.html", 
                                     filetype = "text/html")
            misc_vis.append(("3D Error Plot", plot_error_url))
        if "gen4DPlot" in visNames:
            filepath = os.path.join(upload_dir,task.id + ".html")
            visualisations[visNames["gen4DPlot"]].write_html(filepath)
            plot_4d_url = url_for('uploaded_file', filename = task.id+".html", 
                                  filetype = "text/html")
            misc_vis.append(("4D SOM Plot", plot_4d_url))
        if "genPCAPlot" in visNames:
            filepath = os.path.join(upload_dir,task.id + "pcaplot.html")
            visualisations[visNames["genPCAPlot"]].write_html(filepath)
            plot_error_url = url_for('uploaded_file', filename = task.id+"pcaplot.html", 
                                     filetype = "text/html")
            misc_vis.append(("3D PCA Plot", plot_error_url))
        if "plotDeepSOM4D" in visNames:
            filepath = os.path.join(upload_dir,task.id + "deepSOM4D.html")
            visualisations[visNames["plotDeepSOM4D"]].write_html(filepath)
            plot_error_url = url_for('uploaded_file', filename = task.id+"deepSOM4D.html", 
                                     filetype = "text/html")
            misc_vis.append(("4D PCA DeepSOM Plot", plot_error_url))
        if "plotDeepSOM3D" in visNames:
            filepath = os.path.join(upload_dir,task.id + "deepSOM3D.html")
            visualisations[visNames["plotDeepSOM3D"]].write_html(filepath)
            plot_error_url = url_for('uploaded_file', filename = task.id+"deepSOM3D.html", 
                                     filetype = "text/html")
            misc_vis.append(("3D PCA DeepSOM Plot", plot_error_url))
        if misc_vis == []:
            misc_vis = None

        return jsonify({"state":task.state, 
                        "display_url": url_for('return_visualisation', task_id = task_id, 
                         filenames_dict = str(umatrix_filenames), misc_vis=str(misc_vis), 
                         lvq_metrics = str(lvq_metrics), graph=graph, 
                         build_status="Build finished")})
    return jsonify({"state":task.state, 
                    "display_url": url_for('return_visualisation', task_id = task_id, 
                     graph=graph, build_status=str(task.info))})

@app.route("/result/<task_id>")
def return_visualisation(task_id):
    filenames_dict = request.args.get('filenames_dict', None)
    build_status = request.args.get('build_status', None)
    graph = request.args.get('graph', None)
    misc_vis = request.args.get('misc_vis', None)
    lvq_metrics = request.args.get('lvq_metrics',None)
    if filenames_dict is not None:
        filenames_dict = literal_eval(filenames_dict)
        for node_name, filename in filenames_dict.items():
            filenames_dict[node_name] = url_for('uploaded_file', filename=filename)
    if graph is not None:
        graph = list(literal_eval(graph).items())
    if misc_vis is not None:
        misc_vis = literal_eval(misc_vis)
        if isinstance(misc_vis,tuple):
            misc_vis = [misc_vis]
    if lvq_metrics is not None:
        lvq_metrics = literal_eval(lvq_metrics)
    return render_template('result.html', filenames_dict=filenames_dict, graph=graph, 
           build_status=build_status, misc_vis=misc_vis, lvq_metrics = lvq_metrics)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    """
    Returns the specified image file
    """
    filetype = request.args.get('filetype', 'img/png')
    filepath = os.path.join(upload_dir,filename)
    with open(filepath, 'rb') as f:
        file_stream = io.BytesIO(f.read())
    file_stream.seek(0)
    #os.remove(filepath)
    return send_file(file_stream, mimetype=filetype)

if __name__ == '__main__':
    app.run(debug=True)
    
