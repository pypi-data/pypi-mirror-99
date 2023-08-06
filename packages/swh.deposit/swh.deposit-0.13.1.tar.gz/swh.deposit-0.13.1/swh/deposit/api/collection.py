# Copyright (C) 2017-2020  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import Optional, Tuple

from rest_framework import status

from ..config import DEPOSIT_STATUS_LOAD_SUCCESS, EDIT_IRI
from ..models import Deposit
from ..parsers import (
    SWHAtomEntryParser,
    SWHFileUploadTarParser,
    SWHFileUploadZipParser,
    SWHMultiPartParser,
)
from .common import (
    ACCEPT_ARCHIVE_CONTENT_TYPES,
    APIPost,
    ParsedRequestHeaders,
    Receipt,
    get_collection_by_name,
)


class CollectionAPI(APIPost):
    """Deposit request class defining api endpoints for sword deposit.

    What's known as 'Col-IRI' in the sword specification.

    HTTP verbs supported: POST

    """

    parser_classes = (
        SWHMultiPartParser,
        SWHFileUploadZipParser,
        SWHFileUploadTarParser,
        SWHAtomEntryParser,
    )

    def process_post(
        self,
        req,
        headers: ParsedRequestHeaders,
        collection_name: str,
        deposit: Optional[Deposit] = None,
    ) -> Tuple[int, str, Receipt]:
        """Create a first deposit as:
        - archive deposit (1 zip)
        - multipart (1 zip + 1 atom entry)
        - atom entry

        Args:
            req (Request): the request holding the information to parse
                and inject in db
            collection_name (str): the associated client

        Returns:
            An http response (HttpResponse) according to the situation.

            If everything is ok, a 201 response (created) with a
            deposit receipt.

        Raises:
            - archive deposit:
                - 400 (bad request) if the request is not providing an external
                  identifier
                - 403 (forbidden) if the length of the archive exceeds the
                  max size configured
                - 412 (precondition failed) if the length or hash provided
                  mismatch the reality of the archive.
                - 415 (unsupported media type) if a wrong media type is
                  provided

            - multipart deposit:
                - 400 (bad request) if the request is not providing an external
                  identifier
                - 412 (precondition failed) if the potentially md5 hash
                  provided mismatch the reality of the archive
                - 415 (unsupported media type) if a wrong media type is
                  provided

            - Atom entry deposit:
                - 400 (bad request) if the request is not providing an external
                  identifier
                - 400 (bad request) if the request's body is empty
                - 415 (unsupported media type) if a wrong media type is
                  provided

        """
        assert deposit is None

        deposit = self._deposit_create(req, collection_name, external_id=headers.slug)

        if req.content_type in ACCEPT_ARCHIVE_CONTENT_TYPES:
            receipt = self._binary_upload(req, headers, collection_name, deposit)
        elif req.content_type.startswith("multipart/"):
            receipt = self._multipart_upload(req, headers, collection_name, deposit)
        else:
            receipt = self._atom_entry(req, headers, collection_name, deposit)

        return status.HTTP_201_CREATED, EDIT_IRI, receipt

    def _deposit_create(
        self, request, collection_name: str, external_id: Optional[str]
    ) -> Deposit:
        collection = get_collection_by_name(collection_name)
        client = self.get_client(request)
        deposit_parent: Optional[Deposit] = None

        if external_id:
            # TODO: delete this when clients stopped relying on the slug
            try:
                # find a deposit parent (same external id, status load to success)
                deposit_parent = (
                    Deposit.objects.filter(
                        client=client,
                        external_id=external_id,
                        status=DEPOSIT_STATUS_LOAD_SUCCESS,
                    )
                    .order_by("-id")[0:1]
                    .get()
                )
            except Deposit.DoesNotExist:
                # then no parent for that deposit, deposit_parent already None
                pass

        return Deposit(
            collection=collection,
            external_id=external_id or "",
            client=client,
            parent=deposit_parent,
        )
