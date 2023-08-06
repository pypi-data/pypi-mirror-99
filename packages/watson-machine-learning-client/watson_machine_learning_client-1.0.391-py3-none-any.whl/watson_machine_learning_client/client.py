################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from watson_machine_learning_client.log_util import get_logger
from watson_machine_learning_client.utils import version
from watson_machine_learning_client.learning_system import LearningSystem
from watson_machine_learning_client.experiments import Experiments
from watson_machine_learning_client.repository import Repository
from watson_machine_learning_client.models import Models
from watson_machine_learning_client.definitions import Definitions
from watson_machine_learning_client.instance import ServiceInstance
from watson_machine_learning_client.deployments import Deployments
from watson_machine_learning_client.training import Training
from watson_machine_learning_client.runtimes import Runtimes
from watson_machine_learning_client.functions import Functions
from watson_machine_learning_client.wml_client_error import NoWMLCredentialsProvided
from watson_machine_learning_client.wml_client_error import WMLClientError
import os
import sys

'''
.. module:: WatsonMachineLearningAPIClient
   :platform: Unix, Windows
   :synopsis: Watson Machine Learning API Client.

.. moduleauthor:: IBM
'''


class WatsonMachineLearningAPIClient:

    def __init__(self, wml_credentials, project_id=None):
        self._logger = get_logger(__name__)
        if wml_credentials is None:
            raise NoWMLCredentialsProvided()
        if 'icp' == wml_credentials[u'instance_id'].lower():
            self.ICP = True
            os.environ["DEPLOYMENT_PLATFORM"] = "private"
        else:
            self.ICP = False
        self.wml_credentials = wml_credentials
        self.project_id = project_id
        self.wml_token = None
        self.service_instance = ServiceInstance(self)
        if not self.ICP:
            self.service_instance.details = self.service_instance.get_details()
        self.repository = Repository(self)
        self._models = Models(self)
        self._definitions = Definitions(self)
        self.deployments = Deployments(self)
        if not self.ICP:
            self.experiments = Experiments(self)
            self.learning_system = LearningSystem(self)
            self.training = Training(self)
        self.runtimes = Runtimes(self)
        self._functions = Functions(self)
        self._logger.info(u'Client successfully initialized')
        self.version = version()

        print("NOTE!! DEPRECATED!! This Watson Machine Learning client version is deprecated"
              " starting Sep 1st, 2020 and will be discontinued at the end of the migration period. "
              "Refer to the documentation at 'https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/wml-ai.html'"
              " for the migration process to be able to access new features")

        if (3 == sys.version_info.major) and (6 == sys.version_info.minor):
            print(
                "DEPRECATED!! Python 3.6 framework is deprecated and will be removed on Jan 20th, 2021. It will be "
                "read-only mode starting Nov 20th, 2020. i.e you won't be able to create new assets using this client. "
                "For cloud, switch to using new client https://pypi.org/project/ibm-watson-machine-learning with "
                "python 3.7")

    def _get_headers(self, content_type='application/json', no_content_type=False):
        headers = {
            'Authorization': 'Bearer ' + self.service_instance._get_token(),
            'X-WML-User-Client': 'PythonClient'
        }
        if self._is_IAM():
            headers['ML-Instance-ID'] = self.wml_credentials['instance_id']

        if not self.ICP:
            if self.project_id is not None:
                headers.update({'X-Watson-Project-ID': self.project_id})

        if not no_content_type:
            headers.update({'Content-Type': content_type})

        return headers

    def _get_icptoken(self):
        return self.service_instance._create_token()
    def _is_IAM(self):
        if ('apikey' in self.wml_credentials.keys()):
            if(self.wml_credentials['apikey']!=''):
                 return True
            else:
                raise WMLClientError('apikey value cannot be \'\'. Either pass a valid apikey for IAM token or go with ML token.')
        else:
            return False