# global
import json

# local
from ivy_builder.specs import DataLoaderSpec
from ivy_builder.specs import DatasetDirs
from ivy_builder.specs.dataset_spec import DatasetSpec
from ivy_builder.specs import NetworkSpec
from ivy_builder.specs.trainer_spec import TrainerSpec

__properties_to_ignore = ['activity_regularizer', 'dtype', 'dynamic', 'inbound_nodes', 'input', 'input_mask',
                          'input_shape', 'input_spec', 'layers', 'losses', 'metrics', 'metrics_names', 'name',
                          'name_scope', 'non_trainable_variables', 'non_trainable_weights', 'outbound_nodes',
                          'output', 'output_mask', 'output_shape', 'run_eagerly', 'sample_weights', 'state_updates',
                          'stateful', 'submodules', 'trainable', 'trainable_variables', 'trainable_weights',
                          'updates', 'variables', 'weights', 'experimental_between_graph',
                          'experimental_require_static_shapes', 'experimental_should_init', 'parameter_devices',
                          'should_checkpoint', 'should_save_summary', 'worker_devices', 'graph', 'ndim', 'op',
                          'shape', 'value_index', 'aggregation', 'constraint', 'create', 'device', 'handle',
                          'initial_value', 'initializer', 'synchronization']


def parse_json_to_dict(json_filepath):
    """
    return the data from json file in the form of a python dict
    """
    with open(json_filepath) as json_data_file:
        return json.load(json_data_file)


def save_dict_as_json(dict_to_save, json_filepath):
    """
    save the python dict as a json file at specified filepath
    """
    with open(json_filepath, 'w+') as json_data_file:
        json.dump(dict_to_save, json_data_file, indent=4)


def spec_to_dict(obj, spec_dict=None):
    def __is_jsonable(x):
        try:
            json.dumps(x)
            return True
        except (TypeError, OverflowError):
            return False

    if spec_dict is None:
        spec_dict = dict()
    property_keys = [key for key in dir(type(obj)) if key != '__abstractmethods__' and
                     isinstance(getattr(type(obj), key), property) and
                     key not in __properties_to_ignore and key[0] != '_']
    if not property_keys:
        return spec_dict
    property_values = [getattr(obj, key) for key in property_keys]
    property_dict = dict(zip(property_keys, property_values))
    serializable_property_values = [value if __is_jsonable(value) else str(value) for value in property_values]
    serializable_property_dict = dict(zip(property_keys, serializable_property_values))
    spec_dict[str(type(obj)).split('.')[-1].split("'")[0]] = serializable_property_dict
    for value in property_dict.values():
        spec_dict = spec_to_dict(value, spec_dict)
    return spec_dict


def build_dataset_dirs(dataset_dirs_args=None,
                       dataset_dirs_class=DatasetDirs):
    """
    build dataset directories specification
    """

    # define dataset directories specification arguments
    if dataset_dirs_args is None:
        dataset_dirs_args = dict()

    # return dataset directories specification
    # noinspection PyArgumentList
    return dataset_dirs_class(**dataset_dirs_args)


def build_dataset_spec(dataset_dirs_args=None,
                       dataset_dirs_class=DatasetDirs,
                       dataset_spec_args=None,
                       dataset_spec_class=DatasetSpec):
    """
    build dataset specification
    """

    # build dataset directories
    dataset_dirs = build_dataset_dirs(dataset_dirs_args,
                                      dataset_dirs_class)

    # define dataset specification arguments
    if dataset_spec_args is None:
        dataset_spec_args = dict()
    dataset_spec_args = {**dataset_spec_args, **{'dirs': dataset_dirs}}

    # return dataset specification
    return dataset_spec_class(**dataset_spec_args)


def build_network_specification(network_spec_args=None,
                                network_spec_class=NetworkSpec):
    """
    build network specification
    """

    # define network specification arguments
    if network_spec_args is None:
        network_spec_args = dict()
    network_spec_args = {**network_spec_args}

    # return network
    # noinspection PyArgumentList
    return network_spec_class(**network_spec_args)


def build_network(network_class,
                  network_spec_args=None,
                  network_spec_class=NetworkSpec):
    """
    build network
    """

    # build network specification
    network_spec = build_network_specification(network_spec_args,
                                               network_spec_class)

    # network
    return network_class(network_spec)


