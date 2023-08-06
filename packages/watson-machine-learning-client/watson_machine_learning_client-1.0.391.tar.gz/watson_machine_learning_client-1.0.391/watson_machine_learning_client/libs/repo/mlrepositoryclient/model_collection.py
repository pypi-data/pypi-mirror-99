################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################


import logging
import re
import json
import os
import tarfile, shutil

from .model_adapter import ModelAdapter
from watson_machine_learning_client.libs.repo.swagger_client.rest import ApiException
from watson_machine_learning_client.libs.repo.mlrepository import  ModelArtifact
from watson_machine_learning_client.libs.repo.mlrepository import MetaNames
from watson_machine_learning_client.libs.repo.swagger_client.models import ModelInput, ModelVersionInput, ModelTrainingDataRef, ModelVersionOutput, \
    MetaObjectMetadata, ModelVersionOutputEntity, ModelVersionOutputEntityModel, ArtifactAuthor, EvaluationDefinition, TagRepository
from watson_machine_learning_client.libs.repo.swagger_client.models import EvaluationDefinitionMetrics, ConnectionObjectWithNameRepository, ArrayDataInputRepository, EvaluationDefinitionRepositoryMetrics
from watson_machine_learning_client.libs.repo.swagger_client.models import MlAssetsCreateModelInput, FrameworkOutputRepository, AuthorRepository, EvaluationDefinitionRepository, FrameworkOutputRepositoryLibraries,FrameworkOutputRepositoryRuntimes
from watson_machine_learning_client.libs.repo.swagger_client.models import ContentLocation,HyperParameters
from watson_machine_learning_client.libs.repo.util.json_2_object_mapper import Json2ObjectMapper
from watson_machine_learning_client.libs.repo.util.exceptions import UnsupportedTFSerializationFormat,InvalidCaffeModelArchive
from watson_machine_learning_client.libs.repo.swagger_client.models import  MlAssetsModelSizeOutput
from watson_machine_learning_client.libs.repo.util.unique_id_gen import uid_generate
from watson_machine_learning_client.libs.repo.swagger_client.models.framework_output_repository_runtimes import FrameworkOutputRepositoryRuntimes


logger = logging.getLogger('ModelCollection')


