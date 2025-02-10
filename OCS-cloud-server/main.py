from flask import Flask,request,jsonify,render_template
from supabase import create_client, Client
import os

app = Flask(__name__)


S_URL = "https://qcjovsotomulhqjckaal.supabase.co"
S_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFjam92c290b211bGhxamNrYWFsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg0NzQ5OTIsImV4cCI6MjA1NDA1MDk5Mn0.bX8v5H3udzuQYyt2pt6hWfEqlG6titv_d_0RSQhOsBc"
# Initialize Supabase client
supabase: Client = create_client(S_URL, S_KEY)

@app.route('/login', methods=['GET','POST'])
def userlogin():
    response1 = supabase.table('users').select('*').execute()
    print(response1)
    if(request.method=='POST'):
        userid=request.json.get("username")
        password=request.json.get('password')
        print(password)

        response = supabase.table('users').select('*').eq('userid', userid).execute()
        response1 = supabase.table('users').select('*').execute()
        print(response1)
        if response.data:
            print("HELLO")
            user = response.data[0]
            if(user['password']!=password):
                return render_template('index.html',flag=False)
            else:
                if(user['role']=='admin'):
                    userinfo(userid)
                else:
                    userinfo("-1")    
        else:
            print("hello")
            return render_template('index.html',flag=False)
        
        

    return render_template('index.html',flag=True)


@app.route("/userinfo",methods=['GET','POST'])
def userinfo(userid):
    if(userid=="-1"):
        response=supabase.table('users').select('*').eq('userid', userid).execute()
        return render_template('data.html',response)
    else:
        response=supabase.table('users').select('*').execute()
        return render_template('data.html',response)

    




if __name__ == '__main__':
    app.run(debug=True)

