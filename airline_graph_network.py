import pandas as pd
import networkx as nx
import pickle
import os 
from networkx.algorithms.shortest_paths.weighted import dijkstra_path , dijkstra_path_length
from flask import Flask, render_template, request


app = Flask(__name__)
IMAGES_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = IMAGES_FOLDER

@app.route('/')
def graph_display():
	## get the airport codes or the nodes of the Graph.
	airport_list = list(G.nodes())
	dir = os.getcwd()
	## Pass the graph image as a param to the html page.
	file = os.path.join(app.config['UPLOAD_FOLDER'], 'airport_network.png')
	return render_template('airport_network.html',user_image = file, airport_list = airport_list)

@app.route('/predict',methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		result = request.form.to_dict()
		## get the airport codes 
		airports = list(result.values())
		## get the path and distance using the networkx function.
		path  = dijkstra_path(G, airports[0], airports[1], weight = 'Distance')
		distance  = dijkstra_path_length(G, airports[0], airports[1], weight = 'Distance')
		## send the result to the html page 	
		return render_template("airport_network_result.html",result = (path, distance))
	return

if __name__ == '__main__':
	
	# Load graph
	with open("airline_graph.p", 'rb') as f:  
    		G = pickle.load(f)
	
	print("graph loaded")
	app.run(debug = True,host = '0.0.0.0' , port = 5000 )
