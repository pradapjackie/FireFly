from lxml import etree
from zeep.xsd import Element

# noinspection PyProtectedMember
from zeep.xsd.const import NotSet, _StaticIdentity, xsi_ns


def patched_render_value_item(self, parent, value, render_path):
    """Render the value on the parent lxml.Element"""
    if isinstance(value, _StaticIdentity) and value.__value__ == "Nil":
        elm = etree.SubElement(parent, self.qname)
        elm.set(xsi_ns("nil"), "true")
        return

    if value is None or value is NotSet:
        if self.is_optional:
            return

        elm = etree.SubElement(parent, self.qname)
        if self.nillable:
            elm.set(xsi_ns("nil"), "true")
        return

    node = etree.SubElement(parent, self.qname)
    xsd_type = getattr(value, "_xsd_type", self.type)

    if xsd_type != self.type:
        # noinspection PyProtectedMember
        return value._xsd_type.render(node, value, xsd_type, render_path)
    return self.type.render(node, value, None, render_path)


Element._render_value_item = patched_render_value_item
