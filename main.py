from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")
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
                # Store user info in session
                session['userid'] = userid
                session['role'] = user['role']
                
                if user['role'] == 'admin':
                    response = supabase.table('users').select('*').execute()
                    print(response.data)
                    # Get all projects for admin
                    projects = get_all_projects()
                    return render_template('data.html', response=response.data, projects=projects, userid=userid)
                else:
                    response = supabase.table('users').select('*').eq('userid', userid).execute()
                    print(response)
                    # Get projects for this user
                    projects = get_user_projects(userid)
                    invitations = get_user_invitations(userid)
                    return render_template('data.html', response=response.data, projects=projects, 
                                         invitations=invitations, userid=userid)
        else:
            print("invalid username")
            return render_template('index.html', flag=False)
        
        

    return render_template('index.html',flag=True)


def get_user_projects(userid):
    """Get all projects that the user has access to"""
    try:
        # Get projects where user is a member
        members_response = supabase.table('project_members').select('project_id').eq('user_id', userid).eq('status', 'accepted').execute()
        
        if not members_response.data:
            return []
        
        project_ids = [member['project_id'] for member in members_response.data]
        
        # Get project details
        projects = []
        for project_id in project_ids:
            project_response = supabase.table('projects').select('*').eq('id', project_id).execute()
            if project_response.data:
                projects.extend(project_response.data)
        
        return projects
    except Exception as e:
        print(f"Error getting user projects: {e}")
        return []


def get_user_invitations(userid):
    """Get pending invitations for the user"""
    try:
        invitations_response = supabase.table('project_members').select('*, projects(*)').eq('user_id', userid).eq('status', 'pending').execute()
        return invitations_response.data if invitations_response.data else []
    except Exception as e:
        print(f"Error getting user invitations: {e}")
        return []


def get_all_projects():
    """Get all projects (for admin)"""
    try:
        projects_response = supabase.table('projects').select('*').execute()
        return projects_response.data if projects_response.data else []
    except Exception as e:
        print(f"Error getting all projects: {e}")
        return []


@app.route('/accept_invitation/<int:invitation_id>', methods=['POST'])
def accept_invitation(invitation_id):
    """Accept a project invitation"""
    userid = session.get('userid')
    if not userid:
        return redirect(url_for('userlogin'))
    
    try:
        # Update invitation status to accepted
        supabase.table('project_members').update({'status': 'accepted'}).eq('id', invitation_id).eq('user_id', userid).execute()
        return redirect(url_for('userlogin'))
    except Exception as e:
        print(f"Error accepting invitation: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/decline_invitation/<int:invitation_id>', methods=['POST'])
def decline_invitation(invitation_id):
    """Decline a project invitation"""
    userid = session.get('userid')
    if not userid:
        return redirect(url_for('userlogin'))
    
    try:
        # Update invitation status to declined
        supabase.table('project_members').update({'status': 'declined'}).eq('id', invitation_id).eq('user_id', userid).execute()
        return redirect(url_for('userlogin'))
    except Exception as e:
        print(f"Error declining invitation: {e}")
        return jsonify({'error': str(e)}), 500


    




if __name__ == '__main__':
    app.run()

