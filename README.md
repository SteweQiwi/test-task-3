Install the project
=================

1. **Clone the repository:**

2. **Create and activate a virtual environment:**

   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. **cd backend**

4. **Install dependencies:**

   pip install -r requirements.txt

5. **Apply migrations:**

   python manage.py migrate

6. **Load initial data:**

   sqlite3 db.sqlite3 < db_dump.sql

7. **Run the server:**

   python manage.py runserver


Accessing the API
=================

Authentication
--------------
This API suppots simple_jwt authentication with standard getting of token AND

This API supports session authentication. You can log in through the Django admin interface. Use the following credentials:

Admin User:
- **Username:** root
- **Password:** rootroot

Regular User(staff, you can login from admin):
- **Username:** user2
- **Password:** rootroot

Once logged in, you can access the API endpoints:

- **Threads:** `http://localhost:8000/api/messaging/threads/`
- **Messages:** `http://localhost:8000/api/messaging/threads/<thread_id>/messages/`

Endpoints
---------
- `GET /api/messaging/threads/` - List all threads for the authenticated user.
- `POST /api/messaging/threads/` - Create a new thread (or retrieve an existing one).
- `DELETE /api/messaging/threads/<id>/` - Delete a thread (only for participants).
- `GET /api/messaging/threads/<id>/messages/` - List messages in a thread (requires thread ID in the URL).
- `POST /api/messaging/threads/<id>/messages/` - Create a new message in a thread.
- `POST /api/messaging/threads/<id>/messages/bulk_mark_read/` - Mark a messages as read for not sender.
- `GET /api/messaging/unread_messages/count/` - Retrieve the count of unread messages for the authenticated user.

