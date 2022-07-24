import requests
import json
import base64


url = 'https://cae-bootstore.herokuapp.com'

endpoint_login = "/login"
endpoint_user = "/user"
endpoint_question = "/question"
endpoint_question_all = "/question/all"
endpoint_question_id = "/question/<id>"

def register_user(payload):
    payload_json_string = json.dumps(payload)
    headers = {
        'Content-Type':'application/json'
    }
    response = requests.post(
        url + endpoint_user,
        data = payload_json_string,
        headers = headers
    )
    return response.text

# Basic Authorization
def login_user(user_name, password):
    auth_string = user_name + ":" + password
    
    headers={
        'Authorization' : "Basic "+base64.b64encode(auth_string.encode()).decode()
    }
    user_data = requests.get(
        url + endpoint_login,
        headers=headers
    )
    try:
        return user_data.json()
    except:
        print('Invalid username or password. Try logging in again.')
        


def get_all_questions(token):
    headers={
        'Authorization':'Bearer ' + token
    }   
    all_questions = requests.get(
        url + endpoint_question_all,
        headers = headers
    )
    try:
        all_questions = all_questions.json()['questions']
        return all_questions
    except:
        print(all_questions.text)


def get_my_questions(token):
    headers={
        'Authorization':'Bearer ' + token
    }   
    my_questions = requests.get(
        url + endpoint_question_all,
        headers = headers
    )
    try:
        my_questions = my_questions.json()['questions']
        return my_questions
    except:
        return my_questions.text

def create_question(token, payload):
    payload_json_string = json.dumps(payload)

    headers = {
        'Content-Type':'application/json',
        'Authorization':'Bearer ' + token
    }
    response = requests.post(
        url + endpoint_question,
        data = payload_json_string,
        headers = headers
    )
    return response.text    

def edit_my_question(token, id, payload):
    payload_json_string = json.dumps(payload)
    headers={
        'Content-Type':'application/json',
        'Authorization':'Bearer ' + token
    }
    response = requests.put(
        url + endpoint_question + '/' + id,
        data=payload_json_string,
        headers=headers
    )
    return response.text    

def delete_question(token, id):
    headers = {
        'Authorization':'Bearer ' + token
    } 
    response = requests.delete(
        url + endpoint_question + '/'+ id,
        headers=headers
    )

    return response.text