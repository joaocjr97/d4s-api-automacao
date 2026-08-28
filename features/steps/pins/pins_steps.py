"""Steps de pins."""

from __future__ import annotations

from behave import then, when

from recursos.utils.assertions import assert_not_empty, assert_status
from recursos.utils.config import Config


def _pin_dict(email: str, position_x: int, position_y: int, pin_type: int, document_uuid: str) -> dict:
    return {
        "document": document_uuid,
        "email": email,
        "page_width": Config.PAGE_WIDTH,
        "page_height": Config.PAGE_HEIGHT,
        "page": Config.PAGE,
        "position_x": position_x,
        "position_y": position_y,
        "type": pin_type,
    }


def _remove_pin_dict(email: str, position_x: int, position_y: int) -> dict:
    return {
        "email": email,
        "page": Config.PAGE,
        "position_x": position_x,
        "position_y": position_y,
    }


@when("eu adiciono pins de assinatura, rubrica e selo ao documento")
def adicionar_pins(context) -> None:  # noqa: ANN001
    document_uuid = context.document_uuid
    if not document_uuid:
        raise AssertionError("document_uuid ausente")

    email = getattr(context, "signer_email", None) or Config.EMAIL_TESTE
    pins_defs = (Config.PIN_SIGNATURE, Config.PIN_RUBRIC, Config.PIN_SEAL)
    last_response = None
    for pos_x, pos_y, pin_type in pins_defs:
        pin = _pin_dict(email, pos_x, pos_y, pin_type, document_uuid)
        last_response = context.pins_service.add_pins(document_uuid, [pin])
        assert_status(last_response, 200)

    context.response = last_response
    context.response_json = last_response.json() if last_response else None


@when("eu replico um pin em todas as páginas do documento")
def replicar_pin(context) -> None:  # noqa: ANN001
    document_uuid = context.document_uuid
    if not document_uuid:
        raise AssertionError("document_uuid ausente")

    email = getattr(context, "signer_email", None) or Config.EMAIL_TESTE
    pos_x, pos_y, pin_type = Config.PIN_SIGNATURE
    pin = {
        "email": email,
        "page_height": Config.PAGE_HEIGHT,
        "page_width": Config.PAGE_WIDTH,
        "position_x": pos_x,
        "position_y": pos_y,
        "type": pin_type,
    }
    response = context.pins_service.add_pins_with_replicas(document_uuid, pin)
    context.response = response
    context.response_json = response.json()


@when("eu consulto os pins cadastrados no documento")
def consultar_pins_cadastrados(context) -> None:  # noqa: ANN001
    document_uuid = context.document_uuid
    if not document_uuid:
        raise AssertionError("document_uuid ausente")

    response = context.pins_service.list_pins(document_uuid)
    context.response = response
    context.response_json = response.json()


@then("a lista de pins deve conter os pins cadastrados no documento")
def validar_pins_cadastrados(context) -> None:  # noqa: ANN001
    payload = context.response_json or context.response.json()
    assert_not_empty(payload, message="JSON de pins")
    pins = payload.get("pins") if isinstance(payload, dict) else None
    assert_not_empty(pins, message="lista pins")

    email = getattr(context, "signer_email", None) or Config.EMAIL_TESTE
    esperados = (Config.PIN_SIGNATURE, Config.PIN_RUBRIC, Config.PIN_SEAL)
    for pos_x, pos_y, _pin_type in esperados:
        encontrado = any(
            pin.get("email") == email
            and int(pin.get("position_x")) == pos_x
            and int(pin.get("position_y")) == pos_y
            for pin in pins
        )
        if not encontrado:
            raise AssertionError(
                "Pin não encontrado na listagem: "
                f"email={email}, position_x={pos_x}, position_y={pos_y}. "
                f"Pins retornados: {pins!r}"
            )


@when("eu removo os pins cadastrados do documento")
def remover_pins_cadastrados(context) -> None:  # noqa: ANN001
    document_uuid = context.document_uuid
    if not document_uuid:
        raise AssertionError("document_uuid ausente")

    email = getattr(context, "signer_email", None) or Config.EMAIL_TESTE
    pins_defs = (Config.PIN_SIGNATURE, Config.PIN_RUBRIC, Config.PIN_SEAL)
    pins_to_remove = [
        _remove_pin_dict(email, pos_x, pos_y) for pos_x, pos_y, _pin_type in pins_defs
    ]
    response = context.pins_service.remove_pins(document_uuid, pins_to_remove)
    context.response = response
    context.response_json = response.json()


@then("os pins removidos não devem mais aparecer na listagem do documento")
def validar_pins_removidos(context) -> None:  # noqa: ANN001
    document_uuid = context.document_uuid
    if not document_uuid:
        raise AssertionError("document_uuid ausente")

    response = context.pins_service.list_pins(document_uuid)
    payload = response.json()
    pins = (payload.get("pins") if isinstance(payload, dict) else None) or []

    email = getattr(context, "signer_email", None) or Config.EMAIL_TESTE
    esperados = (Config.PIN_SIGNATURE, Config.PIN_RUBRIC, Config.PIN_SEAL)
    for pos_x, pos_y, _pin_type in esperados:
        ainda_presente = any(
            pin.get("email") == email
            and int(pin.get("position_x")) == pos_x
            and int(pin.get("position_y")) == pos_y
            for pin in pins
        )
        if ainda_presente:
            raise AssertionError(
                "Pin removido ainda aparece na listagem: "
                f"email={email}, position_x={pos_x}, position_y={pos_y}. "
                f"Pins retornados: {pins!r}"
            )
