#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json


RED = "\033[31m"
CYAN = "\033[96m"
BOLD = "\033[1m"
CEND = "\033[0m"


# 1. Conectarse al enlace
def connect_to_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response


# 2. Obtener el número de respuestas contestadas y no contestadas
def get_num_answered(data):
    answers_answered_json = list(
                       filter(lambda x: x["is_answered"], data["items"]))
    return len(answers_answered_json)


def get_num_unanswered(data):
    not_answers_answered_json = list(
                       filter(lambda x: (not x["is_answered"]), data["items"]))
    return(len(not_answers_answered_json))


# 3. Obtener la respuesta con menor número de vistas
def get_fewer_views_answer(data):
    items = data["items"]
    index_list = list(range(0, len(items)-1))
    sorted_indices = sorted(
                       index_list, key=lambda x: (items[x]["view_count"]))
    min_views = items[sorted_indices[0]]["view_count"]
    fewer_views_answers = []
    for index in sorted_indices:
        if items[index]["view_count"] == min_views:
            fewer_views_answers.append(items[index])
        else:
            break
        return fewer_views_answers


# 4. Obtener la respuesta más vieja y más actual
def get_older_answer(data):
    items = data["items"]
    index_list = list(range(0, len(items)-1))
    sorted_indices = sorted(
                       index_list, key=lambda x: (items[x]["creation_date"]))
    older_creation_date = items[sorted_indices[0]
                                ]["creation_date"]
    older_answers = []
    for index in sorted_indices:
        if items[index]["creation_date"] == older_creation_date:
            older_answers.append(items[index])
        else:
            break
        return older_answers


def get_newer_answer(data):
    items = data["items"]
    index_list = list(range(0, len(items)-1))
    sorted_indices = sorted(
                       index_list, key=lambda x: (items[x]["creation_date"]), reverse=True)
    newer_creation_date = items[sorted_indices[0]
                                ]["creation_date"]
    newer_answers = []
    for index in sorted_indices:
        if items[index]["creation_date"] == newer_creation_date:
            newer_answers.append(items[index])
        else:
            break
        return newer_answers


# 5. Obtener la respuesta del owner que tenga una mayor reputación
def get_higher_reputation_owner(data):
    items = data["items"]
    index_list = list(range(0, len(items)-1))
    # NOTA: The JSON was modified?---------------------------------------------!
    #higher_reputation_owner_index = max(
    #                   index_list, key=lambda x: (items[x]["owner"]["reputation"]))

    reputaion_list = []
    for i in items:
        if "reputation" in i["owner"]:
            reputaion_list.append(i["owner"]["reputation"])
    higher_reputation_owner_index = max(
                       index_list, key=lambda x: (reputaion_list[x]))
    return items[higher_reputation_owner_index]


# Run and print all the functions from the first part of the challenge
def run():
    print(BOLD + RED + "-- PROGRAMACIÓN --" + CEND)
    url = "https://api.stackexchange.com/2.2/search?order=desc&sort=activity&intitle=perl&site=stackoverflow"
    response = connect_to_json(url)

    if response:
        response_json = response.json()
        print(CYAN
              + "\n\n2. Obtener el número de respuestas contestadas y no contestadas"
              + CEND)
        print("    Number of answered:",
              get_num_answered(response_json))
        print("    Number of unanswered:", get_num_unanswered(response_json))

        print(CYAN + "\n\n3. Obtener la respuesta con menor número de vistas"
              + CEND)
        print(BOLD + "  Answer(s) with fewer views:" + CEND)
        ans = get_fewer_views_answer(response_json)
        print(json.dumps(ans, indent=4))

        print(CYAN + "\n\n4. Obtener la respuesta más vieja y más actual"
              + CEND)
        print(BOLD + "  Older answer(s):" + CEND)
        ans = get_older_answer(response_json)
        print(json.dumps(ans, indent=4))
        print(BOLD + "\n  Newer answer(s):" + CEND)
        ans = get_newer_answer(response_json)
        print(json.dumps(ans, indent=4))

        print(CYAN
              + "\n\n5. Obtener la respuesta del owner que tenga una mayor reputación"
              + CEND)
        print(BOLD + "  Higher reputation owner:" + CEND)
        ans = get_higher_reputation_owner(response_json)
        print(json.dumps(ans, indent=4))
