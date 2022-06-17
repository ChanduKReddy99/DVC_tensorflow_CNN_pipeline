import os
import joblib
import logging
import tensorflow as tf
from src.utils.common_utils import get_timestamp



def create_and_save_tensorboard_callback(callbacks_dir: str, tensorboard_logs_dir: str) -> None:
    """This function creates and saves the tensorboard callback as binary for later use.

    Args:
        callbacks_dir(str): path to the callbacks directory(callback_dir)
        tensorboard_logs_dir(str): path to the tensorboard logs directory(tensorboard_logs_dir)
    """

    unique_name = get_timestamp('tb_logs')
    tb_running_log_dir = os.path.join(tensorboard_logs_dir, unique_name)
    tensorboard_callbacks = tf.keras.callbacks.TensorBoard(log_dir= tb_running_log_dir)

    tb_callback_path = os.path.join(callbacks_dir, 'tensorboard_callback.bin')
    joblib.dump(tensorboard_callbacks, tb_callback_path)

    logging.info(f'tensorboard callbacks are saved at: {tb_callback_path}')


def create_and_save_checkpointing_callback(callbacks_dir: str, checkpoint_dir: str) -> None:
    """This function creates and saves the checkpointing callback as binary.

    Args:
        callbacks_dir(str): path to the callbacks directory(callback_dir)
        checkpoint_dir(str): path to the checkpoint directory(checkpoint_dir)
    """
    checkpoint_file = os.path.join(checkpoint_dir, 'checkpoint_model.h5')
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath= checkpoint_file, save_best_only= True, monitor= 'val_loss'
    )

    checkpoint_callback_file_path = os.path.join(callbacks_dir, 'checkpoint_callback.bin')
    joblib.dump(checkpoint_callback, checkpoint_callback_file_path)

    logging.info(f'checkpointing callbacks are saved at: {checkpoint_callback_file_path} as binary file')
    

def get_callbacks(callbacks_dir_path: str) -> list:
    """This function returns and save the callbacks from the callbacks directory.

    Args:
        callbacks_dir(str): path to the callbacks directory(callback_dir)
    
    Returns:
        list: list of callbacks for training
    """

    callback_paths= [
        os.path.join(callbacks_dir_path, pickle_file) for pickle_file in os.listdir(callbacks_dir_path) if pickle_file.endswith('.bin')
    ]

    callbacks= [joblib.load(path) for path in callback_paths]

    logging.info(f'saved callbacks are loaded and ready to be used now')

    return callbacks