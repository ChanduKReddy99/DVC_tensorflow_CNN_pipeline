from tqdm import tqdm
import os
import argparse
import logging
from src.utils.common_utils import read_config_yaml, copy_data,create_dirs


logging.basicConfig(
    filename= os.path.join('logs', 'running_logs.log'),
    level= logging.INFO,
    format= '[%(asctime)s: %(levelname)s: %(module)s]:  %(message)s',
    datefmt= '%Y-%m-%d %H:%M:%S',
    filemode='a'
)

def get_data(config_path:str) -> None:
    """This function gets the data from the source by reading config.yaml file and saves it to the data folder.

    Args:
        config_path: path to the config.yaml file
    """
    config= read_config_yaml(config_path)

    source_data_dirs = config['source_data_download_path']
    local_data_dirs = config['local_data_path']

    N= len(source_data_dirs)
    for source_data_dir, local_data_dir in tqdm(zip(source_data_dirs, local_data_dirs),
            total = N,
            desc = 'copying directory:',
            colour= 'green'):
            
            create_dirs([local_data_dir])
            
            copy_data(source_data_dir, local_data_dir)


                    
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stage 01: Get data')
    parser.add_argument('--config', '-c', default= 'configs/config.yaml', help='Path to config file')
    parsed_args= parser.parse_args()

    try:
        logging.info("\n**************************")
        logging.info(">>>>>> Stage 01: get_data started.. <<<<<<<<")
        get_data(parsed_args.config)
        logging.info(">>>>>> Stage 01: get_data is completed <<<<<<<<\n")

    except Exception as e:
        logging.error(e)
        logging.error("\nStage 01: get_data failed....")


