__intro__ = """

   __         _ _     _                          _        _ _            _   
  / _|       | | |   (_)                        | |      | (_)          | |  
 | |_ ___  __| | |__  _  ___  _ __ ___   ___  __| |   ___| |_  ___ _ __ | |_ 
 |  _/ _ \/ _` | '_ \| |/ _ \| '_ ` _ \ / _ \/ _` |  / __| | |/ _ \ '_ \| __|
 | ||  __/ (_| | |_) | | (_) | | | | | |  __/ (_| | | (__| | |  __/ | | | |_ 
 |_| \___|\__,_|_.__/|_|\___/|_| |_| |_|\___|\__,_|  \___|_|_|\___|_| |_|\__|
"""

import warnings
import readline

readline.parse_and_bind("tab: complete")


def validated_data_type_input():
    valid_options = ['csv', 'default', 'images']
    valid_options = {i: val for i, val in enumerate(valid_options, 1)}

    msg = "Please select the data type that you're configuring:\n"
    msg += "\n".join([f"\t{i}) {val}" for i, val in valid_options.items()])
    msg += "\nselect: "

    while True:
        try:
            t = int(input(msg))
            assert t in valid_options.keys()
            break
        except Exception:
            warnings.warn('\n[ERROR] Please, enter a valid option')

    return valid_options[t]


def validated_path_input(data_type):
    from os.path import isdir, isfile
    while True:
        try:
            if data_type == 'csv':
                path = input('Insert the path of the CSV file: ')
                assert isfile(path)
            else:
                path = input('Insert the path of the dataset folder: ')
                assert isdir(path)
            break
        except Exception:
            warnings.warn('\n[ERROR] Invalid path. Please enter a valid path.')

    return path


def add_database():
    from ..data_manager import add_database, list_my_data

    print('Welcome to the Fedbiomed CLI data manager')
    data_type = validated_data_type_input()
    if data_type == 'default':
        tags = ['#MNIST', "#dataset"]
        while input(f'MNIST will be added with tags {tags} [y/N]').lower() != 'y':
            pass
        path = validated_path_input(data_type)
        name = 'MNIST'
        description = 'MNIST database'

    else:
        name = input('Name of the database: ')

        tags = input('Tags (separate them by comma and no spaces): ')
        tags = tags.replace(' ', '').split(',')

        description = input('Description: ')
        path = validated_path_input(data_type)

    try:
        add_database(name=name, tags=tags, data_type=data_type,
                     description=description,
                     path=path)
    except AssertionError as e:
        warnings.warn(f'[ERROR]: {e}')
        exit()

    print('\nGreat! Take a look at your data:')
    list_my_data(verbose=True)


def launch_node():
    from fedbiomed_cli.mqtt import start_mqtt_service
    from fedbiomed_cli.tasks import manage_tasks

    print('Launching node...')
    print('\t - Starting task manager... ', end='\t')
    manage_tasks()
    print('✅')

    print('\t - Starting communication channel with network... \t ✅')
    try:
        print('To stop press Ctrl + C.')
        start_mqtt_service(block=True)
    except KeyboardInterrupt:
        print('Exited.')
        exit()


def main():
    import argparse
    from argparse import RawTextHelpFormatter

    parser = argparse.ArgumentParser(description=f'{__intro__}:A CLI app for fedbiomed researchers.',
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument('-a', '--add', help='Add and configure local dataset', action='store_true')
    parser.add_argument('-l', '--list', help='List my shared_data', action='store_true')
    parser.add_argument('-s', '--start-node', help='Start fedbiomed node.', action='store_true')
    args = parser.parse_args()

    if not any(args.__dict__.values()):
        parser.print_help()
    else:
        print(__intro__)

    if args.add:
        add_database()
    elif args.list:
        print('Listing your data available...')
        from ..data_manager import list_my_data
        data = list_my_data(verbose=True)
        if len(data) == 0:
            print('No data has been set up.')
    elif args.start_node:
        launch_node()
