import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/tasks"]


"""def get_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    service = build("tasks", "v1", credentials=creds)
    return service


def add_task(task_title, task_notes=None, due_date=None):
    service = get_service()
    # Get the user's default task list
    tasklists = service.tasklists().list(maxResults=1).execute()
    tasklist_id = tasklists["items"][0]["id"]

    # Prepare the task body
    task = {"title": task_title}
    if task_notes:
        task["notes"] = task_notes
    if due_date:
        task["due"] = due_date

    result = service.tasks().insert(tasklist=tasklist_id, body=task).execute()
    print(f"Task created: {result['title']} (ID: {result['id']})")"""
