import os
import argparse
import logging
from src.utils.common_utils import read_config_yaml, create_dirs
from src.utils.model import get_VGG16_model, prepare_full_model



logging.basicConfig(
    filename= os.path.join('logs', 'running_logs.log'),
    level= logging.INFO,
    format= '[%(asctime)s: %(levelname)s: %(module)s]: %(message)s',
    datefmt= '%Y-%m-%d %H:%M:%S',
    filemode= 'a'
)


def prepare_base_model(config_path:str, params_path:str) -> None:
    """This function prepares and saves he untrained model. 

    Args:
        config_path: path to the config.yaml file
        params_path: path to the params.yaml file
    """
    config= read_config_yaml(config_path)
    params= read_config_yaml(params_path)

    artifacts = config['artifacts']
    artifacts_dir= artifacts['ARTIFACTS_DIR']

    base_model_dir= artifacts['BASE_MODEL_DIR']
    base_model_name= artifacts['BASE_MODEL_NAME']

    base_model_dir_path= os.path.join(artifacts_dir, base_model_dir)
   
    create_dirs([base_model_dir_path])

    base_model_path= os.path.join(base_model_dir_path, base_model_name)

    base_model= get_VGG16_model(
        input_shape= params['IMAGE_SIZE'],
        model_path= base_model_path
    )

    full_model= prepare_full_model(
        base_model= base_model,
        learning_rate= params['LEARNING_RATE'],
        CLASSES= 2,
        freeze_all = True,
        freeze_till = None
    )

    updated_full_model_path = os.path.join(base_model_dir_path, artifacts['UPDATED_BASE_MODEL_NAME'])
    full_model.save(updated_full_model_path)
    logging.info(f'full untrained model is saved to {updated_full_model_path}')



if __name__ == '__main__':
    parser= argparse.ArgumentParser(description= 'Stage 02: preparing base model')
    parser.add_argument('--config', '-c', default= 'configs/config.yaml', help='Path to config file')
    parser.add_argument('--params', '-p', default= 'params.yaml', help='Path to params file')
    parsed_args= parser.parse_args()

    try:
        logging.info('\n**************************')
        logging.info('>>>>>> Stage 02: preparing base model started <<<<<<')
        prepare_base_model(parsed_args.config, parsed_args.params)
        logging.info('>>>>>> Stage 02: preparing base model is completed <<<<<<\n')

    except Exception as e:
        logging.error(e)
        logging.error('\nStage 02: preparing base model failed....')


