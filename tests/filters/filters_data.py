from clients.filters.filters_schema import DeleteFilterSchema, PatternObjectSchema, VlansSchema, EtherTypeSchema, \
    DeleteFiltersRequestSchema

FILTERS_FOR_DELETE = DeleteFiltersRequestSchema([DeleteFilterSchema(
    hdr_ethernet_dst_addr=PatternObjectSchema(
        value='12:13:14:cc:cc:cc',
        mask=281474976710655
    ),
    hdr_ethernet_src_addr=PatternObjectSchema(
        value='00:1a:3f:f1:4c:c6',
        mask=281474976710655
    ),
    ig_md_dst_addr=PatternObjectSchema(
        value='1.1.1.1',
        mask='255.255.255.255 /32'
    ),
    ig_md_dst_port=PatternObjectSchema(
        value=80,
        mask=65535
    ),
    ig_md_protocol=PatternObjectSchema(
        value=6,
        mask=255
    ),
    ig_md_src_addr=PatternObjectSchema(
        value='2.2.2.2',
        mask='255.255.255.255 /32'
    ),
    ig_md_src_port=PatternObjectSchema(
        value=122,
        mask=65535
    ),
    logic_group=1,
    filtration_type='pass',
    analyze_port=None,
    vlans=VlansSchema(
        vlan0=PatternObjectSchema(
            value=22,
            mask=4095
        ),
        vlanLast=PatternObjectSchema(
            value=14,
            mask=4095
        )
    ),
    ether_type=EtherTypeSchema(
        ether_type=PatternObjectSchema(
            value='0x8847',
            mask=65535
        )
    )
)])
"""
Тестовый объект для проверки удаления фильтров.
Все значения сущностей взяты согласно CreateFilterSchema()
"""

FILTERS_FOR_DELETE_JSON='[{"hdr.ethernet.dst_addr":{"value":"12:13:14:cc:cc:cc","mask":281474976710655},"hdr.ethernet.src_addr":{"value":"00:1a:3f:f1:4c:c6","mask":281474976710655},"ig_md.dst_addr":{"value":"1.1.1.1","mask":"255.255.255.255 /32"},"ig_md.dst_port":{"value":80,"mask":65535},"ig_md.protocol":{"value":6,"mask":255},"ig_md.src_addr":{"value":"2.2.2.2","mask":"255.255.255.255 /32"},"ig_md.src_port":{"value":122,"mask":65535},"logicGroup":1,"filtrationType":"pass","analyzePort":null,"vlans":{"vlan0":{"value":22,"mask":4095},"vlanLast":{"value":14,"mask":4095}},"etherType":{"etherType":{"value":"0x8847","mask":65535}}}]'