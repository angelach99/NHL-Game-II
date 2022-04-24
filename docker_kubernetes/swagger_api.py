# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 03:33:25 2022

@author: vvaib
"""

from flask import Flask, request
import numpy as np
import pickle
import pandas as pd
import flasgger
from flasgger import Swagger

app=Flask(__name__)
Swagger(app)

pickle_in = open("classifier.pkl","rb")
classifier=pickle.load(pickle_in)

@app.route('/')
def welcome():
    return "Welcome All"

@app.route('/predict',methods=["Get"])
def predict_note_authentication():
    
    """Let's Authenticate the NHL prediction 
    This is using docstrings for specifications.
    ---
    parameters:  
      - name: Shots
        in: query
        type: number
        required: true
      - name: Shots Against
        in: query
        type: number
        required: true
      - name: Goals
        in: query
        type: number
        required: true
      - name: Goals Against
        in: query
        type: number
        required: true
      - name: Takeaways
        in: query
        type: number
        required: true
      - name: Takeaways Against
        in: query
        type: number
        required: true
      - name: Hits
        in: query
        type: number
        required: true
      - name: Hits Against
        in: query
        type: number
        required: true
      - name: Blocked Shots
        in: query
        type: number
        required: true
      - name: Blocked Shots Against
        in: query
        type: number
        required: true
      - name: Giveaways
        in: query
        type: number
        required: true
      - name: Giveaways Against
        in: query
        type: number
        required: true
      - name: Missed Shots
        in: query
        type: number
        required: true
      - name: Missed Shots Against
        in: query
        type: number
        required: true
      - name: Penalities
        in: query
        type: number
        required: true
      - name: Penalities Against
        in: query
        type: number
        required: true
      - name: Won Faceoffs
        in: query
        type: number
        required: true
      - name: Lost Faceoffs
        in: query
        type: number
        required: true
      - name: Hoa Away
        in: query
        type: number
        required: true
      - name: Hoa Home
        in: query
        type: number
        required: true
    responses:
        200:
            description: The output values
        
    """
    
    shots=request.args.get("shots")
    shots_against=request.args.get("shots_against")
    goals=request.args.get("Goals")
    goals_against=request.args.get("goals_against")
    takeaways=request.args.get("takeaways")
    takeaways_against=request.args.get("takeaways_against")
    hits=request.args.get("hits")
    hits_against=request.args.get("hits_against")
    blocked_shots=request.args.get("blocked_shots")
    blocked_shots_against=request.args.get("blocked_shots_against")
    giveaways=request.args.get("giveaways")
    giveaways_against=request.args.get("giveaways_against")
    missed_shots=request.args.get("missed_shots")
    missed_shots_against=request.args.get("missed_shots_against")
    penalities=request.args.get("penalities")
    penalities_against=request.args.get("penalities_against")
    won_faceoffs=request.args.get("won_faceoffs")
    lost_faceoffs=request.args.get("Lost faceoffs")
    hoa_away=request.args.get("hoa_away")
    hoa_home=request.args.get("hoa_home")
    prediction=classifier.predict([[shots,shots_against,goals,goals_against,takeaways,takeaways_against,hits,
                                    hits_against,blocked_shots,blocked_shots_against,giveaways,giveaways_against,
                                    missed_shots,missed_shots_against,penalities,penalities_against,won_faceoffs,
                                    lost_faceoffs,hoa_away,hoa_home]])
    odds = classifier.predict_proba([[shots,shots_against,goals,goals_against,takeaways,takeaways_against,hits,
                                    hits_against,blocked_shots,blocked_shots_against,giveaways,giveaways_against,
                                    missed_shots,missed_shots_against,penalities,penalities_against,won_faceoffs,
                                    lost_faceoffs,hoa_away,hoa_home]])
    return "The Team will " + ("Win" if prediction != 0 else "Lose") + " and odds are " + str(odds*100)
    
    #str(prediction)

@app.route('/predict_file',methods=["POST"])
def predict_note_file():
    """Let's Authenticate the NHL prediction 
   This is using docstrings for specifications.
   ---
   parameters:
     - name: file
       in: formData
       type: file
       required: true
     
   responses:
       200:
           description: The output values
       
   """
    df_test=pd.read_csv(request.files.get("file"))
    prediction=classifier.predict(df_test)
    return "The predicted value for the csv is"+ str(list(prediction))
    

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8000)
    