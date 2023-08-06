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


def init_client_config(client_id=None):
    import os
    import uuid
    import configparser
    from .. import CONFIG_FILE

    cfg = configparser.ConfigParser()

    if os.path.isfile(CONFIG_FILE):
        cfg.read(CONFIG_FILE)
        return cfg

    # Create client ID
    client_id = 'client_' + str(uuid.uuid4())

    cfg['default'] = {
        'client_id': client_id,
        'uploads_url': 'https://epione-demo.inria.fr/fedbiomed/upload/',
    }

    cfg['mqtt'] = {
        'broker_url': 'epione-demo.inria.fr',
        'port': 80,
        'keep_alive': 60
    }

    with open(CONFIG_FILE, 'w') as f:
        cfg.write(f)

    return cfg


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


def pick_with_tkinter(mode='file'):
    try:
        from tkinter import filedialog
        # root = TK()
        # root.withdraw()
        # root.attributes("-topmost", True)
        if mode == 'file':
            return filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        else:
            return filedialog.askdirectory()

    except ModuleNotFoundError:
        if mode == 'file':
            return input('Insert the path of the CSV file: ')
        else:
            return input('Insert the path of the dataset folder: ')


def validated_path_input(data_type):
    from os.path import isdir, isfile
    while True:
        try:
            if data_type == 'csv':
                path = pick_with_tkinter(mode='file')
                print(path)
                if not path:
                    print('No file was selected. Exiting...')
                    exit(1)
                assert isfile(path)
            else:
                path = pick_with_tkinter(mode='dir')
                print(path)
                if not path:
                    print('No directory was selected. Exiting...')
                    exit(1)
                assert isdir(path)
            break
        except Exception:
            error_msg = '[ERROR] Invalid path. Please enter a valid path.'
            try:
                from tkinter import messagebox
                messagebox.showerror(title='Error', message=error_msg)
            except ModuleNotFoundError:
                warnings.warn(error_msg)

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

    # Add database

    try:
        add_database(name=name, tags=tags, data_type=data_type,
                     description=description,
                     path=path)
    except AssertionError as e:
        try:
            from tkinter import messagebox
            messagebox.showwarning(title='Warning', message=str(e))
        except ModuleNotFoundError:
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


def delete_database():
    from .. import data_manager
    my_data = data_manager.list_my_data(verbose=False)
    options = [d['name'] for d in my_data]

    msg = "Select the dataset to delete:\n"
    msg += "\n".join([f'{i}) {d}' for i, d in enumerate(options, 1)])
    msg += "\nSelect: "
    while True:
        try:
            opt_idx = int(input(msg)) - 1
            assert opt_idx >= 0

            tags = my_data[opt_idx]['tags']
            data_manager.remove_database(tags)
            print('Dataset removed. Here your available datasets')
            data_manager.list_my_data()
            return
        except (ValueError, IndexError, AssertionError):
            print('Invalid option. Please, try again.')


def launch_cli():
    import argparse
    from argparse import RawTextHelpFormatter

    parser = argparse.ArgumentParser(description=f'{__intro__}:A CLI app for fedbiomed researchers.',
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument('-a', '--add', help='Add and configure local dataset', action='store_true')
    parser.add_argument('-d', '--delete', help='Delete existing local dataset', action='store_true')
    parser.add_argument('-l', '--list', help='List my shared_data', action='store_true')
    parser.add_argument('-s', '--start-node', help='Start fedbiomed node.', action='store_true')
    args = parser.parse_args()

    if not any(args.__dict__.values()):
        parser.print_help()
    else:
        from .. import CLIENT_ID
        print(__intro__)
        print('\t- 🆔 Your client ID:', CLIENT_ID, '\n')

    if args.add:
        add_database()
    elif args.list:
        print('Listing your data available...')
        from ..data_manager import list_my_data
        data = list_my_data(verbose=True)
        if len(data) == 0:
            print('No data has been set up.')
    elif args.delete:
        delete_database()
    elif args.start_node:
        launch_node()


def main():
    try:
        launch_cli()
    except KeyboardInterrupt:
        print('Operation cancelled by user.')