class ModelCollection:
    """
    Client operating on models in repository service.

    :param str base_path: base url to Watson Machine Learning instance
    :param MLRepositoryApi repository_api: client connecting to repository rest api
    :param MLRepositoryClient client: high level client used for simplification and argument for constructors
    """
    def __init__(self, base_path, repository_api, client):

        from watson_machine_learning_client.libs.repo.mlrepositoryclient import MLRepositoryClient
        from watson_machine_learning_client.libs.repo.mlrepositoryclient import MLRepositoryApi

        if not isinstance(base_path, str) and not isinstance(base_path, unicode):
            raise ValueError('Invalid type for base_path: {}'.format(base_path.__class__.__name__))

        if not isinstance(repository_api, MLRepositoryApi):
            raise ValueError('Invalid type for repository_api: {}'.format(repository_api.__class__.__name__))

        if not isinstance(client, MLRepositoryClient):
            raise ValueError('Invalid type for client: {}'.format(client.__class__.__name__))

        self.base_path = base_path
        self.repository_api = repository_api
        self.client = client

    def all(self, queryMap=None):
        """
        Gets info about all models which belong to this user.

        Not complete information is provided by all(). To get detailed information about model use get().

        :return: info about models
        :rtype: list[ModelArtifact]
        """
        logger.debug('Fetching information about all models')
        all_models = self.repository_api.repository_list_models(queryMap)
        list_model_artifact = []
        if all_models is not None:
            resr = all_models.resources
            for iter1 in resr:
                model_entity = iter1.entity
                ver_url = iter1.entity['model_version']
                list_model_artifact.append(ModelAdapter(iter1, ver_url, self.client).artifact())
            return list_model_artifact
        else:
            return []

    def get(self, artifact_id):
        """
        Gets detailed information about model.

        :param str artifact_id: uid used to identify model
        :return: returned object has all attributes of SparkPipelineModelArtifact but its class name is ModelArtifact
        :rtype: ModelArtifact(SparkPipelineModelLoader)
        """
        logger.debug('Fetching information about pipeline model: {}'.format(artifact_id))

        if not isinstance(artifact_id, str) and not isinstance(artifact_id, unicode):
            raise ValueError('Invalid type for artifact_id: {}'.format(artifact_id.__class__.__name__))

        model_output = self.repository_api.v3_ml_assets_models_artifact_id_get(artifact_id)

        if model_output is not None:
            latest_version = model_output.entity['model_version']
            return ModelAdapter(model_output, latest_version, self.client).artifact()
        else:
            logger.debug('Model with guid={} not found'.format(artifact_id))
            raise ApiException('Model with guid={} not found'.format(artifact_id))

    def versions(self, artifact_id):
        """
        Gets all available versions.

        Not implemented yet.

        :param str artifact_id: uid used to identify model
        :return: ???
        :rtype: list[str]
        """

        if not isinstance(artifact_id, str) and not isinstance(artifact_id, unicode):
            raise ValueError('Invalid type for artifact_id: {}'.format(artifact_id.__class__.__name__))

        logger.debug('Fetching information about pipeline model: {}'.format(artifact_id))

        model_output = self.repository_api.repository_list_model_versions(artifact_id)

        list_model_version_artifact = [ModelArtifact]
        if model_output is not None:
            resr = model_output.resources
            for iter1 in resr:
                model_entity = iter1.entity
                ver_url = iter1.entity['model_version']
                list_model_version_artifact.append(ModelAdapter(iter1, iter1.entity['model_version'], self.client).artifact())
            return list_model_version_artifact
        else:
            logger.debug('Model with guid={} not found'.format(artifact_id))
            raise ApiException('Model with guid={} not found'.format(artifact_id))

    def version(self, artifact_id, ver):
        """
        Gets model version with given artifact_id and ver
        :param str artifact_id: uid used to identify model
        :param str ver: uid used to identify version of model
        :return: ModelArtifact(SparkPipelineModelLoader) -- returned object has all attributes of SparkPipelineModelArtifact but its class name is ModelArtifact
        """
        logger.debug('Fetching information about model version: {}, {}'.format(artifact_id, ver))

        if not isinstance(artifact_id, str) and not isinstance(artifact_id, unicode):
            raise ValueError('Invalid type for artifact_id: {}'.format(artifact_id.__class__.__name__))

        if not isinstance(ver, str) and not isinstance(ver, unicode):
            raise ValueError('Invalid type for ver: {}'.format(ver.__class__.__name__))

        model_version_output = self.repository_api.repository_get_model_version(artifact_id, ver)
        if model_version_output is not None:
            if model_version_output is not None:
                return ModelAdapter(model_version_output, model_version_output.entity['model_version'], self.client).artifact()
            else:
                raise Exception('Model with guid={} not found'.format(artifact_id))
        else:
            raise Exception('Model with guid={} not found'.format(artifact_id))

    def version_from_href(self, artifact_version_href):
        """
        Gets model version from given href

        :param str artifact_version_href: href identifying artifact and version
        :return: returned object has all attributes of SparkPipelineModelArtifact but its class name is PipelineModelArtifact
        :rtype: PipelineModelArtifact(SparkPipelineModelLoader)
        """

        if not isinstance(artifact_version_href, str) and not isinstance(artifact_version_href, unicode):
            raise ValueError('Invalid type for artifact_version_href: {}'.format(artifact_version_href.__class__.__name__))

        #if artifact_version_href.startswith(self.base_path):
        matched = re.search('.*/v3/ml_assets/models/([A-Za-z0-9\-]+)/versions/([A-Za-z0-9\-]+)',
                            artifact_version_href)
        matchedV2 = re.search('.*/v2/artifacts/models/([A-Za-z0-9\-]+)/versions/([A-Za-z0-9\-]+)',
                              artifact_version_href)
        if matched is not None:
            artifact_id = matched.group(1)
            version_id = matched.group(2)
            return self.version(artifact_id, version_id)
        elif matchedV2 is not None:
            artifact_id = matchedV2.group(1)
            version_id = matchedV2.group(2)
            return self.version(artifact_id, version_id)
        else:
            raise ValueError('Unexpected artifact version href: {} format'.format(artifact_version_href))

    def remove(self, artifact_id):
        """
        Removes model with given artifact_id.

        :param str artifact_id: uid used to identify model
        """

        if not isinstance(artifact_id, str):
            raise ValueError('Invalid type for artifact_id: {}'.format(artifact_id.__class__.__name__))

        return self.repository_api.v3_ml_assets_models_artifact_id_delete(artifact_id)

    def save(self, artifact, query_param=None):
        if artifact.meta.prop(MetaNames.FRAMEWORK_NAME).startswith("scikit-learn"):
            return self._save_scikit_pipeline_model(artifact, query_param)
        elif artifact.meta.prop(MetaNames.FRAMEWORK_NAME).startswith("xgboost"):
            return self._save_xgboost_model(artifact, query_param)
        elif artifact.meta.prop(MetaNames.FRAMEWORK_NAME).startswith("tensorflow"):
            if isinstance(artifact.ml_pipeline_model, str):
                return self._save_tensorflow_pipeline_model_tar(artifact, query_param)
            else:
                return self._save_tensorflow_pipeline_model(artifact, query_param)
        elif MetaNames.is_archive_framework(artifact.meta.prop(MetaNames.FRAMEWORK_NAME)) :
            if isinstance(artifact.ml_pipeline_model, str):
               return self._save_generic_archive_pipeline_model(artifact, query_param)
            else:
                raise ValueError('Invalid type for artifact_id: {}'.format(artifact.__class__.__name__))
        elif artifact.meta.prop(MetaNames.FRAMEWORK_NAME).startswith("hybrid"):
            return self._save_hybird_pipeline_model(artifact, query_param)
        else:
            return self._save_spark_pipeline_model(artifact, query_param)

    def _save_scikit_pipeline_model(self, artifact, query_param=None):
        """
        Saves model in repository service.

        :param ScikitPipelineModelArtifact artifact: artifact to be saved in the repository service
        :return: saved artifact with changed MetaProps
        :rtype: ScikitPipelineModelArtifact
        """
        logger.debug('Creating a new scikit pipeline model: {}'.format(artifact.name))

        if not issubclass(type(artifact), ModelArtifact):
            raise ValueError('Invalid type for artifact: {}'.format(artifact.__class__.__name__))

        if artifact.meta.prop(MetaNames.MODEL_VERSION_URL) is not None:
            raise ApiException(400, 'Invalid operation: save the same model artifact twice')

        try:
            if artifact.uid is None:
                model_artifact = self._create_pipeline_model(artifact, query_param)
            else:
                model_artifact = artifact

            if model_artifact.uid is None:
                raise RuntimeError('Internal Error: Model without ID')
            else:
                return model_artifact
        except Exception as e:
            logger.info('Error in pipeline model creation')
            import traceback
            print(traceback.format_exc())
            raise e

    def _save_hybird_pipeline_model(self, artifact, query_param=None):
        """
        Saves model in repository service.

        :param ScikitPipelineModelArtifact artifact: artifact to be saved in the repository service
        :return: saved artifact with changed MetaProps
        :rtype: ScikitPipelineModelArtifact
        """
        logger.debug('Creating a new hybrid model: {}'.format(artifact.name))

        if not issubclass(type(artifact), ModelArtifact):
            raise ValueError('Invalid type for artifact: {}'.format(artifact.__class__.__name__))

        if artifact.meta.prop(MetaNames.MODEL_VERSION_URL) is not None:
            raise ApiException(400, 'Invalid operation: save the same model artifact twice')

        try:
            if artifact.uid is None:
                model_artifact = self._create_pipeline_model(artifact, query_param)
            else:
                model_artifact = artifact

            if model_artifact.uid is None:
                raise RuntimeError('Internal Error: Model without ID')
            else:
                return model_artifact
        except Exception as e:
            logger.info('Error in hybrid model creation')
            import traceback
            print(traceback.format_exc())


    def _save_tensorflow_pipeline_model(self, artifact, query_param=None):
        """
        Saves model in repository service.

        :param ScikitPipelineModelArtifact artifact: artifact to be saved in the repository service
        :return: saved artifact with changed MetaProps
        :rtype: ScikitPipelineModelArtifact
        """
        logger.debug('Creating a new tensorflow pipeline model: {}'.format(artifact.name))

        if not issubclass(type(artifact), ModelArtifact):
            raise ValueError('Invalid type for artifact: {}'.format(artifact.__class__.__name__))

        if artifact.meta.prop(MetaNames.MODEL_VERSION_URL) is not None:
            raise ApiException(400, 'Invalid operation: save the same model artifact twice')

        try:
            if artifact.uid is None:
                model_artifact = self._create_pipeline_model(artifact, query_param)
            else:
                model_artifact = artifact

            if model_artifact.uid is None:
                raise RuntimeError('Internal Error: Model without ID')
            else:
                return model_artifact
        except Exception as e:
            logger.info('Error in pipeline model creation')
            import traceback
            print(traceback.format_exc())
            raise e

    def _save_tensorflow_pipeline_model_tar(self, artifact, query_param=None):
        """
        Saves model in repository service.

        :param TensorflowPipelineModelTarArtifact artifact: artifact to be saved in the repository service
        :return: saved artifact with changed MetaProps
        :rtype: TensorflowPipelineModelTarArtifact
        """
        logger.debug('Creating a new tensorflow model artifact: {}'.format(artifact.name))

        if not issubclass(type(artifact), ModelArtifact):
            raise ValueError('Invalid type for artifact: {}'.format(artifact.__class__.__name__))

        if artifact.meta.prop(MetaNames.MODEL_VERSION_URL) is not None:
            raise ApiException(400, 'Invalid operation: Attempted to save the same model artifact twice')

        # validate if the artifact supplied is a valid artifact for Tensorflow

        keras_version = artifact.get_keras_version()
        if keras_version is not None:
            artifact.update_keras_version_meta(keras_version)

        if (not artifact.is_valid_tf_archive()) and keras_version is None:
            raise UnsupportedTFSerializationFormat('The specified compressed archive is invalid. Please ensure the '
                                                   'Tensorflow model is serialized using '
                                                   'tensorflow.saved_model.builder.SavedModelBuilder API. If using '
                                                   'Keras, ensure save() of is used to save the model')

        try:
            if artifact.uid is None:
                model_artifact = self._create_pipeline_model(artifact, query_param)
            else:
                model_artifact = artifact

            if model_artifact.uid is None:
                raise RuntimeError('Internal Error: Model without ID')
            else:
                return model_artifact
        except Exception as e:
            logger.info('Error in pipeline model creation')
            import traceback
            print(traceback.format_exc())
            raise e

    def _save_generic_archive_pipeline_model(self, artifact, query_param = None):
        """
        Saves model in repository service.

        :param GenericArchiveModelArtifact artifact: artifact to be saved in the repository service
        :return: saved artifact with changed MetaProps
        :rtype: GenericArchiveModelArtifact
        """

        logger.debug('Creating a new archive model artifact: {}'.format(artifact.name))

        if not issubclass(type(artifact), ModelArtifact):
            raise ValueError('Invalid type for artifact: {}'.format(artifact.__class__.__name__))

        if artifact.meta.prop(MetaNames.MODEL_VERSION_URL) is not None:
            raise ApiException(400, 'Invalid operation: Attempted to save the same model artifact twice')

        if not os.path.exists(artifact.ml_pipeline_model):
            raise IOError('The artifact specified ( {} ) does not exist.'.format(artifact.ml_pipeline_model))

        if artifact.meta.prop(MetaNames.FRAMEWORK_NAME)=='caffe':
            extracted_path= artifact.extract_tar_file()
            if (not artifact.is_valid_caffe_archive(extracted_path)) is None:
                raise InvalidCaffeModelArchive('The specified compressed caffe model archive is invalid.')


        try:
            if artifact.uid is None:
                model_artifact = self._create_pipeline_model(artifact, query_param)
            else:
                model_artifact = artifact

            if model_artifact.uid is None:
                raise RuntimeError('Internal Error: Model without ID')
            else:
                return model_artifact
        except Exception as e:
            logger.info('Error in pipeline model creation')
            import traceback
            print(traceback.format_exc())
            raise e

    def _save_xgboost_model(self, artifact, query_param = None):
        """
        Saves model in repository service.

        :param ScikitPipelineModelArtifact artifact: artifact to be saved in the repository service
        :return: saved artifact with changed MetaProps
        :rtype: ScikitPipelineModelArtifact
        """
        logger.debug('Creating a new xgboost model: {}'.format(artifact.name))

        if not issubclass(type(artifact), ModelArtifact):
            raise ValueError('Invalid type for artifact: {}'.format(artifact.__class__.__name__))

        if artifact.meta.prop(MetaNames.MODEL_VERSION_URL) is not None:
            raise ApiException(400, 'Invalid operation: save the same model artifact twice')

        try:
            if artifact.uid is None:
                model_artifact = self._create_pipeline_model(artifact, query_param)
            else:
                model_artifact = artifact

            if model_artifact.uid is None:
                raise RuntimeError('Internal Error: Model without ID')
            else:
                return model_artifact

        except Exception as e:
            logger.info('Error in pipeline model creation')
            import traceback
            print(traceback.format_exc())
            raise e

    def _save_spark_pipeline_model(self, artifact, query_param=None):
        """
        Saves model in repository service.

        :param SparkPipelineModelArtifact artifact: artifact to be saved in the repository service
        :return: saved artifact with changed MetaProps
        :rtype: SparkPipelineModelArtifact
        """
        logger.debug('Creating a new pipeline model: {}'.format(artifact.name))

        if not issubclass(type(artifact), ModelArtifact):
            raise ValueError('Invalid type for artifact: {}'.format(artifact.__class__.__name__))

        if artifact.meta.prop(MetaNames.MODEL_VERSION_URL) is not None:
            raise ApiException(400, 'Invalid operation: save the same model artifact twice')
        try:
            if artifact.uid is None:
                if artifact.pipeline_artifact() is None:
                    model_artifact = self._create_pipeline_model(artifact, query_param)
                else:
                    pipeline_artifact = artifact.pipeline_artifact()
                    if pipeline_artifact.uid is None:
                        if pipeline_artifact.meta.prop(MetaNames.TRAINING_DEFINITION_VERSION_URL) is not None:
                            exp_ver_url = pipeline_artifact.meta.prop(MetaNames.TRAINING_DEFINITION_VERSION_URL).encode('utf-8')
                            new_pipeline_artifact = self._get_pipeline(exp_ver_url)
                        else:
                            new_pipeline_artifact = self._create_pipeline(pipeline_artifact)

                        tmp_model_artifact = artifact._copy(pipeline_artifact=new_pipeline_artifact)
                        model_artifact = self._create_pipeline_model(tmp_model_artifact, query_param)
                    else:
                        model_artifact = self._create_pipeline_model(artifact, query_param)
            else:
                model_artifact = artifact

            if model_artifact.uid is None:
                raise RuntimeError('Internal Error: Model without ID')
            else:
                return model_artifact
        except Exception as e:
            logger.info('Error in pipeline model creation')
            import traceback
            print(traceback.format_exc())
            raise e

    def _get_experiment_id_from_url(self, artifact_version_url):
        """
        Gets experiment id from given url

        :return: returned object has all attributes of SparkPipelineArtifact but its class name is PipelineArtifact
        """

        if not isinstance(artifact_version_url, str):
            raise ValueError('Invalid type for artifact_version_href: {}'
                             .format(artifact_version_url.__class__.__name__))

        #if artifact_version_url.startswith(self.base_path):
        matched = re.search(
            '.*/v3/ml_assets/training_definitions/([A-Za-z0-9\-]+)/versions/([A-Za-z0-9\-]+)', artifact_version_url)
        if matched is not None:
            experiment_id = matched.group(1)
            return experiment_id
        else:
            raise ValueError('Unexpected artifact version url in metaprop: {} format'.format(artifact_version_url))
            #else:
            #    raise ValueError('The artifact version href: {} is not within the client host: {}').format(
            #        artifact_version_url,
            #        self.base_path
            #    )

    def _get_pipeline(self, pipeline_version_url):
        return self.client.pipelines.version_from_href(pipeline_version_url)

    def _create_pipeline(self, pipeline_artifact):
        return self.client.pipelines.save(pipeline_artifact)

    def _create_pipeline_model(self, model_artifact, query_param=None):
        model_input = self._prepare_model_input(model_artifact)
        model_output = self.repository_api.ml_assets_model_creation(model_input)

        if model_output is not None:
            location = model_output.metadata.url
            if location is not None:
                logger.debug('New pipeline model created at: {}'.format(location))
                matched = re.search('.*/v3/artifacts/models/([A-Za-z0-9\-]+)', location)
                model_id = model_output.metadata.guid
                #               martifact = model_artifact._copy(uid=model_id)
                new_artifact = ModelAdapter(model_output, model_output.entity['model_version'], self.client).artifact()

                new_artifact.load_model = lambda: model_artifact.ml_pipeline_model

                new_artifact.model_instance = lambda: model_artifact.ml_pipeline_model
                model_artifact_with_version = model_artifact._copy(meta_props=new_artifact.meta,uid=model_id)
                if MetaNames.CONTENT_LOCATION not in model_artifact_with_version.meta.get():
                    status_url = self._upload_pipeline_model_content(model_artifact_with_version, query_param)
                    if status_url is not None and status_url is not "":
                        place_holder =model_artifact_with_version.meta.add(MetaNames.STATUS_URL, status_url)
                        new_async_artifact = model_artifact_with_version._copy(meta_props=place_holder)
                        return new_async_artifact
                    else:
                        return new_artifact

                else:
                    return model_artifact_with_version
        else:
            logger.info('Location of the new pipeline model not found')
            raise ApiException(404, 'No artifact location')

    def _create_pipeline_model_version(self, model_artifact, query_param=None):
        model_version_input = self._get_version_input(model_artifact)
        r = self.repository_api.repository_model_version_creation(model_artifact.uid, model_version_input)
        location = r[2].get('Location')
        if location is not None:
            logger.debug('New model version created at: {}'.format(location))
            try:
                new_version_artifact = self.version_from_href(location)
                new_version_artifact.model_instance = lambda: model_artifact.ml_pipeline_model
                model_artifact_with_version = model_artifact._copy(meta_props=new_version_artifact.meta)
                if MetaNames.CONTENT_LOCATION not in model_artifact_with_version.meta.get():
                    status_url = self._upload_pipeline_model_content(model_artifact_with_version, query_param)
                    if status_url is not None and status_url is not "":
                        place_holder =model_artifact_with_version.meta.add(MetaNames.STATUS_URL, status_url)
                        new_async_artifact = model_artifact_with_version._copy(meta_props=place_holder)
                        return new_async_artifact
                    else:
                        return new_version_artifact
            except Exception as ex:
                raise ex
        else:
            logger.info('Location of the new model version not found')
            raise ApiException(404, 'No artifact location')

    def _upload_pipeline_model_content(self, model_artifact, query_param=None):
        model_id = model_artifact.uid
        version_id = model_artifact.meta.prop(MetaNames.VERSION)
        asyncValue = "false"

        if query_param is not None:
            for key in query_param:
                if (key!='async'):
                    raise ValueError("Got an unexpected keyword argument '%s'"% key)
                else:
                    asyncValue = query_param[key]
                    if(asyncValue!='true' and asyncValue!='false'):
                        raise ValueError("Got an unexpected value '%s' for keyword argument '%s'"% (asyncValue, key))

        if version_id is None:
            raise RuntimeError('Model meta `{}` not set'.format(MetaNames.VERSION))

        content_stream = model_artifact.reader().read()
        if(query_param is not None and asyncValue == 'true'):

                def upload_call():
                    self.repository_api.upload_pipeline_model_version(model_id, version_id, content_stream, query_param)

                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    future = executor.submit(upload_call)
                    try:
                        future.result()
                        logger.info("After future.result future completed:%s "%(str(future.done())))
                    except Exception as exc:
                         logger.info(' Upload to version_id %r generated  exception: %s' % (version_id, exc))
                    else:
                         logger.info("Upload to version id %r success with response." %version_id)


                model_version_url = model_artifact.meta.prop(MetaNames.MODEL_VERSION_URL)
                status_url = '%s/content/status' %(model_version_url)

        else:
            logger.info("In case of either no query param passed  or 'async':'false' is passed")
            self.repository_api.upload_pipeline_model_version(model_id, version_id, content_stream)
            status_url = ""

        content_stream.close()
        model_artifact.reader().close()
        logger.debug('Content uploaded for model version created at: {}, {}'.format(model_id, version_id))
        return status_url

    def get_status(self, url):
        polling_status = self.repository_api.get_async_status(url)
        if polling_status is not None:
            if(polling_status.entity['status_message']=="Running" or polling_status.entity['status_message'] == "Completed"):
                return polling_status.entity['status_message']
            else:
                error_msg=("'Status' = 'ERROR', 'Message' = '%s'" %polling_status.entity['status_message'])
                return error_msg

        else:
            raise ValueError("Request with url ='%s'failed" %url)


    def _extract_model_from_output(self, model_output):
        latest_version = model_output.entity.latest_version
        if latest_version is not None:
            content_status, content_location = None, None
            if hasattr(model_output.entity.model_version, 'content_status'):
                content_status = model_output.entity.model_version.content_status
            if hasattr(model_output.entity.model_version, 'content_location'):
                content_location = model_output.entity.model_version.content_location
            if hasattr(model_output.entity.model_version, 'hyper_parameters'):
                hyper_parameters = model_output.entity.model_version.hyper_parameters
            latest_version_output = ModelVersionOutput(
                MetaObjectMetadata(
                    latest_version.guid,
                    latest_version.href, None, None
                ),
                ModelVersionOutputEntity(
                    ModelVersionOutputEntityModel(model_output.metadata.guid, model_output.metadata.href),
                    latest_version.content_href, None, None, content_status, content_location,hyper_parameters,category
                )
            )
        else:
            latest_version_output = None
        return ModelAdapter(model_output, latest_version_output, self.client).artifact()

    @staticmethod
    def _prepare_model_input(artifact):
        meta = artifact.meta

        mauthor = AuthorRepository(
            artifact.meta.prop(MetaNames.AUTHOR_NAME))

        runtime = artifact.meta.prop(MetaNames.RUNTIME)

        runtimes = artifact.meta.prop(MetaNames.RUNTIMES)

        framework_runtimes = artifact.meta.prop(MetaNames.FRAMEWORK_RUNTIMES)

        frlibraries = artifact.meta.prop(MetaNames.FRAMEWORK_LIBRARIES)
        hyperparameters = artifact.meta.prop(MetaNames.HYPER_PARAMETERS)
        output_data_schema = artifact.meta.prop(MetaNames.OUTPUT_DATA_SCHEMA)
        runtime_url_input = artifact.meta.prop(MetaNames.RUNTIMES.URL)

        tags_data_list = artifact.meta.prop(MetaNames.TAGS)
        if isinstance(artifact.meta.prop(MetaNames.TAGS), str):
            tags_list = json.loads(artifact.meta.prop(MetaNames.TAGS))
            tags_data_list = []
            if isinstance(tags_list, list):
                for iter1 in tags_list:
                    tags_data = TagRepository()
                    for key in iter1:
                        if key == 'value':
                            tags_data.value= iter1['value']
                        if key == 'description':
                            tags_data.description = iter1['description']
                    tags_data_list.append(tags_data)
            else:
                raise ValueError("Invalid tag Input")

        if runtime is not None:
            try:
                name,version = runtime.split("-")
                runtime = FrameworkOutputRepositoryRuntimes(name,version)
            except Exception as ex:
                raise ex


        if runtimes is not None:
            if isinstance(artifact.meta.prop(MetaNames.RUNTIMES),str):
                runtimes = json.loads(artifact.meta.prop(MetaNames.RUNTIMES))
            else:
                runtimes = artifact.meta.prop(MetaNames.RUNTIMES)
            if not issubclass (type(runtimes), list):
                raise ValueError('Invalid data format for runtimes.')

        if framework_runtimes is not None:
            if isinstance(artifact.meta.prop(MetaNames.FRAMEWORK_RUNTIMES),str):
                framework_runtimes = json.loads(artifact.meta.prop(MetaNames.FRAMEWORK_RUNTIMES))
            else:
                framework_runtimes = artifact.meta.prop(MetaNames.FRAMEWORK_RUNTIMES)
            if not issubclass (type(framework_runtimes), list):
                raise ValueError('Invalid data format for framework_runtimes.')

        run_frmRun = None
        if framework_runtimes is not None:
            run_frmRun = framework_runtimes
        elif runtimes is not None:
            run_frmRun = runtimes

        frlibrary_param_list = []
        if frlibraries is not None:
            if isinstance(artifact.meta.prop(MetaNames.FRAMEWORK_LIBRARIES),str):
                frlibraryvalue = json.loads(artifact.meta.prop(MetaNames.FRAMEWORK_LIBRARIES))
            else:
                frlibraryvalue = artifact.meta.prop(MetaNames.FRAMEWORK_LIBRARIES)
            if not issubclass (type(frlibraryvalue), list):
                raise ValueError('Invalid data format for framework libraries.')
            for iter1 in frlibraryvalue:
                frlibrary_param = FrameworkOutputRepositoryLibraries(
                    iter1.get('name', None),
                    iter1.get('version', None)
                )
                frlibrary_param_list.append(frlibrary_param)
                mframework = FrameworkOutputRepository(
                    name=artifact.meta.prop(MetaNames.FRAMEWORK_NAME),
                    version=artifact.meta.prop(MetaNames.FRAMEWORK_VERSION),
                    runtime=runtime,
                    runtimes=run_frmRun,
                    libraries=frlibrary_param_list
                )
        else:
            mframework = FrameworkOutputRepository(
                name=artifact.meta.prop(MetaNames.FRAMEWORK_NAME),
                version=artifact.meta.prop(MetaNames.FRAMEWORK_VERSION),
                runtime=runtime,
                runtimes=run_frmRun
            )

        hyper_param_list = []
        if isinstance(hyperparameters, str):

            hyperparameters_list = json.loads(artifact.meta.prop(MetaNames.HYPER_PARAMETERS))

            if isinstance(hyperparameters_list, list):
              for iter1 in hyperparameters_list:
                hyper_param = HyperParameters()
                for key in iter1:
                    if key == 'name':
                        hyper_param.name = iter1['name']
                    if key == 'string_value':
                        hyper_param.string_value = iter1['string_value']
                    if key == 'double_value':
                       hyper_param.double_value = iter1['double_value']
                    if key == 'int_value':
                       hyper_param.int_value = iter1['int_value']
                hyper_param_list.append(hyper_param)

        training_data_list = []
        model_input_evaluation = None
        content_location = None
        category = None
        label_column=artifact.meta.prop(MetaNames.LABEL_FIELD)
        category = artifact.meta.prop(MetaNames.CATEGORY)

        if artifact.meta.prop(MetaNames.CONTENT_LOCATION) is not None:
            if isinstance(artifact.meta.prop(MetaNames.CONTENT_LOCATION),str):
                contentloc=json.loads(artifact.meta.prop(MetaNames.CONTENT_LOCATION))
            else:
                contentloc=artifact.meta.prop(MetaNames.CONTENT_LOCATION)
            content_location = ContentLocation(
                contentloc.get('url', None),
                contentloc.get('connection', None),
                contentloc.get('source', None))

        if artifact.meta.prop(MetaNames.FRAMEWORK_NAME).startswith("scikit") \
                or artifact.meta.prop(MetaNames.FRAMEWORK_NAME).startswith("xgboost"):
            return MlAssetsCreateModelInput(
                tags=tags_data_list,
                framework=mframework,
                name=artifact.name,
                description=meta.prop(MetaNames.DESCRIPTION),
                author=mauthor,
                label_column=label_column,
                training_data_schema=meta.prop(MetaNames.TRAINING_DATA_SCHEMA),
                hyper_parameters=hyper_param_list,
                output_data_schema=output_data_schema,
                runtime_url=runtime_url_input
            )
        elif artifact.meta.prop(MetaNames.FRAMEWORK_NAME).startswith("tensorflow") \
                or MetaNames.is_archive_framework(artifact.meta.prop(MetaNames.FRAMEWORK_NAME)):
            return MlAssetsCreateModelInput(
                tags=tags_data_list,
                framework=mframework,
                name=artifact.name,
                description=meta.prop(MetaNames.DESCRIPTION),
                author=mauthor,
                label_column=meta.prop(MetaNames.LABEL_FIELD),
                hyper_parameters=hyper_param_list,
                output_data_schema=output_data_schema ,
                runtime_url=runtime_url_input
            )
        elif artifact.meta.prop(MetaNames.FRAMEWORK_NAME).startswith("hybrid"):
            return MlAssetsCreateModelInput(
                tags=tags_data_list,
                framework=mframework,
                name=artifact.name,
                description=meta.prop(MetaNames.DESCRIPTION),
                author=mauthor,
                label_column=label_column,
                content_location= content_location,
                hyper_parameters=hyper_param_list,
                output_data_schema=output_data_schema,
                runtime_url=runtime_url_input,
                category=category
            )
        else:
            if artifact.meta.prop(MetaNames.TRAINING_DATA_REFERENCE) is not None:
                dataref_list=artifact.meta.prop(MetaNames.TRAINING_DATA_REFERENCE)
                if isinstance(dataref_list, str):
                    dataref_list = json.loads(artifact.meta.prop(MetaNames.TRAINING_DATA_REFERENCE))
                training_data_list = []
                if isinstance(dataref_list, list):
                    for iter1 in dataref_list:
                        training_data = ConnectionObjectWithNameRepository()
                        for key in iter1:
                            if key == 'name':
                                training_data.name = iter1['name']
                            if key == 'source':
                                training_data.source = iter1['source']
                            if key == 'connection':
                                training_data.connection = iter1['connection']
                        training_data_list.append(training_data)
                elif isinstance(dataref_list, dict):
                    training_data = ConnectionObjectWithNameRepository(
                        dataref_list.get('name', None),
                        dataref_list.get('connection', None),
                        dataref_list.get('source', None)
                    )
                    training_data_list.append(training_data)
                else:
                    raise ApiException(404, 'Pipeline not found')
            if artifact.meta.prop(MetaNames.EVALUATION_METHOD) is not None:
                metrics = Json2ObjectMapper.read(artifact.meta.prop(MetaNames.EVALUATION_METRICS))
                metrics = list(map(
                    lambda metrics_set: EvaluationDefinitionRepositoryMetrics(metrics_set["name"], metrics_set["threshold"], metrics_set["value"]),
                    metrics
                ))
                model_input_evaluation = EvaluationDefinitionRepository(
                    artifact.meta.prop(MetaNames.EVALUATION_METHOD),
                    metrics)

            if artifact.pipeline_artifact() is not None:
                pipeline_artifact = artifact.pipeline_artifact()
                model_input = MlAssetsCreateModelInput(
                    tags=tags_data_list,
                    framework=mframework,
                    name=artifact.name,
                    description=meta.prop(MetaNames.DESCRIPTION),
                    training_definition_url=pipeline_artifact.meta.prop(MetaNames.TRAINING_DEFINITION_VERSION_URL),
                    author=mauthor,
                    label_column=artifact.meta.prop(MetaNames.LABEL_FIELD),
                    training_data_reference=training_data_list,
                    input_data_schema=meta.prop(MetaNames.INPUT_DATA_SCHEMA),
                    evaluation=model_input_evaluation,
                    training_data_schema=artifact.meta.prop(MetaNames.TRAINING_DATA_SCHEMA),
                    transformed_label=artifact.meta.prop(MetaNames.TRANSFORMED_LABEL_FIELD),
                    content_location=content_location,
                    hyper_parameters=hyper_param_list,
                    output_data_schema=output_data_schema,
                    runtime_url=runtime_url_input
                )
            else:
                model_input = MlAssetsCreateModelInput(
                    tags=tags_data_list,
                    framework=mframework,
                    name=artifact.name,
                    description=meta.prop(MetaNames.DESCRIPTION),
                    author=mauthor,
                    label_column=artifact.meta.prop(MetaNames.LABEL_FIELD),
                    training_data_reference=training_data_list,
                    input_data_schema=meta.prop(MetaNames.INPUT_DATA_SCHEMA),
                    evaluation=model_input_evaluation,
                    training_data_schema=artifact.meta.prop(MetaNames.TRAINING_DATA_SCHEMA),
                    transformed_label=artifact.meta.prop(MetaNames.TRANSFORMED_LABEL_FIELD),
                    content_location=content_location,
                    hyper_parameters=hyper_param_list,
                    output_data_schema=output_data_schema,
                    runtime_url=runtime_url_input
                )
            return model_input

    @staticmethod
    def _get_version_input(artifact):
        meta = artifact.meta
        if artifact.meta.prop(MetaNames.FRAMEWORK_NAME).startswith("scikit-model-") \
                or artifact.meta.prop(MetaNames.FRAMEWORK_NAME).startswith("xgboost"):
            return ModelVersionInput()
        else:
            training_data_ref = Json2ObjectMapper.read(meta.prop(MetaNames.TRAINING_DATA_REFERENCE))
            #if not training_data_ref: #check if is empty dict
            #    training_data_ref = None

            metrics = Json2ObjectMapper.read(meta.prop(MetaNames.EVALUATION_METRICS))
            metrics = list(map(
                lambda metrics_set: EvaluationDefinitionMetrics(metrics_set["name"], metrics_set["threshold"], metrics_set["value"]),
                metrics
            ))

            return ModelVersionInput(training_data_ref, EvaluationDefinition(
                meta.prop(MetaNames.EVALUATION_METHOD),
                metrics
            ))

