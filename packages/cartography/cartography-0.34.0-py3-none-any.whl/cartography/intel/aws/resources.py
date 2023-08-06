from typing import Dict

from . import apigateway
from . import dynamodb
from . import ecr
from . import eks
from . import elasticache
from . import elasticsearch
from . import emr
from . import iam
from . import kms
from . import lambda_function
from . import permission_relationships
from . import rds
from . import redshift
from . import resourcegroupstaggingapi
from . import route53
from . import s3
from .ec2.auto_scaling_groups import sync_ec2_auto_scaling_groups
from .ec2.instances import sync_ec2_instances
from .ec2.internet_gateways import sync_internet_gateways
from .ec2.key_pairs import sync_ec2_key_pairs
from .ec2.load_balancer_v2s import sync_load_balancer_v2s
from .ec2.load_balancers import sync_load_balancers
from .ec2.network_interfaces import sync_network_interfaces
from .ec2.security_groups import sync_ec2_security_groupinfo
from .ec2.subnets import sync_subnets
from .ec2.tgw import sync_transit_gateways
from .ec2.vpc import sync_vpc
from .ec2.vpc_peerings import sync_vpc_peerings

RESOURCE_FUNCTIONS: Dict = {
    'iam': iam.sync,
    's3': s3.sync,
    'dynamodb': dynamodb.sync,
    'ec2:autoscalinggroup': sync_ec2_auto_scaling_groups,
    'ec2:instance': sync_ec2_instances,
    'ec2:keypair': sync_ec2_key_pairs,
    'ec2:load_balancer': sync_load_balancers,
    'ec2:load_balancer_v2': sync_load_balancer_v2s,
    'ec2:network_interface': sync_network_interfaces,
    'ec2:security_group': sync_ec2_security_groupinfo,
    'ec2:subnet': sync_subnets,
    'ec2:tgw': sync_transit_gateways,
    'ec2:vpc': sync_vpc,
    'ec2:vpc_peering': sync_vpc_peerings,
    'ec2:internet_gateway': sync_internet_gateways,
    'ecr': ecr.sync,
    'eks': eks.sync,
    'elasticache': elasticache.sync,
    'emr': emr.sync,
    'lambda_function': lambda_function.sync,
    'kms': kms.sync,
    'rds': rds.sync,
    'redshift': redshift.sync,
    'route53': route53.sync,
    'elasticsearch': elasticsearch.sync,
    'permission_relationships': permission_relationships.sync,
    'resourcegroupstaggingapi': resourcegroupstaggingapi.sync,
    'apigateway': apigateway.sync,
}
