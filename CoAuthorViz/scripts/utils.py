import os
import json


def load_sessions(verbose=1):
    dataset_dir = './coauthor-v1.0'
    sessions = [
        os.path.join(dataset_dir, path)
        for path in os.listdir(dataset_dir)
        if path.endswith('jsonl')
    ]
    if verbose:
        print(
            f'Successfully downloaded {len(sessions)} writing sessions in CoAuthor!')
    return sessions


def read_session(session, verbose=1):
    events = []
    with open(session, 'r') as f:
        for event in f:
            events.append(json.loads(event))
    if verbose:
        print(
            f'Successfully read {len(events)} events in a writing session from {session}')
    return events


def read_file(file_name):
    # dataset_dir = './coauthor-v1.0'
    # session = dataset_dir + "/" + file_name
    session = file_name
    events = read_session(session)
    return events


def read_id(file_name):
    file_name = file_name.split("/")[-1]
    file_name = file_name.split(".")[0]
    return file_name
