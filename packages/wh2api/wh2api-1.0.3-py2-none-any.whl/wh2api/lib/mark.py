# -*- coding: utf-8 -*-

from . import wh_setting, api_list
# | 1. [마크 등록]              | /api/mark/create               |   POST    |   X\*   |  X   |
# | 2. [마크 수정]              | /api/mark/{mark_idx}/update    |   POST    |   X\*   |  X   |
# | 3. [마크 조회]              | /api/mark/{mark_idx}/read      |    GET    |   X\*   |  X   |
# | 4. [마크 삭제]              | /api/mark/{mark_idx}/delete    |   POST    |   X\*   |  X   |
# | 5. [마크 내 마크 추가]      | /api/mark/{mark_idx}/mark/add  |   POST    |   X\*   |  X   |
# | 6. [마크 내 마크 목록 조회] | /api/mark/{mark_idx}/mark/list |    GET    |   X\*   |  X   |

def create(file_path, description="", kind="shot or asset", task_idx="", status_idx="", thumbnail_path=""):
    api = api_list.mark_create

    if kind =="":
        data = {"description": description, "status_idx":status_idx,"file_path":file_path}
    else:
        if task_idx =="":
            print("Task_idx값 비어 있습니다.")
            return ""
        else:
            data = {"description":description,"kind":kind,"task_idx":task_idx,"status_idx":status_idx,"file_path":file_path}

    if thumbnail_path =="":
        result = wh_setting.post_requests(api=api, data=data)

    else:
        file = {"attached":thumbnail_path}
        result = wh_setting.post_requests(api =api,data =data,files=file)
    return result

def update(mark_idx,file_path, description="", kind="shot or asset", task_idx="", status_idx="", thumbnail_path=""):
    api = api_list.mark_update %(mark_idx)

    if kind =="":
        data = {"description": description, "status_idx":status_idx,"file_path":file_path}
    else:
        if task_idx =="":
            print("Task_idx값 비어 있습니다.")
            return ""
        else:
            data = {"description":description,"kind":kind,"task_idx":task_idx,"status_idx":status_idx,"file_path":file_path}

#파일 여부 있는지 확인.
    if thumbnail_path == "":
        result = wh_setting.post_requests(api=api, data=data)

    else:
        file = {"attached": thumbnail_path}
        result = wh_setting.post_requests(api=api, data=data, files=file)
    return result

def read(mark_idx):
    api = api_list.mark_read %(mark_idx)
    result = wh_setting.get_requests(api=api)
    return result

def delete(mark_idx):
    api = api_list.mark_delete % (mark_idx)
    result = wh_setting.post_requests(api=api)
    return result

def in_add(mark_idx,child_mark_idx=[],child_file_path=[]):
    api = api_list.mark_in_add %(mark_idx)

    data = {"child_mark_idx[]":child_mark_idx,"child_file_path[]":child_file_path}

    result = wh_setting.post_requests(api =api,data =data)
    return result

def in_list(mark_idx):
    api = api_list.mark_in_list % (mark_idx)
    result = wh_setting.get_requests(api=api)
    return result