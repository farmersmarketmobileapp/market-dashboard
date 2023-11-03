import pandas as pd
import json


def prepare_map_data():

    global df
    with open('./data/user.json', encoding='UTF8') as f:
        #enerates list o dictionaries
        data = json.loads(f.read())
        #print(data)

    df = pd.DataFrame()

    userName_list = list()
    email_list = list()
    specialization_list = list()
    latitude_list = list()
    longitude_list = list()

    for e in data:
        print(e)
        #print(e['usersName'])
        try:
            userName_list.append(e['usersName'])
        except KeyError:
            userName_list.append("KeyError")

        email_list.append(e['username'])

        try:
            specialization_list.append(e['userFarmSpecialization'])
        except KeyError:
            specialization_list.append("KeyError")
            print("Hier kommt ein key error für " + e['username'])
        try:
            latitude_list.append(e["userFarmLocation"][1])
            longitude_list.append(e["userFarmLocation"][0])
        except KeyError:
            latitude_list.append(-1)
            longitude_list.append(-1)
            print("Hier kommt ein key error für " + e['username'])

    #define dataframe columns
    df['userName'] = userName_list
    df['email'] = email_list
    df['specialization'] = specialization_list
    df['lat'] = latitude_list
    df['lng'] = longitude_list

    df.to_feather(path='./data/user.feather')
    df.to_csv('./data/user.csv')

    return df


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    prepare_map_data()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
