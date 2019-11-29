from flask import Flask
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



except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    print("Falha conexao com o banco!")

finally:
 
    @app.route('/')
    def grafic():
        frame = pd.DataFrame(df)
        frame.dropna(inplace=True)
        frame1 = frame[(frame['mensalidade']>3000) & (frame['universidade_nome'])]
        #rel_mens_uf = frame1[['uf_busca', 'mensalidade']]
        dados_mens = frame1['mensalidade']
        dados_uni_name = frame1['universidade_nome']
        print(dados_uni_name)
        vet_dados_mens=[]
        vet_dados_uini_name=[]
        for i in dados_mens:
            vet_dados_mens.append(i)
        for j in dados_uni_name:
            vet_dados_uini_name.append(j)
            print(j)
        
        dados_json = {
            "dados_mens": vet_dados_mens,
            "dados_uni_name": vet_dados_uini_name
            }

        values_json = json.dumps(dados_json)
        

        @socketio.on('message')
        def menssagem(message):
            print(message) 
            emit('message', values_json)
            #time.sleep(1)
        return render_template('home.html')

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port= 8888)
   