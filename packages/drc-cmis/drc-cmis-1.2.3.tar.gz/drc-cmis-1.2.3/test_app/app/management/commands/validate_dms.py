import io
import uuid

from django.core.management.base import BaseCommand
from django.utils import timezone

from drc_cmis.client_builder import get_cmis_client
from drc_cmis.models import CMISConfig
from drc_cmis.utils.utils import get_random_string


class Command(BaseCommand):
    help = "Try all the CMIS operations used in drc_cmis against a DMS"

    def add_arguments(self, parser):
        parser.add_argument("client_url", type=str)
        parser.add_argument("binding", type=str)
        parser.add_argument("client_user", type=str)
        parser.add_argument("client_password", type=str)
        parser.add_argument("zaak_folder_path", type=str)
        parser.add_argument("other_folder_path", type=str)

    def handle(self, *args, **options):
        if CMISConfig.objects.count() == 0:
            CMISConfig.objects.create(
                client_url=options["client_url"],
                binding=options["binding"],
                client_user=options["client_user"],
                client_password=options["client_password"],
                zaak_folder_path=options["zaak_folder_path"],
                other_folder_path=options["other_folder_path"],
            )
        else:
            config = CMISConfig.objects.get()
            config.client_url = options["client_url"]
            config.binding = options["binding"]
            config.client_user = options["client_user"]
            config.client_password = options["client_password"]
            config.other_folder_path = options["other_folder_path"]
            config.zaak_folder_path = options["zaak_folder_path"]
            config.save()

        # General
        cmis_client = get_cmis_client()
        cmis_client.get_repository_info()
        get_root_folder_id(cmis_client)
        get_other_base_folder(cmis_client)
        print("General: Success")

        try:
            # Folders
            get_folder(cmis_client)
            create_folder(cmis_client)
            delete_folder(cmis_client)
            get_or_create_folder(cmis_client)
            create_zaaktype_folder(cmis_client)
            create_zaak_folder(cmis_client)
            create_cmis_folder_in_zaaktype(cmis_client)
            create_cmis_folder_in_zaak(cmis_client)
            print("Folders: Success")

            # Content objects
            create_content_object_oio(cmis_client)
            create_content_object_gebruiksrechten(cmis_client)
            get_content_object_oio(cmis_client)
            get_content_object_gebruiksrechten(cmis_client)
            delete_content_object_oio(cmis_client)
            delete_content_object_gebruiksrechten(cmis_client)
            print("Content objects: Success")

            # Documents
            create_document(cmis_client)
            lock_unlock_document(cmis_client)
            get_pwc(cmis_client)
            update_document(cmis_client)
            create_document_copy(cmis_client)
            move_document(cmis_client)
            delete_document(cmis_client)
            print("Documents: Success")
        except Exception as exc:
            # Clean up
            cmis_client.get_or_create_other_folder().delete_tree()
            print("Cleaned up")
            raise exc

        # Clean up
        cmis_client.get_or_create_other_folder().delete_tree()
        print("Cleaned up")


# ---* General *---
def get_other_base_folder(client):
    client.get_or_create_other_folder()


def get_root_folder_id(client):
    client.root_folder_id


# ---* Folders *---
def get_folder(client):
    client.get_folder(client.root_folder_id)


def create_folder(client):
    client.create_folder(
        f"TestFolder-{get_random_string()}",
        client.get_or_create_other_folder().objectId,
    )


def get_or_create_folder(client):
    client.get_or_create_folder(
        f"TestFolder-{get_random_string()}", client.get_or_create_other_folder()
    )


def create_zaaktype_folder(client):
    config = CMISConfig.objects.get()
    if config.binding == "BROWSER":
        properties = {
            "drc:zaaktype__url": "https://ref.tst.vng.cloud/ztc/api/v1/zaaktypen/0119dd4e-7be9-477e-bccf-75023b1453c1",
            "drc:zaaktype__identificatie": "1",
            "cmis:objectTypeId": f"{client.get_object_type_id_prefix('zaaktypefolder')}drc:zaaktypefolder",
        }
    elif config.binding == "WEBSERVICE":
        properties = {
            "drc:zaaktype__url": {
                "value": "https://ref.tst.vng.cloud/ztc/api/v1/zaaktypen/0119dd4e-7be9-477e-bccf-75023b1453c1",
                "type": "propertyString",
            },
            "drc:zaaktype__identificatie": {"value": "1", "type": "propertyString"},
            "cmis:objectTypeId": {
                "value": f"{client.get_object_type_id_prefix('zaaktypefolder')}drc:zaaktypefolder",
                "type": "propertyId",
            },
        }

    return client.create_folder(
        f"TestZaaktypeFolder-{get_random_string()}",
        client.get_or_create_other_folder().objectId,
        properties,
    )


