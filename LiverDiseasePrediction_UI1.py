# -*- coding: utf-8 -*-
"""
Created on Sat May 28 10:46:31 2022

@author: Divyarani
"""


#Importing Libraries
import pandas as pd
import webbrowser
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pickle
from dash.dependencies import Input, Output, State
import os
import numpy as np


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server


def load_model():
    
    global pickle_model
    global pickle_cTransformer
    
    
    file1 = open('./assets/tuned_ada_model.pkl','rb')
    pickle_model = pickle.load(file1)
    
    #file2 = open('./assets/winch_pickle_cTransformer.pkl','rb')
    #pickle_cTransformer = pickle.load(file2)
    
def estimate_price(Age,Gender,Total_Bilirubin,Direct_Bilirubin,Alkphos,Sgpt,Sgpot,Total_Protein,Albumin,AG_Ratio):
    
    to_predict = [[Age,Gender,Total_Bilirubin,Direct_Bilirubin,Alkphos,Sgpt,Sgpot,Total_Protein,Albumin,AG_Ratio]]
        
    return pickle_model.predict(to_predict)

                          
    
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")
    
    
    
def create_app_ui():
    main_layout = html.Div([
            html.Div([
                html.H4("Enter The Patient Details", style={
                    'text-align':'center','color':'#007bff'
                    }),
                html.Hr(),
                html.Div([
                    html.I("Age"),
                    html.Br(),
                    dcc.Input(id='age',type='number',placeholder="", className='input-field'),
                    html.Br(),
                    
                    html.I('Gender'),
                    html.Br(),
                    dcc.Input(id='gender',type='number',placeholder="", className='input-field'),
                    html.Br(),
                    html.Br(),
                    
                    html.I('Total Bilirubin'),
                    html.Br(),
                    dcc.Input(id='total_bilirubin',type='number',placeholder="", className='input-field'),
                    html.Br(),
                    html.Br(),
                    
                    html.I('Direct Bilirubin'),
                    html.Br(),
                    dcc.Input(id='direct_bilirubin',type='number',placeholder="", className='input-field'),
                    html.Br(),
                    html.Br(),
                    
                    html.I('Alkaline phosphatase'),
                    html.Br(),
                    dcc.Input(id='alkphos',type='number',placeholder="", className='input-field'),
                    html.Br(),
                    html.Br(),
                    
                    html.I('Alanine Aminotransferase'),
                    html.Br(),
                    dcc.Input(id='sgpt',type='number',placeholder="", className='input-field'),
                    html.Br(),
                    html.Br(),
                    
                    html.I('Aspartate Aminotransferase'),
                    html.Br(),
                    dcc.Input(id='sgpot',type='number',placeholder="", className='input-field'),
                    html.Br(),
                    html.Br(),
                    
                    html.I('Total Protein'),
                    html.Br(),
                    dcc.Input(id='total_protein',type='number',placeholder="", className='input-field'),
                    html.Br(),
                    html.Br(),
                    
                    html.I('Albumin'),
                    html.Br(),
                    dcc.Input(id='albumin',type='number',placeholder="", className='input-field'),
                    html.Br(),
                    html.Br(),
                    
                    html.I('Albumin/Globulin Ratio'),
                    html.Br(),
                    dcc.Input(id='ag_ratio',type='number',placeholder="", className='input-field'),
                    html.Br(),
                    html.Br(),
                    
                    html.Div([
                        dbc.Row([
                            dbc.Col(html.Div([
                                dbc.Button(
                                    children='Estimate',
                                    id = 'button_estimate',
                                    className='est-btn',
                                    color='primary'
                                    )
                                
                                
                                ]), md=7),
                            
                            dbc.Col(html.Div([
                                dbc.Button(
                                    children='Reset',
                                    id = 'reset_button',
                                    className='est-btn',
                                    color='primary'
                                    )
                                ]), md=5)
                            
                            ])
                        ]),
                    
                    html.Br(),
                    
                    html.Div([
                        html.H5("The Result is: "),
                        html.H5(id = 'result', style={'color':'#e25f6b'})
                        
                        ])
                    
                    
                    
                    
                    ], className='sub-div')
                
                ], className='main-div')
        
        
        
        ])
                                       
    return main_layout
 
    
@app.callback(
    Output('result', 'children'),
    [
     Input('button_estimate','n_clicks')
     ],
    [
     State('age', 'value'),
     State('gender', 'value'),
     State('total_bilirubin', 'value'),
     State('direct_bilirubin', 'value'),
     State('alkphos', 'value'),
     State('sgpt', 'value'),
     State('sgpot', 'value'),
     State('total_protein', 'value'),
     State('albumin', 'value'),
     State('ag_ratio', 'value')
     
     ]
    )


def update_app_ui(n_clicks,Age,Gender,Total_Bilirubin,Direct_Bilirubin,Alkphos,Sgpt,Sgpot,Total_Protein,Albumin,AG_Ratio):
    if n_clicks != None:
        if n_clicks > 0 :
            pred = estimate_price(Age,Gender,Total_Bilirubin,Direct_Bilirubin,Alkphos,Sgpt,Sgpot,Total_Protein,Albumin,AG_Ratio)
            #print(pred, "Estimated Price")
            
            if pred == 0:
                pred1 = "The Patient's not affected by Liver Disease"
            else:
                pred1 = "The Patient's affected by Liver Disease"
            
            return str(pred1)
    
            
    
@app.callback(
    [
     Output('age', 'value'),
     Output('gender', 'value'),
     Output('total_bilirubin', 'value'),
     Output('direct_bilirubin', 'value'),
     Output('alkphos', 'value'),
     Output('sgpt', 'value'),
     Output('sgpot', 'value'),
     Output('total_protein', 'value'),
     Output('albumin', 'value'),
     Output('ag_ratio', 'value')
     
     ],
    [
     Input('reset_button','n_clicks')   
     
     ],
    [
     State('age', 'value'),
     State('gender', 'value'),
     State('total_bilirubin', 'value'),
     State('direct_bilirubin', 'value'),
     State('alkphos', 'value'),
     State('sgpt', 'value'),
     State('sgpot', 'value'),
     State('total_protein', 'value'),
     State('albumin', 'value'),
     State('ag_ratio', 'value')
     ]
    
    
    )

def reset_form(n_clicks,Age,Gender,Total_Bilirubin,Direct_Bilirubin,Alkphos,Sgpt,Sgpot,Total_Protein,Albumin,AG_Ratio):
    if n_clicks != None:
        if n_clicks > 0:
            return "", "", "", "", "", "", "", "", "", ""
        else:
            return "", "", "", "", "", "", "", "", "", ""
    else:
        return "", "", "", "", "", "", "", "", "", ""

def main():
    print("Welcome to the Application")
    
    load_model()
    open_browser()
    
    global project_name
    project_name = 'Liver Disease Prediction'
    
    global app
    app.title = project_name
    app.layout = create_app_ui()
    app.run_server(debug=True)
    
    print("This would be executed only after the server is down/stopped")
    
    app = None
    project_name = None
    
    
if __name__ == '__main__':
    main()
    
