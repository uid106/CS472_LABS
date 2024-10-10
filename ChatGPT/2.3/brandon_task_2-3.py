"""
Serve web UI and API for the application.

See here for instructions on how to serve matplotlib figures:
 - https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
"""

import atexit
import io
from contextlib import redirect_stdout
from datetime import datetime
from importlib import resources
from itertools import islice

import flask
from flask import current_app, request

# Import necessary modules and functions for executing commands, managing logs, etc.
from ..commands import execute_cmd
from ..dirs import get_logs_dir
from ..llm import reply
from ..logmanager import LogManager, get_user_conversations
from ..message import Message
from ..models import get_model
from ..tools import execute_msg

# Initialize a Flask Blueprint to define API routes
api = flask.Blueprint("api", __name__)

# Basic "Hello World!" route to confirm the API is working
@api.route("/api")
def api_root():
    return flask.jsonify({"message": "Hello World!"})


# Route to fetch user conversations, with a limit on how many to retrieve
@api.route("/api/conversations")
def api_conversations():
    limit = int(request.args.get("limit", 100))  # Default limit is 100 conversations
    conversations = list(islice(get_user_conversations(), limit))  # Get conversations
    return flask.jsonify(conversations)  # Return the conversations as JSON


# Route to fetch a specific conversation by its log file
@api.route("/api/conversations/<path:logfile>")
def api_conversation(logfile: str):
    """Get a conversation."""
    log = LogManager.load(logfile)  # Load the conversation log from the file
    return flask.jsonify(log.to_dict(branches=True))  # Return the log in JSON format


# Route to create or update a conversation
@api.route("/api/conversations/<path:logfile>", methods=["PUT"])
def api_conversation_put(logfile: str):
    """Create or update a conversation."""
    msgs = []
    req_json = flask.request.json  # Get JSON from the request body
    if req_json and "messages" in req_json:
        # Iterate through the messages and convert to Message objects
        for msg in req_json["messages"]:
            timestamp: datetime = datetime.fromisoformat(msg["timestamp"])
            msgs.append(Message(msg["role"], msg["content"], timestamp=timestamp))

    # Check if the log directory already exists; if not, create it
    logdir = get_logs_dir() / logfile
    if logdir.exists():
        raise ValueError(f"Conversation already exists: {logdir.name}")
    logdir.mkdir(parents=True)
    
    # Save the messages into the log
    log = LogManager(msgs, logdir=logdir)
    log.write()  # Write the log to a file
    return {"status": "ok"}  # Return success status


# Route to post a new message to an existing conversation
@api.route("/api/conversations/<path:logfile>", methods=["POST"])
def api_conversation_post(logfile: str):
    """Post a message to the conversation."""
    req_json = flask.request.json  # Get JSON from the request body
    branch = (req_json or {}).get("branch", "main")  # Default branch is 'main'
    
    # Load the conversation log file
    log = LogManager.load(logfile, branch=branch)
    
    # Ensure that necessary fields (role, content) are provided
    assert req_json
    assert "role" in req_json
    assert "content" in req_json
    
    # Create a new message and append it to the conversation log
    msg = Message(req_json["role"], req_json["content"], files=req_json.get("files", []))
    log.append(msg)
    
    return {"status": "ok"}  # Return success status


# Route to generate a response based on the conversation's messages
@api.route("/api/conversations/<path:logfile>/generate", methods=["POST"])
def api_conversation_generate(logfile: str):
    # Get the model specified in the request, or use the server's default model
    req_json = flask.request.json or {}
    model = req_json.get("model", get_model().model)

    # Load the conversation from the log file
    log = LogManager.load(logfile, branch=req_json.get("branch", "main"))

    # Check if the last message in the log is from the user and process commands
    if log[-1].role == "user":
        f = io.StringIO()  # Capture command output
        print("Begin capturing stdout, to pass along command output.")
        with redirect_stdout(f):  # Redirect stdout to capture the command output
            resp = execute_cmd(log[-1], log)
        print("Done capturing stdout.")
        
        if resp:  # If the command produced a response, save it to the log
            log.write()
            output = f.getvalue()
            return flask.jsonify([{"role": "system", "content": output, "stored": False}])

    # Prepare messages for response generation (context trimming, if needed)
    msgs = log.prepare_messages()

    # Generate a response using the model
    msg = reply(msgs, model=model, stream=True)  # Response can be streamed
    msg = msg.replace(quiet=True)  # Quietly replace the last message
    
    # Append the response and any additional tool messages to the log
    resp_msgs = []
    log.append(msg)
    resp_msgs.append(msg)
    for reply_msg in execute_msg(msg, ask=False):  # Run tools if necessary
        log.append(reply_msg)
        resp_msgs.append(reply_msg)

    # Return the response messages as JSON
    return flask.jsonify([{"role": msg.role, "content": msg.content} for msg in resp_msgs])


# Context for loading paths for static and media files
gptme_path_ctx = resources.as_file(resources.files("gptme"))
root_path = gptme_path_ctx.__enter__()
static_path = root_path / "server" / "static"
media_path = root_path.parent / "media"

# Ensure that resources are cleaned up on exit
atexit.register(gptme_path_ctx.__exit__, None, None, None)


# Serve the main index.html page from the root URL
@api.route("/")
def root():
    return current_app.send_static_file("index.html")


# Serve the favicon (logo) of the application
@api.route("/favicon.png")
def favicon():
    return flask.send_from_directory(media_path, "logo.png")


# Function to create and configure the Flask app
def create_app() -> flask.Flask:
    """Create the Flask app."""
    app = flask.Flask(__name__, static_folder=static_path)  # Set the static folder
    app.register_blueprint(api)  # Register the API blueprint with the app
    return app  # Return the Flask app instance
