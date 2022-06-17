import os
import argparse
import logging
from src.utils.common_utils import read_config_yaml, create_dirs
from src.utils.callback_utils import create_and_save_tensorboard_callback, create_and_save_checkpointing_callback


logging.basicConfig(
    filename= os.path.join('logs', 'running_logs.log'),
    level= logging.INFO,
    format= '[%(asctime)s: %(levelname)s: %(module)s]: %(message)s',
    datefmt= '%Y-%m-%d %H:%M:%S',
    filemode= 'a'
)

def prepare_callbacks(config_path: str) -> None:
    """This function prepares the callbacks as binary.

    Args:
        config_path: path to the config yaml file
    """
    config= read_config_yaml(config_path)

    artifacts = config['artifacts']
    artifacts_dir= artifacts['ARTIFACTS_DIR']

    tensorboard_logs_dir= os.path.join(artifacts_dir, artifacts['TENSORBOARD_ROOT_LOG_DIR'])

    checkpoint_dir= os.path.join(artifacts_dir, artifacts['CHECKPOINT_DIR'])

    callbacks_dir= os.path.join(artifacts_dir, artifacts['CALLBACKS_DIR'])

    create_dirs([tensorboard_logs_dir, checkpoint_dir, callbacks_dir])

    create_and_save_tensorboard_callback(callbacks_dir, tensorboard_logs_dir)

    create_and_save_checkpointing_callback(callbacks_dir, checkpoint_dir)



if __name__ == '__main__':
    parser= argparse.ArgumentParser(description= 'This script prepares the callbacks as binary.')
    parser.add_argument('--config_path', '-c',default= 'configs/config.yaml', help= 'path to the config yaml file')
    parsed_args= parser.parse_args()

    try:
        logging.info('\n***************************')
        logging.info('>>>>>>>  stage03_prepare_callbacks started ...')
        prepare_callbacks(parsed_args.config_path)
        logging.info('>>>>>>>  stage03_prepare_callbacks finished successfully...<<<<<<')

    except Exception as e:
        logging.error(e)
        logging.error('>>>>>>>  stage03_prepare_callbacks failed...<<<<<<')
        



    