from myapp import app
import json, plotly
from flask import render_template, request, Response, jsonify
from wrangling_scripts.wrangle_data import return_figures

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])

def index():
    try:
        if request.method == 'POST':                  
            figures = return_figures(request.form['portfolio'], request.form['toggle']) #get values from inputs as arguments
        else:
            figures = return_figures()
    except:
        figures = return_figures()
        

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON)
   
   