def create_zaak_folder(client):
    config = CMISConfig.objects.get()
    if config.binding == "BROWSER":
        properties = {
            "drc:zaaktype__url": "https://ref.tst.vng.cloud/ztc/api/v1/zaaktypen/0119dd4e-7be9-477e-bccf-75023b1453c1",
            "drc:zaaktype__identificatie": "1",
            "cmis:objectTypeId": f"{client.get_object_type_id_prefix('zaaktypefolder')}drc:zaaktypefolder",
        }
    elif config.binding == "WEBSERVICE":
        properties = {
            "drc:zaaktype__url": {
                "value": "https://ref.tst.vng.cloud/ztc/api/v1/zaaktypen/0119dd4e-7be9-477e-bccf-75023b1453c1",
                "type": "propertyString",
            },
            "drc:zaaktype__identificatie": {"value": "1", "type": "propertyString"},
            "cmis:objectTypeId": {
                "value": f"{client.get_object_type_id_prefix('zaaktypefolder')}drc:zaaktypefolder",
                "type": "propertyId",
            },
        }
    return client.create_folder(
        f"TestZaakFolder-{get_random_string()}",
        client.get_or_create_other_folder().objectId,
        properties,
    )


def create_cmis_folder_in_zaaktype(client):
    zaaktype_folder = create_zaaktype_folder(client)
    client.create_folder(f"TestFolder-{get_random_string()}", zaaktype_folder.objectId)


def create_cmis_folder_in_zaak(client):
    zaak_folder = create_zaak_folder(client)
    client.create_folder(f"TestFolder-{get_random_string()}", zaak_folder.objectId)


def delete_folder(client):
    folder = client.create_folder(
        f"TestFolder-{get_random_string()}",
        client.get_or_create_other_folder().objectId,
    )
    folder.delete_tree()


def get_or_create_zaaktype_folder(client):
    zaak_type = {
        "url": "https://ref.tst.vng.cloud/ztc/api/v1/zaaktypen/0119dd4e-7be9-477e-bccf-75023b1453c1",
        "identificatie": 1,
        "omschrijving": "Melding Openbare Ruimte",
    }

    client.get_or_create_zaaktype_folder(zaak_type)


# ---* Content Objects *---
def create_content_object_oio(client):
    oio_data = {
        "object": "https://testserver/api/v1/zaken/12345",
        "informatieobject": "https://testserver/api/v1/documenten/12345",
        "object_type": "zaak",
    }
    client.create_content_object(data=oio_data, object_type="oio")


def create_content_object_gebruiksrechten(client):
    gebruiksrechten_data = {
        "informatieobject": "https://testserver/api/v1/documenten/12345",
        "startdatum": "2018-12-24T00:00:00Z",
        "omschrijving_voorwaarden": "Een hele set onredelijke voorwaarden",
    }

    client.create_content_object(
        data=gebruiksrechten_data, object_type="gebruiksrechten"
    )


def get_content_object_oio(client):
    oio_data = {
        "object": "https://testserver/api/v1/zaken/12345",
        "informatieobject": "https://testserver/api/v1/documenten/12345",
        "object_type": "zaak",
    }
    oio = client.create_content_object(data=oio_data, object_type="oio")

    client.get_content_object(drc_uuid=oio.uuid, object_type="oio")


def get_content_object_gebruiksrechten(client):
    gebruiksrechten_data = {
        "informatieobject": "https://testserver/api/v1/documenten/12345",
        "startdatum": "2018-12-24T00:00:00Z",
        "omschrijving_voorwaarden": "Een hele set onredelijke voorwaarden",
    }

    gebruiksrechten = client.create_content_object(
        data=gebruiksrechten_data, object_type="gebruiksrechten"
    )

    client.get_content_object(
        drc_uuid=gebruiksrechten.uuid, object_type="gebruiksrechten"
    )


