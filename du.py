from flask import Flask  #Flask é um pequeno framework web escrito em Python e baseado na biblioteca WSGI Werkzeug e na biblioteca de Jinja2. 
from flask import render_template
import json
from flask_socketio import SocketIO
from flask_socketio import send, emit
import time
import pandas as pd

 
app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'Eduardo'
socketio = SocketIO(app)


try:
    df = pd.read_csv('dados.csv')



except :
    print ("Erro ao tentar abrir o dataset!")
    

finally:
 
    @app.route('/')
    def grafic():
        frame = pd.DataFrame(df) #Cria um dataframe do dataset
        frame.dropna(inplace=True) #exclui as linhas que contem um Not a Number (NaN)
        frame1 = frame[(frame['mensalidade']>6000) & (frame['universidade_nome'])].sort_values('mensalidade',ascending=False)  #cria um dataframe relacionando a mensalidade com os nomes das instituições cujo a mensalidade é superior a 6000,00
        dados_mens = frame1['mensalidade'] # cria uma série da coluna mensalidade embasada na relação frame1
        dados_uni_name = frame1['universidade_nome'] # cria uma série da coluna universidade_nome embasada na relação frame1
        vet_dados_mens=[] #lista para os valores da serie dados_mens
        vet_dados_uini_name=[] #lista para os valores da serie vet_dados_uini_name
        vet_dados_notas_corte_ampla=[]  #lista para os valores da serie vet_dados_notas_corte_ampla

        for i in dados_mens: #loop para interar a série dados_mens na lista vet_dados_mens
            vet_dados_mens.append(i)
        
        for j in dados_uni_name: #loop para interar a série dados_mens na lista dados_uni_name
            vet_dados_uini_name.append(j)

        #Bivlioteca python       
        dados_json = {
            "dados_mens": vet_dados_mens,
            "dados_uni_name": vet_dados_uini_name
            
            }
        
        #converte a biblioteca dados_json em objeto json
        values_json = json.dumps(dados_json)
        
        #cria uma conexão com o socket
        @socketio.on('message')
        def menssagem(message):
            print(message) 
            emit('message', values_json) #envia o objeto values_json para o cliente
            
        return render_template('home.html') #renderiza o html

#configura o server
if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port= 8888)
   