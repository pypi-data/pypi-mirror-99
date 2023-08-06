import fire
import torch.nn as nn
from torchvision.models.resnet import (model_urls, resnet18, resnet34, resnet50, resnet101, resnet152, resnext50_32x4d,
                                       resnext101_32x8d, wide_resnet50_2, wide_resnet101_2)

from azureml.designer.core.model.model_spec.builtin_model_meta.task_type import TaskType
from azureml.designer.modules.dl.pytorch.initialize_models.utils import load_pretrained_model_from_url
from azureml.studio.core.io.model_directory import save_pytorch_state_dict_model
from azureml.studio.core.logger import logger
from azureml.studio.internal.error import (ErrorMapping, InvalidModelDirectoryError)
from azureml.studio.internal.error_handler import error_handler
from azureml.designer.modules.dl.pytorch.package_info import PACKAGE_NAME, VERSION

SUPPORTED_NETS = {
    'resnet18': resnet18,
    'resnet34': resnet34,
    'resnet50': resnet50,
    'resnet101': resnet101,
    'resnet152': resnet152,
    'resnext50_32x4d': resnext50_32x4d,
    'resnext101_32x8d': resnext101_32x8d,
    'wide_resnet50_2': wide_resnet50_2,
    'wide_resnet101_2': wide_resnet101_2,
}


class ResNet(nn.Module):
    def __init__(self, model_name=None, **model_settings):
        super().__init__()
        self.model_creator = SUPPORTED_NETS.get(model_name)
        if not self.model_creator:
            ErrorMapping.throw(
                InvalidModelDirectoryError(arg_name=model_name,
                                           reason=f"'{model_name}' is not a supported resnet",
                                           troubleshoot_hint=f'Please select from supported nets {SUPPORTED_NETS}'))

        self.pretrained = model_settings.get('pretrained')
        # 'num_classes' validation will be in training because it is determined by input dataset.
        self.num_classes = model_settings.get('num_classes')
        if self.pretrained:
            # drop 'num_classes' parameter to avoid out-layer size mismatch for pre-trained model creator.
            model_settings.pop('num_classes', None)
            load_pretrained_model_from_url(model_url=model_urls.get(model_name, None))

        logger.info(f'Initializing {model_name} with model setting {model_settings}.')
        self.model = self.model_creator(**model_settings)
        # need to update net in init to avoid extra assignment of model to gpu/cpu.
        self.update_net()

    def update_net(self):
        # to fill the gap between class number of dataset and out-layer size of pre-trained model.
        if self.pretrained and self.num_classes is not None:
            # one way is to add a linear layer.
            self.out_linear_model = nn.Linear(self.model.fc.out_features, self.num_classes)
            logger.info(f'Added a linear layer {self.out_linear_model} to update net.')

    # 'forward' is a overriden method of nn.Module
    def forward(self, x):
        return self.out_linear_model(self.model(x)) if hasattr(self, 'out_linear_model') else self.model(x)


@error_handler
def save_untrained_model(untrained_model_path, model_name='resnext101_32x8d', pretrained=True):
    '''Save 'ResNet' model.
    Actual model initialization is in training where out-layer size is given as 'num_classes' of input dataset.

    :param untrained_model_path: untrained model path
    :param model_name: resnet init function name
    :param pretrained: whether to use a model pre-trained on ImageNet
    :return:
    '''
    # For model sdk limitation, have to import absolute path of model class if model class and entry are
    # in the same script, otherwise, '__main__' will be saved as 'module' in model spec.
    from azureml.designer.modules.dl.pytorch.initialize_models.vision.classification.resnet import ResNet

    # Add package version log
    logger.info(f'{PACKAGE_NAME} {VERSION}')

    model_config = {
        'model_name': model_name,
        'pretrained': pretrained,
    }
    logger.info(f'Constructed model config: {model_config}.')
    save_pytorch_state_dict_model(
        save_to=untrained_model_path,
        pytorch_model=ResNet(**model_config),
        init_params=model_config,
        task_type=TaskType.MultiClassification,
    )


if __name__ == '__main__':
    fire.Fire(save_untrained_model)
