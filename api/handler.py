import pickle
import pandas as pd
from flask import Flask, request, Response
from HealthInsurance import HealthInsurance
import os

#loading model
path = os.path.join(os.path.abspath(''), 'models')
with open(os.path.join(path, 'final_lgbm_model.pkl'),'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

@app.route('/predict', methods = ['POST'])
def health_insurance_predict():
    test_json = request.get_json()
    
    if test_json: # there is data
        if isinstance( test_json, dict ): # unique example
            test_raw = pd.DataFrame( test_json, index=[0] )
            
        else: # multiple example
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() )
            
        # Instantiate HealthInsurance class
        pipeline = HealthInsurance()
        
        # feature engineering
        df1 = pipeline.data_cleaning( test_raw )
        
        # data preparation
        df2 = pipeline.data_preparation( df1 )
        
        # prediction
        df_response = pipeline.get_prediction( model, df1, df2, test_raw )
        
        return df_response
    
    else:
        return Response( '{"response": "No data provided"}', status=200, mimetype='application/json' )
    
if __name__ == '__main__':
    app.run( '0.0.0.0', port=5000, debug = True )