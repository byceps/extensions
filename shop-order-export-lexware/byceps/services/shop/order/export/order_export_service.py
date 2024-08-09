"""
byceps.services.shop.order.export.order_export_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2014-2024 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from datetime import datetime, UTC
from decimal import Decimal
from typing import Any
from zoneinfo import ZoneInfo

from flask import current_app

from byceps.services.shop.order import order_service
from byceps.services.shop.order.models.detailed_order import DetailedOrder
from byceps.services.shop.order.models.order import OrderID
from byceps.services.user import user_service
from byceps.util.templating import load_template


def export_order_as_xml(order_id: OrderID) -> dict[str, str] | None:
    """Export the order as an XML document."""
    order = order_service.find_order_with_details(order_id)

    if order is None:
        return None

    context = _assemble_context(order)
    xml = _render_template(context)

    return {
        'content': xml,
        'content_type': 'application/xml; charset=iso-8859-1',
    }


def _assemble_context(order: DetailedOrder) -> dict[str, Any]:
    """Assemble template context."""
    email_address = user_service.get_email_address(order.placed_by.id)

    now = datetime.utcnow()

    return {
        'order': order,
        'email_address': email_address,
        'line_items': order.line_items,
        'now': now,
        'format_export_amount': _format_export_amount,
        'format_export_datetime': _format_export_datetime,
    }


def _format_export_amount(amount: Decimal) -> str:
    """Format the monetary amount as required by the export format
    specification.
    """
    # Quantize to two decimal places.
    quantized = amount.quantize(Decimal('.00'))

    return f'{quantized:.2f}'


def _format_export_datetime(dt: datetime) -> str:
    """Format date and time as required by the export format specification."""
    export_tz = ZoneInfo(current_app.config['SHOP_ORDER_EXPORT_TIMEZONE'])
    dt_utc = dt.replace(tzinfo=UTC)
    dt_local = dt_utc.astimezone(export_tz)
    return dt_local.isoformat()


def _render_template(context: dict[str, Any]) -> str:
    """Load and render export template."""
    path = 'services/shop/order/export/templates/export.xml'
    with current_app.open_resource(path, 'r') as f:
        source = f.read()

    template = load_template(source)
    return template.render(**context)
