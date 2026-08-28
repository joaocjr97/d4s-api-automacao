"""Steps de webhooks."""

from __future__ import annotations

from behave import then, when

from recursos.utils.assertions import assert_not_empty
from recursos.utils.config import Config


@when("eu adiciono um webhook ao documento configurado")
def adicionar_webhook(context) -> None:  # noqa: ANN001
    document_uuid = Config.UUID_DOC_WEBHOOK
    if not document_uuid:
        raise AssertionError("UUID_DOC_WEBHOOK não configurado no .env")

    response = context.webhooks_service.add(document_uuid, Config.URL_WEBHOOK)
    context.response = response
    context.response_json = response.json()


@when("eu consulto o webhook cadastrado no documento")
def consultar_webhook_cadastrado(context) -> None:  # noqa: ANN001
    document_uuid = Config.UUID_DOC_WEBHOOK
    if not document_uuid:
        raise AssertionError("UUID_DOC_WEBHOOK não configurado no .env")

    response = context.webhooks_service.list(document_uuid)
    context.response = response
    context.response_json = response.json()


@then("o webhook retornado deve refletir a url cadastrada")
def validar_webhook_cadastrado(context) -> None:  # noqa: ANN001
    payload = context.response_json or context.response.json()
    assert_not_empty(payload, message="JSON do webhook")

    # A API retorna ora um objeto único, ora uma lista de webhooks cadastrados.
    webhooks = payload if isinstance(payload, list) else [payload]
    assert_not_empty(webhooks, message="lista de webhooks")

    urls = [item.get("webhook_url") for item in webhooks if isinstance(item, dict)]
    if Config.URL_WEBHOOK not in urls:
        raise AssertionError(
            f"webhook_url {Config.URL_WEBHOOK!r} não encontrada na resposta: {urls!r}"
        )
