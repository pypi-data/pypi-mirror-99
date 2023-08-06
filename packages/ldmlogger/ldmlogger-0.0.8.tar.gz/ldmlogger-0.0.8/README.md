# LDMLogger

## Class LDMLogger contains methods for working with LDM framework.

## Methods:

### def __init__(self, user_token, project_id=None, server_url="http://localhost:5000", root_dir=Path(os.getcwd()).parent, should_upload_sources = False)
    Creates new instance of class LDMLogger


### def start_run(self, comment = "", git_commit_url = "" ):
    Starts a new run
### def log(self, body):
    Logs message msg to server.
### def finish_run(self):
    Finish the current run.
### def validate(self, results, dataset_type="Train"):
    Validate on dataset.
### def upload_file(self, file_name, comment = ""):
    Uploads file (file_name) to the logging server and attaches it to the current run.
### def add_project(self, name, project_type, description=""):
    Adding project.
### def upload_dataset(self, path_to_dataset,dataset_type_in="Train"):
    Uploads dataset to server.
### def upload_sources(self):
    Creates a .zip of root_dir and uploads it to the LDM server.
### def download_dataset(self, path="", dataset_type_in="Train"):
    Downloads dataset from server.
### def save_colab_notebook_history_to_file(self, file_name):
    Creates new notebook containing history of all executed cells of the current notebook.



