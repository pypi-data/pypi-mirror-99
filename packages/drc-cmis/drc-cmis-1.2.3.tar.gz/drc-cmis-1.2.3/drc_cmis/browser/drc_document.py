import datetime
import logging
import mimetypes
import uuid
from datetime import date
from io import BytesIO
from typing import List, Optional, Union

from django.utils import timezone

import pytz

from drc_cmis.utils.mapper import (
    DOCUMENT_MAP,
    GEBRUIKSRECHTEN_MAP,
    OBJECTINFORMATIEOBJECT_MAP,
    ZAAK_MAP,
    ZAAKTYPE_MAP,
    mapper,
)
from drc_cmis.utils.query import CMISQuery
from drc_cmis.utils.utils import extract_latest_version, get_random_string

from .request import CMISRequest

logger = logging.getLogger(__name__)


class CMISBaseObject(CMISRequest):
    name_map = None
    type_name = None
    type_class = None

    def __init__(self, data):
        super().__init__()
        self.data = data

        # Convert any timestamps to datetime objects
        properties = data.get("properties", {})
        for prop_name, prop_details in properties.items():
            if prop_details["type"] == "datetime" and prop_details["value"] is not None:
                prop_details["value"] = timezone.make_aware(
                    datetime.datetime.fromtimestamp(int(prop_details["value"]) / 1000),
                    pytz.timezone(self.time_zone),
                )

        self.properties = properties

    def __getattr__(self, name: str):
        try:
            return super(CMISRequest, self).__getattribute__(name)
        except AttributeError:
            pass

        if name in self.properties:
            return self.properties[name]["value"]

        convert_name = f"cmis:{name}"
        if convert_name in self.properties:
            return self.properties[convert_name]["value"]

        convert_name = f"drc:{name}"
        if self.name_map is not None and name in self.name_map:
            convert_name = self.name_map.get(name)

        if convert_name not in self.properties:
            raise AttributeError(f"No property '{convert_name}'")

        return self.properties[convert_name]["value"]

    @classmethod
    def build_properties(cls, data: dict) -> dict:
        """Construct property dictionary."""

        props = {}
        for key, value in data.items():
            prop_name = mapper(key, type=cls.type_name)
            if not prop_name:
                logger.debug("CMIS_ADAPTER: No property name found for key '%s'", key)
                continue
            if value is not None:
                if isinstance(value, datetime.date) or isinstance(value, datetime.date):
                    value = value.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                props[prop_name] = str(value)

        return props


class CMISContentObject(CMISBaseObject):
    def delete_object(self):
        """Delete all versions of an object"""
        data = {"objectId": self.objectId, "cmisaction": "delete"}
        logger.debug("CMIS_ADAPTER: delete_object: request data: %s", data)
        json_response = self.post_request(self.root_folder_url, data=data)
        logger.debug("CMIS_ADAPTER: delete_object: response data: %s", json_response)
        return json_response

    def get_parent_folders(self) -> List["Folder"]:
        """Get the parent folders of an object.

        An object has multiple parent folders if it has been multifiled.
        """
        params = {
            "objectId": self.objectId,
            "cmisselector": "parents",
        }
        logger.debug("CMIS_ADAPTER: get_parent_folders: request params: %s", params)

        json_response = self.get_request(self.root_folder_url, params=params)
        logger.debug(
            "CMIS_ADAPTER: get_parent_folders: response data: %s", json_response
        )
        return self.get_all_objects(json_response, Folder)

    def move_object(self, target_folder: "Folder"):
        source_folder = self.get_parent_folders()[0]

        data = {
            "objectId": self.objectId,
            "cmisaction": "move",
            "sourceFolderId": source_folder.objectId,
            "targetFolderId": target_folder.objectId,
        }

        logger.debug("CMIS_ADAPTER: move_object: request data: %s", data)

        # invoke the URL
        json_response = self.post_request(self.root_folder_url, data=data)
        logger.debug("CMIS_ADAPTER: move_object: response data: %s", json_response)
        self.data = json_response
        self.properties = json_response.get("properties")
        return self

    def _update_properties(self, properties: dict) -> "CMISContentObject":
        data = {"objectId": self.objectId, "cmisaction": "update"}
        prop_count = 0
        for prop_key, prop_value in properties.items():
            # Skip property because update is not allowed
            if prop_key == "cmis:objectTypeId":
                continue

            if isinstance(prop_value, date):
                prop_value = prop_value.strftime("%Y-%m-%dT%H:%I:%S.000Z")

            data["propertyId[%s]" % prop_count] = prop_key
            data["propertyValue[%s]" % prop_count] = prop_value
            prop_count += 1
        logger.debug("CMIS_ADAPTER: update_properties: request data: %s", data)

        # invoke the URL
        json_response = self.post_request(self.root_folder_url, data=data)
        logger.debug(
            "CMIS_ADAPTER: update_properties: response data: %s", json_response
        )
        self.data = json_response
        self.properties = json_response.get("properties")

        return self


