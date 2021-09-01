from flask import Flask,request,url_for,render_template,redirect,session
import numpy as np
import pandas as pd
import plotly
import plotly_express as px
import json

app = Flask(__name__)
lst_sessions = []
dct_sessions = {}
jpl_sessions = {}

app.secret_key = ''
@app.route('/')
def welcome():
    return redirect('/home')

@app.route('/eda')
def eda():
    try:
        jpl = jpl_sessions[session['key']]
    except:
        df1 = pd.DataFrame()
        try:
            df1 = dct_sessions[session['key']]
        except:
            df1 = pd.DataFrame(data={'Hello': ['Welcome']})
        pl = px.histogram(df1, x=df1.columns[0])
        jpl = json.dumps(pl, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template('eda.html', jpl=jpl)


@app.route('/submit_eda',methods=['POST'])
def submit_eda():
    global dct_sessions
    global lst_sessions
    graph_type = 'histogram'
    dct_graphs = {'line':['x','y','color'],'bar':['x','y','color'],'scatter':['x','y','color'],'hist':['x','color'],'box':['x','y','color'],'violin':['x','y','color'],'heatmap':['x','y','z','color'],'scatter_3d':['x','y','z','color'],'line_3d':['x','y','z','color']}
    df1 = pd.DataFrame()
    try:
        df1 = dct_sessions[session['key']]
    except:
        df1 = pd.DataFrame(data={'Hello': ['Welcome']})
    dct_text = {'x':df1.columns[0]}
    try:
        graph_type = request.form['chart_dropdown']
        for i in dct_graphs[graph_type]:
            if request.form[i] == '':
                pass
            else:
                dct_text[i] = request.form[i]
            print(i)
    except:
        pass
    jpl = ''
    print(request.form['chart_dropdown'])
    if request.form['chart_dropdown'] == 'line':
        pl = px.line(df1, **dct_text)
        print(dct_text)
        jpl = json.dumps(pl, cls=plotly.utils.PlotlyJSONEncoder)
    elif request.form['chart_dropdown'] == 'bar':
        pl = px.bar(df1, **dct_text)
        jpl = json.dumps(pl, cls=plotly.utils.PlotlyJSONEncoder)
    elif request.form['chart_dropdown'] == 'hist':
        pl = px.histogram(df1, **dct_text)
        jpl = json.dumps(pl, cls=plotly.utils.PlotlyJSONEncoder)
    elif request.form['chart_dropdown'] == 'scatter':
        pl = px.scatter(df1, **dct_text)
        jpl = json.dumps(pl, cls=plotly.utils.PlotlyJSONEncoder)
    elif request.form['chart_dropdown'] == 'box':
        pl = px.box(df1, **dct_text)
        jpl = json.dumps(pl, cls=plotly.utils.PlotlyJSONEncoder)
    elif request.form['chart_dropdown'] == 'violin':
        pl = px.violin(df1, **dct_text)
        jpl = json.dumps(pl, cls=plotly.utils.PlotlyJSONEncoder)
    elif request.form['chart_dropdown'] == 'heatmap':
        pl = px.density_heatmap(df1, **dct_text)
        jpl = json.dumps(pl, cls=plotly.utils.PlotlyJSONEncoder)
    elif request.form['chart_dropdown'] == 'scatter_3d':
        pl = px.scatter_3d(df1, **dct_text)
        jpl = json.dumps(pl, cls=plotly.utils.PlotlyJSONEncoder)
    elif request.form['chart_dropdown'] == 'line_3d':
        pl = px.line_3d(df1, **dct_text)
        jpl = json.dumps(pl, cls=plotly.utils.PlotlyJSONEncoder)

    jpl_sessions[session['key']] = jpl
    return redirect('/eda')


@app.route('/submit',methods = ['POST'])
def submit():
    global dct_sessions
    global lst_sessions
    if request.method == 'POST':
        try:
            df = pd.read_csv(request.files['data_file'])
            print(df)
            session['start'] = request.form['start_index']
            session['end'] = request.form['end_index']
        except:
            session['start'] = request.form['start_index']
            session['end'] = request.form['end_index']
            return redirect('/home')

        if len(df) <= 0:
            return redirect('/home')

        try:
            if session['key'] in lst_sessions:
                dct_sessions[session['key']] = df
            else:
                for i in range(100000):
                    tmp = int(np.random.random(1) * 10000000)
                    if tmp not in lst_sessions:
                        lst_sessions.append(tmp)
                        dct_sessions[tmp] = df
                        session['key'] = tmp
                        break

        except:
            for i in range(100000):
                tmp = int(np.random.random(1) * 10000000)
                if tmp not in lst_sessions:
                    lst_sessions.append(tmp)
                    dct_sessions[tmp] = df
                    session['key'] = tmp
                    break

    return redirect('/home')

@app.route('/home')
def home():
    global dct_sessions
    global lst_sessions
    try:
        df1 = dct_sessions[session['key']]
        start = session['start']
        end = session['end']
    except:
        df1 = pd.DataFrame({"welcome": ["hello"]})
        start = 0
        end = 10
    print(start)
    print(end)
    print(df1.iloc[int(start):int(end)])
    return render_template('index.html',df=df1.iloc[int(start):int(end)],start=int(start),end=int(end))

if __name__ == '__main__':
    app.run(debug=True)
