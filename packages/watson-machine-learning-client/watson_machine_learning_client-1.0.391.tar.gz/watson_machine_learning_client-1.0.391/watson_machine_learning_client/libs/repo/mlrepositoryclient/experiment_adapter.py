################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################


import re
import json,ast
from watson_machine_learning_client.libs.repo.mlrepository import MetaNames, MetaProps
from watson_machine_learning_client.libs.repo.mlrepository import PipelineArtifact
from watson_machine_learning_client.libs.repo.swagger_client.models.ml_assets_create_experiment_output import MlAssetsCreateExperimentOutput
from watson_machine_learning_client.libs.repo.mlrepositoryartifact import SparkPipelineLoader, SparkPipelineContentLoader,\
    IBMSparkPipelineContentLoader, MLPipelineContentLoader
from watson_machine_learning_client.libs.repo.util import Json2ObjectMapper
from watson_machine_learning_client.libs.repo.util.library_imports import LibraryChecker
from watson_machine_learning_client.libs.repo.base_constants import *
from watson_machine_learning_client.libs.repo.mlrepositoryartifact.generic_file_pipeline_model_loader import GenericFilePipelineModelLoader
from watson_machine_learning_client.libs.repo.mlrepository.generic_archive_pipeline_artifact import GenericArchivePipelineArtifact
from watson_machine_learning_client.libs.repo.util.generic_archive_file_check import GenericArchiveFrameworkCheck
lib_checker = LibraryChecker()

class ExperimentAdapter(object):
    """
    Adapter creating pipeline artifact using output from service.
    """
    @staticmethod
    def __strip_output(output):
        return ast.literal_eval(json.dumps(output))

    def __init__(self, pipeline_output, version_output, client):
        self.pipeline_output = pipeline_output
        self.version_output = version_output
        self.client = client
        self.pipeline_entity = self.__strip_output(pipeline_output.entity)
        if pipeline_output is not None and not isinstance(pipeline_output, MlAssetsCreateExperimentOutput):
            raise ValueError('Invalid type for pipeline: {}'.format(pipeline_output.__class__.__name__))

        if self.pipeline_entity['framework'] is not None:
            self.pipeline_type = pipeline_output.entity['framework']


    def artifact(self):
#       if re.match('sparkml-pipeline-\d+\.\d+', self.pipeline_type['name']) is not None:
        if re.match('mllib', self.pipeline_type['name']) is not None:
            lib_checker.check_lib(PYSPARK)
            pipeline_artifact_builder = type(
                "PipelineArtifact",
                (SparkPipelineContentLoader, SparkPipelineLoader, PipelineArtifact, object),
                {}
            )
        elif re.match('wml', self.pipeline_type['name']) is not None:
            lib_checker.check_lib(PYSPARK)
            lib_checker.check_lib(MLPIPELINE)
            pipeline_artifact_builder = type(
                "WMLPipelineArtifact",
                (MLPipelineContentLoader, SparkPipelineLoader, PipelineArtifact, object),
                {}
            )
        elif GenericArchiveFrameworkCheck.is_archive_framework(self.pipeline_type['name']):
            pipeline_artifact_builder = type(
                "GenericArchivePipelineArtifact",
                (GenericFilePipelineModelLoader, GenericArchivePipelineArtifact, object),
                {}
            )
        else:
            raise ValueError('Invalid pipeline_type: {}'.format(self.pipeline_type['name']))

        prop_map = {
            MetaNames.CREATION_TIME: self.pipeline_output.metadata.created_at,
            MetaNames.LAST_UPDATED: self.pipeline_output.metadata.modified_at,
            MetaNames.FRAMEWORK_VERSION: self.pipeline_type['version'],
            MetaNames.FRAMEWORK_NAME: self.pipeline_type['name']
        }
        if 'libraries' in self.pipeline_type:
            if self.pipeline_type.get('libraries') is not None:
                prop_map[MetaNames.FRAMEWORK_LIBRARIES] = self.pipeline_type.get('libraries')

        if self.pipeline_entity.get('description', None) is not None:
            prop_map[MetaNames.DESCRIPTION] = self.pipeline_entity['description']

        if self.pipeline_entity.get('author', None) is not None:
            authorval = self.pipeline_entity.get('author')
            if authorval.get('name', None) is not None:
                prop_map[MetaNames.AUTHOR_NAME] = authorval['name']

        if self.pipeline_entity.get('tags', None) is not None:
            prop_map[MetaNames.TAGS] = self.pipeline_entity.get('tags')

        if self.pipeline_entity.get('training_data_reference', None) is not None:
            # prop_map[MetaNames.TRAINING_DATA_REF] = str(self.pipeline_entity['training_data']).encode('ascii')
            prop_map[MetaNames.TRAINING_DATA_REFERENCE] = str(self.pipeline_entity['training_data_reference'])
      #  name = ''.join(map(lambda x: chr(ord(x)),self.pipeline_output.entity['name']))
        name = self.pipeline_entity.get('name', None)

        pipeline_url = self.pipeline_output.metadata.url
        pipeline_id = pipeline_url.split("/training_definitions/")[1].split("/")[0]

        pipeline_artifact = pipeline_artifact_builder(
            pipeline_id,
            name,
            MetaProps(prop_map))

        pipeline_artifact.client = self.client

        if self.version_output is not None:
            version_url = self.version_output['url']
            training_definition_url = version_url.split("/versions")[0]



            version_prop_map = {
                MetaNames.VERSION: self.version_output['guid'],
                MetaNames.TRAINING_DEFINITION_VERSION_URL:version_url,
                MetaNames.TRAINING_DEFINITION_URL:training_definition_url
            }
            pipeline_artifact._content_href = self.version_output['content_url']

        else:
            version_prop_map = {
                MetaNames.VERSION: self.pipeline_output.entity['training_definition_version']['guid']
            }
            pipeline_artifact._content_href = self.pipeline_output.entity['training_definition_version']['content_url']

        pipeline_artifact.meta.merge(MetaProps(version_prop_map))

        return pipeline_artifact