class Document(CMISContentObject):
    table = "drc:document"
    name_map = DOCUMENT_MAP

    @classmethod
    def build_properties(cls, data: dict, new: bool = True) -> dict:

        props = {}
        for key, value in data.items():
            prop_name = mapper(key, type="document")
            if not prop_name:
                logger.debug("CMIS_ADAPTER: No property name found for key '%s'", key)
                continue
            props[prop_name] = value

        # For documents that are not new, the uuid shouldn't be written
        props.pop(mapper("uuid"), None)

        if new:
            # increase likelihood of uniqueness of title by appending a random string
            title, suffix = data.get("titel"), get_random_string()
            if title is not None:
                props["cmis:name"] = f"{title}-{suffix}"

            # For new documents, the uuid needs to be set
            new_uuid = str(uuid.uuid4())
            props[mapper("uuid", type="document")] = new_uuid

            # The identification needs to be set ONLY for newly created documents.
            # identificatie is immutable once the document is created
            if not props.get(mapper("identificatie")):
                prop_name = mapper("identificatie")
                props[prop_name] = new_uuid

        return props

    def checkout(self):
        data = {"objectId": self.objectId, "cmisaction": "checkOut"}
        logger.debug("CMIS_ADAPTER: checkout: request data: %s", data)
        json_response = self.post_request(self.root_folder_url, data=data)
        logger.debug("CMIS_ADAPTER: checkout: response data: %s", json_response)
        return Document(json_response)

    def update_content(self, content: BytesIO, filename: Optional[str] = None):
        self.set_content_stream(content, filename)

    def update_properties(self, properties: dict):
        return self._update_properties(properties)

    def get_private_working_copy(self) -> Union["Document", None]:
        """
        Retrieve the private working copy version of a document.
        """
        logger.debug(
            "CMIS_ADAPTER: Fetching the PWC for the current document (UUID '%s')",
            self.uuid,
        )

        if self.versionSeriesCheckedOutId is None:
            all_versions = self.get_all_versions()
            for document in all_versions:
                if document.versionLabel == "pwc":
                    return document
        else:
            # http://docs.oasis-open.org/cmis/CMIS/v1.1/os/CMIS-v1.1-os.html#x1-5590004
            params = {
                "cmisselector": "object",  # get the object rather than the content
                "objectId": self.versionSeriesCheckedOutId,
            }
            logger.debug(
                "CMIS_ADAPTER: get_private_working_copy: request params: %s", params
            )

            data = self.get_request(self.root_folder_url, params)
            logger.debug(
                "CMIS_ADAPTER: get_private_working_copy: response data: %s", data
            )
            return type(self)(data)

    def get_latest_version(self):
        """Get the latest version or the PWC"""
        query = CMISQuery("SELECT * FROM drc:document WHERE drc:document__uuid = '%s'")

        data = {
            "cmisaction": "query",
            "statement": query(self.uuid),
        }
        logger.debug("CMIS_ADAPTER: get_latest_version: request data: %s", data)
        json_response = self.post_request(self.base_url, data)
        logger.debug(
            "CMIS_ADAPTER: get_latest_version: response data: %s", json_response
        )

        return extract_latest_version(type(self), json_response.get("results"))

    def checkin(self, checkin_comment, major=True):
        props = {
            "objectId": self.objectId,
            "cmisaction": "checkIn",
            "checkinComment": checkin_comment,
            "major": major,
        }
        logger.debug("CMIS_ADAPTER: checkin: request data: %s", props)

        # invoke the URL
        json_response = self.post_request(self.root_folder_url, props)
        logger.debug("CMIS_ADAPTER: checkin: response data: %s", json_response)
        return Document(json_response)

    def set_content_stream(self, content_file: BytesIO, filename: Optional[str] = None):
        data = {"objectId": self.objectId, "cmisaction": "setContent"}

        mimetype = None
        # need to determine the mime type
        if filename:
            mimetype, _encoding = mimetypes.guess_type(
                filename
            )  # If the extension is not recognised, mimetype is None

        if not mimetype:
            mimetype = "application/binary"

        files = {self.name: (self.name, content_file, mimetype)}
        logger.debug("CMIS_ADAPTER: set_content_stream: request data: %s", data)

        json_response = self.post_request(self.root_folder_url, data=data, files=files)
        logger.debug(
            "CMIS_ADAPTER: set_content_stream: response data: %s", json_response
        )
        return Document(json_response)

    def get_content_stream(self) -> BytesIO:
        params = {"objectId": self.objectId, "cmisaction": "content"}
        logger.debug("CMIS_ADAPTER: get_content_stream: request params: %s", params)
        file_content = self.get_request(self.root_folder_url, params=params)
        logger.debug(
            "CMIS_ADAPTER: get_content_stream: retrieved file length %i",
            len(file_content),
        )
        return BytesIO(file_content)

    def get_all_versions(self) -> List["Document"]:
        """
        Retrieve all versions for a given document.

        Versions are ordered by most-recent first based on cmis:creationDate. If there
        is a PWC, it shall be the first object.

        http://docs.oasis-open.org/cmis/CMIS/v1.1/errata01/os/CMIS-v1.1-errata01-os-complete.html#x1-3440006
        """

        params = {"objectId": self.objectId, "cmisselector": "versions"}
        logger.debug("CMIS_ADAPTER: get_all_versions: request params: %s", params)
        all_versions = self.get_request(self.root_folder_url, params=params)
        logger.debug("CMIS_ADAPTER: get_all_versions: response data: %s", all_versions)
        return [Document(data) for data in all_versions]

    def delete_object(self) -> None:
        """
        Permanently delete the object from the CMIS store, with all its versions.

        By default, all versions should be deleted according to the CMIS standard. If
        the document is currently locked (i.e. there is a private working copy), we need
        to cancel that checkout first.
        """
        latest_version = self.get_latest_version()
        if latest_version.isVersionSeriesCheckedOut:
            cancel_checkout_data = {
                "cmisaction": "cancelCheckout",
                "objectId": latest_version.objectId,
            }
            logger.debug(
                "CMIS_ADAPTER: delete_object: request data: %s", cancel_checkout_data
            )

            response = self.post_request(
                self.root_folder_url, data=cancel_checkout_data
            )

            logger.debug("CMIS_ADAPTER: delete_object: response data: %s", response)

            refreshed_document = self.get_latest_version()
            return refreshed_document.delete_object()
        return super().delete_object()


