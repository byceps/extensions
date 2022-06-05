"""
byceps.blueprints.admin.shop.order.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2014-2022 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from flask import Response

from .....services.shop.order.export import service as order_export_service


# -------------------------------------------------------------------- #
# export


@blueprint.get('/<uuid:order_id>/export')
@permission_required('shop_order.view')
def export(order_id):
    """Export the order as an XML document."""
    xml_export = order_export_service.export_order_as_xml(order_id)

    if xml_export is None:
        abort(404)

    return Response(
        xml_export['content'], content_type=xml_export['content_type']
    )


# -------------------------------------------------------------------- #
