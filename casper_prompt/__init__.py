from prompt_toolkit.contrib.shortcuts import get_input
from prompt_toolkit.contrib.completers import WordCompleter
from nap.url import Url

import warnings
warnings.filterwarnings('ignore')


def server_url():
    server = get_input("JSS server url with port: ")
    if 'https://' not in server:
        server = 'https://' + server
    return server


def normal_time(weird_time):
    """
    Converts strange casper time in min since midnight to hours:min
    """
    hours = str(int(weird_time) // 60)
    min = str(int(weird_time) % 60)
    if min == '0':
        min = '00'
    return hours + ':' + min


def classes(casper_api):
    all_classes_json = casper_api.get('classes').json()
    class_dict = {}
    for casper_class in all_classes_json['classes']:
        class_dict[casper_class['id']] = casper_class['name']
    class_options_mixed = ['List', 'Exit'] + class_dict.keys() + class_dict.values()
    class_options = [str(v) for v in class_options_mixed]
    class_completer = WordCompleter(class_options, ignore_case=True)
    classes_id = casper_api.join('classes/id/')
    classes_name = casper_api.join('classes/name/')
    while True:
        print("List classes with 'List', choose class by id or name, or exscape with 'Exit':")
        choice = get_input("> ",
                           completer=class_completer)
        choice = choice.lower()
        if choice == 'list':
            for k, v in class_dict.items():
                print k, v
        elif choice == 'exit':
            break
        elif choice in [v.lower() for v in class_options]:
            try:
                int(choice)
            except ValueError:
                casper_class = classes_name.get(choice).json()
            else:
                casper_class = classes_id.get(choice).json()

            print 'Class: ' + casper_class['class']['name']

            print 'Faculty: ',
            for teacher in casper_class['class']['teachers']:
                print teacher,
            print ''

            print 'Meeting on: ' + casper_class['class']['meeting_times'][0]['days']
            print 'From ' + normal_time(casper_class['class']['meeting_times'][0]['start_time']),
            print 'To ' + normal_time(casper_class['class']['meeting_times'][0]['end_time'])


            print 'Students:'
            for student in casper_class['class']['students']:
                print '  ', student
        else:
            print 'What did you mean by ' + choice + '?'
            for class_name in class_dict.values():
                if choice in class_name.lower():
                    print '  Did you mean ' + class_name + '?'




if __name__ == '__main__':
    server = server_url()
    api_url = server + '/JSSResource/'
    user = get_input("JSS Username: ")
    password = get_input("JSS Password: ", is_password=True)
    auth = (user, password)
    headers = {'Accept': 'application/json'}
    casper_api = Url(api_url, auth=auth, verify=False, headers=headers)
    #print casper_api.get('classes').json()
    #print api_url
    classes(casper_api)
