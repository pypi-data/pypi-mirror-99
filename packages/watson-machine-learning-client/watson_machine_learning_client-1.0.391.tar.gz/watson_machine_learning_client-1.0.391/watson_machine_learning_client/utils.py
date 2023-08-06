################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from __future__ import print_function
from watson_machine_learning_client.wml_client_error import WMLClientError
import re
import os
import sys
import pkg_resources
import shutil
import tarfile
from watson_machine_learning_client.log_util import get_logger


INSTANCE_DETAILS_TYPE = u'instance_details_type'
DEPLOYMENT_DETAILS_TYPE = u'deployment_details_type'
EXPERIMENT_RUN_DETAILS_TYPE = u'experiment_run_details_type'
MODEL_DETAILS_TYPE = u'model_details_type'
DEFINITION_DETAILS_TYPE = u'definition_details_type'
EXPERIMENT_DETAILS_TYPE = u'experiment_details_type'
TRAINING_RUN_DETAILS_TYPE = u'training_run_details_type'
FUNCTION_DETAILS_TYPE = u'function_details_type'
RUNTIME_SPEC_DETAILS_TYPE = u'runtime_spec_details_type'
LIBRARY_DETAILS_TYPE = u'library_details_type'

UNKNOWN_ARRAY_TYPE = u'resource_type'
UNKNOWN_TYPE = u'unknown_type'

SPARK_MLLIB = u'mllib'
SPSS_FRAMEWORK = u'spss-modeler'
TENSORFLOW_FRAMEWORK = u'tensorflow'
XGBOOST_FRAMEWORK = u'xgboost'
SCIKIT_LEARN_FRAMEWORK = u'scikit-learn'
PMML_FRAMEWORK = u'pmml'

STR_TYPE = type(u'string or unicode')
STR_TYPE_NAME = STR_TYPE.__name__


def is_python_2():
    return sys.version_info[0] == 2


def str_type_conv(string):
    if is_python_2() and type(string) is str:
        return unicode(string)
    else:
        return string


def meta_props_str_conv(meta_props):
    for key in meta_props:
        if is_python_2() and type(meta_props[key]) is str:
            meta_props[key] = unicode(meta_props[key])


def get_url(url, headers, params=None, isIcp=False):
    import requests

    if isIcp:
        return requests.get(url, headers=headers, params=params, verify=False)
    else:
        return requests.get(url, headers=headers, params=params)


def print_text_header_h1(title):
    title = str_type_conv(title)
    print(u'\n\n' + (u'#' * len(title)) + u'\n')
    print(title)
    print(u'\n' + (u'#' * len(title)) + u'\n\n')


def print_text_header_h2(title):
    title = str_type_conv(title)
    print(u'\n\n' + (u'-' * len(title)))
    print(title)
    print((u'-' * len(title)) + u'\n\n')


