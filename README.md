# OCS Cloud Server

Online Coding System (OCS) Cloud Server - A Flask-based application for managing users, projects, and group collaborations.

## Features

- User authentication with password hashing (currently MD5 client-side for legacy compatibility)
- Role-based access control (Admin and User roles)
- Group project management
- Project invitation system
- Repository/project visibility after accepting invitations

## Setup

### Prerequisites

- Python 3.12 or higher
- Supabase account

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Anish-Daruka/OCS-cloud-server.git
cd OCS-cloud-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Supabase credentials:
```
S_API=your_supabase_anon_key
SECRET_KEY=your_flask_secret_key
```

4. Set up the database tables in Supabase:
   - Run the SQL commands in `schema.sql` in your Supabase SQL editor
   - This will create the `projects` and `project_members` tables

### Running the Application

```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Database Schema

### Tables

1. **users** - Stores user information
   - userid (unique)
   - passwordhash
   - role (admin/user)

2. **projects** - Stores project/repository information
   - id
   - name
   - description
   - owner_id
   - repository_url
   - created_at, updated_at

3. **project_members** - Manages project memberships and invitations
   - id
   - project_id
   - user_id
   - status (pending/accepted/declined)
   - role (owner/admin/member)
   - invited_by
   - invited_at, responded_at

## Features Explained

### Group Project Invitations

When a user is invited to a group project:

1. An entry is created in the `project_members` table with status='pending'
2. The user sees the invitation on their dashboard after login
3. The user can accept or decline the invitation
4. After accepting, the status changes to 'accepted'
5. The project now appears in "My Projects / Repositories" section

### Repository Visibility

- **Before accepting invitation**: Project is not visible in user's project list
- **After accepting invitation**: Project appears in the "My Projects / Repositories" section
- **Admin users**: Can see all projects in the system

## API Endpoints

- `GET/POST /` - User login
- `POST /accept_invitation/<invitation_id>` - Accept a project invitation
- `POST /decline_invitation/<invitation_id>` - Decline a project invitation

## Security Notes

- **IMPORTANT**: The application currently uses MD5 for password hashing (client-side hashing before transmission). MD5 is cryptographically broken and should NOT be used for new implementations.
- **For production use**: Replace MD5 with secure alternatives like bcrypt or argon2 for server-side password hashing
- Ensure `SECRET_KEY` is set to a random, secure value (use `secrets.token_hex(32)` to generate one)
- Keep Supabase API keys secure and never commit them to version control
- The invitation endpoints include authorization checks to prevent users from accepting/declining invitations that don't belong to them
- CSRF (Cross-Site Request Forgery) protection is implemented using session-based tokens for all state-changing operations
- Error messages are generic to prevent information disclosure through timing or error analysis

## Troubleshooting

### Repository Not Showing After Accepting Invitation

If you accepted a project invitation but don't see the repository:

1. **Check invitation status**: Log out and log back in to refresh the page
2. **Verify database**: Ensure the `project_members` entry has status='accepted'
3. **Check project_id**: Verify the project_id exists in the `projects` table
4. **Review logs**: Check console output for any error messages

### Common Issues

- **Database tables not found**: Run the `schema.sql` file in Supabase
- **Login fails**: Verify password is being hashed correctly
- **No projects showing**: Ensure projects exist and user has accepted memberships

## Contributing

Please ensure all code changes are tested and follow the existing code style.

## License

This project is for educational purposes.
