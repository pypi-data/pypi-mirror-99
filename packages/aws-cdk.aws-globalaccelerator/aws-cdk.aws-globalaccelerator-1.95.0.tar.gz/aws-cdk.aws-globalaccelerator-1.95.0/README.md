# AWS::GlobalAccelerator Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Introduction

AWS Global Accelerator (AGA) is a service that improves the availability and performance of your applications with local or global users. It provides static IP addresses that act as a fixed entry point to your application endpoints in a single or multiple AWS Regions, such as your Application Load Balancers, Network Load Balancers or Amazon EC2 instances.

This module supports features under [AWS Global Accelerator](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_GlobalAccelerator.html) that allows users set up resources using the `@aws-cdk/aws-globalaccelerator` module.

## Accelerator

The `Accelerator` resource is a Global Accelerator resource type that contains information about how you create an accelerator. An accelerator includes one or more listeners that process inbound connections and direct traffic to one or more endpoint groups, each of which includes endpoints, such as Application Load Balancers, Network Load Balancers, and Amazon EC2 instances.

To create the `Accelerator`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_globalaccelerator as globalaccelerator

globalaccelerator.Accelerator(stack, "Accelerator")
```

## Listener

The `Listener` resource is a Global Accelerator resource type that contains information about how you create a listener to process inbound connections from clients to an accelerator. Connections arrive to assigned static IP addresses on a port, port range, or list of port ranges that you specify.

To create the `Listener` listening on TCP 80:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
globalaccelerator.Listener(stack, "Listener",
    accelerator=accelerator,
    port_ranges=[{
        "from_port": 80,
        "to_port": 80
    }
    ]
)
```

## EndpointGroup

The `EndpointGroup` resource is a Global Accelerator resource type that contains information about how you create an endpoint group for the specified listener. An endpoint group is a collection of endpoints in one AWS Region.

To create the `EndpointGroup`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
globalaccelerator.EndpointGroup(stack, "Group", listener=listener)
```

## Add Endpoint into EndpointGroup

You may use the following methods to add endpoints into the `EndpointGroup`:

* `addEndpoint` to add a generic `endpoint` into the `EndpointGroup`.
* `addLoadBalancer` to add an Application Load Balancer or Network Load Balancer.
* `addEc2Instance` to add an EC2 Instance.
* `addElasticIpAddress` to add an Elastic IP Address.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
endpoint_group = globalaccelerator.EndpointGroup(stack, "Group", listener=listener)
alb = elbv2.ApplicationLoadBalancer(stack, "ALB", vpc=vpc, internet_facing=True)
nlb = elbv2.NetworkLoadBalancer(stack, "NLB", vpc=vpc, internet_facing=True)
eip = ec2.CfnEIP(stack, "ElasticIpAddress")
instances = Array()for ( let i = 0; i < 2; i++) {
  instances.push(new ec2.Instance(stack, `Instance${i}`, {
    vpc,
    machineImage: new ec2.AmazonLinuxImage(),
    instanceType: new ec2.InstanceType('t3.small'),
  }));
}

endpoint_group.add_load_balancer("AlbEndpoint", alb)
endpoint_group.add_load_balancer("NlbEndpoint", nlb)
endpoint_group.add_elastic_ip_address("EipEndpoint", eip)
endpoint_group.add_ec2_instance("InstanceEndpoint", instances[0])
endpoint_group.add_endpoint("InstanceEndpoint2", instances[1].instance_id)
```

## Accelerator Security Groups

When using certain AGA features (client IP address preservation), AGA creates elastic network interfaces (ENI) in your AWS account which are
associated with a Security Group, and which are reused for all AGAs associated with that VPC. Per the
[best practices](https://docs.aws.amazon.com/global-accelerator/latest/dg/best-practices-aga.html) page, AGA creates a specific security group
called `GlobalAccelerator` for each VPC it has an ENI in. You can use the security group created by AGA as a source group in other security
groups, such as those for EC2 instances or Elastic Load Balancers, in order to implement least-privilege security group rules.

CloudFormation doesn't support referencing the security group created by AGA. CDK has a library that enables you to reference the AGA security group
for a VPC using an AwsCustomResource.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
vpc = Vpc(stack, "VPC")
alb = elbv2.ApplicationLoadBalancer(stack, "ALB", vpc=vpc, internet_facing=False)
accelerator = ga.Accelerator(stack, "Accelerator")
listener = ga.Listener(stack, "Listener",
    accelerator=accelerator,
    port_ranges=[{
        "from_port": 443,
        "to_port": 443
    }
    ]
)
endpoint_group = ga.EndpointGroup(stack, "Group", listener=listener)
endpoint_group.add_load_balancer("AlbEndpoint", alb)

# Remember that there is only one AGA security group per VPC.
# This code will fail at CloudFormation deployment time if you do not have an AGA
aga_sg = ga.AcceleratorSecurityGroup.from_vpc(stack, "GlobalAcceleratorSG", vpc)

# Allow connections from the AGA to the ALB
alb.connections.allow_from(aga_sg, Port.tcp(443))
```