def get_type_of_details(details):
    if 'resources' in details:
        return UNKNOWN_ARRAY_TYPE
    elif details is None:
        raise WMLClientError('Details doesn\'t exist.')
    else:
        try:
            if re.search(u'\/wml_instances\/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return INSTANCE_DETAILS_TYPE
        except:
            pass

        try:
            if re.search(u'\/deployments\/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return DEPLOYMENT_DETAILS_TYPE
        except:
            pass

        try:
            if re.search(u'\/experiments\/[^\/]+/runs/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return EXPERIMENT_RUN_DETAILS_TYPE
        except:
            pass

        try:
            if re.search('\/published_models\/[^\/]+$', details[u'metadata'][u'url']) is not None or re.search(u'\/v3\/ml_assets\/models\/[^\/]+$', details['entity']['ml_asset_url']) is not None:
                return MODEL_DETAILS_TYPE
        except:
            pass

        try:
            if re.search(u'\/ml_assets\/training_definitions\/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return DEFINITION_DETAILS_TYPE
        except:
            pass

        try:
            if re.search(u'\/experiments\/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return EXPERIMENT_DETAILS_TYPE
        except:
            pass

        try:
            if re.search(u'\/models\/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return TRAINING_RUN_DETAILS_TYPE
        except:
            pass

        try:
            if re.search(u'\/functions\/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return FUNCTION_DETAILS_TYPE
        except:
            pass

        try:
            if re.search(u'\/runtimes\/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return RUNTIME_SPEC_DETAILS_TYPE
        except:
            pass

        try:
            if re.search(u'\/libraries\/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return LIBRARY_DETAILS_TYPE
        except:
            pass

        return UNKNOWN_TYPE


def pack(directory_path):
    pass


def unpack(filename):
    pass


def load_model_from_directory(framework, directory_path):
    if framework == SPARK_MLLIB:
        from pyspark.ml import PipelineModel
        return PipelineModel.read().load(directory_path)
    elif framework == SPSS_FRAMEWORK:
        pass
    elif framework == TENSORFLOW_FRAMEWORK:
        pass
    elif framework == SCIKIT_LEARN_FRAMEWORK or framework == XGBOOST_FRAMEWORK:
        try:
            from sklearn.externals import joblib
            pkl_files = [x for x in os.listdir(directory_path) if x.endswith('.pkl')]

            if len(pkl_files) < 1:
                raise WMLClientError('No pkl files in directory.')

            model_id = pkl_files[0]
            return joblib.load(os.path.join(directory_path, model_id))
        except Exception as e:
            raise WMLClientError('Cannot load model from pkl file.', e)
    elif framework == PMML_FRAMEWORK:
        pass
    else:
        raise WMLClientError(u'Invalid framework specified: \'{}\'.'.format(framework))


# def load_model_from_directory(framework, directory_path):
#     if framework == SPARK_MLLIB:
#         from pyspark.ml import PipelineModel
#         return PipelineModel.read().load(directory_path)
#     elif framework == SPSS_FRAMEWORK:
#         pass
#     elif framework == TENSORFLOW_FRAMEWORK:
#         pass
#     elif framework == SCIKIT_LEARN_FRAMEWORK or framework == XGBOOST_FRAMEWORK:
#         from sklearn.externals import joblib
#         model_id = directory_path[directory_path.rfind('/') + 1:] + ".pkl"
#         return joblib.load(os.path.join(directory_path, model_id))
#     elif framework == PMML_MODEL:
#         pass
#     else:
#         raise WMLClientError('Invalid framework specified: \'{}\'.'.format(framework))


def load_model_from_package(framework, directory):
    unpack(directory)
    load_model_from_directory(framework, directory)


def save_model_to_file(model, framework, base_path, filename):
    if filename.find('.') != -1:
        base_name = filename[:filename.find('.') + 1]
        file_extension = filename[filename.find('.'):]
    else:
        base_name = filename
        file_extension = 'tar.gz'

    if framework == SPARK_MLLIB:
        model.write.overwrite.save(os.path.join(base_path, base_name))
    elif framework == SPSS_FRAMEWORK:
        pass
    elif framework == TENSORFLOW_FRAMEWORK:
        pass
    elif framework == XGBOOST_FRAMEWORK:
        pass
    elif framework == SCIKIT_LEARN_FRAMEWORK:
        os.makedirs(os.path.join(base_path, base_name))
        from sklearn.externals import joblib
        joblib.dump(model, os.path.join(base_path, base_name, base_name + ".pkl"))
    elif framework == PMML_FRAMEWORK:
        pass
    else:
        raise WMLClientError(u'Invalid framework specified: \'{}\'.'.format(framework))


def format_metrics(latest_metrics_list):
    formatted_metrics = u''

    for i in latest_metrics_list:

        values = i[u'values']

        if len(values) > 0:
            sorted_values = sorted(values, key=lambda k: k[u'name'])
        else:
            sorted_values = values

        for j in sorted_values:
            formatted_metrics = formatted_metrics + i[u'phase'] + ':' + j[u'name']+'='+'{0:.4f}'.format(j[u'value']) + '\n'

    return formatted_metrics


def docstring_parameter(args):
    def dec(obj):
        #obj.__doc__ = obj.__doc__.format(**args)
        return obj
    return dec


def group_metrics(metrics):
    grouped_metrics = []

    if len(metrics) > 0:
        import collections
        grouped_metrics = collections.defaultdict(list)
        for d in metrics:
            k = d[u'phase']
            grouped_metrics[k].append(d)

    return grouped_metrics


class StatusLogger:
    def __init__(self, initial_state):
        self.last_state = initial_state
        print(initial_state, end='')

    def log_state(self, state):
        if state == self.last_state:
            print('.', end='')
        else:
            print('\n{}'.format(state), end='')
            self.last_state = state

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def version():
    try:
        version = pkg_resources.get_distribution("watson-machine-learning-client").version
    except pkg_resources.DistributionNotFound:
        version = u'0.0.1-local'

    return version


def get_file_from_cos(cos_credentials):
    import ibm_boto3
    from ibm_botocore.client import Config

    client_cos = ibm_boto3.client(service_name='s3',
        ibm_api_key_id=cos_credentials['IBM_API_KEY_ID'],
        ibm_auth_endpoint=cos_credentials['IBM_AUTH_ENDPOINT'],
        config=Config(signature_version='oauth'),
        endpoint_url=cos_credentials['ENDPOINT'])

    streaming_body = client_cos.get_object(Bucket=cos_credentials['BUCKET'], Key=cos_credentials['FILE'])['Body']
    training_definition_bytes = streaming_body.read()
    streaming_body.close()
    filename = cos_credentials['FILE']
    f = open(filename, 'wb')
    f.write(training_definition_bytes)
    f.close()

    return filename


def extract_model_from_repository(model_uid, client):
    """
        Downloads and extracts archived model from wml repository.
        :param model_uid:
        :param client:
        :return: extracted directory path
    """
    create_empty_directory(model_uid)
    current_dir = os.getcwd()

    os.chdir(model_uid)
    model_dir = os.getcwd()

    fname = 'downloaded_' + model_uid + '.tar.gz'
    client.repository.download(model_uid, filename=fname)

    if fname.endswith("tar.gz"):
        tar = tarfile.open(fname)
        tar.extractall()
        tar.close()
    else:
        raise WMLClientError('Invalid type. Expected tar.gz')

    os.chdir(current_dir)
    return model_dir


def extract_mlmodel_from_archive(archive_path, model_uid):
    """
        Extracts archived model under model uid directory.
        :param model_uid:
        :param archive_path:
        :return: extracted directory path
    """
    create_empty_directory(model_uid)
    current_dir = os.getcwd()

    os.rename(archive_path, os.path.join(model_uid, archive_path))

    os.chdir(model_uid)
    model_dir = os.getcwd()

    if archive_path.endswith("tar.gz"):
        tar = tarfile.open(archive_path)
        tar.extractall()
        tar.close()
    else:
        raise WMLClientError('Invalid type. Expected tar.gz')

    os.chdir(current_dir)
    return os.path.join(model_uid, 'model.mlmodel')


def get_model_filename(directory, model_extension):
    logger = get_logger(__name__)
    model_filepath = None

    for file in os.listdir(directory):
        if file.endswith(model_extension):
            if model_filepath is None:
                model_filepath = os.path.join(directory, file)
            else:
                logger.warning('More than one file with extension \'{}\'.'.format(model_extension))

    if model_filepath is None:
        raise WMLClientError('No file with extension \'{}\'.'.format(model_extension))

    return model_filepath


def delete_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)


def create_empty_directory(directory):
    delete_directory(directory)
    os.makedirs(directory)


def install_package(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])


def is_ipython():
    # checks if the code is run in the notebook
    try:
        get_ipython
        return True
    except Exception:
        return False


def create_download_link(file_path, title="Download file."):
    # creates download link for binary files on notebook filesystem (Watson Studio)

    if is_ipython():
        from IPython.display import HTML
        import base64

        filename = os.path.basename(file_path)

        with open(file_path, 'rb') as file:
            b_model = file.read()
        b64 = base64.b64encode(b_model)
        payload = b64.decode()
        html = '<a download="{file_path}" href="data:binary;base64,{payload}" target="_blank">{title}</a>'
        html = html.format(payload=payload, title=title, file_path=filename)

        return HTML(html)


def convert_metadata_to_parameters(meta_data):
    parameters = []

    if meta_data is not None:
        if is_python_2():
            for key, value in meta_data.iteritems():
                parameters.append({'name': str(key), 'value': value})
        else:
            for key, value in meta_data.items():
                parameters.append({'name': str(key), 'value': value})

    return parameters


def is_of_python_basic_type(el):
    if type(el) in [int, float, bool, str]:
        return True
    elif type(el) in [list, tuple]:
        return all([is_of_python_basic_type(t) for t in el])
    elif type(el) is dict:
        if not all(type(k) == str for k in el.keys()):
            return False

        return is_of_python_basic_type(list(el.values()))
    else:
        return False
