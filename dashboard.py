import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Loads the dataset
df_plotly = pd.read_csv('plotly.csv', sep=',')
#X = df_reference.drop(columns=['TARGET'])
#y = df_reference['TARGET']

st.set_page_config(layout="wide",initial_sidebar_state="collapsed")

def user_input_features():
        B1 = st.sidebar.slider('NAME_CONTRACT_TYPE',  0, 1,  0)
        B2 = st.sidebar.slider('CODE_GENDER', 0, 1, 1)
        B3 = st.sidebar.slider('FLAG_OWN_CAR', 0, 1, 0)
        B4 = st.sidebar.slider('FLAG_OWN_REALTY', 0, 1, 1)
        B5 = st.sidebar.slider('CNT_CHILDREN', 0, 19, 0)
        B6 = st.sidebar.slider('AMT_INCOME_TOTAL', 0, 400000, 202500)
        B7 = st.sidebar.slider('AMT_CREDIT', 0, 1000000, 406597)
        B8 = st.sidebar.slider('AMT_ANNUITY', 0,100000, 24700)
        B9 = st.sidebar.slider('EXT_SOURCE_2',  0.00000, 1.00000, 0.262949)
        B10 = st.sidebar.slider('EXT_SOURCE_3', 0.00000, 1.00000, 0.139376)
        B11 = st.sidebar.slider('AGE', 0,100,26)
        B12 = st.sidebar.slider('ANCIENNITE', 0,80,2)


    
        # Inputs to ML model
        global data
        data= {
      		"NAME_CONTRACT_TYPE": B1,
     		"CODE_GENDER": B2,
      		"FLAG_OWN_CAR": B3,
      		"FLAG_OWN_REALTY": B4,
      		"CNT_CHILDREN": B5,
      		"AMT_INCOME_TOTAL": B6,
      		"AMT_CREDIT": B7,
      		"AMT_ANNUITY": B8,
      		"EXT_SOURCE_2": B9,
      		"EXT_SOURCE_3": B10,
      		"AGE": B11,
      		"ANCIENNITE": B12
    
              }            
        features = pd.DataFrame(data, index=[0])
        return features

df = user_input_features()


tab1, tab2, tab3 = st.tabs(["Eligibilité", "Interprétabilité", "Explainabilité"])

with tab1:
     
    st.title("Bienvenue au Place de Marché!")
    st.write(
       	"The model evaluates your eligibility for a loan based on your user inputs below.\
       	Pass the appropriate details about your personal situation using the questions below to discover if you are eligible (or not)."
    	)
    # Input 1
    B1 = st.radio("Type de pret?",
     	("0", "1"), index=0, key = "1")
    
    # Input 2
    B2 = st.radio("Votre sexe? O=Femme, 1=Homme",
       	("0", "1"), index=1, key = "2")
    
    	# Input 3
    B3 = st.radio("Vous etes propriètaire d'une voiture?, 0=Non, 1=Oui",
        ("0", "1"), index=0, key = "3")
    
    # Input 4
    B4 = st.radio("Vous etes propriètaire d'une maison/appartement?, 0=Non, 1=Oui",
        ("0", "1"), index=1, key = "4")
    
    # Input 5
    B5 = st.number_input("Combien d'enfants avez-vous?",
                                 min_value=0, value=0, step=500)
    
    # Input 6
    B6 = st.number_input('Vos revenus annuels?',
                               min_value=0, value=202500, step=500)
    
    # Input 7
    B7 = st.number_input('Montant total de vos prets?',
                               min_value=0, value=406597, step=500)
    
    # Input 8
    B8 = st.number_input('Remboursements annuels de vos prets?',
                                min_value=0, value=24700, step=1)
    
    B9 = 0.262949   
    B10= 0.139376
    
    # Input 11
    B11 = st.number_input('Votre Age?',
                               min_value=0, value=26, step=1)
    
    # Input 12
    B12 = st.number_input('Anciennité chez votre employeur actuelle?',
                                min_value=0, value=2, step=1)
    
    
    # When 'Submit' is selected
    if st.button("Submit"):
    
        # Inputs to ML model
        data= {
      		"NAME_CONTRACT_TYPE": B1,
     		"CODE_GENDER": B2,
      		"FLAG_OWN_CAR": B3,
      		"FLAG_OWN_REALTY": B4,
      		"CNT_CHILDREN": B5,
      		"AMT_INCOME_TOTAL": B6,
      		"AMT_CREDIT": B7,
      		"AMT_ANNUITY": B8,
      		"EXT_SOURCE_2": B9,
      		"EXT_SOURCE_3": B10,
      		"AGE": B11,
      		"ANCIENNITE": B12
    
              }            
        
    
        response = requests.post(f"https://p7fastapi.azurewebsites.net/", json=data)
     #      response = requests.post(f"http://localhost:8000/", json=data)
        prediction=response.text
 
        if prediction < '0.5': 
            st.write('Accepté :thumbsup:')
     #      st.image("https://ocp7api.azurewebsites.net/OK")
        else: 
            st.write('Refusé :thumbsdown:') 
     #      st.image("https://ocp7api.azurewebsites.net/KO")

        y=prediction
        st.write('Probability = ', y, '  (Threshold=0.5)')


