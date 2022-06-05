Order Export for Lexware
========================

Export shop orders as `openTrans <https://www.opentrans.de/>`_ XML so
they can be imported into Lexware.

This extension consists of a dedicated service and a view function.


Installation
------------

- Copy the path ``byceps/services/shop/order/export`` to
  ``byceps/services/shop/order`` in your BYCEPS installation.
- Copy the code (imports, view function) from
  ``byceps/blueprints/admin/shop/order/views.py`` and add it to the file
  of the same name and in the path in your BYCEPS installation.
- Add the following line to the dropdown menu in
  ``byceps/blueprints/admin/shop/order/templates/admin/shop/order/_view_actions.html``
  (currently after line 7, but that may change):

  .. code:: jinja

      <li><a class="dropdown-item" href="{{ url_for('.export', order_id=order.id) }}" download="{{ order.order_number }}.xml">{{ render_icon('download') }} {{ _('Export for Lexware (XML)') }}</a></li>

- Finally, restart the application.

If successful, you should see a new item to export the order in the
actions dropdown of the single order view in the shop administration.
After selecting it, an XML file should be offered for download.
