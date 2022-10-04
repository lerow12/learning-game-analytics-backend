import hug
import src.receiver as receiver

def test_upload_file():
    TEST_STR = b"JSON STRING"
    response = hug.test.post(receiver, "/upload", TEST_STR)
    assert response.status == hug.HTTP_200
    assert response.data == TEST_STR.decode("utf-8")
