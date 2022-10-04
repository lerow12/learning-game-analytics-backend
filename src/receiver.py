"""Receives incoming game logs and passes them to
the correct interface"""

import hug

@hug.post("/upload")
def upload_file(body):
    print(body)
    return body