class Gebruiksrechten(CMISContentObject):
    table = "drc:gebruiksrechten"
    name_map = GEBRUIKSRECHTEN_MAP
    type_name = "gebruiksrechten"

    def update_properties(self, properties: dict) -> "Gebruiksrechten":
        """
        Update the properties of an existing gebruiksrechten.

        :param properties: dict, the new properties
        :return: Updated gebruiksrechten
        """
        return self._update_properties(properties)


class ObjectInformatieObject(CMISContentObject):
    table = "drc:oio"
    name_map = OBJECTINFORMATIEOBJECT_MAP
    type_name = "oio"


class Folder(CMISBaseObject):
    table = "cmis:folder"

    def get_children_folders(self, child_type: Union[str, dict] = None) -> List:
        """Get all the folders in the current folder

        :param child_type: str or dict, Contains the object type ID of the children folders to retrieve.
        If it is a dict, then the child type is the value of the key "value".
        """

        if child_type is not None:
            if isinstance(child_type, dict):
                object_type_id = child_type["value"]
            else:
                object_type_id = child_type

            # Alfresco case: the object type ID has an extra prefix (F:drc:zaakfolder, instead of drc:zaakfolder)
            # The prefix needs to be removed for the query
            if len(object_type_id.split(":")) > 2:
                object_type_id = ":".join(object_type_id.split(":")[1:])
        else:
            object_type_id = "cmis:folder"

        data = {
            "cmisaction": "query",
            "statement": f"SELECT * FROM {object_type_id} WHERE IN_FOLDER('{self.objectId}')",
        }
        logger.debug("CMIS_ADAPTER: get_children_folders: request data: %s", data)
        json_response = self.post_request(self.base_url, data=data)
        logger.debug(
            "CMIS_ADAPTER: get_children_folders: response data: %s", json_response
        )
        return self.get_all_results(json_response, Folder)

    def delete_tree(self, **kwargs):
        data = {"objectId": self.objectId, "cmisaction": "deleteTree"}
        logger.debug("CMIS_ADAPTER: delete_tree: request data: %s", data)
        json_response = self.post_request(self.root_folder_url, data=data)
        logger.debug("CMIS_ADAPTER: delete_tree: response data: %s", json_response)


class ZaakTypeFolder(CMISBaseObject):
    table = "drc:zaaktypefolder"
    name_map = ZAAKTYPE_MAP
    type_name = "zaaktype"


class ZaakFolder(CMISBaseObject):
    table = "drc:zaakfolder"
    name_map = ZAAK_MAP
    type_name = "zaak"
