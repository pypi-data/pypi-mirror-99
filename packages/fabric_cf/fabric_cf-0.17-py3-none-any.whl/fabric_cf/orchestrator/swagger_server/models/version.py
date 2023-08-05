# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from fabric_cf.orchestrator.swagger_server.models.base_model_ import Model
from fabric_cf.orchestrator.swagger_server import util


class Version(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, version: str=None, gitsha1: str=None):  # noqa: E501
        """Version - a model defined in Swagger

        :param version: The version of this Version.  # noqa: E501
        :type version: str
        :param gitsha1: The gitsha1 of this Version.  # noqa: E501
        :type gitsha1: str
        """
        self.swagger_types = {
            'version': str,
            'gitsha1': str
        }

        self.attribute_map = {
            'version': 'version',
            'gitsha1': 'gitsha1'
        }
        self._version = version
        self._gitsha1 = gitsha1

    @classmethod
    def from_dict(cls, dikt) -> 'Version':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Version of this Version.  # noqa: E501
        :rtype: Version
        """
        return util.deserialize_model(dikt, cls)

    @property
    def version(self) -> str:
        """Gets the version of this Version.


        :return: The version of this Version.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version: str):
        """Sets the version of this Version.


        :param version: The version of this Version.
        :type version: str
        """

        self._version = version

    @property
    def gitsha1(self) -> str:
        """Gets the gitsha1 of this Version.


        :return: The gitsha1 of this Version.
        :rtype: str
        """
        return self._gitsha1

    @gitsha1.setter
    def gitsha1(self, gitsha1: str):
        """Sets the gitsha1 of this Version.


        :param gitsha1: The gitsha1 of this Version.
        :type gitsha1: str
        """

        self._gitsha1 = gitsha1
