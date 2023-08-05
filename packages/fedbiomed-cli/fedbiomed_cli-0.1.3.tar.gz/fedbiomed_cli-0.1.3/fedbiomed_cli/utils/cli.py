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