def delete_content_object_oio(client):
    oio_data = {
        "object": "https://testserver/api/v1/zaken/12345",
        "informatieobject": "https://testserver/api/v1/documenten/12345",
        "object_type": "zaak",
    }
    oio = client.create_content_object(data=oio_data, object_type="oio")

    oio.delete_object()


def delete_content_object_gebruiksrechten(client):
    gebruiksrechten_data = {
        "informatieobject": "https://testserver/api/v1/documenten/12345",
        "startdatum": "2018-12-24T00:00:00Z",
        "omschrijving_voorwaarden": "Een hele set onredelijke voorwaarden",
    }

    gebruiksrechten = client.create_content_object(
        data=gebruiksrechten_data, object_type="gebruiksrechten"
    )

    gebruiksrechten.delete_object()


# ---* Documents *---
def create_document(client):
    data = {
        "creatiedatum": timezone.now(),
        "titel": "detailed summary",
    }
    content = io.BytesIO(b"Test content")
    client.create_document(identification=uuid.uuid4(), data=data, content=content)


def lock_unlock_document(client):
    data = {
        "creatiedatum": timezone.now(),
        "titel": "detailed summary",
    }
    content = io.BytesIO(b"Test content")
    document = client.create_document(
        identification=uuid.uuid4(), data=data, content=content
    )
    client.lock_document(
        drc_uuid=document.uuid, lock="00569792-f72f-420c-8b72-9c2fb9dd7601"
    )
    client.unlock_document(
        drc_uuid=document.uuid, lock="00569792-f72f-420c-8b72-9c2fb9dd7601"
    )


def get_pwc(client):
    data = {
        "creatiedatum": timezone.now(),
        "titel": "detailed summary",
    }
    content = io.BytesIO(b"Test content")
    document = client.create_document(
        identification=uuid.uuid4(), data=data, content=content
    )
    client.lock_document(
        drc_uuid=document.uuid, lock="00569792-f72f-420c-8b72-9c2fb9dd7601"
    )
    document.get_private_working_copy()


def update_document(client):
    data = {
        "creatiedatum": timezone.now(),
        "titel": "detailed summary",
    }
    content = io.BytesIO(b"Content before update")
    document = client.create_document(
        identification=uuid.uuid4(), data=data, content=content
    )

    new_data = {
        "auteur": "updated auteur",
        "link": "http://an.updated.link",
        "beschrijving": "updated beschrijving",
    }
    new_content = io.BytesIO(b"Content after update")

    client.lock_document(
        drc_uuid=document.uuid, lock="00569792-f72f-420c-8b72-9c2fb9dd7601"
    )
    client.update_document(
        drc_uuid=document.uuid,
        data=new_data,
        content=new_content,
        lock="00569792-f72f-420c-8b72-9c2fb9dd7601",
    )
    client.unlock_document(
        drc_uuid=document.uuid, lock="00569792-f72f-420c-8b72-9c2fb9dd7601"
    )


def create_document_copy(client):
    data = {
        "creatiedatum": timezone.now(),
        "titel": "detailed summary",
    }
    content = io.BytesIO(b"Test content")
    document = client.create_document(
        identification=uuid.uuid4(), data=data, content=content
    )

    client.copy_document(document, client.get_or_create_other_folder())


def move_document(client):
    data = {
        "creatiedatum": timezone.now(),
        "titel": "detailed summary",
    }
    content = io.BytesIO(b"Test content")
    document = client.create_document(
        identification=uuid.uuid4(), data=data, content=content
    )
    folder = client.create_folder(
        "TestFolderForMove", client.get_or_create_other_folder().objectId
    )
    document.move_object(folder)


def delete_document(client):
    data = {
        "creatiedatum": timezone.now(),
        "titel": "detailed summary",
    }
    content = io.BytesIO(b"Test content")
    document = client.create_document(
        identification=uuid.uuid4(), data=data, content=content
    )
    client.delete_document(drc_uuid=document.uuid)
