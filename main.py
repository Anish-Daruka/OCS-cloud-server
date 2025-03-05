from flask import Flask, request, jsonify, render_template, redirect, url_for
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
load_dotenv()
S_URL = "https://qcjovsotomulhqjckaal.supabase.co"
S_KEY = os.getenv("S_API")
# Initialize Supabase client
print(S_KEY)
supabase: Client = create_client(S_URL, S_KEY)

@app.route('/', methods=['GET','POST'])
def userlogin():
    if request.method=='POST':
        print(request)
        # Always use form data
        userid = request.form.get("username")
        password = request.form.get("password")
        print(password)

        response = supabase.table('users').select('*').eq('userid', userid).execute()
        response1 = supabase.table('users').select('*').execute()
        print(response)
        
        if response.data:
            user = response.data[0]
            if user['passwordhash'] != password:
                print("wrongpassword")
                return render_template('index.html', flag=False)
            else:
                print("correct")
                if user['role'] == 'admin':
                    response = supabase.table('users').select('*').execute()
                    print(response.data)
                    return render_template('data.html', response=response.data)
                else:
                    response = supabase.table('users').select('*').eq('userid', userid).execute()
                    print(response)
                    return render_template('data.html', response=response.data)
        else:
            print("invalid username")
            return render_template('index.html', flag=False)
        
        

    return render_template('index.html',flag=True)


    




if __name__ == '__main__':
    app.run()