with tab2:    

    
# Print specified input parameters
    st.header('Client Input parameters')
    st.write(df)

    #     response = requests.post(f"https://p7fastapi.azurewebsites.net/", json=data)
    response = requests.post(f"https://p7fastapi.azurewebsites.net/", json=data)
    prediction=response.text
 
    x=prediction
    st.write('Probability = ', x, '  (Threshold=0.5)')
#    st.write("---")
    if prediction < '0.2': 
         st.write(":thumbsup: Félicitations! Votre crédit est accepté!")
    elif prediction < '0.5': 
         st.write(":thumbsup: Félicitations! Votre crédit est accepté!")
    else: 
         st.write(":thumbsdown: Désolé, votre crédit est réfusé. N'hésitez pas à contacter votre téléconseiller pour plus d'information!") 
    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
    	
        if prediction < '0.2': 
    #         st.write(":thumbsup: Félicitations! Votre crédit est accepté!")
    #         st.write("---")
             st.header('L’interprétabilité locale')
             st.image("local2.png")
        elif prediction < '0.5': 
    #         st.write(":thumbsup: Félicitations! Votre crédit est accepté!")
    #         st.write("---")
             st.header('L’interprétabilité locale')
    #        st.image("http://localhost:8000/OK")	    
             st.image("https://p7fastapi.azurewebsites.net/OK")   
        else: 
    #         st.write(":thumbsdown: Désolé, votre crédit est réfusé. N'hésitez pas à contacter votre téléconseiller pour plus d'information!") 
    #         st.write("---")
             st.header('L’interprétabilité locale')
    #         st.image("http://localhost:8000/KO")
             st.image("https://p7fastapi.azurewebsites.net/OK")	

    with col2:
    
            st.header('L’interprétabilité globale')
            st.image("global1.png")

with tab3:
    st.header('Client parameters')
    st.write(df)

    response = requests.post(f"https://p7fastapi.azurewebsites.net/", json=data)
    # response = requests.post(f"http://localhost:8000/", json=data)
    prediction=response.text
 
    x=prediction
    st.write('Probability = ', x, '  (Threshold=0.5)')
    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(data_frame=df_plotly, x='AGE', color='TARGET')
        st.plotly_chart(fig, use_container_width=True)
        fig = px.histogram(data_frame=df_plotly, x='PREDICTION', color='TARGET')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(data_frame=df_plotly, x='EXT_SOURCE_2', color='TARGET')
        st.plotly_chart(fig, use_container_width=True)        
        fig = px.histogram(data_frame=df_plotly, x='EXT_SOURCE_3', color='TARGET')
        st.plotly_chart(fig, use_container_width=True)