def build_data_loader_spec(network_class,
                           dataset_dirs_args=None,
                           dataset_dirs_class=DatasetDirs,
                           dataset_spec_args=None,
                           dataset_spec_class=DatasetSpec,
                           data_loader_spec_args=None,
                           data_loader_spec_class=DataLoaderSpec,
                           network_spec_args=None,
                           network_spec_class=NetworkSpec):
    """
    build data loader specification
    """

    # build dataset specification
    dataset_spec = build_dataset_spec(dataset_dirs_args,
                                      dataset_dirs_class,
                                      dataset_spec_args,
                                      dataset_spec_class)

    # build network
    network = build_network(network_class,
                            network_spec_args,
                            network_spec_class)

    # define data loader specification arguments
    if data_loader_spec_args is None:
        data_loader_spec_args = dict()
    data_loader_spec_args = {**data_loader_spec_args, **{'dataset_spec': dataset_spec, 'network': network}}

    # return data loader
    return data_loader_spec_class(**data_loader_spec_args)


def build_data_loader(data_loader_class,
                      network_class,
                      dataset_dirs_args=None,
                      dataset_dirs_class=DatasetDirs,
                      dataset_spec_args=None,
                      dataset_spec_class=DatasetSpec,
                      data_loader_spec_args=None,
                      data_loader_spec_class=DataLoaderSpec,
                      network_spec_args=None,
                      network_spec_class=NetworkSpec):
    """
    build data loader
    """

    # build data loader specification
    data_loader_spec = build_data_loader_spec(network_class,
                                              dataset_dirs_args,
                                              dataset_dirs_class,
                                              dataset_spec_args,
                                              dataset_spec_class,
                                              data_loader_spec_args,
                                              data_loader_spec_class,
                                              network_spec_args,
                                              network_spec_class)

    # return data loader
    return data_loader_class(data_loader_spec)


def build_trainer_spec(data_loader_class,
                       network_class,
                       dataset_dirs_args=None,
                       dataset_dirs_class=DatasetDirs,
                       dataset_spec_args=None,
                       dataset_spec_class=DatasetSpec,
                       data_loader_spec_args=None,
                       data_loader_spec_class=DataLoaderSpec,
                       network_spec_args=None,
                       network_spec_class=NetworkSpec,
                       trainer_spec_args=None,
                       trainer_spec_class=TrainerSpec):
    """
    build trainer specification
    """

    # build data loader
    data_loader = build_data_loader(data_loader_class,
                                    network_class,
                                    dataset_dirs_args,
                                    dataset_dirs_class,
                                    dataset_spec_args,
                                    dataset_spec_class,
                                    data_loader_spec_args,
                                    data_loader_spec_class,
                                    network_spec_args,
                                    network_spec_class)

    # define trainer specification arguments
    if trainer_spec_args is None:
        trainer_spec_args = dict()
    trainer_spec_args = {**trainer_spec_args, **{'data_loader': data_loader,
                                                 'network': data_loader.spec.network}}

    # return trainer specification
    return trainer_spec_class(**trainer_spec_args)


def build_tune_trainer(data_loader_class,
                       network_class,
                       trainer_class,
                       tune_trainer_class,
                       dataset_dirs_args=None,
                       dataset_dirs_class=DatasetDirs,
                       dataset_spec_args=None,
                       dataset_spec_class=DatasetSpec,
                       data_loader_spec_args=None,
                       data_loader_spec_class=DataLoaderSpec,
                       network_spec_args=None,
                       network_spec_class=NetworkSpec,
                       trainer_spec_args=None,
                       trainer_spec_class=TrainerSpec):
    """
    build trainer
    """
    return tune_trainer_class(data_loader_class,
                              network_class,
                              trainer_class,
                              dataset_dirs_args,
                              dataset_dirs_class,
                              dataset_spec_args,
                              dataset_spec_class,
                              data_loader_spec_args,
                              data_loader_spec_class,
                              network_spec_args,
                              network_spec_class,
                              trainer_spec_args,
                              trainer_spec_class)


def build_trainer(data_loader_class,
                  network_class,
                  trainer_class,
                  dataset_dirs_args=None,
                  dataset_dirs_class=DatasetDirs,
                  dataset_spec_args=None,
                  dataset_spec_class=DatasetSpec,
                  data_loader_spec_args=None,
                  data_loader_spec_class=DataLoaderSpec,
                  network_spec_args=None,
                  network_spec_class=NetworkSpec,
                  trainer_spec_args=None,
                  trainer_spec_class=TrainerSpec):
    """
    build trainer
    """

    # build trainer spec
    trainer_spec = build_trainer_spec(data_loader_class,
                                      network_class,
                                      dataset_dirs_args,
                                      dataset_dirs_class,
                                      dataset_spec_args,
                                      dataset_spec_class,
                                      data_loader_spec_args,
                                      data_loader_spec_class,
                                      network_spec_args,
                                      network_spec_class,
                                      trainer_spec_args,
                                      trainer_spec_class)

    # return trainer
    return trainer_class(trainer_spec)
