from functools import total_ordering
import os
import yaml
import logging
import shutil
from tqdm import tqdm
import time



def read_config_yaml(file_path: str) -> dict:
    """This function reads the config file and returns the data in a dictionary.
    
    args:
        config_path: path to the config yaml file

    returns:
        config: dictionary containing the data from the config file
        """
    with open(file_path) as yaml_file:
        content = yaml.safe_load(yaml_file)
        logging.info('Config file successfully read.')
        return content

def create_dirs(dir_paths: list) -> None:
    """This function creates the directories if they do not exist.
    
    args:
        dir_paths: list of paths to the directories to be created
    """
    for dir_path in dir_paths:
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f'{dir_path} created successfully...')

def copy_data(source_data_dir:str, local_data_dir:str) -> None:
    """This function copies the data from the source to the destination directory.
    args:
        source_data_dir: path to the source data directory
        local_data_dir: path to the destination data directory
    """
    lift_of_files= os.listdir(source_data_dir)
    N= len(lift_of_files)
    for file_name in tqdm(lift_of_files, 
                           total=N, 
                           desc= f'copying data from {source_data_dir} to {local_data_dir} ...', 
                           colour='green'):
                           source= os.path.join(source_data_dir, file_name)
                           dest= os.path.join(local_data_dir, file_name)
                           shutil.copy(source, dest)
    logging.info(f'all the files have been copied from {source_data_dir} to {local_data_dir} successfully...')


def get_timestamp(name:str) -> str:
    """This function returns the unique name with timestamp.
    args:
        name(str): name of the file/directory
    returns:
        str: unique name with timestamp
    """
    timestamp= time.asctime().replace(' ', '_').replace(':', '.')
    unique_name= f'{name}_at_{timestamp}'
    return unique_name


    


