"""Receives incoming game logs and passes them to
the correct interface"""

import hug
from src.nyingi_event_structure import EventContainer, MetadataStruct
from src.nyingi_interface import unpack_nyingi_events
from json import loads as jsonLoad
from urllib.parse import unquote


@hug.post("/upload")
def upload_file(body: hug.types.text):
    events = []
    game_name = None

    for event in unquote(body).strip().split(sep="\n"):
        new_event = EventContainer(**jsonLoad(event))
        if new_event.event_id == 0:
            game_data = MetadataStruct(**jsonLoad(new_event.json_string))
            game_name = game_data.game_name
            events.append(new_event)
        else:
            events.append(new_event)

    match game_name:
        case "Nyingi":
            unpack_nyingi_events(events)
            return
        case None:
            return body
