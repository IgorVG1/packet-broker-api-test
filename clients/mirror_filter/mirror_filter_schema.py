from typing import List, Optional

from pydantic import BaseModel, RootModel, Field, ConfigDict


class IgMdSchema(BaseModel):
    """
    Описание структуры pydantic-model ipv4.
    Attributes:
        value: str
        mask: str
    """
    value: str
    mask: str


class GetMirrorFilterSchema(BaseModel):
    """
    Описание структуры pydantic-model правила фильтрации зеркалирования при получении от сервера.
    Attributes:
        ig_md_dst_addr (ig_md.dst_addr): IgMdSchema
        ig_md_src_addr (ig_md.src_addr): IgMdSchema
        ingress_group (ingressGroup): int
        dest_num: int
        mirror_group (mirrorGroup): int
        traffic_type (trafficType): int
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    ig_md_dst_addr: Optional[IgMdSchema]    = Field(default=None, alias='ig_md.dst_addr')
    ig_md_src_addr: Optional[IgMdSchema]    = Field(default=None, alias='ig_md.src_addr')
    ingress_group: int | None               = Field(alias='ingressGroup')
    dest_num: int | None
    mirror_group: int | None                = Field(alias='mirrorGroup')
    traffic_type: int | None                = Field(alias='trafficType')


class CreateMirrorFilterSchema(BaseModel):
    """
    Описание структуры pydantic-model правила фильтрации зеркалирования при отправке на сервер в запросе на добавление.
    Attributes:
        dest_num (destNum): int
        mirror_group (mirrorGroup): int
        ingress_group (ingressGroup): int
        traffic_type (trafficType): int
        new_dst_port (newDstPort): str
        new_ip_dst (newIpDst): str
        new_ip_dst_mask (newIpDstMask): int
        new_ip_proto (newIpProto): str
        new_ip_src (newIpSrc): str
        new_ip_src_mask (newIpSrcMask): int
        new_ipv6_dst (newIpv6Dst): str
        new_ipv6_dst_mask (newIpv6DstMask): str
        new_ipv6_proto (newIpv6Proto): str
        new_ipv6_src (newIpv6Src): str
        new_ipv6_src_mask (newIpv6SrcMask): str
        new_src_port (newSrcPort): str
        new_traffic_type (newTrafficType): str
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    dest_num: int                   = Field(default=10, alias='destNum')
    mirror_group: int               = Field(default=1, alias='mirrorGroup')
    ingress_group: int              = Field(default=1, alias='ingressGroup')
    traffic_type: int               = Field(default=0, alias='trafficType')
    new_dst_port: str | None        = Field(default=None, alias='newDstPort')
    new_ip_dst: str                 = Field(default="2.2.2.2", alias='newIpDst')
    new_ip_dst_mask: int            = Field(default=32, alias='newIpDstMask')
    new_ip_proto: str | None        = Field(default=None, alias='newIpProto')
    new_ip_src: str                 = Field(default="1.1.1.1", alias='newIpSrc')
    new_ip_src_mask: int            = Field(default=32, alias='newIpSrcMask')
    new_ipv6_dst: str | None        = Field(default=None, alias='newIpv6Dst')
    new_ipv6_dst_mask: str | None   = Field(default=None, alias='newIpv6DstMask')
    new_ipv6_proto: str | None      = Field(default=None, alias='newIpv6Proto')
    new_ipv6_src: str | None        = Field(default=None, alias='newIpv6Src')
    new_ipv6_src_mask: str | None   = Field(default=None, alias='newIpv6SrcMask')
    new_src_port: str | None        = Field(default=None, alias='newSrcPort')
    new_traffic_type: str | None    = Field(default=None, alias='newTrafficType')


class DeleteMirrorFilterSchema(BaseModel):
    """
    Описание структуры pydantic-model правила фильтрации зеркалирования при отправке на сервер в запросе на удаление.
    Attributes:
        ig_md_dst_addr (ig_md.dst_addr): IgMdSchema
        ig_md_src_addr (ig_md.src_addr): IgMdSchema
        dest_num (destNum): int
        mirror_group (mirrorGroup): int
        ingress_group (ingressGroup): int
        traffic_type (trafficType): int
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    ig_md_dst_addr: IgMdSchema  = Field(default=IgMdSchema(value='2.2.2.2',
                                                           mask='255.255.255.255 /32'),
                                        alias='ig_md.dst_addr')
    ig_md_src_addr: IgMdSchema  = Field(default=IgMdSchema(value='1.1.1.1',
                                                           mask='255.255.255.255 /32'),
                                        alias='ig_md.src_addr')
    dest_num: int               = Field(default=10, alias='destNum')
    mirror_group: int           = Field(default=1, alias='mirrorGroup')
    ingress_group: int          = Field(default=1, alias='ingressGroup')
    traffic_type: int           = Field(default=0, alias='trafficType')


class GetPsfMirrorFilterSchema(BaseModel):
    """
    Описание структуры pydantic-model правила фильтрации зеркалирования PSF при получении от сервера.
    Attributes:
        ig_md_dst_addr (ig_md.dst_addr): IgMdSchema
        ig_md_src_addr (ig_md.src_addr): IgMdSchema
        ingress_group (ingressGroup): int
        dest_num: int
        mirror_group (mirrorGroup): int
        traffic_type (trafficType): int
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    ig_md_dst_addr: Optional[IgMdSchema]    = Field(default=None, alias='ig_md.dst_addr')
    ig_md_src_addr: Optional[IgMdSchema]    = Field(default=None, alias='ig_md.src_addr')
    ingress_group: int | None               = Field(alias='ingressGroup')
    dest_num: int | None
    mirror_group: int | None                = Field(alias='mirrorGroup')
    traffic_type: int | None                = Field(alias='trafficType')


class GetMirrorFilterListResponseSchema(RootModel):
    """
    Описание структуры ответа на получение списка правил фильтрации зеркалирования.
    Attributes:
        root: List[GetMirrorFilterSchema] - Список правил фильтрации зеркалирования.
    """
    root: List[GetMirrorFilterSchema]


class CreateMirrorFilterRequestSchema(RootModel):
    """
    Описание структуры запроса на добавление правил фильтрации зеркалирования.
    Attributes:
        root: List[CreateMirrorFilterSchema] - Список правил фильтрации зеркалирования.
    """
    root: List[CreateMirrorFilterSchema] = Field(default=[CreateMirrorFilterSchema()])


class DeleteMirrorFilterRequestSchema(RootModel):
    """
    Описание структуры запроса на добавление правил фильтрации зеркалирования.
    Attributes:
        root: List[DeleteMirrorFilterSchema] - Список правил фильтрации зеркалирования.
    """
    root: List[DeleteMirrorFilterSchema] = Field(default=[DeleteMirrorFilterSchema()])


class GetPsfMirrorFilterListResponseSchema(RootModel):
    """
    Описание структуры ответа на получение списка правил фильтрации зеркалирования PSF.
    Attributes:
        root: List[GetPsfMirrorFilterSchema] - Список правил фильтрации зеркалирования PSF.
    """
    root: List[GetPsfMirrorFilterSchema]