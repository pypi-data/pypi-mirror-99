# -*- coding: utf-8 -*-

from . import wh_setting, api_list

def list(project_idx,episode_idx,sequence_idx="all"):

    if sequence_idx == "all":
        api = api_list.shot_bulk_list %(project_idx, episode_idx)

    else:
        api = api_list.shot_list %(project_idx,episode_idx,sequence_idx)

    result = wh_setting.get_requests(api=api)
    return result

def read(project_idx,shot_idx):
    api = api_list.shot_read %(project_idx,shot_idx)
    result = wh_setting.get_requests(api=api)
    return result

def create(project_idx,episode_idx,sequence_idx,shot_name,description="",status_idx="1"):
    api = api_list.shot_create %(project_idx,episode_idx,sequence_idx)
    data = {"shot_name":shot_name,"description":description,"status_idx":status_idx}
    result = wh_setting.post_requests(api=api, data=data)
    return result

def bulk_create(project_idx,episode_idx, sequence_name=[], shot_name=[],description=[], direction_note=[],
                thumbnail =[], length=[], timecode_in=[], timecode_out=[], original_edit_path=[]):
    api = api_list.shot_bulk_create %(project_idx)
    data = {"sequence_name[]":sequence_name,
            "shot_name[]":shot_name,
            "description[]":description,
            "direction_note[]":direction_note,
            "length[]":length,
            "timecode_in[]":timecode_in,
            "timecode_out[]":timecode_out,
            "original_edit_path[]":original_edit_path}
    files ={"attached[]":thumbnail}
    episode_data = {"episode_idx":episode_idx}

    #데이터 유효성 체크

    #리스트의 길이가 다 같은지 체크
    if len(sequence_name) == len(shot_name) == len(description) == len(direction_note):
        data.update(episode_data)

    else:

        #리스트 갑중에 제일 긴 숫자를 구
        max_length = len(max(sequence_name, shot_name , description, direction_note))
        for input_key in data:
            if max_length != len(data[input_key]):
                print(input_key + "의 데이터가 부족 합니다.")
            else:
                pass
        return ""

    result = wh_setting.post_requests(api=api,data=data, files=files)
    return result


def thumbnail_update(project_idx,shot_idx,thumbnail_path):
    api = api_list.shot_thumbnail_up %(project_idx,shot_idx)
    # thumbnail = open(thumbnail_path,'rb')
    data = {"attached":thumbnail_path}
    result = wh_setting.post_requests(api=api, files=data)
    return result


def overview(project_idx,episode_idx=""):
    if episode_idx == "":
        api = api_list.shot_overview_all %(project_idx)
    else :
        api = api_list.shot_overview %(project_idx,episode_idx)
    result = wh_setting.get_requests(api=api)
    return result

def relation(project_idx,episode_idx):
    api = api_list.shot_relation %(project_idx,episode_idx)
    result = wh_setting.get_requests(api=api)
    return result['overview']