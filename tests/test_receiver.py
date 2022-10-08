import hug
import src.receiver as receiver


def test_upload_file():
    TEST_EVENT = b'{"EVENTID": -1, "Timestamp": "", "jsonString": ""}'
    response = hug.test.post(receiver, "/upload", TEST_EVENT)
    assert response.status == hug.HTTP_200
    assert response.data == TEST_EVENT.decode("utf-8")
