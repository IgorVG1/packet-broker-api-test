import json

NODES_CONFIG_STRING = \
'{"nodes":[{"id":"ingress-1","type":"ingress","data":{"ports":[],"logicGroup":["selection-1"],"counter":0},"position":{"x":0,"y":0}},{"id":"selection-1","type":"selection","data":{"ingressGroup":"ingress-1","filter":{"ipProtocol":null,"srcPort":null,"dstPort":null,"trafficType":0},"matchPriority":0,"counter":0},"position":{"x":300,"y":0}},{"id":"balancing-1","type":"balancing","data":{"logicGroup":"selection-1","balancingType":null},"position":{"x":700,"y":0}},{"id":"filtration-1","type":"filtration","data":{"logicGroup":"selection-1","counter":0},"position":{"x":1250,"y":0}},{"id":"egress-1","type":"egress","data":{"ports":[],"logicGroup":"selection-1","counter":0},"position":{"x":1600,"y":0}},{"id":"mirroring-1","type":"mirror","data":{"ports":[],"ingressGroup":"ingress-1","priority":0},"position":{"x":300,"y":350}},{"id":"unknown-1","type":"unknown","data":{"ports":[],"ingressGroup":"ingress-1","counter":0},"position":{"x":300,"y":600}}],"edges":[],"position":[250,25],"zoom":0.6,"viewport":{"x":250,"y":25,"zoom":0.6}}'

NODES_CONFIG_JSON = \
json.loads(NODES_CONFIG_STRING)