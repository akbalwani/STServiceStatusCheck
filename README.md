it's a python script which checks the ST service status and alert administrators about service failure.

1. Start by installing all requirements "pip install -r requirements.txt"
2. MOdify the below in script.
- stHost (IP Address of the node being monitored.) and stPort values (8444 for non root installation)
- basicAuth (generated using command -> "echo -n user:pass|base64")
    also, you can use a python lib to base64 encode it, the main purpose is not storing password in plain text.
