import io
import logging
from tensorboard import summary
import tensorflow as tf
# from src.utils.common_utils import get_timestamp


def _get_model_summary(model):
    with io.StringIO() as stream:
        model.summary(
            print_fn= lambda x: stream.write(f'{x}\n')
        )
        summary_str = stream.getvalue()
    return summary_str


def get_VGG16_model(input_shape: list, model_path:str) -> tf.keras.models.Model:
    """This function does that return and save the base model extraced from the VGG16 model.
    Args:
        input_shape(list): shape of the input image
        model_path(str): path to save the base model

    Returns:
        model(tf.keras.Model): base model
    """
    model = tf.keras.applications.vgg16.VGG16(
        input_shape= input_shape,
        weights= 'imagenet',
        include_top= False 
    )

    logging.info(f'VGG16 base model summary: \n{_get_model_summary(model)}')
    model.save(model_path)
    logging.info(f'VGG16 base model is saved to {model_path}')
    return model


def prepare_full_model(base_model, learning_rate, CLASSES= 2, 
               freeze_all= False, freeze_till= None) -> tf.keras.models.Model:
    """This function prepares the complete transfer learning model artchitecture.

    Args:
        base_model(tf.keras.Model): base VGG16 model
        learning_rate(float): learning rate for training
        CLASSES(int): number of classes to train. Default is 2
        freeze_all(bool, optional): if True, all layers are frozen i,e untrainable. Default is False
        freeze_till(int, optional): this is the values of the layer index to be frozen. Default is None
            
    Returns:
         model(tf.keras.Model): complete model architecture is ready to be used/trained
    """
    if freeze_all:
        for layer in base_model.layers:
            layer.trainable = False
    elif (freeze_till is not None) and (freeze_till > 0):
        for layer in base_model.layers[:-freeze_till]:
            layer.trainable = False
    
    ##add our layers to the base model

    flatten_in= tf.keras.layers.Flatten()(base_model.output)

    prediction = tf.keras.layers.Dense(
        units = CLASSES,
        activation = 'softmax',
    )(flatten_in)

    full_model = tf.keras.models.Model(
        inputs = base_model.input,
        outputs = prediction
    )

    full_model.compile(
        optimizer= tf.keras.optimizers.Adam(learning_rate= learning_rate),
        loss= tf.keras.losses.CategoricalCrossentropy(),
        metrics= ['accuracy']
    )

    logging.info('custom model is compiled and ready to be trained')
    logging.info(f'Full model summary: \n{_get_model_summary(full_model)}')
    return full_model

