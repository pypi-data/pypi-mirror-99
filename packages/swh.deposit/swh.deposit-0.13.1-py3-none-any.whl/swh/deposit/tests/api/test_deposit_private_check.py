# Copyright (C) 2017-2021  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from django.urls import reverse_lazy as reverse
import pytest
from rest_framework import status

from swh.deposit.api.checks import MANDATORY_FIELDS_MISSING
from swh.deposit.api.private.deposit_check import (
    MANDATORY_ARCHIVE_INVALID,
    MANDATORY_ARCHIVE_MISSING,
    MANDATORY_ARCHIVE_UNSUPPORTED,
)
from swh.deposit.config import (
    COL_IRI,
    DEPOSIT_STATUS_DEPOSITED,
    DEPOSIT_STATUS_REJECTED,
    DEPOSIT_STATUS_VERIFIED,
    PRIVATE_CHECK_DEPOSIT,
)
from swh.deposit.models import Deposit
from swh.deposit.parsers import parse_xml
from swh.deposit.tests.common import (
    create_arborescence_archive,
    create_archive_with_archive,
)

PRIVATE_CHECK_DEPOSIT_NC = PRIVATE_CHECK_DEPOSIT + "-nc"


def private_check_url_endpoints(collection, deposit):
    """There are 2 endpoints to check (one with collection, one without)"""
    return [
        reverse(PRIVATE_CHECK_DEPOSIT, args=[collection.name, deposit.id]),
        reverse(PRIVATE_CHECK_DEPOSIT_NC, args=[deposit.id]),
    ]


@pytest.mark.parametrize("extension", ["zip", "tar", "tar.gz", "tar.bz2", "tar.xz"])
def test_deposit_ok(
    authenticated_client, deposit_collection, ready_deposit_ok, extension
):
    """Proper deposit should succeed the checks (-> status ready)

    """
    deposit = ready_deposit_ok
    for url in private_check_url_endpoints(deposit_collection, deposit):
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == DEPOSIT_STATUS_VERIFIED
        deposit = Deposit.objects.get(pk=deposit.id)
        assert deposit.status == DEPOSIT_STATUS_VERIFIED

        deposit.status = DEPOSIT_STATUS_DEPOSITED
        deposit.save()


@pytest.mark.parametrize("extension", ["zip", "tar", "tar.gz", "tar.bz2", "tar.xz"])
def test_deposit_invalid_tarball(
    tmp_path, authenticated_client, deposit_collection, extension
):
    """Deposit with tarball (of 1 tarball) should fail the checks: rejected

    """
    deposit = create_deposit_archive_with_archive(
        tmp_path, extension, authenticated_client, deposit_collection.name
    )
    for url in private_check_url_endpoints(deposit_collection, deposit):
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == DEPOSIT_STATUS_REJECTED
        details = data["details"]
        # archive checks failure
        assert len(details["archive"]) == 1
        assert details["archive"][0]["summary"] == MANDATORY_ARCHIVE_INVALID

        deposit = Deposit.objects.get(pk=deposit.id)
        assert deposit.status == DEPOSIT_STATUS_REJECTED


def test_deposit_ko_missing_tarball(
    authenticated_client, deposit_collection, ready_deposit_only_metadata
):
    """Deposit without archive should fail the checks: rejected

    """
    deposit = ready_deposit_only_metadata
    assert deposit.status == DEPOSIT_STATUS_DEPOSITED

    for url in private_check_url_endpoints(deposit_collection, deposit):
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == DEPOSIT_STATUS_REJECTED
        details = data["details"]
        # archive checks failure
        assert len(details["archive"]) == 1
        assert details["archive"][0]["summary"] == MANDATORY_ARCHIVE_MISSING
        deposit = Deposit.objects.get(pk=deposit.id)
        assert deposit.status == DEPOSIT_STATUS_REJECTED

        deposit.status = DEPOSIT_STATUS_DEPOSITED
        deposit.save()


def test_deposit_ko_unsupported_tarball(
    tmp_path, authenticated_client, deposit_collection, ready_deposit_invalid_archive
):
    """Deposit with an unsupported tarball should fail the checks: rejected

    """
    deposit = ready_deposit_invalid_archive
    assert DEPOSIT_STATUS_DEPOSITED == deposit.status

    for url in private_check_url_endpoints(deposit_collection, deposit):
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == DEPOSIT_STATUS_REJECTED
        details = data["details"]

        # archive checks failure
        assert len(details["archive"]) == 1
        assert details["archive"][0]["summary"] == MANDATORY_ARCHIVE_UNSUPPORTED
        # metadata check failure
        assert len(details["metadata"]) == 1
        mandatory = details["metadata"][0]
        assert mandatory["summary"] == MANDATORY_FIELDS_MISSING
        assert set(mandatory["fields"]) == set(
            [
                "atom:author or codemeta:author",
                "atom:name or atom:title or codemeta:name",
            ]
        )

        deposit = Deposit.objects.get(pk=deposit.id)
        assert deposit.status == DEPOSIT_STATUS_REJECTED

        deposit.status = DEPOSIT_STATUS_DEPOSITED
        deposit.save()


def test_check_deposit_metadata_ok(
    authenticated_client, deposit_collection, ready_deposit_ok
):
    """Proper deposit should succeed the checks (-> status ready)
       with all **MUST** metadata

       using the codemeta metadata test set
    """
    deposit = ready_deposit_ok
    assert deposit.status == DEPOSIT_STATUS_DEPOSITED

    for url in private_check_url_endpoints(deposit_collection, deposit):
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["status"] == DEPOSIT_STATUS_VERIFIED
        deposit = Deposit.objects.get(pk=deposit.id)
        assert deposit.status == DEPOSIT_STATUS_VERIFIED

        deposit.status = DEPOSIT_STATUS_DEPOSITED
        deposit.save()


def create_deposit_archive_with_archive(
    root_path, archive_extension, client, collection_name
):
    # we create the holding archive to a given extension
    archive = create_arborescence_archive(
        root_path,
        "archive1",
        "file1",
        b"some content in file",
        extension=archive_extension,
    )

    # now we create an archive holding the first created archive
    invalid_archive = create_archive_with_archive(root_path, "invalid.tgz", archive)

    # we deposit it
    response = client.post(
        reverse(COL_IRI, args=[collection_name]),
        content_type="application/x-tar",
        data=invalid_archive["data"],
        CONTENT_LENGTH=invalid_archive["length"],
        HTTP_MD5SUM=invalid_archive["md5sum"],
        HTTP_SLUG="external-id",
        HTTP_IN_PROGRESS=False,
        HTTP_CONTENT_DISPOSITION="attachment; filename=%s" % (invalid_archive["name"],),
    )

    # then
    assert response.status_code == status.HTTP_201_CREATED
    response_content = parse_xml(response.content)
    deposit_status = response_content["swh:deposit_status"]
    assert deposit_status == DEPOSIT_STATUS_DEPOSITED
    deposit_id = int(response_content["swh:deposit_id"])

    deposit = Deposit.objects.get(pk=deposit_id)
    assert DEPOSIT_STATUS_DEPOSITED == deposit.status
    return deposit
