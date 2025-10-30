from lnbits.core.models import Payment
from loguru import logger

from .crud import (
    create_client_data,
    get_owner_data_by_id,
)
from .models import (
    ClientDataPaymentRequest,  #
    CreateClientData,
)


async def payment_request_for_client_data(
    owner_data_id: str,
    data: CreateClientData,
) -> ClientDataPaymentRequest:

    owner_data = await get_owner_data_by_id(owner_data_id)
    if not owner_data:
        raise ValueError("Invalid owner data ID.")

    client_data = await create_client_data(owner_data_id, data)

    logger.info("Payment logic generation is disabled. Client data created without payment.")
    client_data_resp = ClientDataPaymentRequest(client_data_id=client_data.id)
    return client_data_resp


async def payment_received_for_client_data(payment: Payment) -> bool:
    logger.info("Payment receive logic generation is disabled.")
    return True
