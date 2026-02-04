from typing import List
from pydantic import BaseModel, RootModel, ConfigDict, Field


class PatternObjectSchema(BaseModel):
    """
    Описание структуры шаблонного объекта для сущностей в моделе DeleteFilterSchema.

    Attributes:
        value: str
        mask: str
    """
    value: str | int
    mask: str | int


class VlansSchema(BaseModel):
    """
    Описание структуры объекта "vlans" в моделе DeleteFilterSchema.

    Attributes:
        vlan0: PatternObjectSchema
        vlan_last (vlanLast): PatternObjectSchema
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    vlan0: PatternObjectSchema
    vlan_last: PatternObjectSchema = Field(alias='vlanLast')


class EtherTypeSchema(BaseModel):
    """
    Описание структуры объекта "ether_type" в моделе DeleteFilterSchema.

    Attributes:
        ether_type (etherType): PatternObjectSchema
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    ether_type: PatternObjectSchema = Field(alias='etherType')


class CreateFilterSchema(BaseModel):
    """
    Описание структуры задания.
    Attributes:
        filtration_type: str
        logic_group: int
        new_ip_dst: str
        new_ip_dst_mask: int
        new_ip_src: str
        new_ip_src_mask: int
        new_ipv6_src: str
        new_ipv6_dst: str
        new_vlan0: int
        new_vlan_last: int
        new_ip_proto: str
        new_ipv6_proto: str
        new_ether_type: str
        new_mac_src: str
        new_mac_dst: str
        new_src_port: int
        new_dst_port: int
        new_tls_filtration_mask: bool
        new_tls_filtration: bool
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    filtration_type: str            = Field(alias='filtrationType', default="pass")
    logic_group: int                = Field(alias='logicGroup', default=1)
    new_ip_dst: str                 = Field(alias='newIpDst', default='1.1.1.1')
    new_ip_dst_mask: int            = Field(alias='newIpDstMask', default=32)
    new_ip_src: str                 = Field(alias='newIpSrc', default='2.2.2.2')
    new_ip_src_mask: int            = Field(alias='newIpSrcMask', default=32)
    new_ipv6_src: str               = Field(alias='newIpv6Src', default="1::f")
    new_ipv6_dst: str               = Field(alias='newIpv6Dst', default="1::f")
    new_vlan0: int                  = Field(alias='newVlan0', default=22)
    new_vlan_last: int              = Field(alias='newVlanLast', default=14)
    new_ip_proto: str               = Field(alias='newIpProto', default="6")
    new_ipv6_proto: str             = Field(alias='newIpv6Proto', default="b")
    new_ether_type: str             = Field(alias='newEtherType', default="0x8847")
    new_mac_src: str                = Field(alias='newMacSrc', default="001A3FF14CC6")
    new_mac_dst: str                = Field(alias='newMacDst', default="121314CCCCCC")
    new_src_port: int               = Field(alias='newSrcPort', default=122)
    new_dst_port: int               = Field(alias='newDstPort', default=80)
    new_tls_filtration_mask: bool   = Field(alias='newTLSFiltrationMask', default=False)
    new_tls_filtration: bool        = Field(alias='newTLSFiltration', default=False)


class DeleteFilterSchema(BaseModel):
    """
    Описание структуры задания.
    Attributes:
        hdr_ethernet_dst_addr: PatternObjectSchema
        hdr_ethernet_src_addr: PatternObjectSchema
        ig_md_dst_addr: PatternObjectSchema
        ig_md_dst_port: PatternObjectSchema
        ig_md_protocol: PatternObjectSchema
        ig_md_src_addr: PatternObjectSchema
        ig_md_src_port: PatternObjectSchema
        logic_group: int
        filtration_type: str
        analyze_port: None
        vlans: VlansSchema
        ether_type: EtherTypeSchema

    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    hdr_ethernet_dst_addr: PatternObjectSchema  = Field(alias='hdr.ethernet.dst_addr')
    hdr_ethernet_src_addr: PatternObjectSchema  = Field(alias='hdr.ethernet.src_addr')
    ig_md_dst_addr: PatternObjectSchema         = Field(alias='ig_md.dst_addr')
    ig_md_dst_port: PatternObjectSchema         = Field(alias='ig_md.dst_port')
    ig_md_protocol: PatternObjectSchema         = Field(alias='ig_md.protocol')
    ig_md_src_addr: PatternObjectSchema         = Field(alias='ig_md.src_addr')
    ig_md_src_port: PatternObjectSchema         = Field(alias='ig_md.src_port')
    logic_group: int                            = Field(alias='logicGroup')
    filtration_type: str                        = Field(alias='filtrationType')
    analyze_port: None                          = Field(alias='analyzePort')
    vlans: VlansSchema
    ether_type: EtherTypeSchema                 = Field(alias='etherType')



class CreateFiltersRequestSchema(RootModel):
    """
    Описание структуры запроса на добавление фильтров.
    List[CreateFilterSchema]
    """

    root: List[CreateFilterSchema]


class DeleteFiltersRequestSchema(RootModel):
    """
    Описание структуры запроса на удаление фильтров.
    List[DeleteFilterSchema]
    """
    root: List[DeleteFilterSchema]