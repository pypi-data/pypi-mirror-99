'''
# AWS App Mesh Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Developer Preview](https://img.shields.io/badge/cdk--constructs-developer--preview-informational.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are in **developer preview** before they
> become stable. We will only make breaking changes to address unforeseen API issues. Therefore,
> these APIs are not subject to [Semantic Versioning](https://semver.org/), and breaking changes
> will be announced in release notes. This means that while you may use them, you may need to
> update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

AWS App Mesh is a service mesh based on the [Envoy](https://www.envoyproxy.io/) proxy that makes it easy to monitor and control microservices. App Mesh standardizes how your microservices communicate, giving you end-to-end visibility and helping to ensure high-availability for your applications.

App Mesh gives you consistent visibility and network traffic controls for every microservice in an application.

App Mesh supports microservice applications that use service discovery naming for their components. To use App Mesh, you must have an existing application running on AWS Fargate, Amazon ECS, Amazon EKS, Kubernetes on AWS, or Amazon EC2.

For futher information on **AWS AppMesh** visit the [AWS Docs for AppMesh](https://docs.aws.amazon.com/app-mesh/index.html).

## Create the App and Stack

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = cdk.App()
stack = cdk.Stack(app, "stack")
```

## Creating the Mesh

A service mesh is a logical boundary for network traffic between the services that reside within it.

After you create your service mesh, you can create virtual services, virtual nodes, virtual routers, and routes to distribute traffic between the applications in your mesh.

The following example creates the `AppMesh` service mesh with the default filter of `DROP_ALL`, see [docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-egressfilter.html) here for more info on egress filters.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
mesh = Mesh(stack, "AppMesh",
    mesh_name="myAwsmMesh"
)
```

The mesh can also be created with the "ALLOW_ALL" egress filter by overwritting the property.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
mesh = Mesh(stack, "AppMesh",
    mesh_name="myAwsmMesh",
    egress_filter=MeshFilterType.ALLOW_ALL
)
```

## Adding VirtualRouters

The *Mesh* needs *VirtualRouters* as logical units to route requests to *VirtualNodes*.

Virtual routers handle traffic for one or more virtual services within your mesh.
After you create a virtual router, you can create and associate routes to your virtual router that direct incoming requests to different virtual nodes.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
router = mesh.add_virtual_router("router",
    listeners=[appmesh.VirtualRouterListener.http(8080)]
)
```

The router can also be created using the constructor and passing in the mesh instead of calling the `addVirtualRouter()` method for the mesh.
The same pattern applies to all constructs within the appmesh library, for any mesh.addXZY method, a new constuctor can also be used.
This is particularly useful for cross stack resources are required.
Where creating the `mesh` as part of an infrastructure stack and creating the `resources` such as `nodes` is more useful to keep in the application stack.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
mesh = Mesh(stack, "AppMesh",
    mesh_name="myAwsmMesh",
    egress_filter=MeshFilterType.Allow_All
)

router = VirtualRouter(stack, "router",
    mesh=mesh, # notice that mesh is a required property when creating a router with a new statement
    listeners=[appmesh.VirtualRouterListener.http(8081)]
)
```

The *VirtualRouterListener* class provides an easy interface for defining new protocol specific listeners.
The `http()`, `http2()`, `grpc()` and `tcp()` methods are available for use.
They accept a single port parameter, that is used to define what port to match requests on.
The port parameter can be omitted, and it will default to port 8080.

## Adding VirtualService

A virtual service is an abstraction of a real service that is provided by a virtual node directly or indirectly by means of a virtual router. Dependent services call your virtual service by its virtualServiceName, and those requests are routed to the virtual node or virtual router that is specified as the provider for the virtual service.

We recommend that you use the service discovery name of the real service that you're targeting (such as `my-service.default.svc.cluster.local`).

When creating a virtual service:

* If you want the virtual service to spread traffic across multiple virtual nodes, specify a Virtual router.
* If you want the virtual service to reach a virtual node directly, without a virtual router, specify a Virtual node.

Adding a virtual router as the provider:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
appmesh.VirtualService("virtual-service",
    virtual_service_name="my-service.default.svc.cluster.local", # optional
    virtual_service_provider=appmesh.VirtualServiceProvider.virtual_router(router)
)
```

Adding a virtual node as the provider:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
appmesh.VirtualService("virtual-service",
    virtual_service_name="my-service.default.svc.cluster.local", # optional
    virtual_service_provider=appmesh.VirtualServiceProvider.virtual_node(node)
)
```

## Adding a VirtualNode

A `virtual node` acts as a logical pointer to a particular task group, such as an Amazon ECS service or a Kubernetes deployment.

When you create a `virtual node`, any inbound traffic that your `virtual node` expects should be specified as a listener. Any outbound traffic that your `virtual node` expects to reach should be specified as a backend.

The response metadata for your new `virtual node` contains the Amazon Resource Name (ARN) that is associated with the `virtual node`. Set this value (either the full ARN or the truncated resource name) as the APPMESH_VIRTUAL_NODE_NAME environment variable for your task group's Envoy proxy container in your task definition or pod spec. For example, the value could be mesh/default/virtualNode/simpleapp. This is then mapped to the node.id and node.cluster Envoy parameters.

> Note
> If you require your Envoy stats or tracing to use a different name, you can override the node.cluster value that is set by APPMESH_VIRTUAL_NODE_NAME with the APPMESH_VIRTUAL_NODE_CLUSTER environment variable.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
vpc = ec2.Vpc(stack, "vpc")
namespace = servicediscovery.PrivateDnsNamespace(self, "test-namespace",
    vpc=vpc,
    name="domain.local"
)
service = namespace.create_service("Svc")

node = mesh.add_virtual_node("virtual-node",
    service_discovery=appmesh.ServiceDiscovery.cloud_map(
        service=service
    ),
    listeners=[appmesh.VirtualNodeListener.http_node_listener(
        port=8081,
        health_check={
            "healthy_threshold": 3,
            "interval": Duration.seconds(5), # minimum
            "path": "/health-check-path",
            "port": 8080,
            "protocol": Protocol.HTTP,
            "timeout": Duration.seconds(2), # minimum
            "unhealthy_threshold": 2
        }
    )],
    access_log=appmesh.AccessLog.from_file_path("/dev/stdout")
)
```

Create a `VirtualNode` with the constructor and add tags.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
node = VirtualNode(self, "node",
    mesh=mesh,
    service_discovery=appmesh.ServiceDiscovery.cloud_map(
        service=service
    ),
    listeners=[appmesh.VirtualNodeListener.http_node_listener(
        port=8080,
        health_check={
            "healthy_threshold": 3,
            "interval": Duration.seconds(5), # min
            "path": "/ping",
            "port": 8080,
            "protocol": Protocol.HTTP,
            "timeout": Duration.seconds(2), # min
            "unhealthy_threshold": 2
        },
        timeout={
            "idle": cdk.Duration.seconds(5)
        }
    )],
    backend_defaults={
        "client_policy": appmesh.ClientPolicy.file_trust(
            certificate_chain="/keys/local_cert_chain.pem"
        )
    },
    access_log=appmesh.AccessLog.from_file_path("/dev/stdout")
)

cdk.Tag.add(node, "Environment", "Dev")
```

Create a `VirtualNode` with the constructor and add backend virtual service.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
node = VirtualNode(self, "node",
    mesh=mesh,
    service_discovery=appmesh.ServiceDiscovery.cloud_map(
        service=service
    ),
    listeners=[appmesh.VirtualNodeListener.http_node_listener(
        port=8080,
        health_check={
            "healthy_threshold": 3,
            "interval": Duration.seconds(5), # min
            "path": "/ping",
            "port": 8080,
            "protocol": Protocol.HTTP,
            "timeout": Duration.seconds(2), # min
            "unhealthy_threshold": 2
        },
        timeout={
            "idle": cdk.Duration.seconds(5)
        }
    )],
    access_log=appmesh.AccessLog.from_file_path("/dev/stdout")
)

virtual_service = appmesh.VirtualService(stack, "service-1",
    service_discovery=appmesh.ServiceDiscovery.dns("service1.domain.local"),
    mesh=mesh,
    client_policy=appmesh.ClientPolicy.file_trust(
        certificate_chain="/keys/local_cert_chain.pem",
        ports=[8080, 8081]
    )
)

node.add_backend(appmesh.Backend.virtual_service(virtual_service))
```

The `listeners` property can be left blank and added later with the `node.addListener()` method. The `healthcheck` and `timeout` properties are optional but if specifying a listener, the `port` must be added.

The `backends` property can be added with `node.addBackend()`. We define a virtual service and add it to the virtual node to allow egress traffic to other node.

The `backendDefaults` property are added to the node while creating the virtual node. These are virtual node's default settings for all backends.

## Adding TLS to a listener

The `tlsCertificate` property can be added to a Virtual Node listener or Virtual Gateway listener to add TLS configuration.
A certificate from AWS Certificate Manager can be incorporated or a customer provided certificate can be specified with a `certificateChain` path file and a `privateKey` file path.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_certificatemanager as certificatemanager

# A Virtual Node with listener TLS from an ACM provided certificate
cert = certificatemanager.Certificate(self, "cert", ...)

node = appmesh.VirtualNode(stack, "node",
    mesh=mesh,
    dns_host_name="node",
    listeners=[appmesh.VirtualNodeListener.grpc(
        port=80,
        tls_certificate=appmesh.TlsCertificate.acm(
            certificate=cert,
            tls_mode=TlsMode.STRICT
        )
    )]
)

# A Virtual Gateway with listener TLS from a customer provided file certificate
gateway = appmesh.VirtualGateway(self, "gateway",
    mesh=mesh,
    listeners=[appmesh.VirtualGatewayListener.grpc(
        port=8080,
        tls_certificate=appmesh.TlsCertificate.file(
            certificate_chain="path/to/certChain",
            private_key="path/to/privateKey",
            tls_mode=TlsMode.STRICT
        )
    )],
    virtual_gateway_name="gateway"
)
```

## Adding a Route

A `route` is associated with a virtual router, and it's used to match requests for a virtual router and distribute traffic accordingly to its associated virtual nodes.

If your `route` matches a request, you can distribute traffic to one or more target virtual nodes with relative weighting.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
router.add_route("route-http",
    route_spec=appmesh.RouteSpec.http(
        weighted_targets=[{
            "virtual_node": node
        }
        ],
        match={
            "prefix_path": "/path-to-app"
        }
    )
)
```

Add an HTTP2 route that matches based on method, scheme and header:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
router.add_route("route-http2",
    route_spec=appmesh.RouteSpec.http2(
        weighted_targets=[{
            "virtual_node": node
        }
        ],
        match={
            "prefix_path": "/",
            "method": appmesh.HttpRouteMatchMethod.POST,
            "protocol": appmesh.HttpRouteProtocol.HTTPS,
            "headers": [
                # All specified headers must match for the route to match.
                appmesh.HttpHeaderMatch.value_is("Content-Type", "application/json"),
                appmesh.HttpHeaderMatch.value_is_not("Content-Type", "application/json")
            ]
        }
    )
)
```

Add a single route with multiple targets and split traffic 50/50

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
router.add_route("route-http",
    route_spec=appmesh.RouteSpec.http(
        weighted_targets=[{
            "virtual_node": node,
            "weight": 50
        }, {
            "virtual_node": node,
            "weight": 50
        }
        ],
        match={
            "prefix_path": "/path-to-app"
        }
    )
)
```

Add an http2 route with retries:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
router.add_route("route-http2-retry",
    route_spec=appmesh.RouteSpec.http2(
        weighted_targets=[{"virtual_node": node}],
        retry_policy={
            # Retry if the connection failed
            "tcp_retry_events": [appmesh.TcpRetryEvent.CONNECTION_ERROR],
            # Retry if HTTP responds with a gateway error (502, 503, 504)
            "http_retry_events": [appmesh.HttpRetryEvent.GATEWAY_ERROR],
            # Retry five times
            "retry_attempts": 5,
            # Use a 1 second timeout per retry
            "retry_timeout": cdk.Duration.seconds(1)
        }
    )
)
```

Add a gRPC route with retries:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
router.add_route("route-grpc-retry",
    route_spec=appmesh.RouteSpec.grpc(
        weighted_targets=[{"virtual_node": node}],
        match={"service_name": "servicename"},
        retry_policy={
            "tcp_retry_events": [appmesh.TcpRetryEvent.CONNECTION_ERROR],
            "http_retry_events": [appmesh.HttpRetryEvent.GATEWAY_ERROR],
            # Retry if gRPC responds that the request was cancelled, a resource
            # was exhausted, or if the service is unavailable
            "grpc_retry_events": [appmesh.GrpcRetryEvent.CANCELLED, appmesh.GrpcRetryEvent.RESOURCE_EXHAUSTED, appmesh.GrpcRetryEvent.UNAVAILABLE
            ],
            "retry_attempts": 5,
            "retry_timeout": cdk.Duration.seconds(1)
        }
    )
)
```

The *RouteSpec* class provides an easy interface for defining new protocol specific route specs.
The `tcp()`, `http()` and `http2()` methods provide the spec necessary to define a protocol specific spec.

For HTTP based routes, the match field can be used to match on a route prefix.
By default, an HTTP based route will match on `/`. All matches must start with a leading `/`.
The timeout field can also be specified for `idle` and `perRequest` timeouts.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
router.add_route("route-http",
    route_spec=appmesh.RouteSpec.grpc(
        weighted_targets=[{
            "virtual_node": node
        }
        ],
        match={
            "service_name": "my-service.default.svc.cluster.local"
        },
        timeout={
            "idle": Duration.seconds(2),
            "per_request": Duration.seconds(1)
        }
    )
)
```

## Adding a Virtual Gateway

A *virtual gateway* allows resources outside your mesh to communicate to resources that are inside your mesh.
The virtual gateway represents an Envoy proxy running in an Amazon ECS task, in a Kubernetes service, or on an Amazon EC2 instance.
Unlike a virtual node, which represents an Envoy running with an application, a virtual gateway represents Envoy deployed by itself.

A virtual gateway is similar to a virtual node in that it has a listener that accepts traffic for a particular port and protocol (HTTP, HTTP2, GRPC).
The traffic that the virtual gateway receives, is directed to other services in your mesh,
using rules defined in gateway routes which can be added to your virtual gateway.

Create a virtual gateway with the constructor:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
certificate_authority_arn = "arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/12345678-1234-1234-1234-123456789012"

gateway = appmesh.VirtualGateway(stack, "gateway",
    mesh=mesh,
    listeners=[appmesh.VirtualGatewayListener.http(
        port=443,
        health_check={
            "interval": cdk.Duration.seconds(10)
        }
    )],
    backend_defaults={
        "client_policy": appmesh.ClientPolicy.acm_trust(
            certificate_authorities=[acmpca.CertificateAuthority.from_certificate_authority_arn(stack, "certificate", certificate_authority_arn)],
            ports=[8080, 8081]
        )
    },
    access_log=appmesh.AccessLog.from_file_path("/dev/stdout"),
    virtual_gateway_name="virtualGateway"
)
```

Add a virtual gateway directly to the mesh:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
gateway = mesh.add_virtual_gateway("gateway",
    access_log=appmesh.AccessLog.from_file_path("/dev/stdout"),
    virtual_gateway_name="virtualGateway",
    listeners=[appmesh.VirtualGatewayListener.http(
        port=443,
        health_check={
            "interval": cdk.Duration.seconds(10)
        }
    )]
)
```

The listeners field can be omitted which will default to an HTTP Listener on port 8080.
A gateway route can be added using the `gateway.addGatewayRoute()` method.

The `backendDefaults` property is added to the node while creating the virtual gateway. These are virtual gateway's default settings for all backends.

## Adding a Gateway Route

A *gateway route* is attached to a virtual gateway and routes traffic to an existing virtual service.
If a route matches a request, it can distribute traffic to a target virtual service.

For HTTP based routes, the match field can be used to match on a route prefix.
By default, an HTTP based route will match on `/`. All matches must start with a leading `/`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
gateway.add_gateway_route("gateway-route-http",
    route_spec=appmesh.GatewayRouteSpec.http(
        route_target=virtual_service,
        match={
            "prefix_match": "/"
        }
    )
)
```

For GRPC based routes, the match field can be used to match on service names.
You cannot omit the field, and must specify a match for these routes.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
gateway.add_gateway_route("gateway-route-grpc",
    route_spec=appmesh.GatewayRouteSpec.grpc(
        route_target=virtual_service,
        match={
            "service_name": "my-service.default.svc.cluster.local"
        }
    )
)
```

## Importing Resources

Each mesh resource comes with two static methods for importing a reference to an existing App Mesh resource.
These imported resources can be used as references for other resources in your mesh.
There are two static methods, `from<Resource>Arn` and `from<Resource>Attributes` where the `<Resource>` is replaced with the resource name.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
arn = "arn:aws:appmesh:us-east-1:123456789012:mesh/testMesh/virtualNode/testNode"
appmesh.VirtualNode.from_virtual_node_arn(stack, "importedVirtualNode", arn)
```

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
appmesh.VirtualNode.from_virtual_node_attributes(stack, "imported-virtual-node",
    mesh=appmesh.Mesh.from_mesh_name(stack, "Mesh", "testMesh"),
    virtual_node_name=virtual_node_name
)
```

To import a mesh, there are two static methods, `fromMeshArn` and `fromMeshName`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
arn = "arn:aws:appmesh:us-east-1:123456789012:mesh/testMesh"
appmesh.Mesh.from_mesh_arn(stack, "imported-mesh", arn)
```

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
appmesh.Mesh.from_mesh_name(stack, "imported-mesh", "abc")
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_acmpca
import aws_cdk.aws_certificatemanager
import aws_cdk.aws_servicediscovery
import aws_cdk.core
import constructs


class AccessLog(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-appmesh.AccessLog",
):
    '''(experimental) Configuration for Envoy Access logs for mesh endpoints.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_AccessLogProxy"]:
        return _AccessLogProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(AccessLog, self, [])

    @jsii.member(jsii_name="fromFilePath") # type: ignore[misc]
    @builtins.classmethod
    def from_file_path(cls, file_path: builtins.str) -> "AccessLog":
        '''(experimental) Path to a file to write access logs to.

        :param file_path: -

        :default: - no file based access logging

        :stability: experimental
        '''
        return typing.cast("AccessLog", jsii.sinvoke(cls, "fromFilePath", [file_path]))

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, scope: aws_cdk.core.Construct) -> "AccessLogConfig":
        '''(experimental) Called when the AccessLog type is initialized.

        Can be used to enforce
        mutual exclusivity with future properties

        :param scope: -

        :stability: experimental
        '''
        ...


class _AccessLogProxy(AccessLog):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> "AccessLogConfig":
        '''(experimental) Called when the AccessLog type is initialized.

        Can be used to enforce
        mutual exclusivity with future properties

        :param scope: -

        :stability: experimental
        '''
        return typing.cast("AccessLogConfig", jsii.invoke(self, "bind", [scope]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.AccessLogConfig",
    jsii_struct_bases=[],
    name_mapping={
        "virtual_gateway_access_log": "virtualGatewayAccessLog",
        "virtual_node_access_log": "virtualNodeAccessLog",
    },
)
class AccessLogConfig:
    def __init__(
        self,
        *,
        virtual_gateway_access_log: typing.Optional["CfnVirtualGateway.VirtualGatewayAccessLogProperty"] = None,
        virtual_node_access_log: typing.Optional["CfnVirtualNode.AccessLogProperty"] = None,
    ) -> None:
        '''(experimental) All Properties for Envoy Access logs for mesh endpoints.

        :param virtual_gateway_access_log: (experimental) VirtualGateway CFN configuration for Access Logging. Default: - no access logging
        :param virtual_node_access_log: (experimental) VirtualNode CFN configuration for Access Logging. Default: - no access logging

        :stability: experimental
        '''
        if isinstance(virtual_gateway_access_log, dict):
            virtual_gateway_access_log = CfnVirtualGateway.VirtualGatewayAccessLogProperty(**virtual_gateway_access_log)
        if isinstance(virtual_node_access_log, dict):
            virtual_node_access_log = CfnVirtualNode.AccessLogProperty(**virtual_node_access_log)
        self._values: typing.Dict[str, typing.Any] = {}
        if virtual_gateway_access_log is not None:
            self._values["virtual_gateway_access_log"] = virtual_gateway_access_log
        if virtual_node_access_log is not None:
            self._values["virtual_node_access_log"] = virtual_node_access_log

    @builtins.property
    def virtual_gateway_access_log(
        self,
    ) -> typing.Optional["CfnVirtualGateway.VirtualGatewayAccessLogProperty"]:
        '''(experimental) VirtualGateway CFN configuration for Access Logging.

        :default: - no access logging

        :stability: experimental
        '''
        result = self._values.get("virtual_gateway_access_log")
        return typing.cast(typing.Optional["CfnVirtualGateway.VirtualGatewayAccessLogProperty"], result)

    @builtins.property
    def virtual_node_access_log(
        self,
    ) -> typing.Optional["CfnVirtualNode.AccessLogProperty"]:
        '''(experimental) VirtualNode CFN configuration for Access Logging.

        :default: - no access logging

        :stability: experimental
        '''
        result = self._values.get("virtual_node_access_log")
        return typing.cast(typing.Optional["CfnVirtualNode.AccessLogProperty"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.AcmCertificateOptions",
    jsii_struct_bases=[],
    name_mapping={"certificate": "certificate", "tls_mode": "tlsMode"},
)
class AcmCertificateOptions:
    def __init__(
        self,
        *,
        certificate: aws_cdk.aws_certificatemanager.ICertificate,
        tls_mode: "TlsMode",
    ) -> None:
        '''(experimental) ACM Certificate Properties.

        :param certificate: (experimental) The ACM certificate.
        :param tls_mode: (experimental) The TLS mode.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "certificate": certificate,
            "tls_mode": tls_mode,
        }

    @builtins.property
    def certificate(self) -> aws_cdk.aws_certificatemanager.ICertificate:
        '''(experimental) The ACM certificate.

        :stability: experimental
        '''
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast(aws_cdk.aws_certificatemanager.ICertificate, result)

    @builtins.property
    def tls_mode(self) -> "TlsMode":
        '''(experimental) The TLS mode.

        :stability: experimental
        '''
        result = self._values.get("tls_mode")
        assert result is not None, "Required property 'tls_mode' is missing"
        return typing.cast("TlsMode", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcmCertificateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Backend(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-appmesh.Backend",
):
    '''(experimental) Contains static factory methods to create backends.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_BackendProxy"]:
        return _BackendProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(Backend, self, [])

    @jsii.member(jsii_name="virtualService") # type: ignore[misc]
    @builtins.classmethod
    def virtual_service(
        cls,
        virtual_service: "IVirtualService",
        *,
        client_policy: typing.Optional["ClientPolicy"] = None,
    ) -> "Backend":
        '''(experimental) Construct a Virtual Service backend.

        :param virtual_service: -
        :param client_policy: (experimental) Client policy for the backend. Default: none

        :stability: experimental
        '''
        props = VirtualServiceBackendOptions(client_policy=client_policy)

        return typing.cast("Backend", jsii.sinvoke(cls, "virtualService", [virtual_service, props]))

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, _scope: aws_cdk.core.Construct) -> "BackendConfig":
        '''(experimental) Return backend config.

        :param _scope: -

        :stability: experimental
        '''
        ...


class _BackendProxy(Backend):
    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct) -> "BackendConfig":
        '''(experimental) Return backend config.

        :param _scope: -

        :stability: experimental
        '''
        return typing.cast("BackendConfig", jsii.invoke(self, "bind", [_scope]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.BackendConfig",
    jsii_struct_bases=[],
    name_mapping={"virtual_service_backend": "virtualServiceBackend"},
)
class BackendConfig:
    def __init__(
        self,
        *,
        virtual_service_backend: "CfnVirtualNode.BackendProperty",
    ) -> None:
        '''(experimental) Properties for a backend.

        :param virtual_service_backend: (experimental) Config for a Virtual Service backend.

        :stability: experimental
        '''
        if isinstance(virtual_service_backend, dict):
            virtual_service_backend = CfnVirtualNode.BackendProperty(**virtual_service_backend)
        self._values: typing.Dict[str, typing.Any] = {
            "virtual_service_backend": virtual_service_backend,
        }

    @builtins.property
    def virtual_service_backend(self) -> "CfnVirtualNode.BackendProperty":
        '''(experimental) Config for a Virtual Service backend.

        :stability: experimental
        '''
        result = self._values.get("virtual_service_backend")
        assert result is not None, "Required property 'virtual_service_backend' is missing"
        return typing.cast("CfnVirtualNode.BackendProperty", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.BackendDefaults",
    jsii_struct_bases=[],
    name_mapping={"client_policy": "clientPolicy"},
)
class BackendDefaults:
    def __init__(
        self,
        *,
        client_policy: typing.Optional["ClientPolicy"] = None,
    ) -> None:
        '''(experimental) Represents the properties needed to define backend defaults.

        :param client_policy: (experimental) Client policy for backend defaults. Default: none

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if client_policy is not None:
            self._values["client_policy"] = client_policy

    @builtins.property
    def client_policy(self) -> typing.Optional["ClientPolicy"]:
        '''(experimental) Client policy for backend defaults.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("client_policy")
        return typing.cast(typing.Optional["ClientPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackendDefaults(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnGatewayRoute(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appmesh.CfnGatewayRoute",
):
    '''A CloudFormation ``AWS::AppMesh::GatewayRoute``.

    :cloudformationResource: AWS::AppMesh::GatewayRoute
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        mesh_name: builtins.str,
        spec: typing.Union["CfnGatewayRoute.GatewayRouteSpecProperty", aws_cdk.core.IResolvable],
        virtual_gateway_name: builtins.str,
        gateway_route_name: typing.Optional[builtins.str] = None,
        mesh_owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Create a new ``AWS::AppMesh::GatewayRoute``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param mesh_name: ``AWS::AppMesh::GatewayRoute.MeshName``.
        :param spec: ``AWS::AppMesh::GatewayRoute.Spec``.
        :param virtual_gateway_name: ``AWS::AppMesh::GatewayRoute.VirtualGatewayName``.
        :param gateway_route_name: ``AWS::AppMesh::GatewayRoute.GatewayRouteName``.
        :param mesh_owner: ``AWS::AppMesh::GatewayRoute.MeshOwner``.
        :param tags: ``AWS::AppMesh::GatewayRoute.Tags``.
        '''
        props = CfnGatewayRouteProps(
            mesh_name=mesh_name,
            spec=spec,
            virtual_gateway_name=virtual_gateway_name,
            gateway_route_name=gateway_route_name,
            mesh_owner=mesh_owner,
            tags=tags,
        )

        jsii.create(CfnGatewayRoute, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrGatewayRouteName")
    def attr_gateway_route_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: GatewayRouteName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrGatewayRouteName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrMeshName")
    def attr_mesh_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: MeshName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMeshName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrMeshOwner")
    def attr_mesh_owner(self) -> builtins.str:
        '''
        :cloudformationAttribute: MeshOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMeshOwner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrResourceOwner")
    def attr_resource_owner(self) -> builtins.str:
        '''
        :cloudformationAttribute: ResourceOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceOwner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrUid")
    def attr_uid(self) -> builtins.str:
        '''
        :cloudformationAttribute: Uid
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUid"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrVirtualGatewayName")
    def attr_virtual_gateway_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: VirtualGatewayName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVirtualGatewayName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::AppMesh::GatewayRoute.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> builtins.str:
        '''``AWS::AppMesh::GatewayRoute.MeshName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-meshname
        '''
        return typing.cast(builtins.str, jsii.get(self, "meshName"))

    @mesh_name.setter
    def mesh_name(self, value: builtins.str) -> None:
        jsii.set(self, "meshName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="spec")
    def spec(
        self,
    ) -> typing.Union["CfnGatewayRoute.GatewayRouteSpecProperty", aws_cdk.core.IResolvable]:
        '''``AWS::AppMesh::GatewayRoute.Spec``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-spec
        '''
        return typing.cast(typing.Union["CfnGatewayRoute.GatewayRouteSpecProperty", aws_cdk.core.IResolvable], jsii.get(self, "spec"))

    @spec.setter
    def spec(
        self,
        value: typing.Union["CfnGatewayRoute.GatewayRouteSpecProperty", aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "spec", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualGatewayName")
    def virtual_gateway_name(self) -> builtins.str:
        '''``AWS::AppMesh::GatewayRoute.VirtualGatewayName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-virtualgatewayname
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualGatewayName"))

    @virtual_gateway_name.setter
    def virtual_gateway_name(self, value: builtins.str) -> None:
        jsii.set(self, "virtualGatewayName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="gatewayRouteName")
    def gateway_route_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::GatewayRoute.GatewayRouteName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-gatewayroutename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayRouteName"))

    @gateway_route_name.setter
    def gateway_route_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "gatewayRouteName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshOwner")
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::GatewayRoute.MeshOwner``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-meshowner
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "meshOwner"))

    @mesh_owner.setter
    def mesh_owner(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "meshOwner", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnGatewayRoute.GatewayRouteSpecProperty",
        jsii_struct_bases=[],
        name_mapping={
            "grpc_route": "grpcRoute",
            "http2_route": "http2Route",
            "http_route": "httpRoute",
        },
    )
    class GatewayRouteSpecProperty:
        def __init__(
            self,
            *,
            grpc_route: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GrpcGatewayRouteProperty"]] = None,
            http2_route: typing.Optional[typing.Union["CfnGatewayRoute.HttpGatewayRouteProperty", aws_cdk.core.IResolvable]] = None,
            http_route: typing.Optional[typing.Union["CfnGatewayRoute.HttpGatewayRouteProperty", aws_cdk.core.IResolvable]] = None,
        ) -> None:
            '''
            :param grpc_route: ``CfnGatewayRoute.GatewayRouteSpecProperty.GrpcRoute``.
            :param http2_route: ``CfnGatewayRoute.GatewayRouteSpecProperty.Http2Route``.
            :param http_route: ``CfnGatewayRoute.GatewayRouteSpecProperty.HttpRoute``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutespec.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if grpc_route is not None:
                self._values["grpc_route"] = grpc_route
            if http2_route is not None:
                self._values["http2_route"] = http2_route
            if http_route is not None:
                self._values["http_route"] = http_route

        @builtins.property
        def grpc_route(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GrpcGatewayRouteProperty"]]:
            '''``CfnGatewayRoute.GatewayRouteSpecProperty.GrpcRoute``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutespec.html#cfn-appmesh-gatewayroute-gatewayroutespec-grpcroute
            '''
            result = self._values.get("grpc_route")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GrpcGatewayRouteProperty"]], result)

        @builtins.property
        def http2_route(
            self,
        ) -> typing.Optional[typing.Union["CfnGatewayRoute.HttpGatewayRouteProperty", aws_cdk.core.IResolvable]]:
            '''``CfnGatewayRoute.GatewayRouteSpecProperty.Http2Route``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutespec.html#cfn-appmesh-gatewayroute-gatewayroutespec-http2route
            '''
            result = self._values.get("http2_route")
            return typing.cast(typing.Optional[typing.Union["CfnGatewayRoute.HttpGatewayRouteProperty", aws_cdk.core.IResolvable]], result)

        @builtins.property
        def http_route(
            self,
        ) -> typing.Optional[typing.Union["CfnGatewayRoute.HttpGatewayRouteProperty", aws_cdk.core.IResolvable]]:
            '''``CfnGatewayRoute.GatewayRouteSpecProperty.HttpRoute``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutespec.html#cfn-appmesh-gatewayroute-gatewayroutespec-httproute
            '''
            result = self._values.get("http_route")
            return typing.cast(typing.Optional[typing.Union["CfnGatewayRoute.HttpGatewayRouteProperty", aws_cdk.core.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayRouteSpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnGatewayRoute.GatewayRouteTargetProperty",
        jsii_struct_bases=[],
        name_mapping={"virtual_service": "virtualService"},
    )
    class GatewayRouteTargetProperty:
        def __init__(
            self,
            *,
            virtual_service: typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GatewayRouteVirtualServiceProperty"],
        ) -> None:
            '''
            :param virtual_service: ``CfnGatewayRoute.GatewayRouteTargetProperty.VirtualService``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutetarget.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "virtual_service": virtual_service,
            }

        @builtins.property
        def virtual_service(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GatewayRouteVirtualServiceProperty"]:
            '''``CfnGatewayRoute.GatewayRouteTargetProperty.VirtualService``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutetarget.html#cfn-appmesh-gatewayroute-gatewayroutetarget-virtualservice
            '''
            result = self._values.get("virtual_service")
            assert result is not None, "Required property 'virtual_service' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GatewayRouteVirtualServiceProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayRouteTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnGatewayRoute.GatewayRouteVirtualServiceProperty",
        jsii_struct_bases=[],
        name_mapping={"virtual_service_name": "virtualServiceName"},
    )
    class GatewayRouteVirtualServiceProperty:
        def __init__(self, *, virtual_service_name: builtins.str) -> None:
            '''
            :param virtual_service_name: ``CfnGatewayRoute.GatewayRouteVirtualServiceProperty.VirtualServiceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutevirtualservice.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "virtual_service_name": virtual_service_name,
            }

        @builtins.property
        def virtual_service_name(self) -> builtins.str:
            '''``CfnGatewayRoute.GatewayRouteVirtualServiceProperty.VirtualServiceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutevirtualservice.html#cfn-appmesh-gatewayroute-gatewayroutevirtualservice-virtualservicename
            '''
            result = self._values.get("virtual_service_name")
            assert result is not None, "Required property 'virtual_service_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayRouteVirtualServiceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnGatewayRoute.GrpcGatewayRouteActionProperty",
        jsii_struct_bases=[],
        name_mapping={"target": "target"},
    )
    class GrpcGatewayRouteActionProperty:
        def __init__(
            self,
            *,
            target: typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GatewayRouteTargetProperty"],
        ) -> None:
            '''
            :param target: ``CfnGatewayRoute.GrpcGatewayRouteActionProperty.Target``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayrouteaction.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "target": target,
            }

        @builtins.property
        def target(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GatewayRouteTargetProperty"]:
            '''``CfnGatewayRoute.GrpcGatewayRouteActionProperty.Target``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayrouteaction.html#cfn-appmesh-gatewayroute-grpcgatewayrouteaction-target
            '''
            result = self._values.get("target")
            assert result is not None, "Required property 'target' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GatewayRouteTargetProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcGatewayRouteActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnGatewayRoute.GrpcGatewayRouteMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"service_name": "serviceName"},
    )
    class GrpcGatewayRouteMatchProperty:
        def __init__(
            self,
            *,
            service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param service_name: ``CfnGatewayRoute.GrpcGatewayRouteMatchProperty.ServiceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroutematch.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if service_name is not None:
                self._values["service_name"] = service_name

        @builtins.property
        def service_name(self) -> typing.Optional[builtins.str]:
            '''``CfnGatewayRoute.GrpcGatewayRouteMatchProperty.ServiceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroutematch.html#cfn-appmesh-gatewayroute-grpcgatewayroutematch-servicename
            '''
            result = self._values.get("service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcGatewayRouteMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnGatewayRoute.GrpcGatewayRouteProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "match": "match"},
    )
    class GrpcGatewayRouteProperty:
        def __init__(
            self,
            *,
            action: typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GrpcGatewayRouteActionProperty"],
            match: typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GrpcGatewayRouteMatchProperty"],
        ) -> None:
            '''
            :param action: ``CfnGatewayRoute.GrpcGatewayRouteProperty.Action``.
            :param match: ``CfnGatewayRoute.GrpcGatewayRouteProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroute.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "action": action,
                "match": match,
            }

        @builtins.property
        def action(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GrpcGatewayRouteActionProperty"]:
            '''``CfnGatewayRoute.GrpcGatewayRouteProperty.Action``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroute.html#cfn-appmesh-gatewayroute-grpcgatewayroute-action
            '''
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GrpcGatewayRouteActionProperty"], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GrpcGatewayRouteMatchProperty"]:
            '''``CfnGatewayRoute.GrpcGatewayRouteProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroute.html#cfn-appmesh-gatewayroute-grpcgatewayroute-match
            '''
            result = self._values.get("match")
            assert result is not None, "Required property 'match' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GrpcGatewayRouteMatchProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcGatewayRouteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnGatewayRoute.HttpGatewayRouteActionProperty",
        jsii_struct_bases=[],
        name_mapping={"target": "target"},
    )
    class HttpGatewayRouteActionProperty:
        def __init__(
            self,
            *,
            target: typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GatewayRouteTargetProperty"],
        ) -> None:
            '''
            :param target: ``CfnGatewayRoute.HttpGatewayRouteActionProperty.Target``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteaction.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "target": target,
            }

        @builtins.property
        def target(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GatewayRouteTargetProperty"]:
            '''``CfnGatewayRoute.HttpGatewayRouteActionProperty.Target``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteaction.html#cfn-appmesh-gatewayroute-httpgatewayrouteaction-target
            '''
            result = self._values.get("target")
            assert result is not None, "Required property 'target' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.GatewayRouteTargetProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpGatewayRouteActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnGatewayRoute.HttpGatewayRouteMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"prefix": "prefix"},
    )
    class HttpGatewayRouteMatchProperty:
        def __init__(self, *, prefix: builtins.str) -> None:
            '''
            :param prefix: ``CfnGatewayRoute.HttpGatewayRouteMatchProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroutematch.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "prefix": prefix,
            }

        @builtins.property
        def prefix(self) -> builtins.str:
            '''``CfnGatewayRoute.HttpGatewayRouteMatchProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroutematch.html#cfn-appmesh-gatewayroute-httpgatewayroutematch-prefix
            '''
            result = self._values.get("prefix")
            assert result is not None, "Required property 'prefix' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpGatewayRouteMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnGatewayRoute.HttpGatewayRouteProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "match": "match"},
    )
    class HttpGatewayRouteProperty:
        def __init__(
            self,
            *,
            action: typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.HttpGatewayRouteActionProperty"],
            match: typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.HttpGatewayRouteMatchProperty"],
        ) -> None:
            '''
            :param action: ``CfnGatewayRoute.HttpGatewayRouteProperty.Action``.
            :param match: ``CfnGatewayRoute.HttpGatewayRouteProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroute.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "action": action,
                "match": match,
            }

        @builtins.property
        def action(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.HttpGatewayRouteActionProperty"]:
            '''``CfnGatewayRoute.HttpGatewayRouteProperty.Action``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroute.html#cfn-appmesh-gatewayroute-httpgatewayroute-action
            '''
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.HttpGatewayRouteActionProperty"], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.HttpGatewayRouteMatchProperty"]:
            '''``CfnGatewayRoute.HttpGatewayRouteProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroute.html#cfn-appmesh-gatewayroute-httpgatewayroute-match
            '''
            result = self._values.get("match")
            assert result is not None, "Required property 'match' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnGatewayRoute.HttpGatewayRouteMatchProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpGatewayRouteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.CfnGatewayRouteProps",
    jsii_struct_bases=[],
    name_mapping={
        "mesh_name": "meshName",
        "spec": "spec",
        "virtual_gateway_name": "virtualGatewayName",
        "gateway_route_name": "gatewayRouteName",
        "mesh_owner": "meshOwner",
        "tags": "tags",
    },
)
class CfnGatewayRouteProps:
    def __init__(
        self,
        *,
        mesh_name: builtins.str,
        spec: typing.Union[CfnGatewayRoute.GatewayRouteSpecProperty, aws_cdk.core.IResolvable],
        virtual_gateway_name: builtins.str,
        gateway_route_name: typing.Optional[builtins.str] = None,
        mesh_owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::AppMesh::GatewayRoute``.

        :param mesh_name: ``AWS::AppMesh::GatewayRoute.MeshName``.
        :param spec: ``AWS::AppMesh::GatewayRoute.Spec``.
        :param virtual_gateway_name: ``AWS::AppMesh::GatewayRoute.VirtualGatewayName``.
        :param gateway_route_name: ``AWS::AppMesh::GatewayRoute.GatewayRouteName``.
        :param mesh_owner: ``AWS::AppMesh::GatewayRoute.MeshOwner``.
        :param tags: ``AWS::AppMesh::GatewayRoute.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "mesh_name": mesh_name,
            "spec": spec,
            "virtual_gateway_name": virtual_gateway_name,
        }
        if gateway_route_name is not None:
            self._values["gateway_route_name"] = gateway_route_name
        if mesh_owner is not None:
            self._values["mesh_owner"] = mesh_owner
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def mesh_name(self) -> builtins.str:
        '''``AWS::AppMesh::GatewayRoute.MeshName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-meshname
        '''
        result = self._values.get("mesh_name")
        assert result is not None, "Required property 'mesh_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Union[CfnGatewayRoute.GatewayRouteSpecProperty, aws_cdk.core.IResolvable]:
        '''``AWS::AppMesh::GatewayRoute.Spec``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-spec
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast(typing.Union[CfnGatewayRoute.GatewayRouteSpecProperty, aws_cdk.core.IResolvable], result)

    @builtins.property
    def virtual_gateway_name(self) -> builtins.str:
        '''``AWS::AppMesh::GatewayRoute.VirtualGatewayName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-virtualgatewayname
        '''
        result = self._values.get("virtual_gateway_name")
        assert result is not None, "Required property 'virtual_gateway_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gateway_route_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::GatewayRoute.GatewayRouteName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-gatewayroutename
        '''
        result = self._values.get("gateway_route_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::GatewayRoute.MeshOwner``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-meshowner
        '''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::AppMesh::GatewayRoute.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGatewayRouteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMesh(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appmesh.CfnMesh",
):
    '''A CloudFormation ``AWS::AppMesh::Mesh``.

    :cloudformationResource: AWS::AppMesh::Mesh
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        mesh_name: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMesh.MeshSpecProperty"]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Create a new ``AWS::AppMesh::Mesh``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param mesh_name: ``AWS::AppMesh::Mesh.MeshName``.
        :param spec: ``AWS::AppMesh::Mesh.Spec``.
        :param tags: ``AWS::AppMesh::Mesh.Tags``.
        '''
        props = CfnMeshProps(mesh_name=mesh_name, spec=spec, tags=tags)

        jsii.create(CfnMesh, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrMeshName")
    def attr_mesh_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: MeshName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMeshName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrMeshOwner")
    def attr_mesh_owner(self) -> builtins.str:
        '''
        :cloudformationAttribute: MeshOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMeshOwner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrResourceOwner")
    def attr_resource_owner(self) -> builtins.str:
        '''
        :cloudformationAttribute: ResourceOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceOwner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrUid")
    def attr_uid(self) -> builtins.str:
        '''
        :cloudformationAttribute: Uid
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUid"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::AppMesh::Mesh.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::Mesh.MeshName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-meshname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "meshName"))

    @mesh_name.setter
    def mesh_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "meshName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="spec")
    def spec(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMesh.MeshSpecProperty"]]:
        '''``AWS::AppMesh::Mesh.Spec``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-spec
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMesh.MeshSpecProperty"]], jsii.get(self, "spec"))

    @spec.setter
    def spec(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMesh.MeshSpecProperty"]],
    ) -> None:
        jsii.set(self, "spec", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnMesh.EgressFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class EgressFilterProperty:
        def __init__(self, *, type: builtins.str) -> None:
            '''
            :param type: ``CfnMesh.EgressFilterProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-egressfilter.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
            }

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnMesh.EgressFilterProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-egressfilter.html#cfn-appmesh-mesh-egressfilter-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EgressFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnMesh.MeshSpecProperty",
        jsii_struct_bases=[],
        name_mapping={"egress_filter": "egressFilter"},
    )
    class MeshSpecProperty:
        def __init__(
            self,
            *,
            egress_filter: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMesh.EgressFilterProperty"]] = None,
        ) -> None:
            '''
            :param egress_filter: ``CfnMesh.MeshSpecProperty.EgressFilter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-meshspec.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if egress_filter is not None:
                self._values["egress_filter"] = egress_filter

        @builtins.property
        def egress_filter(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMesh.EgressFilterProperty"]]:
            '''``CfnMesh.MeshSpecProperty.EgressFilter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-meshspec.html#cfn-appmesh-mesh-meshspec-egressfilter
            '''
            result = self._values.get("egress_filter")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMesh.EgressFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MeshSpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.CfnMeshProps",
    jsii_struct_bases=[],
    name_mapping={"mesh_name": "meshName", "spec": "spec", "tags": "tags"},
)
class CfnMeshProps:
    def __init__(
        self,
        *,
        mesh_name: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnMesh.MeshSpecProperty]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::AppMesh::Mesh``.

        :param mesh_name: ``AWS::AppMesh::Mesh.MeshName``.
        :param spec: ``AWS::AppMesh::Mesh.Spec``.
        :param tags: ``AWS::AppMesh::Mesh.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if mesh_name is not None:
            self._values["mesh_name"] = mesh_name
        if spec is not None:
            self._values["spec"] = spec
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def mesh_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::Mesh.MeshName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-meshname
        '''
        result = self._values.get("mesh_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnMesh.MeshSpecProperty]]:
        '''``AWS::AppMesh::Mesh.Spec``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-spec
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnMesh.MeshSpecProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::AppMesh::Mesh.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMeshProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRoute(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appmesh.CfnRoute",
):
    '''A CloudFormation ``AWS::AppMesh::Route``.

    :cloudformationResource: AWS::AppMesh::Route
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        mesh_name: builtins.str,
        spec: typing.Union[aws_cdk.core.IResolvable, "CfnRoute.RouteSpecProperty"],
        virtual_router_name: builtins.str,
        mesh_owner: typing.Optional[builtins.str] = None,
        route_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Create a new ``AWS::AppMesh::Route``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param mesh_name: ``AWS::AppMesh::Route.MeshName``.
        :param spec: ``AWS::AppMesh::Route.Spec``.
        :param virtual_router_name: ``AWS::AppMesh::Route.VirtualRouterName``.
        :param mesh_owner: ``AWS::AppMesh::Route.MeshOwner``.
        :param route_name: ``AWS::AppMesh::Route.RouteName``.
        :param tags: ``AWS::AppMesh::Route.Tags``.
        '''
        props = CfnRouteProps(
            mesh_name=mesh_name,
            spec=spec,
            virtual_router_name=virtual_router_name,
            mesh_owner=mesh_owner,
            route_name=route_name,
            tags=tags,
        )

        jsii.create(CfnRoute, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrMeshName")
    def attr_mesh_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: MeshName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMeshName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrMeshOwner")
    def attr_mesh_owner(self) -> builtins.str:
        '''
        :cloudformationAttribute: MeshOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMeshOwner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrResourceOwner")
    def attr_resource_owner(self) -> builtins.str:
        '''
        :cloudformationAttribute: ResourceOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceOwner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrRouteName")
    def attr_route_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: RouteName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRouteName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrUid")
    def attr_uid(self) -> builtins.str:
        '''
        :cloudformationAttribute: Uid
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUid"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrVirtualRouterName")
    def attr_virtual_router_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: VirtualRouterName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVirtualRouterName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::AppMesh::Route.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> builtins.str:
        '''``AWS::AppMesh::Route.MeshName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-meshname
        '''
        return typing.cast(builtins.str, jsii.get(self, "meshName"))

    @mesh_name.setter
    def mesh_name(self, value: builtins.str) -> None:
        jsii.set(self, "meshName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="spec")
    def spec(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnRoute.RouteSpecProperty"]:
        '''``AWS::AppMesh::Route.Spec``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-spec
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnRoute.RouteSpecProperty"], jsii.get(self, "spec"))

    @spec.setter
    def spec(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnRoute.RouteSpecProperty"],
    ) -> None:
        jsii.set(self, "spec", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualRouterName")
    def virtual_router_name(self) -> builtins.str:
        '''``AWS::AppMesh::Route.VirtualRouterName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-virtualroutername
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualRouterName"))

    @virtual_router_name.setter
    def virtual_router_name(self, value: builtins.str) -> None:
        jsii.set(self, "virtualRouterName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshOwner")
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::Route.MeshOwner``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-meshowner
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "meshOwner"))

    @mesh_owner.setter
    def mesh_owner(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "meshOwner", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="routeName")
    def route_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::Route.RouteName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-routename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeName"))

    @route_name.setter
    def route_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "routeName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.DurationProperty",
        jsii_struct_bases=[],
        name_mapping={"unit": "unit", "value": "value"},
    )
    class DurationProperty:
        def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
            '''
            :param unit: ``CfnRoute.DurationProperty.Unit``.
            :param value: ``CfnRoute.DurationProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-duration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "unit": unit,
                "value": value,
            }

        @builtins.property
        def unit(self) -> builtins.str:
            '''``CfnRoute.DurationProperty.Unit``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-duration.html#cfn-appmesh-route-duration-unit
            '''
            result = self._values.get("unit")
            assert result is not None, "Required property 'unit' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> jsii.Number:
            '''``CfnRoute.DurationProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-duration.html#cfn-appmesh-route-duration-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.GrpcRetryPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_retries": "maxRetries",
            "per_retry_timeout": "perRetryTimeout",
            "grpc_retry_events": "grpcRetryEvents",
            "http_retry_events": "httpRetryEvents",
            "tcp_retry_events": "tcpRetryEvents",
        },
    )
    class GrpcRetryPolicyProperty:
        def __init__(
            self,
            *,
            max_retries: jsii.Number,
            per_retry_timeout: typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"],
            grpc_retry_events: typing.Optional[typing.List[builtins.str]] = None,
            http_retry_events: typing.Optional[typing.List[builtins.str]] = None,
            tcp_retry_events: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            '''
            :param max_retries: ``CfnRoute.GrpcRetryPolicyProperty.MaxRetries``.
            :param per_retry_timeout: ``CfnRoute.GrpcRetryPolicyProperty.PerRetryTimeout``.
            :param grpc_retry_events: ``CfnRoute.GrpcRetryPolicyProperty.GrpcRetryEvents``.
            :param http_retry_events: ``CfnRoute.GrpcRetryPolicyProperty.HttpRetryEvents``.
            :param tcp_retry_events: ``CfnRoute.GrpcRetryPolicyProperty.TcpRetryEvents``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "max_retries": max_retries,
                "per_retry_timeout": per_retry_timeout,
            }
            if grpc_retry_events is not None:
                self._values["grpc_retry_events"] = grpc_retry_events
            if http_retry_events is not None:
                self._values["http_retry_events"] = http_retry_events
            if tcp_retry_events is not None:
                self._values["tcp_retry_events"] = tcp_retry_events

        @builtins.property
        def max_retries(self) -> jsii.Number:
            '''``CfnRoute.GrpcRetryPolicyProperty.MaxRetries``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-maxretries
            '''
            result = self._values.get("max_retries")
            assert result is not None, "Required property 'max_retries' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def per_retry_timeout(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]:
            '''``CfnRoute.GrpcRetryPolicyProperty.PerRetryTimeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-perretrytimeout
            '''
            result = self._values.get("per_retry_timeout")
            assert result is not None, "Required property 'per_retry_timeout' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"], result)

        @builtins.property
        def grpc_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnRoute.GrpcRetryPolicyProperty.GrpcRetryEvents``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-grpcretryevents
            '''
            result = self._values.get("grpc_retry_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def http_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnRoute.GrpcRetryPolicyProperty.HttpRetryEvents``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-httpretryevents
            '''
            result = self._values.get("http_retry_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def tcp_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnRoute.GrpcRetryPolicyProperty.TcpRetryEvents``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-tcpretryevents
            '''
            result = self._values.get("tcp_retry_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcRetryPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.GrpcRouteActionProperty",
        jsii_struct_bases=[],
        name_mapping={"weighted_targets": "weightedTargets"},
    )
    class GrpcRouteActionProperty:
        def __init__(
            self,
            *,
            weighted_targets: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.WeightedTargetProperty"]]],
        ) -> None:
            '''
            :param weighted_targets: ``CfnRoute.GrpcRouteActionProperty.WeightedTargets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcrouteaction.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "weighted_targets": weighted_targets,
            }

        @builtins.property
        def weighted_targets(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.WeightedTargetProperty"]]]:
            '''``CfnRoute.GrpcRouteActionProperty.WeightedTargets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcrouteaction.html#cfn-appmesh-route-grpcrouteaction-weightedtargets
            '''
            result = self._values.get("weighted_targets")
            assert result is not None, "Required property 'weighted_targets' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.WeightedTargetProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcRouteActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.GrpcRouteMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metadata": "metadata",
            "method_name": "methodName",
            "service_name": "serviceName",
        },
    )
    class GrpcRouteMatchProperty:
        def __init__(
            self,
            *,
            metadata: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteMetadataProperty"]]]] = None,
            method_name: typing.Optional[builtins.str] = None,
            service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param metadata: ``CfnRoute.GrpcRouteMatchProperty.Metadata``.
            :param method_name: ``CfnRoute.GrpcRouteMatchProperty.MethodName``.
            :param service_name: ``CfnRoute.GrpcRouteMatchProperty.ServiceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutematch.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if metadata is not None:
                self._values["metadata"] = metadata
            if method_name is not None:
                self._values["method_name"] = method_name
            if service_name is not None:
                self._values["service_name"] = service_name

        @builtins.property
        def metadata(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteMetadataProperty"]]]]:
            '''``CfnRoute.GrpcRouteMatchProperty.Metadata``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutematch.html#cfn-appmesh-route-grpcroutematch-metadata
            '''
            result = self._values.get("metadata")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteMetadataProperty"]]]], result)

        @builtins.property
        def method_name(self) -> typing.Optional[builtins.str]:
            '''``CfnRoute.GrpcRouteMatchProperty.MethodName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutematch.html#cfn-appmesh-route-grpcroutematch-methodname
            '''
            result = self._values.get("method_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_name(self) -> typing.Optional[builtins.str]:
            '''``CfnRoute.GrpcRouteMatchProperty.ServiceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutematch.html#cfn-appmesh-route-grpcroutematch-servicename
            '''
            result = self._values.get("service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcRouteMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.GrpcRouteMetadataMatchMethodProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exact": "exact",
            "prefix": "prefix",
            "range": "range",
            "regex": "regex",
            "suffix": "suffix",
        },
    )
    class GrpcRouteMetadataMatchMethodProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            range: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.MatchRangeProperty"]] = None,
            regex: typing.Optional[builtins.str] = None,
            suffix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param exact: ``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Exact``.
            :param prefix: ``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Prefix``.
            :param range: ``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Range``.
            :param regex: ``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Regex``.
            :param suffix: ``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Suffix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact
            if prefix is not None:
                self._values["prefix"] = prefix
            if range is not None:
                self._values["range"] = range
            if regex is not None:
                self._values["regex"] = regex
            if suffix is not None:
                self._values["suffix"] = suffix

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Exact``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.MatchRangeProperty"]]:
            '''``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Range``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-range
            '''
            result = self._values.get("range")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.MatchRangeProperty"]], result)

        @builtins.property
        def regex(self) -> typing.Optional[builtins.str]:
            '''``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Regex``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-regex
            '''
            result = self._values.get("regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def suffix(self) -> typing.Optional[builtins.str]:
            '''``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Suffix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-suffix
            '''
            result = self._values.get("suffix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcRouteMetadataMatchMethodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.GrpcRouteMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "invert": "invert", "match": "match"},
    )
    class GrpcRouteMetadataProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            invert: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            match: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteMetadataMatchMethodProperty"]] = None,
        ) -> None:
            '''
            :param name: ``CfnRoute.GrpcRouteMetadataProperty.Name``.
            :param invert: ``CfnRoute.GrpcRouteMetadataProperty.Invert``.
            :param match: ``CfnRoute.GrpcRouteMetadataProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadata.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
            }
            if invert is not None:
                self._values["invert"] = invert
            if match is not None:
                self._values["match"] = match

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnRoute.GrpcRouteMetadataProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadata.html#cfn-appmesh-route-grpcroutemetadata-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def invert(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''``CfnRoute.GrpcRouteMetadataProperty.Invert``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadata.html#cfn-appmesh-route-grpcroutemetadata-invert
            '''
            result = self._values.get("invert")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteMetadataMatchMethodProperty"]]:
            '''``CfnRoute.GrpcRouteMetadataProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadata.html#cfn-appmesh-route-grpcroutemetadata-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteMetadataMatchMethodProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcRouteMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.GrpcRouteProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "match": "match",
            "retry_policy": "retryPolicy",
            "timeout": "timeout",
        },
    )
    class GrpcRouteProperty:
        def __init__(
            self,
            *,
            action: typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteActionProperty"],
            match: typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteMatchProperty"],
            retry_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRetryPolicyProperty"]] = None,
            timeout: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcTimeoutProperty"]] = None,
        ) -> None:
            '''
            :param action: ``CfnRoute.GrpcRouteProperty.Action``.
            :param match: ``CfnRoute.GrpcRouteProperty.Match``.
            :param retry_policy: ``CfnRoute.GrpcRouteProperty.RetryPolicy``.
            :param timeout: ``CfnRoute.GrpcRouteProperty.Timeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroute.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "action": action,
                "match": match,
            }
            if retry_policy is not None:
                self._values["retry_policy"] = retry_policy
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def action(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteActionProperty"]:
            '''``CfnRoute.GrpcRouteProperty.Action``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroute.html#cfn-appmesh-route-grpcroute-action
            '''
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteActionProperty"], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteMatchProperty"]:
            '''``CfnRoute.GrpcRouteProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroute.html#cfn-appmesh-route-grpcroute-match
            '''
            result = self._values.get("match")
            assert result is not None, "Required property 'match' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteMatchProperty"], result)

        @builtins.property
        def retry_policy(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRetryPolicyProperty"]]:
            '''``CfnRoute.GrpcRouteProperty.RetryPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroute.html#cfn-appmesh-route-grpcroute-retrypolicy
            '''
            result = self._values.get("retry_policy")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRetryPolicyProperty"]], result)

        @builtins.property
        def timeout(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcTimeoutProperty"]]:
            '''``CfnRoute.GrpcRouteProperty.Timeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroute.html#cfn-appmesh-route-grpcroute-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcTimeoutProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcRouteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.GrpcTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"idle": "idle", "per_request": "perRequest"},
    )
    class GrpcTimeoutProperty:
        def __init__(
            self,
            *,
            idle: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]] = None,
            per_request: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]] = None,
        ) -> None:
            '''
            :param idle: ``CfnRoute.GrpcTimeoutProperty.Idle``.
            :param per_request: ``CfnRoute.GrpcTimeoutProperty.PerRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpctimeout.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if idle is not None:
                self._values["idle"] = idle
            if per_request is not None:
                self._values["per_request"] = per_request

        @builtins.property
        def idle(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]]:
            '''``CfnRoute.GrpcTimeoutProperty.Idle``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpctimeout.html#cfn-appmesh-route-grpctimeout-idle
            '''
            result = self._values.get("idle")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]], result)

        @builtins.property
        def per_request(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]]:
            '''``CfnRoute.GrpcTimeoutProperty.PerRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpctimeout.html#cfn-appmesh-route-grpctimeout-perrequest
            '''
            result = self._values.get("per_request")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.HeaderMatchMethodProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exact": "exact",
            "prefix": "prefix",
            "range": "range",
            "regex": "regex",
            "suffix": "suffix",
        },
    )
    class HeaderMatchMethodProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            range: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.MatchRangeProperty"]] = None,
            regex: typing.Optional[builtins.str] = None,
            suffix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param exact: ``CfnRoute.HeaderMatchMethodProperty.Exact``.
            :param prefix: ``CfnRoute.HeaderMatchMethodProperty.Prefix``.
            :param range: ``CfnRoute.HeaderMatchMethodProperty.Range``.
            :param regex: ``CfnRoute.HeaderMatchMethodProperty.Regex``.
            :param suffix: ``CfnRoute.HeaderMatchMethodProperty.Suffix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact
            if prefix is not None:
                self._values["prefix"] = prefix
            if range is not None:
                self._values["range"] = range
            if regex is not None:
                self._values["regex"] = regex
            if suffix is not None:
                self._values["suffix"] = suffix

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''``CfnRoute.HeaderMatchMethodProperty.Exact``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnRoute.HeaderMatchMethodProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.MatchRangeProperty"]]:
            '''``CfnRoute.HeaderMatchMethodProperty.Range``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-range
            '''
            result = self._values.get("range")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.MatchRangeProperty"]], result)

        @builtins.property
        def regex(self) -> typing.Optional[builtins.str]:
            '''``CfnRoute.HeaderMatchMethodProperty.Regex``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-regex
            '''
            result = self._values.get("regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def suffix(self) -> typing.Optional[builtins.str]:
            '''``CfnRoute.HeaderMatchMethodProperty.Suffix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-suffix
            '''
            result = self._values.get("suffix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderMatchMethodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.HttpRetryPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_retries": "maxRetries",
            "per_retry_timeout": "perRetryTimeout",
            "http_retry_events": "httpRetryEvents",
            "tcp_retry_events": "tcpRetryEvents",
        },
    )
    class HttpRetryPolicyProperty:
        def __init__(
            self,
            *,
            max_retries: jsii.Number,
            per_retry_timeout: typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"],
            http_retry_events: typing.Optional[typing.List[builtins.str]] = None,
            tcp_retry_events: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            '''
            :param max_retries: ``CfnRoute.HttpRetryPolicyProperty.MaxRetries``.
            :param per_retry_timeout: ``CfnRoute.HttpRetryPolicyProperty.PerRetryTimeout``.
            :param http_retry_events: ``CfnRoute.HttpRetryPolicyProperty.HttpRetryEvents``.
            :param tcp_retry_events: ``CfnRoute.HttpRetryPolicyProperty.TcpRetryEvents``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "max_retries": max_retries,
                "per_retry_timeout": per_retry_timeout,
            }
            if http_retry_events is not None:
                self._values["http_retry_events"] = http_retry_events
            if tcp_retry_events is not None:
                self._values["tcp_retry_events"] = tcp_retry_events

        @builtins.property
        def max_retries(self) -> jsii.Number:
            '''``CfnRoute.HttpRetryPolicyProperty.MaxRetries``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html#cfn-appmesh-route-httpretrypolicy-maxretries
            '''
            result = self._values.get("max_retries")
            assert result is not None, "Required property 'max_retries' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def per_retry_timeout(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]:
            '''``CfnRoute.HttpRetryPolicyProperty.PerRetryTimeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html#cfn-appmesh-route-httpretrypolicy-perretrytimeout
            '''
            result = self._values.get("per_retry_timeout")
            assert result is not None, "Required property 'per_retry_timeout' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"], result)

        @builtins.property
        def http_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnRoute.HttpRetryPolicyProperty.HttpRetryEvents``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html#cfn-appmesh-route-httpretrypolicy-httpretryevents
            '''
            result = self._values.get("http_retry_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def tcp_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnRoute.HttpRetryPolicyProperty.TcpRetryEvents``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html#cfn-appmesh-route-httpretrypolicy-tcpretryevents
            '''
            result = self._values.get("tcp_retry_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpRetryPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.HttpRouteActionProperty",
        jsii_struct_bases=[],
        name_mapping={"weighted_targets": "weightedTargets"},
    )
    class HttpRouteActionProperty:
        def __init__(
            self,
            *,
            weighted_targets: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.WeightedTargetProperty"]]],
        ) -> None:
            '''
            :param weighted_targets: ``CfnRoute.HttpRouteActionProperty.WeightedTargets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteaction.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "weighted_targets": weighted_targets,
            }

        @builtins.property
        def weighted_targets(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.WeightedTargetProperty"]]]:
            '''``CfnRoute.HttpRouteActionProperty.WeightedTargets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteaction.html#cfn-appmesh-route-httprouteaction-weightedtargets
            '''
            result = self._values.get("weighted_targets")
            assert result is not None, "Required property 'weighted_targets' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.WeightedTargetProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpRouteActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.HttpRouteHeaderProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "invert": "invert", "match": "match"},
    )
    class HttpRouteHeaderProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            invert: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            match: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HeaderMatchMethodProperty"]] = None,
        ) -> None:
            '''
            :param name: ``CfnRoute.HttpRouteHeaderProperty.Name``.
            :param invert: ``CfnRoute.HttpRouteHeaderProperty.Invert``.
            :param match: ``CfnRoute.HttpRouteHeaderProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteheader.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
            }
            if invert is not None:
                self._values["invert"] = invert
            if match is not None:
                self._values["match"] = match

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnRoute.HttpRouteHeaderProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteheader.html#cfn-appmesh-route-httprouteheader-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def invert(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''``CfnRoute.HttpRouteHeaderProperty.Invert``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteheader.html#cfn-appmesh-route-httprouteheader-invert
            '''
            result = self._values.get("invert")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HeaderMatchMethodProperty"]]:
            '''``CfnRoute.HttpRouteHeaderProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteheader.html#cfn-appmesh-route-httprouteheader-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HeaderMatchMethodProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpRouteHeaderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.HttpRouteMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "prefix": "prefix",
            "headers": "headers",
            "method": "method",
            "scheme": "scheme",
        },
    )
    class HttpRouteMatchProperty:
        def __init__(
            self,
            *,
            prefix: builtins.str,
            headers: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnRoute.HttpRouteHeaderProperty", aws_cdk.core.IResolvable]]]] = None,
            method: typing.Optional[builtins.str] = None,
            scheme: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param prefix: ``CfnRoute.HttpRouteMatchProperty.Prefix``.
            :param headers: ``CfnRoute.HttpRouteMatchProperty.Headers``.
            :param method: ``CfnRoute.HttpRouteMatchProperty.Method``.
            :param scheme: ``CfnRoute.HttpRouteMatchProperty.Scheme``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "prefix": prefix,
            }
            if headers is not None:
                self._values["headers"] = headers
            if method is not None:
                self._values["method"] = method
            if scheme is not None:
                self._values["scheme"] = scheme

        @builtins.property
        def prefix(self) -> builtins.str:
            '''``CfnRoute.HttpRouteMatchProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-prefix
            '''
            result = self._values.get("prefix")
            assert result is not None, "Required property 'prefix' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def headers(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnRoute.HttpRouteHeaderProperty", aws_cdk.core.IResolvable]]]]:
            '''``CfnRoute.HttpRouteMatchProperty.Headers``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-headers
            '''
            result = self._values.get("headers")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnRoute.HttpRouteHeaderProperty", aws_cdk.core.IResolvable]]]], result)

        @builtins.property
        def method(self) -> typing.Optional[builtins.str]:
            '''``CfnRoute.HttpRouteMatchProperty.Method``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-method
            '''
            result = self._values.get("method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scheme(self) -> typing.Optional[builtins.str]:
            '''``CfnRoute.HttpRouteMatchProperty.Scheme``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-scheme
            '''
            result = self._values.get("scheme")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpRouteMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.HttpRouteProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "match": "match",
            "retry_policy": "retryPolicy",
            "timeout": "timeout",
        },
    )
    class HttpRouteProperty:
        def __init__(
            self,
            *,
            action: typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HttpRouteActionProperty"],
            match: typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HttpRouteMatchProperty"],
            retry_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HttpRetryPolicyProperty"]] = None,
            timeout: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HttpTimeoutProperty"]] = None,
        ) -> None:
            '''
            :param action: ``CfnRoute.HttpRouteProperty.Action``.
            :param match: ``CfnRoute.HttpRouteProperty.Match``.
            :param retry_policy: ``CfnRoute.HttpRouteProperty.RetryPolicy``.
            :param timeout: ``CfnRoute.HttpRouteProperty.Timeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "action": action,
                "match": match,
            }
            if retry_policy is not None:
                self._values["retry_policy"] = retry_policy
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def action(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HttpRouteActionProperty"]:
            '''``CfnRoute.HttpRouteProperty.Action``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html#cfn-appmesh-route-httproute-action
            '''
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HttpRouteActionProperty"], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HttpRouteMatchProperty"]:
            '''``CfnRoute.HttpRouteProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html#cfn-appmesh-route-httproute-match
            '''
            result = self._values.get("match")
            assert result is not None, "Required property 'match' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HttpRouteMatchProperty"], result)

        @builtins.property
        def retry_policy(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HttpRetryPolicyProperty"]]:
            '''``CfnRoute.HttpRouteProperty.RetryPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html#cfn-appmesh-route-httproute-retrypolicy
            '''
            result = self._values.get("retry_policy")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HttpRetryPolicyProperty"]], result)

        @builtins.property
        def timeout(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HttpTimeoutProperty"]]:
            '''``CfnRoute.HttpRouteProperty.Timeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html#cfn-appmesh-route-httproute-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.HttpTimeoutProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpRouteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.HttpTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"idle": "idle", "per_request": "perRequest"},
    )
    class HttpTimeoutProperty:
        def __init__(
            self,
            *,
            idle: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]] = None,
            per_request: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]] = None,
        ) -> None:
            '''
            :param idle: ``CfnRoute.HttpTimeoutProperty.Idle``.
            :param per_request: ``CfnRoute.HttpTimeoutProperty.PerRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httptimeout.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if idle is not None:
                self._values["idle"] = idle
            if per_request is not None:
                self._values["per_request"] = per_request

        @builtins.property
        def idle(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]]:
            '''``CfnRoute.HttpTimeoutProperty.Idle``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httptimeout.html#cfn-appmesh-route-httptimeout-idle
            '''
            result = self._values.get("idle")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]], result)

        @builtins.property
        def per_request(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]]:
            '''``CfnRoute.HttpTimeoutProperty.PerRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httptimeout.html#cfn-appmesh-route-httptimeout-perrequest
            '''
            result = self._values.get("per_request")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.MatchRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"end": "end", "start": "start"},
    )
    class MatchRangeProperty:
        def __init__(self, *, end: jsii.Number, start: jsii.Number) -> None:
            '''
            :param end: ``CfnRoute.MatchRangeProperty.End``.
            :param start: ``CfnRoute.MatchRangeProperty.Start``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-matchrange.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "end": end,
                "start": start,
            }

        @builtins.property
        def end(self) -> jsii.Number:
            '''``CfnRoute.MatchRangeProperty.End``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-matchrange.html#cfn-appmesh-route-matchrange-end
            '''
            result = self._values.get("end")
            assert result is not None, "Required property 'end' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def start(self) -> jsii.Number:
            '''``CfnRoute.MatchRangeProperty.Start``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-matchrange.html#cfn-appmesh-route-matchrange-start
            '''
            result = self._values.get("start")
            assert result is not None, "Required property 'start' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatchRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.RouteSpecProperty",
        jsii_struct_bases=[],
        name_mapping={
            "grpc_route": "grpcRoute",
            "http2_route": "http2Route",
            "http_route": "httpRoute",
            "priority": "priority",
            "tcp_route": "tcpRoute",
        },
    )
    class RouteSpecProperty:
        def __init__(
            self,
            *,
            grpc_route: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteProperty"]] = None,
            http2_route: typing.Optional[typing.Union["CfnRoute.HttpRouteProperty", aws_cdk.core.IResolvable]] = None,
            http_route: typing.Optional[typing.Union["CfnRoute.HttpRouteProperty", aws_cdk.core.IResolvable]] = None,
            priority: typing.Optional[jsii.Number] = None,
            tcp_route: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.TcpRouteProperty"]] = None,
        ) -> None:
            '''
            :param grpc_route: ``CfnRoute.RouteSpecProperty.GrpcRoute``.
            :param http2_route: ``CfnRoute.RouteSpecProperty.Http2Route``.
            :param http_route: ``CfnRoute.RouteSpecProperty.HttpRoute``.
            :param priority: ``CfnRoute.RouteSpecProperty.Priority``.
            :param tcp_route: ``CfnRoute.RouteSpecProperty.TcpRoute``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if grpc_route is not None:
                self._values["grpc_route"] = grpc_route
            if http2_route is not None:
                self._values["http2_route"] = http2_route
            if http_route is not None:
                self._values["http_route"] = http_route
            if priority is not None:
                self._values["priority"] = priority
            if tcp_route is not None:
                self._values["tcp_route"] = tcp_route

        @builtins.property
        def grpc_route(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteProperty"]]:
            '''``CfnRoute.RouteSpecProperty.GrpcRoute``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-grpcroute
            '''
            result = self._values.get("grpc_route")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.GrpcRouteProperty"]], result)

        @builtins.property
        def http2_route(
            self,
        ) -> typing.Optional[typing.Union["CfnRoute.HttpRouteProperty", aws_cdk.core.IResolvable]]:
            '''``CfnRoute.RouteSpecProperty.Http2Route``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-http2route
            '''
            result = self._values.get("http2_route")
            return typing.cast(typing.Optional[typing.Union["CfnRoute.HttpRouteProperty", aws_cdk.core.IResolvable]], result)

        @builtins.property
        def http_route(
            self,
        ) -> typing.Optional[typing.Union["CfnRoute.HttpRouteProperty", aws_cdk.core.IResolvable]]:
            '''``CfnRoute.RouteSpecProperty.HttpRoute``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-httproute
            '''
            result = self._values.get("http_route")
            return typing.cast(typing.Optional[typing.Union["CfnRoute.HttpRouteProperty", aws_cdk.core.IResolvable]], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''``CfnRoute.RouteSpecProperty.Priority``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def tcp_route(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.TcpRouteProperty"]]:
            '''``CfnRoute.RouteSpecProperty.TcpRoute``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-tcproute
            '''
            result = self._values.get("tcp_route")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.TcpRouteProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouteSpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.TcpRouteActionProperty",
        jsii_struct_bases=[],
        name_mapping={"weighted_targets": "weightedTargets"},
    )
    class TcpRouteActionProperty:
        def __init__(
            self,
            *,
            weighted_targets: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.WeightedTargetProperty"]]],
        ) -> None:
            '''
            :param weighted_targets: ``CfnRoute.TcpRouteActionProperty.WeightedTargets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcprouteaction.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "weighted_targets": weighted_targets,
            }

        @builtins.property
        def weighted_targets(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.WeightedTargetProperty"]]]:
            '''``CfnRoute.TcpRouteActionProperty.WeightedTargets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcprouteaction.html#cfn-appmesh-route-tcprouteaction-weightedtargets
            '''
            result = self._values.get("weighted_targets")
            assert result is not None, "Required property 'weighted_targets' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.WeightedTargetProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TcpRouteActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.TcpRouteProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "timeout": "timeout"},
    )
    class TcpRouteProperty:
        def __init__(
            self,
            *,
            action: typing.Union[aws_cdk.core.IResolvable, "CfnRoute.TcpRouteActionProperty"],
            timeout: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.TcpTimeoutProperty"]] = None,
        ) -> None:
            '''
            :param action: ``CfnRoute.TcpRouteProperty.Action``.
            :param timeout: ``CfnRoute.TcpRouteProperty.Timeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcproute.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "action": action,
            }
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def action(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnRoute.TcpRouteActionProperty"]:
            '''``CfnRoute.TcpRouteProperty.Action``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcproute.html#cfn-appmesh-route-tcproute-action
            '''
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnRoute.TcpRouteActionProperty"], result)

        @builtins.property
        def timeout(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.TcpTimeoutProperty"]]:
            '''``CfnRoute.TcpRouteProperty.Timeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcproute.html#cfn-appmesh-route-tcproute-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.TcpTimeoutProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TcpRouteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.TcpTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"idle": "idle"},
    )
    class TcpTimeoutProperty:
        def __init__(
            self,
            *,
            idle: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]] = None,
        ) -> None:
            '''
            :param idle: ``CfnRoute.TcpTimeoutProperty.Idle``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcptimeout.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if idle is not None:
                self._values["idle"] = idle

        @builtins.property
        def idle(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]]:
            '''``CfnRoute.TcpTimeoutProperty.Idle``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcptimeout.html#cfn-appmesh-route-tcptimeout-idle
            '''
            result = self._values.get("idle")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.DurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TcpTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnRoute.WeightedTargetProperty",
        jsii_struct_bases=[],
        name_mapping={"virtual_node": "virtualNode", "weight": "weight"},
    )
    class WeightedTargetProperty:
        def __init__(self, *, virtual_node: builtins.str, weight: jsii.Number) -> None:
            '''
            :param virtual_node: ``CfnRoute.WeightedTargetProperty.VirtualNode``.
            :param weight: ``CfnRoute.WeightedTargetProperty.Weight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-weightedtarget.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "virtual_node": virtual_node,
                "weight": weight,
            }

        @builtins.property
        def virtual_node(self) -> builtins.str:
            '''``CfnRoute.WeightedTargetProperty.VirtualNode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-weightedtarget.html#cfn-appmesh-route-weightedtarget-virtualnode
            '''
            result = self._values.get("virtual_node")
            assert result is not None, "Required property 'virtual_node' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def weight(self) -> jsii.Number:
            '''``CfnRoute.WeightedTargetProperty.Weight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-weightedtarget.html#cfn-appmesh-route-weightedtarget-weight
            '''
            result = self._values.get("weight")
            assert result is not None, "Required property 'weight' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WeightedTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.CfnRouteProps",
    jsii_struct_bases=[],
    name_mapping={
        "mesh_name": "meshName",
        "spec": "spec",
        "virtual_router_name": "virtualRouterName",
        "mesh_owner": "meshOwner",
        "route_name": "routeName",
        "tags": "tags",
    },
)
class CfnRouteProps:
    def __init__(
        self,
        *,
        mesh_name: builtins.str,
        spec: typing.Union[aws_cdk.core.IResolvable, CfnRoute.RouteSpecProperty],
        virtual_router_name: builtins.str,
        mesh_owner: typing.Optional[builtins.str] = None,
        route_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::AppMesh::Route``.

        :param mesh_name: ``AWS::AppMesh::Route.MeshName``.
        :param spec: ``AWS::AppMesh::Route.Spec``.
        :param virtual_router_name: ``AWS::AppMesh::Route.VirtualRouterName``.
        :param mesh_owner: ``AWS::AppMesh::Route.MeshOwner``.
        :param route_name: ``AWS::AppMesh::Route.RouteName``.
        :param tags: ``AWS::AppMesh::Route.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "mesh_name": mesh_name,
            "spec": spec,
            "virtual_router_name": virtual_router_name,
        }
        if mesh_owner is not None:
            self._values["mesh_owner"] = mesh_owner
        if route_name is not None:
            self._values["route_name"] = route_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def mesh_name(self) -> builtins.str:
        '''``AWS::AppMesh::Route.MeshName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-meshname
        '''
        result = self._values.get("mesh_name")
        assert result is not None, "Required property 'mesh_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnRoute.RouteSpecProperty]:
        '''``AWS::AppMesh::Route.Spec``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-spec
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, CfnRoute.RouteSpecProperty], result)

    @builtins.property
    def virtual_router_name(self) -> builtins.str:
        '''``AWS::AppMesh::Route.VirtualRouterName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-virtualroutername
        '''
        result = self._values.get("virtual_router_name")
        assert result is not None, "Required property 'virtual_router_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::Route.MeshOwner``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-meshowner
        '''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::Route.RouteName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-routename
        '''
        result = self._values.get("route_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::AppMesh::Route.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRouteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnVirtualGateway(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway",
):
    '''A CloudFormation ``AWS::AppMesh::VirtualGateway``.

    :cloudformationResource: AWS::AppMesh::VirtualGateway
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        mesh_name: builtins.str,
        spec: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewaySpecProperty"],
        mesh_owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        virtual_gateway_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::AppMesh::VirtualGateway``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param mesh_name: ``AWS::AppMesh::VirtualGateway.MeshName``.
        :param spec: ``AWS::AppMesh::VirtualGateway.Spec``.
        :param mesh_owner: ``AWS::AppMesh::VirtualGateway.MeshOwner``.
        :param tags: ``AWS::AppMesh::VirtualGateway.Tags``.
        :param virtual_gateway_name: ``AWS::AppMesh::VirtualGateway.VirtualGatewayName``.
        '''
        props = CfnVirtualGatewayProps(
            mesh_name=mesh_name,
            spec=spec,
            mesh_owner=mesh_owner,
            tags=tags,
            virtual_gateway_name=virtual_gateway_name,
        )

        jsii.create(CfnVirtualGateway, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrMeshName")
    def attr_mesh_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: MeshName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMeshName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrMeshOwner")
    def attr_mesh_owner(self) -> builtins.str:
        '''
        :cloudformationAttribute: MeshOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMeshOwner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrResourceOwner")
    def attr_resource_owner(self) -> builtins.str:
        '''
        :cloudformationAttribute: ResourceOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceOwner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrUid")
    def attr_uid(self) -> builtins.str:
        '''
        :cloudformationAttribute: Uid
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUid"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrVirtualGatewayName")
    def attr_virtual_gateway_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: VirtualGatewayName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVirtualGatewayName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::AppMesh::VirtualGateway.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> builtins.str:
        '''``AWS::AppMesh::VirtualGateway.MeshName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-meshname
        '''
        return typing.cast(builtins.str, jsii.get(self, "meshName"))

    @mesh_name.setter
    def mesh_name(self, value: builtins.str) -> None:
        jsii.set(self, "meshName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="spec")
    def spec(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewaySpecProperty"]:
        '''``AWS::AppMesh::VirtualGateway.Spec``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-spec
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewaySpecProperty"], jsii.get(self, "spec"))

    @spec.setter
    def spec(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewaySpecProperty"],
    ) -> None:
        jsii.set(self, "spec", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshOwner")
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::VirtualGateway.MeshOwner``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-meshowner
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "meshOwner"))

    @mesh_owner.setter
    def mesh_owner(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "meshOwner", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualGatewayName")
    def virtual_gateway_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::VirtualGateway.VirtualGatewayName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-virtualgatewayname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualGatewayName"))

    @virtual_gateway_name.setter
    def virtual_gateway_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "virtualGatewayName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.SubjectAlternativeNameMatchersProperty",
        jsii_struct_bases=[],
        name_mapping={"exact": "exact"},
    )
    class SubjectAlternativeNameMatchersProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            '''
            :param exact: ``CfnVirtualGateway.SubjectAlternativeNameMatchersProperty.Exact``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-subjectalternativenamematchers.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact

        @builtins.property
        def exact(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnVirtualGateway.SubjectAlternativeNameMatchersProperty.Exact``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-subjectalternativenamematchers.html#cfn-appmesh-virtualgateway-subjectalternativenamematchers-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectAlternativeNameMatchersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.SubjectAlternativeNamesProperty",
        jsii_struct_bases=[],
        name_mapping={"match": "match"},
    )
    class SubjectAlternativeNamesProperty:
        def __init__(
            self,
            *,
            match: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.SubjectAlternativeNameMatchersProperty"],
        ) -> None:
            '''
            :param match: ``CfnVirtualGateway.SubjectAlternativeNamesProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-subjectalternativenames.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "match": match,
            }

        @builtins.property
        def match(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.SubjectAlternativeNameMatchersProperty"]:
            '''``CfnVirtualGateway.SubjectAlternativeNamesProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-subjectalternativenames.html#cfn-appmesh-virtualgateway-subjectalternativenames-match
            '''
            result = self._values.get("match")
            assert result is not None, "Required property 'match' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.SubjectAlternativeNameMatchersProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectAlternativeNamesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayAccessLogProperty",
        jsii_struct_bases=[],
        name_mapping={"file": "file"},
    )
    class VirtualGatewayAccessLogProperty:
        def __init__(
            self,
            *,
            file: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayFileAccessLogProperty"]] = None,
        ) -> None:
            '''
            :param file: ``CfnVirtualGateway.VirtualGatewayAccessLogProperty.File``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayaccesslog.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if file is not None:
                self._values["file"] = file

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayFileAccessLogProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayAccessLogProperty.File``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayaccesslog.html#cfn-appmesh-virtualgateway-virtualgatewayaccesslog-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayFileAccessLogProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayAccessLogProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayBackendDefaultsProperty",
        jsii_struct_bases=[],
        name_mapping={"client_policy": "clientPolicy"},
    )
    class VirtualGatewayBackendDefaultsProperty:
        def __init__(
            self,
            *,
            client_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayClientPolicyProperty"]] = None,
        ) -> None:
            '''
            :param client_policy: ``CfnVirtualGateway.VirtualGatewayBackendDefaultsProperty.ClientPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaybackenddefaults.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if client_policy is not None:
                self._values["client_policy"] = client_policy

        @builtins.property
        def client_policy(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayClientPolicyProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayBackendDefaultsProperty.ClientPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaybackenddefaults.html#cfn-appmesh-virtualgateway-virtualgatewaybackenddefaults-clientpolicy
            '''
            result = self._values.get("client_policy")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayClientPolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayBackendDefaultsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayClientPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"tls": "tls"},
    )
    class VirtualGatewayClientPolicyProperty:
        def __init__(
            self,
            *,
            tls: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayClientPolicyTlsProperty"]] = None,
        ) -> None:
            '''
            :param tls: ``CfnVirtualGateway.VirtualGatewayClientPolicyProperty.TLS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclientpolicy.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if tls is not None:
                self._values["tls"] = tls

        @builtins.property
        def tls(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayClientPolicyTlsProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayClientPolicyProperty.TLS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclientpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayclientpolicy-tls
            '''
            result = self._values.get("tls")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayClientPolicyTlsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayClientPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayClientPolicyTlsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "validation": "validation",
            "certificate": "certificate",
            "enforce": "enforce",
            "ports": "ports",
        },
    )
    class VirtualGatewayClientPolicyTlsProperty:
        def __init__(
            self,
            *,
            validation: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextProperty"],
            certificate: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayClientTlsCertificateProperty"]] = None,
            enforce: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            ports: typing.Optional[typing.Union[typing.List[jsii.Number], aws_cdk.core.IResolvable]] = None,
        ) -> None:
            '''
            :param validation: ``CfnVirtualGateway.VirtualGatewayClientPolicyTlsProperty.Validation``.
            :param certificate: ``CfnVirtualGateway.VirtualGatewayClientPolicyTlsProperty.Certificate``.
            :param enforce: ``CfnVirtualGateway.VirtualGatewayClientPolicyTlsProperty.Enforce``.
            :param ports: ``CfnVirtualGateway.VirtualGatewayClientPolicyTlsProperty.Ports``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclientpolicytls.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "validation": validation,
            }
            if certificate is not None:
                self._values["certificate"] = certificate
            if enforce is not None:
                self._values["enforce"] = enforce
            if ports is not None:
                self._values["ports"] = ports

        @builtins.property
        def validation(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextProperty"]:
            '''``CfnVirtualGateway.VirtualGatewayClientPolicyTlsProperty.Validation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclientpolicytls.html#cfn-appmesh-virtualgateway-virtualgatewayclientpolicytls-validation
            '''
            result = self._values.get("validation")
            assert result is not None, "Required property 'validation' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextProperty"], result)

        @builtins.property
        def certificate(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayClientTlsCertificateProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayClientPolicyTlsProperty.Certificate``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclientpolicytls.html#cfn-appmesh-virtualgateway-virtualgatewayclientpolicytls-certificate
            '''
            result = self._values.get("certificate")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayClientTlsCertificateProperty"]], result)

        @builtins.property
        def enforce(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''``CfnVirtualGateway.VirtualGatewayClientPolicyTlsProperty.Enforce``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclientpolicytls.html#cfn-appmesh-virtualgateway-virtualgatewayclientpolicytls-enforce
            '''
            result = self._values.get("enforce")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def ports(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], aws_cdk.core.IResolvable]]:
            '''``CfnVirtualGateway.VirtualGatewayClientPolicyTlsProperty.Ports``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclientpolicytls.html#cfn-appmesh-virtualgateway-virtualgatewayclientpolicytls-ports
            '''
            result = self._values.get("ports")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], aws_cdk.core.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayClientPolicyTlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayClientTlsCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"file": "file", "sds": "sds"},
    )
    class VirtualGatewayClientTlsCertificateProperty:
        def __init__(
            self,
            *,
            file: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsFileCertificateProperty"]] = None,
            sds: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsSdsCertificateProperty"]] = None,
        ) -> None:
            '''
            :param file: ``CfnVirtualGateway.VirtualGatewayClientTlsCertificateProperty.File``.
            :param sds: ``CfnVirtualGateway.VirtualGatewayClientTlsCertificateProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclienttlscertificate.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsFileCertificateProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayClientTlsCertificateProperty.File``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclienttlscertificate.html#cfn-appmesh-virtualgateway-virtualgatewayclienttlscertificate-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsFileCertificateProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsSdsCertificateProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayClientTlsCertificateProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclienttlscertificate.html#cfn-appmesh-virtualgateway-virtualgatewayclienttlscertificate-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsSdsCertificateProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayClientTlsCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={"grpc": "grpc", "http": "http", "http2": "http2"},
    )
    class VirtualGatewayConnectionPoolProperty:
        def __init__(
            self,
            *,
            grpc: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayGrpcConnectionPoolProperty"]] = None,
            http: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayHttpConnectionPoolProperty"]] = None,
            http2: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayHttp2ConnectionPoolProperty"]] = None,
        ) -> None:
            '''
            :param grpc: ``CfnVirtualGateway.VirtualGatewayConnectionPoolProperty.GRPC``.
            :param http: ``CfnVirtualGateway.VirtualGatewayConnectionPoolProperty.HTTP``.
            :param http2: ``CfnVirtualGateway.VirtualGatewayConnectionPoolProperty.HTTP2``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayconnectionpool.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if grpc is not None:
                self._values["grpc"] = grpc
            if http is not None:
                self._values["http"] = http
            if http2 is not None:
                self._values["http2"] = http2

        @builtins.property
        def grpc(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayGrpcConnectionPoolProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayConnectionPoolProperty.GRPC``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayconnectionpool.html#cfn-appmesh-virtualgateway-virtualgatewayconnectionpool-grpc
            '''
            result = self._values.get("grpc")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayGrpcConnectionPoolProperty"]], result)

        @builtins.property
        def http(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayHttpConnectionPoolProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayConnectionPoolProperty.HTTP``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayconnectionpool.html#cfn-appmesh-virtualgateway-virtualgatewayconnectionpool-http
            '''
            result = self._values.get("http")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayHttpConnectionPoolProperty"]], result)

        @builtins.property
        def http2(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayHttp2ConnectionPoolProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayConnectionPoolProperty.HTTP2``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayconnectionpool.html#cfn-appmesh-virtualgateway-virtualgatewayconnectionpool-http2
            '''
            result = self._values.get("http2")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayHttp2ConnectionPoolProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayFileAccessLogProperty",
        jsii_struct_bases=[],
        name_mapping={"path": "path"},
    )
    class VirtualGatewayFileAccessLogProperty:
        def __init__(self, *, path: builtins.str) -> None:
            '''
            :param path: ``CfnVirtualGateway.VirtualGatewayFileAccessLogProperty.Path``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayfileaccesslog.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "path": path,
            }

        @builtins.property
        def path(self) -> builtins.str:
            '''``CfnVirtualGateway.VirtualGatewayFileAccessLogProperty.Path``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayfileaccesslog.html#cfn-appmesh-virtualgateway-virtualgatewayfileaccesslog-path
            '''
            result = self._values.get("path")
            assert result is not None, "Required property 'path' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayFileAccessLogProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayGrpcConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={"max_requests": "maxRequests"},
    )
    class VirtualGatewayGrpcConnectionPoolProperty:
        def __init__(self, *, max_requests: jsii.Number) -> None:
            '''
            :param max_requests: ``CfnVirtualGateway.VirtualGatewayGrpcConnectionPoolProperty.MaxRequests``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaygrpcconnectionpool.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "max_requests": max_requests,
            }

        @builtins.property
        def max_requests(self) -> jsii.Number:
            '''``CfnVirtualGateway.VirtualGatewayGrpcConnectionPoolProperty.MaxRequests``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaygrpcconnectionpool.html#cfn-appmesh-virtualgateway-virtualgatewaygrpcconnectionpool-maxrequests
            '''
            result = self._values.get("max_requests")
            assert result is not None, "Required property 'max_requests' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayGrpcConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "healthy_threshold": "healthyThreshold",
            "interval_millis": "intervalMillis",
            "protocol": "protocol",
            "timeout_millis": "timeoutMillis",
            "unhealthy_threshold": "unhealthyThreshold",
            "path": "path",
            "port": "port",
        },
    )
    class VirtualGatewayHealthCheckPolicyProperty:
        def __init__(
            self,
            *,
            healthy_threshold: jsii.Number,
            interval_millis: jsii.Number,
            protocol: builtins.str,
            timeout_millis: jsii.Number,
            unhealthy_threshold: jsii.Number,
            path: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param healthy_threshold: ``CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty.HealthyThreshold``.
            :param interval_millis: ``CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty.IntervalMillis``.
            :param protocol: ``CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty.Protocol``.
            :param timeout_millis: ``CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty.TimeoutMillis``.
            :param unhealthy_threshold: ``CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty.UnhealthyThreshold``.
            :param path: ``CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty.Path``.
            :param port: ``CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "healthy_threshold": healthy_threshold,
                "interval_millis": interval_millis,
                "protocol": protocol,
                "timeout_millis": timeout_millis,
                "unhealthy_threshold": unhealthy_threshold,
            }
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def healthy_threshold(self) -> jsii.Number:
            '''``CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty.HealthyThreshold``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy-healthythreshold
            '''
            result = self._values.get("healthy_threshold")
            assert result is not None, "Required property 'healthy_threshold' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def interval_millis(self) -> jsii.Number:
            '''``CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty.IntervalMillis``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy-intervalmillis
            '''
            result = self._values.get("interval_millis")
            assert result is not None, "Required property 'interval_millis' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def protocol(self) -> builtins.str:
            '''``CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy-protocol
            '''
            result = self._values.get("protocol")
            assert result is not None, "Required property 'protocol' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def timeout_millis(self) -> jsii.Number:
            '''``CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty.TimeoutMillis``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy-timeoutmillis
            '''
            result = self._values.get("timeout_millis")
            assert result is not None, "Required property 'timeout_millis' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def unhealthy_threshold(self) -> jsii.Number:
            '''``CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty.UnhealthyThreshold``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy-unhealthythreshold
            '''
            result = self._values.get("unhealthy_threshold")
            assert result is not None, "Required property 'unhealthy_threshold' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''``CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty.Path``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''``CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayHealthCheckPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayHttp2ConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={"max_requests": "maxRequests"},
    )
    class VirtualGatewayHttp2ConnectionPoolProperty:
        def __init__(self, *, max_requests: jsii.Number) -> None:
            '''
            :param max_requests: ``CfnVirtualGateway.VirtualGatewayHttp2ConnectionPoolProperty.MaxRequests``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhttp2connectionpool.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "max_requests": max_requests,
            }

        @builtins.property
        def max_requests(self) -> jsii.Number:
            '''``CfnVirtualGateway.VirtualGatewayHttp2ConnectionPoolProperty.MaxRequests``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhttp2connectionpool.html#cfn-appmesh-virtualgateway-virtualgatewayhttp2connectionpool-maxrequests
            '''
            result = self._values.get("max_requests")
            assert result is not None, "Required property 'max_requests' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayHttp2ConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayHttpConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_connections": "maxConnections",
            "max_pending_requests": "maxPendingRequests",
        },
    )
    class VirtualGatewayHttpConnectionPoolProperty:
        def __init__(
            self,
            *,
            max_connections: jsii.Number,
            max_pending_requests: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param max_connections: ``CfnVirtualGateway.VirtualGatewayHttpConnectionPoolProperty.MaxConnections``.
            :param max_pending_requests: ``CfnVirtualGateway.VirtualGatewayHttpConnectionPoolProperty.MaxPendingRequests``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhttpconnectionpool.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "max_connections": max_connections,
            }
            if max_pending_requests is not None:
                self._values["max_pending_requests"] = max_pending_requests

        @builtins.property
        def max_connections(self) -> jsii.Number:
            '''``CfnVirtualGateway.VirtualGatewayHttpConnectionPoolProperty.MaxConnections``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhttpconnectionpool.html#cfn-appmesh-virtualgateway-virtualgatewayhttpconnectionpool-maxconnections
            '''
            result = self._values.get("max_connections")
            assert result is not None, "Required property 'max_connections' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def max_pending_requests(self) -> typing.Optional[jsii.Number]:
            '''``CfnVirtualGateway.VirtualGatewayHttpConnectionPoolProperty.MaxPendingRequests``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhttpconnectionpool.html#cfn-appmesh-virtualgateway-virtualgatewayhttpconnectionpool-maxpendingrequests
            '''
            result = self._values.get("max_pending_requests")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayHttpConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayListenerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "port_mapping": "portMapping",
            "connection_pool": "connectionPool",
            "health_check": "healthCheck",
            "tls": "tls",
        },
    )
    class VirtualGatewayListenerProperty:
        def __init__(
            self,
            *,
            port_mapping: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayPortMappingProperty"],
            connection_pool: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayConnectionPoolProperty"]] = None,
            health_check: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty"]] = None,
            tls: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsProperty"]] = None,
        ) -> None:
            '''
            :param port_mapping: ``CfnVirtualGateway.VirtualGatewayListenerProperty.PortMapping``.
            :param connection_pool: ``CfnVirtualGateway.VirtualGatewayListenerProperty.ConnectionPool``.
            :param health_check: ``CfnVirtualGateway.VirtualGatewayListenerProperty.HealthCheck``.
            :param tls: ``CfnVirtualGateway.VirtualGatewayListenerProperty.TLS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistener.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "port_mapping": port_mapping,
            }
            if connection_pool is not None:
                self._values["connection_pool"] = connection_pool
            if health_check is not None:
                self._values["health_check"] = health_check
            if tls is not None:
                self._values["tls"] = tls

        @builtins.property
        def port_mapping(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayPortMappingProperty"]:
            '''``CfnVirtualGateway.VirtualGatewayListenerProperty.PortMapping``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistener.html#cfn-appmesh-virtualgateway-virtualgatewaylistener-portmapping
            '''
            result = self._values.get("port_mapping")
            assert result is not None, "Required property 'port_mapping' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayPortMappingProperty"], result)

        @builtins.property
        def connection_pool(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayConnectionPoolProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayListenerProperty.ConnectionPool``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistener.html#cfn-appmesh-virtualgateway-virtualgatewaylistener-connectionpool
            '''
            result = self._values.get("connection_pool")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayConnectionPoolProperty"]], result)

        @builtins.property
        def health_check(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayListenerProperty.HealthCheck``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistener.html#cfn-appmesh-virtualgateway-virtualgatewaylistener-healthcheck
            '''
            result = self._values.get("health_check")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayHealthCheckPolicyProperty"]], result)

        @builtins.property
        def tls(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayListenerProperty.TLS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistener.html#cfn-appmesh-virtualgateway-virtualgatewaylistener-tls
            '''
            result = self._values.get("tls")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayListenerTlsAcmCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_arn": "certificateArn"},
    )
    class VirtualGatewayListenerTlsAcmCertificateProperty:
        def __init__(self, *, certificate_arn: builtins.str) -> None:
            '''
            :param certificate_arn: ``CfnVirtualGateway.VirtualGatewayListenerTlsAcmCertificateProperty.CertificateArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsacmcertificate.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "certificate_arn": certificate_arn,
            }

        @builtins.property
        def certificate_arn(self) -> builtins.str:
            '''``CfnVirtualGateway.VirtualGatewayListenerTlsAcmCertificateProperty.CertificateArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsacmcertificate.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlsacmcertificate-certificatearn
            '''
            result = self._values.get("certificate_arn")
            assert result is not None, "Required property 'certificate_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerTlsAcmCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayListenerTlsCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"acm": "acm", "file": "file", "sds": "sds"},
    )
    class VirtualGatewayListenerTlsCertificateProperty:
        def __init__(
            self,
            *,
            acm: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsAcmCertificateProperty"]] = None,
            file: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsFileCertificateProperty"]] = None,
            sds: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsSdsCertificateProperty"]] = None,
        ) -> None:
            '''
            :param acm: ``CfnVirtualGateway.VirtualGatewayListenerTlsCertificateProperty.ACM``.
            :param file: ``CfnVirtualGateway.VirtualGatewayListenerTlsCertificateProperty.File``.
            :param sds: ``CfnVirtualGateway.VirtualGatewayListenerTlsCertificateProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlscertificate.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if acm is not None:
                self._values["acm"] = acm
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def acm(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsAcmCertificateProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayListenerTlsCertificateProperty.ACM``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlscertificate.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlscertificate-acm
            '''
            result = self._values.get("acm")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsAcmCertificateProperty"]], result)

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsFileCertificateProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayListenerTlsCertificateProperty.File``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlscertificate.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlscertificate-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsFileCertificateProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsSdsCertificateProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayListenerTlsCertificateProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlscertificate.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlscertificate-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsSdsCertificateProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerTlsCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayListenerTlsFileCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_chain": "certificateChain",
            "private_key": "privateKey",
        },
    )
    class VirtualGatewayListenerTlsFileCertificateProperty:
        def __init__(
            self,
            *,
            certificate_chain: builtins.str,
            private_key: builtins.str,
        ) -> None:
            '''
            :param certificate_chain: ``CfnVirtualGateway.VirtualGatewayListenerTlsFileCertificateProperty.CertificateChain``.
            :param private_key: ``CfnVirtualGateway.VirtualGatewayListenerTlsFileCertificateProperty.PrivateKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsfilecertificate.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "certificate_chain": certificate_chain,
                "private_key": private_key,
            }

        @builtins.property
        def certificate_chain(self) -> builtins.str:
            '''``CfnVirtualGateway.VirtualGatewayListenerTlsFileCertificateProperty.CertificateChain``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsfilecertificate.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlsfilecertificate-certificatechain
            '''
            result = self._values.get("certificate_chain")
            assert result is not None, "Required property 'certificate_chain' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def private_key(self) -> builtins.str:
            '''``CfnVirtualGateway.VirtualGatewayListenerTlsFileCertificateProperty.PrivateKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsfilecertificate.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlsfilecertificate-privatekey
            '''
            result = self._values.get("private_key")
            assert result is not None, "Required property 'private_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerTlsFileCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayListenerTlsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate": "certificate",
            "mode": "mode",
            "validation": "validation",
        },
    )
    class VirtualGatewayListenerTlsProperty:
        def __init__(
            self,
            *,
            certificate: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsCertificateProperty"],
            mode: builtins.str,
            validation: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextProperty"]] = None,
        ) -> None:
            '''
            :param certificate: ``CfnVirtualGateway.VirtualGatewayListenerTlsProperty.Certificate``.
            :param mode: ``CfnVirtualGateway.VirtualGatewayListenerTlsProperty.Mode``.
            :param validation: ``CfnVirtualGateway.VirtualGatewayListenerTlsProperty.Validation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertls.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "certificate": certificate,
                "mode": mode,
            }
            if validation is not None:
                self._values["validation"] = validation

        @builtins.property
        def certificate(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsCertificateProperty"]:
            '''``CfnVirtualGateway.VirtualGatewayListenerTlsProperty.Certificate``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertls.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertls-certificate
            '''
            result = self._values.get("certificate")
            assert result is not None, "Required property 'certificate' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsCertificateProperty"], result)

        @builtins.property
        def mode(self) -> builtins.str:
            '''``CfnVirtualGateway.VirtualGatewayListenerTlsProperty.Mode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertls.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertls-mode
            '''
            result = self._values.get("mode")
            assert result is not None, "Required property 'mode' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def validation(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayListenerTlsProperty.Validation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertls.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertls-validation
            '''
            result = self._values.get("validation")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerTlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayListenerTlsSdsCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_name": "secretName"},
    )
    class VirtualGatewayListenerTlsSdsCertificateProperty:
        def __init__(self, *, secret_name: builtins.str) -> None:
            '''
            :param secret_name: ``CfnVirtualGateway.VirtualGatewayListenerTlsSdsCertificateProperty.SecretName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlssdscertificate.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "secret_name": secret_name,
            }

        @builtins.property
        def secret_name(self) -> builtins.str:
            '''``CfnVirtualGateway.VirtualGatewayListenerTlsSdsCertificateProperty.SecretName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlssdscertificate.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlssdscertificate-secretname
            '''
            result = self._values.get("secret_name")
            assert result is not None, "Required property 'secret_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerTlsSdsCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextProperty",
        jsii_struct_bases=[],
        name_mapping={
            "trust": "trust",
            "subject_alternative_names": "subjectAlternativeNames",
        },
    )
    class VirtualGatewayListenerTlsValidationContextProperty:
        def __init__(
            self,
            *,
            trust: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextTrustProperty"],
            subject_alternative_names: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.SubjectAlternativeNamesProperty"]] = None,
        ) -> None:
            '''
            :param trust: ``CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextProperty.Trust``.
            :param subject_alternative_names: ``CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextProperty.SubjectAlternativeNames``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontext.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "trust": trust,
            }
            if subject_alternative_names is not None:
                self._values["subject_alternative_names"] = subject_alternative_names

        @builtins.property
        def trust(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextTrustProperty"]:
            '''``CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextProperty.Trust``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontext.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontext-trust
            '''
            result = self._values.get("trust")
            assert result is not None, "Required property 'trust' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextTrustProperty"], result)

        @builtins.property
        def subject_alternative_names(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.SubjectAlternativeNamesProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextProperty.SubjectAlternativeNames``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontext.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontext-subjectalternativenames
            '''
            result = self._values.get("subject_alternative_names")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.SubjectAlternativeNamesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerTlsValidationContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"file": "file", "sds": "sds"},
    )
    class VirtualGatewayListenerTlsValidationContextTrustProperty:
        def __init__(
            self,
            *,
            file: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextFileTrustProperty"]] = None,
            sds: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextSdsTrustProperty"]] = None,
        ) -> None:
            '''
            :param file: ``CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextTrustProperty.File``.
            :param sds: ``CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextTrustProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontexttrust.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextFileTrustProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextTrustProperty.File``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontexttrust.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontexttrust-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextFileTrustProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextSdsTrustProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayListenerTlsValidationContextTrustProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontexttrust.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontexttrust-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextSdsTrustProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerTlsValidationContextTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayLoggingProperty",
        jsii_struct_bases=[],
        name_mapping={"access_log": "accessLog"},
    )
    class VirtualGatewayLoggingProperty:
        def __init__(
            self,
            *,
            access_log: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayAccessLogProperty"]] = None,
        ) -> None:
            '''
            :param access_log: ``CfnVirtualGateway.VirtualGatewayLoggingProperty.AccessLog``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylogging.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if access_log is not None:
                self._values["access_log"] = access_log

        @builtins.property
        def access_log(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayAccessLogProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayLoggingProperty.AccessLog``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylogging.html#cfn-appmesh-virtualgateway-virtualgatewaylogging-accesslog
            '''
            result = self._values.get("access_log")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayAccessLogProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayLoggingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayPortMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"port": "port", "protocol": "protocol"},
    )
    class VirtualGatewayPortMappingProperty:
        def __init__(self, *, port: jsii.Number, protocol: builtins.str) -> None:
            '''
            :param port: ``CfnVirtualGateway.VirtualGatewayPortMappingProperty.Port``.
            :param protocol: ``CfnVirtualGateway.VirtualGatewayPortMappingProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayportmapping.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "port": port,
                "protocol": protocol,
            }

        @builtins.property
        def port(self) -> jsii.Number:
            '''``CfnVirtualGateway.VirtualGatewayPortMappingProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayportmapping.html#cfn-appmesh-virtualgateway-virtualgatewayportmapping-port
            '''
            result = self._values.get("port")
            assert result is not None, "Required property 'port' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def protocol(self) -> builtins.str:
            '''``CfnVirtualGateway.VirtualGatewayPortMappingProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayportmapping.html#cfn-appmesh-virtualgateway-virtualgatewayportmapping-protocol
            '''
            result = self._values.get("protocol")
            assert result is not None, "Required property 'protocol' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayPortMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewaySpecProperty",
        jsii_struct_bases=[],
        name_mapping={
            "listeners": "listeners",
            "backend_defaults": "backendDefaults",
            "logging": "logging",
        },
    )
    class VirtualGatewaySpecProperty:
        def __init__(
            self,
            *,
            listeners: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnVirtualGateway.VirtualGatewayListenerProperty", aws_cdk.core.IResolvable]]],
            backend_defaults: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayBackendDefaultsProperty"]] = None,
            logging: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayLoggingProperty"]] = None,
        ) -> None:
            '''
            :param listeners: ``CfnVirtualGateway.VirtualGatewaySpecProperty.Listeners``.
            :param backend_defaults: ``CfnVirtualGateway.VirtualGatewaySpecProperty.BackendDefaults``.
            :param logging: ``CfnVirtualGateway.VirtualGatewaySpecProperty.Logging``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayspec.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "listeners": listeners,
            }
            if backend_defaults is not None:
                self._values["backend_defaults"] = backend_defaults
            if logging is not None:
                self._values["logging"] = logging

        @builtins.property
        def listeners(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnVirtualGateway.VirtualGatewayListenerProperty", aws_cdk.core.IResolvable]]]:
            '''``CfnVirtualGateway.VirtualGatewaySpecProperty.Listeners``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayspec.html#cfn-appmesh-virtualgateway-virtualgatewayspec-listeners
            '''
            result = self._values.get("listeners")
            assert result is not None, "Required property 'listeners' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnVirtualGateway.VirtualGatewayListenerProperty", aws_cdk.core.IResolvable]]], result)

        @builtins.property
        def backend_defaults(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayBackendDefaultsProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewaySpecProperty.BackendDefaults``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayspec.html#cfn-appmesh-virtualgateway-virtualgatewayspec-backenddefaults
            '''
            result = self._values.get("backend_defaults")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayBackendDefaultsProperty"]], result)

        @builtins.property
        def logging(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayLoggingProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewaySpecProperty.Logging``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayspec.html#cfn-appmesh-virtualgateway-virtualgatewayspec-logging
            '''
            result = self._values.get("logging")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayLoggingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewaySpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayTlsValidationContextAcmTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_authority_arns": "certificateAuthorityArns"},
    )
    class VirtualGatewayTlsValidationContextAcmTrustProperty:
        def __init__(
            self,
            *,
            certificate_authority_arns: typing.List[builtins.str],
        ) -> None:
            '''
            :param certificate_authority_arns: ``CfnVirtualGateway.VirtualGatewayTlsValidationContextAcmTrustProperty.CertificateAuthorityArns``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextacmtrust.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "certificate_authority_arns": certificate_authority_arns,
            }

        @builtins.property
        def certificate_authority_arns(self) -> typing.List[builtins.str]:
            '''``CfnVirtualGateway.VirtualGatewayTlsValidationContextAcmTrustProperty.CertificateAuthorityArns``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextacmtrust.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextacmtrust-certificateauthorityarns
            '''
            result = self._values.get("certificate_authority_arns")
            assert result is not None, "Required property 'certificate_authority_arns' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayTlsValidationContextAcmTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayTlsValidationContextFileTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_chain": "certificateChain"},
    )
    class VirtualGatewayTlsValidationContextFileTrustProperty:
        def __init__(self, *, certificate_chain: builtins.str) -> None:
            '''
            :param certificate_chain: ``CfnVirtualGateway.VirtualGatewayTlsValidationContextFileTrustProperty.CertificateChain``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextfiletrust.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "certificate_chain": certificate_chain,
            }

        @builtins.property
        def certificate_chain(self) -> builtins.str:
            '''``CfnVirtualGateway.VirtualGatewayTlsValidationContextFileTrustProperty.CertificateChain``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextfiletrust.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextfiletrust-certificatechain
            '''
            result = self._values.get("certificate_chain")
            assert result is not None, "Required property 'certificate_chain' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayTlsValidationContextFileTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayTlsValidationContextProperty",
        jsii_struct_bases=[],
        name_mapping={
            "trust": "trust",
            "subject_alternative_names": "subjectAlternativeNames",
        },
    )
    class VirtualGatewayTlsValidationContextProperty:
        def __init__(
            self,
            *,
            trust: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextTrustProperty"],
            subject_alternative_names: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.SubjectAlternativeNamesProperty"]] = None,
        ) -> None:
            '''
            :param trust: ``CfnVirtualGateway.VirtualGatewayTlsValidationContextProperty.Trust``.
            :param subject_alternative_names: ``CfnVirtualGateway.VirtualGatewayTlsValidationContextProperty.SubjectAlternativeNames``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontext.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "trust": trust,
            }
            if subject_alternative_names is not None:
                self._values["subject_alternative_names"] = subject_alternative_names

        @builtins.property
        def trust(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextTrustProperty"]:
            '''``CfnVirtualGateway.VirtualGatewayTlsValidationContextProperty.Trust``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontext.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontext-trust
            '''
            result = self._values.get("trust")
            assert result is not None, "Required property 'trust' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextTrustProperty"], result)

        @builtins.property
        def subject_alternative_names(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.SubjectAlternativeNamesProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayTlsValidationContextProperty.SubjectAlternativeNames``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontext.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontext-subjectalternativenames
            '''
            result = self._values.get("subject_alternative_names")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.SubjectAlternativeNamesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayTlsValidationContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayTlsValidationContextSdsTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_name": "secretName"},
    )
    class VirtualGatewayTlsValidationContextSdsTrustProperty:
        def __init__(self, *, secret_name: builtins.str) -> None:
            '''
            :param secret_name: ``CfnVirtualGateway.VirtualGatewayTlsValidationContextSdsTrustProperty.SecretName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextsdstrust.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "secret_name": secret_name,
            }

        @builtins.property
        def secret_name(self) -> builtins.str:
            '''``CfnVirtualGateway.VirtualGatewayTlsValidationContextSdsTrustProperty.SecretName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextsdstrust.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextsdstrust-secretname
            '''
            result = self._values.get("secret_name")
            assert result is not None, "Required property 'secret_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayTlsValidationContextSdsTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGateway.VirtualGatewayTlsValidationContextTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"acm": "acm", "file": "file", "sds": "sds"},
    )
    class VirtualGatewayTlsValidationContextTrustProperty:
        def __init__(
            self,
            *,
            acm: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextAcmTrustProperty"]] = None,
            file: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextFileTrustProperty"]] = None,
            sds: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextSdsTrustProperty"]] = None,
        ) -> None:
            '''
            :param acm: ``CfnVirtualGateway.VirtualGatewayTlsValidationContextTrustProperty.ACM``.
            :param file: ``CfnVirtualGateway.VirtualGatewayTlsValidationContextTrustProperty.File``.
            :param sds: ``CfnVirtualGateway.VirtualGatewayTlsValidationContextTrustProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontexttrust.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if acm is not None:
                self._values["acm"] = acm
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def acm(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextAcmTrustProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayTlsValidationContextTrustProperty.ACM``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontexttrust.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontexttrust-acm
            '''
            result = self._values.get("acm")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextAcmTrustProperty"]], result)

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextFileTrustProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayTlsValidationContextTrustProperty.File``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontexttrust.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontexttrust-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextFileTrustProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextSdsTrustProperty"]]:
            '''``CfnVirtualGateway.VirtualGatewayTlsValidationContextTrustProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontexttrust.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontexttrust-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualGateway.VirtualGatewayTlsValidationContextSdsTrustProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayTlsValidationContextTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.CfnVirtualGatewayProps",
    jsii_struct_bases=[],
    name_mapping={
        "mesh_name": "meshName",
        "spec": "spec",
        "mesh_owner": "meshOwner",
        "tags": "tags",
        "virtual_gateway_name": "virtualGatewayName",
    },
)
class CfnVirtualGatewayProps:
    def __init__(
        self,
        *,
        mesh_name: builtins.str,
        spec: typing.Union[aws_cdk.core.IResolvable, CfnVirtualGateway.VirtualGatewaySpecProperty],
        mesh_owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        virtual_gateway_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::AppMesh::VirtualGateway``.

        :param mesh_name: ``AWS::AppMesh::VirtualGateway.MeshName``.
        :param spec: ``AWS::AppMesh::VirtualGateway.Spec``.
        :param mesh_owner: ``AWS::AppMesh::VirtualGateway.MeshOwner``.
        :param tags: ``AWS::AppMesh::VirtualGateway.Tags``.
        :param virtual_gateway_name: ``AWS::AppMesh::VirtualGateway.VirtualGatewayName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "mesh_name": mesh_name,
            "spec": spec,
        }
        if mesh_owner is not None:
            self._values["mesh_owner"] = mesh_owner
        if tags is not None:
            self._values["tags"] = tags
        if virtual_gateway_name is not None:
            self._values["virtual_gateway_name"] = virtual_gateway_name

    @builtins.property
    def mesh_name(self) -> builtins.str:
        '''``AWS::AppMesh::VirtualGateway.MeshName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-meshname
        '''
        result = self._values.get("mesh_name")
        assert result is not None, "Required property 'mesh_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnVirtualGateway.VirtualGatewaySpecProperty]:
        '''``AWS::AppMesh::VirtualGateway.Spec``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-spec
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, CfnVirtualGateway.VirtualGatewaySpecProperty], result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::VirtualGateway.MeshOwner``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-meshowner
        '''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::AppMesh::VirtualGateway.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    @builtins.property
    def virtual_gateway_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::VirtualGateway.VirtualGatewayName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-virtualgatewayname
        '''
        result = self._values.get("virtual_gateway_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVirtualGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnVirtualNode(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode",
):
    '''A CloudFormation ``AWS::AppMesh::VirtualNode``.

    :cloudformationResource: AWS::AppMesh::VirtualNode
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        mesh_name: builtins.str,
        spec: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeSpecProperty"],
        mesh_owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        virtual_node_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::AppMesh::VirtualNode``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param mesh_name: ``AWS::AppMesh::VirtualNode.MeshName``.
        :param spec: ``AWS::AppMesh::VirtualNode.Spec``.
        :param mesh_owner: ``AWS::AppMesh::VirtualNode.MeshOwner``.
        :param tags: ``AWS::AppMesh::VirtualNode.Tags``.
        :param virtual_node_name: ``AWS::AppMesh::VirtualNode.VirtualNodeName``.
        '''
        props = CfnVirtualNodeProps(
            mesh_name=mesh_name,
            spec=spec,
            mesh_owner=mesh_owner,
            tags=tags,
            virtual_node_name=virtual_node_name,
        )

        jsii.create(CfnVirtualNode, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrMeshName")
    def attr_mesh_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: MeshName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMeshName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrMeshOwner")
    def attr_mesh_owner(self) -> builtins.str:
        '''
        :cloudformationAttribute: MeshOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMeshOwner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrResourceOwner")
    def attr_resource_owner(self) -> builtins.str:
        '''
        :cloudformationAttribute: ResourceOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceOwner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrUid")
    def attr_uid(self) -> builtins.str:
        '''
        :cloudformationAttribute: Uid
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUid"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrVirtualNodeName")
    def attr_virtual_node_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: VirtualNodeName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVirtualNodeName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::AppMesh::VirtualNode.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> builtins.str:
        '''``AWS::AppMesh::VirtualNode.MeshName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-meshname
        '''
        return typing.cast(builtins.str, jsii.get(self, "meshName"))

    @mesh_name.setter
    def mesh_name(self, value: builtins.str) -> None:
        jsii.set(self, "meshName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="spec")
    def spec(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeSpecProperty"]:
        '''``AWS::AppMesh::VirtualNode.Spec``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-spec
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeSpecProperty"], jsii.get(self, "spec"))

    @spec.setter
    def spec(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeSpecProperty"],
    ) -> None:
        jsii.set(self, "spec", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshOwner")
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::VirtualNode.MeshOwner``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-meshowner
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "meshOwner"))

    @mesh_owner.setter
    def mesh_owner(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "meshOwner", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualNodeName")
    def virtual_node_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::VirtualNode.VirtualNodeName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-virtualnodename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNodeName"))

    @virtual_node_name.setter
    def virtual_node_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "virtualNodeName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.AccessLogProperty",
        jsii_struct_bases=[],
        name_mapping={"file": "file"},
    )
    class AccessLogProperty:
        def __init__(
            self,
            *,
            file: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.FileAccessLogProperty"]] = None,
        ) -> None:
            '''
            :param file: ``CfnVirtualNode.AccessLogProperty.File``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-accesslog.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if file is not None:
                self._values["file"] = file

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.FileAccessLogProperty"]]:
            '''``CfnVirtualNode.AccessLogProperty.File``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-accesslog.html#cfn-appmesh-virtualnode-accesslog-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.FileAccessLogProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.AwsCloudMapInstanceAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class AwsCloudMapInstanceAttributeProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: ``CfnVirtualNode.AwsCloudMapInstanceAttributeProperty.Key``.
            :param value: ``CfnVirtualNode.AwsCloudMapInstanceAttributeProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapinstanceattribute.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnVirtualNode.AwsCloudMapInstanceAttributeProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapinstanceattribute.html#cfn-appmesh-virtualnode-awscloudmapinstanceattribute-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnVirtualNode.AwsCloudMapInstanceAttributeProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapinstanceattribute.html#cfn-appmesh-virtualnode-awscloudmapinstanceattribute-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsCloudMapInstanceAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "namespace_name": "namespaceName",
            "service_name": "serviceName",
            "attributes": "attributes",
        },
    )
    class AwsCloudMapServiceDiscoveryProperty:
        def __init__(
            self,
            *,
            namespace_name: builtins.str,
            service_name: builtins.str,
            attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.AwsCloudMapInstanceAttributeProperty"]]]] = None,
        ) -> None:
            '''
            :param namespace_name: ``CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty.NamespaceName``.
            :param service_name: ``CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty.ServiceName``.
            :param attributes: ``CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty.Attributes``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapservicediscovery.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "namespace_name": namespace_name,
                "service_name": service_name,
            }
            if attributes is not None:
                self._values["attributes"] = attributes

        @builtins.property
        def namespace_name(self) -> builtins.str:
            '''``CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty.NamespaceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapservicediscovery.html#cfn-appmesh-virtualnode-awscloudmapservicediscovery-namespacename
            '''
            result = self._values.get("namespace_name")
            assert result is not None, "Required property 'namespace_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def service_name(self) -> builtins.str:
            '''``CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty.ServiceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapservicediscovery.html#cfn-appmesh-virtualnode-awscloudmapservicediscovery-servicename
            '''
            result = self._values.get("service_name")
            assert result is not None, "Required property 'service_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.AwsCloudMapInstanceAttributeProperty"]]]]:
            '''``CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty.Attributes``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapservicediscovery.html#cfn-appmesh-virtualnode-awscloudmapservicediscovery-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.AwsCloudMapInstanceAttributeProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsCloudMapServiceDiscoveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.BackendDefaultsProperty",
        jsii_struct_bases=[],
        name_mapping={"client_policy": "clientPolicy"},
    )
    class BackendDefaultsProperty:
        def __init__(
            self,
            *,
            client_policy: typing.Optional[typing.Union["CfnVirtualNode.ClientPolicyProperty", aws_cdk.core.IResolvable]] = None,
        ) -> None:
            '''
            :param client_policy: ``CfnVirtualNode.BackendDefaultsProperty.ClientPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-backenddefaults.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if client_policy is not None:
                self._values["client_policy"] = client_policy

        @builtins.property
        def client_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnVirtualNode.ClientPolicyProperty", aws_cdk.core.IResolvable]]:
            '''``CfnVirtualNode.BackendDefaultsProperty.ClientPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-backenddefaults.html#cfn-appmesh-virtualnode-backenddefaults-clientpolicy
            '''
            result = self._values.get("client_policy")
            return typing.cast(typing.Optional[typing.Union["CfnVirtualNode.ClientPolicyProperty", aws_cdk.core.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BackendDefaultsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.BackendProperty",
        jsii_struct_bases=[],
        name_mapping={"virtual_service": "virtualService"},
    )
    class BackendProperty:
        def __init__(
            self,
            *,
            virtual_service: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualServiceBackendProperty"]] = None,
        ) -> None:
            '''
            :param virtual_service: ``CfnVirtualNode.BackendProperty.VirtualService``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-backend.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if virtual_service is not None:
                self._values["virtual_service"] = virtual_service

        @builtins.property
        def virtual_service(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualServiceBackendProperty"]]:
            '''``CfnVirtualNode.BackendProperty.VirtualService``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-backend.html#cfn-appmesh-virtualnode-backend-virtualservice
            '''
            result = self._values.get("virtual_service")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualServiceBackendProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BackendProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ClientPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"tls": "tls"},
    )
    class ClientPolicyProperty:
        def __init__(
            self,
            *,
            tls: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ClientPolicyTlsProperty"]] = None,
        ) -> None:
            '''
            :param tls: ``CfnVirtualNode.ClientPolicyProperty.TLS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicy.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if tls is not None:
                self._values["tls"] = tls

        @builtins.property
        def tls(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ClientPolicyTlsProperty"]]:
            '''``CfnVirtualNode.ClientPolicyProperty.TLS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicy.html#cfn-appmesh-virtualnode-clientpolicy-tls
            '''
            result = self._values.get("tls")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ClientPolicyTlsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClientPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ClientPolicyTlsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "validation": "validation",
            "certificate": "certificate",
            "enforce": "enforce",
            "ports": "ports",
        },
    )
    class ClientPolicyTlsProperty:
        def __init__(
            self,
            *,
            validation: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextProperty"],
            certificate: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ClientTlsCertificateProperty"]] = None,
            enforce: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            ports: typing.Optional[typing.Union[typing.List[jsii.Number], aws_cdk.core.IResolvable]] = None,
        ) -> None:
            '''
            :param validation: ``CfnVirtualNode.ClientPolicyTlsProperty.Validation``.
            :param certificate: ``CfnVirtualNode.ClientPolicyTlsProperty.Certificate``.
            :param enforce: ``CfnVirtualNode.ClientPolicyTlsProperty.Enforce``.
            :param ports: ``CfnVirtualNode.ClientPolicyTlsProperty.Ports``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicytls.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "validation": validation,
            }
            if certificate is not None:
                self._values["certificate"] = certificate
            if enforce is not None:
                self._values["enforce"] = enforce
            if ports is not None:
                self._values["ports"] = ports

        @builtins.property
        def validation(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextProperty"]:
            '''``CfnVirtualNode.ClientPolicyTlsProperty.Validation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicytls.html#cfn-appmesh-virtualnode-clientpolicytls-validation
            '''
            result = self._values.get("validation")
            assert result is not None, "Required property 'validation' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextProperty"], result)

        @builtins.property
        def certificate(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ClientTlsCertificateProperty"]]:
            '''``CfnVirtualNode.ClientPolicyTlsProperty.Certificate``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicytls.html#cfn-appmesh-virtualnode-clientpolicytls-certificate
            '''
            result = self._values.get("certificate")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ClientTlsCertificateProperty"]], result)

        @builtins.property
        def enforce(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''``CfnVirtualNode.ClientPolicyTlsProperty.Enforce``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicytls.html#cfn-appmesh-virtualnode-clientpolicytls-enforce
            '''
            result = self._values.get("enforce")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def ports(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], aws_cdk.core.IResolvable]]:
            '''``CfnVirtualNode.ClientPolicyTlsProperty.Ports``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicytls.html#cfn-appmesh-virtualnode-clientpolicytls-ports
            '''
            result = self._values.get("ports")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], aws_cdk.core.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClientPolicyTlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ClientTlsCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"file": "file", "sds": "sds"},
    )
    class ClientTlsCertificateProperty:
        def __init__(
            self,
            *,
            file: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsFileCertificateProperty"]] = None,
            sds: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsSdsCertificateProperty"]] = None,
        ) -> None:
            '''
            :param file: ``CfnVirtualNode.ClientTlsCertificateProperty.File``.
            :param sds: ``CfnVirtualNode.ClientTlsCertificateProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clienttlscertificate.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsFileCertificateProperty"]]:
            '''``CfnVirtualNode.ClientTlsCertificateProperty.File``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clienttlscertificate.html#cfn-appmesh-virtualnode-clienttlscertificate-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsFileCertificateProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsSdsCertificateProperty"]]:
            '''``CfnVirtualNode.ClientTlsCertificateProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clienttlscertificate.html#cfn-appmesh-virtualnode-clienttlscertificate-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsSdsCertificateProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClientTlsCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.DnsServiceDiscoveryProperty",
        jsii_struct_bases=[],
        name_mapping={"hostname": "hostname"},
    )
    class DnsServiceDiscoveryProperty:
        def __init__(self, *, hostname: builtins.str) -> None:
            '''
            :param hostname: ``CfnVirtualNode.DnsServiceDiscoveryProperty.Hostname``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-dnsservicediscovery.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "hostname": hostname,
            }

        @builtins.property
        def hostname(self) -> builtins.str:
            '''``CfnVirtualNode.DnsServiceDiscoveryProperty.Hostname``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-dnsservicediscovery.html#cfn-appmesh-virtualnode-dnsservicediscovery-hostname
            '''
            result = self._values.get("hostname")
            assert result is not None, "Required property 'hostname' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsServiceDiscoveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.DurationProperty",
        jsii_struct_bases=[],
        name_mapping={"unit": "unit", "value": "value"},
    )
    class DurationProperty:
        def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
            '''
            :param unit: ``CfnVirtualNode.DurationProperty.Unit``.
            :param value: ``CfnVirtualNode.DurationProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-duration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "unit": unit,
                "value": value,
            }

        @builtins.property
        def unit(self) -> builtins.str:
            '''``CfnVirtualNode.DurationProperty.Unit``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-duration.html#cfn-appmesh-virtualnode-duration-unit
            '''
            result = self._values.get("unit")
            assert result is not None, "Required property 'unit' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> jsii.Number:
            '''``CfnVirtualNode.DurationProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-duration.html#cfn-appmesh-virtualnode-duration-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.FileAccessLogProperty",
        jsii_struct_bases=[],
        name_mapping={"path": "path"},
    )
    class FileAccessLogProperty:
        def __init__(self, *, path: builtins.str) -> None:
            '''
            :param path: ``CfnVirtualNode.FileAccessLogProperty.Path``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-fileaccesslog.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "path": path,
            }

        @builtins.property
        def path(self) -> builtins.str:
            '''``CfnVirtualNode.FileAccessLogProperty.Path``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-fileaccesslog.html#cfn-appmesh-virtualnode-fileaccesslog-path
            '''
            result = self._values.get("path")
            assert result is not None, "Required property 'path' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FileAccessLogProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.GrpcTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"idle": "idle", "per_request": "perRequest"},
    )
    class GrpcTimeoutProperty:
        def __init__(
            self,
            *,
            idle: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]] = None,
            per_request: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]] = None,
        ) -> None:
            '''
            :param idle: ``CfnVirtualNode.GrpcTimeoutProperty.Idle``.
            :param per_request: ``CfnVirtualNode.GrpcTimeoutProperty.PerRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-grpctimeout.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if idle is not None:
                self._values["idle"] = idle
            if per_request is not None:
                self._values["per_request"] = per_request

        @builtins.property
        def idle(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]]:
            '''``CfnVirtualNode.GrpcTimeoutProperty.Idle``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-grpctimeout.html#cfn-appmesh-virtualnode-grpctimeout-idle
            '''
            result = self._values.get("idle")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]], result)

        @builtins.property
        def per_request(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]]:
            '''``CfnVirtualNode.GrpcTimeoutProperty.PerRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-grpctimeout.html#cfn-appmesh-virtualnode-grpctimeout-perrequest
            '''
            result = self._values.get("per_request")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.HealthCheckProperty",
        jsii_struct_bases=[],
        name_mapping={
            "healthy_threshold": "healthyThreshold",
            "interval_millis": "intervalMillis",
            "protocol": "protocol",
            "timeout_millis": "timeoutMillis",
            "unhealthy_threshold": "unhealthyThreshold",
            "path": "path",
            "port": "port",
        },
    )
    class HealthCheckProperty:
        def __init__(
            self,
            *,
            healthy_threshold: jsii.Number,
            interval_millis: jsii.Number,
            protocol: builtins.str,
            timeout_millis: jsii.Number,
            unhealthy_threshold: jsii.Number,
            path: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param healthy_threshold: ``CfnVirtualNode.HealthCheckProperty.HealthyThreshold``.
            :param interval_millis: ``CfnVirtualNode.HealthCheckProperty.IntervalMillis``.
            :param protocol: ``CfnVirtualNode.HealthCheckProperty.Protocol``.
            :param timeout_millis: ``CfnVirtualNode.HealthCheckProperty.TimeoutMillis``.
            :param unhealthy_threshold: ``CfnVirtualNode.HealthCheckProperty.UnhealthyThreshold``.
            :param path: ``CfnVirtualNode.HealthCheckProperty.Path``.
            :param port: ``CfnVirtualNode.HealthCheckProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "healthy_threshold": healthy_threshold,
                "interval_millis": interval_millis,
                "protocol": protocol,
                "timeout_millis": timeout_millis,
                "unhealthy_threshold": unhealthy_threshold,
            }
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def healthy_threshold(self) -> jsii.Number:
            '''``CfnVirtualNode.HealthCheckProperty.HealthyThreshold``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-healthythreshold
            '''
            result = self._values.get("healthy_threshold")
            assert result is not None, "Required property 'healthy_threshold' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def interval_millis(self) -> jsii.Number:
            '''``CfnVirtualNode.HealthCheckProperty.IntervalMillis``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-intervalmillis
            '''
            result = self._values.get("interval_millis")
            assert result is not None, "Required property 'interval_millis' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def protocol(self) -> builtins.str:
            '''``CfnVirtualNode.HealthCheckProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-protocol
            '''
            result = self._values.get("protocol")
            assert result is not None, "Required property 'protocol' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def timeout_millis(self) -> jsii.Number:
            '''``CfnVirtualNode.HealthCheckProperty.TimeoutMillis``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-timeoutmillis
            '''
            result = self._values.get("timeout_millis")
            assert result is not None, "Required property 'timeout_millis' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def unhealthy_threshold(self) -> jsii.Number:
            '''``CfnVirtualNode.HealthCheckProperty.UnhealthyThreshold``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-unhealthythreshold
            '''
            result = self._values.get("unhealthy_threshold")
            assert result is not None, "Required property 'unhealthy_threshold' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''``CfnVirtualNode.HealthCheckProperty.Path``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''``CfnVirtualNode.HealthCheckProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.HttpTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"idle": "idle", "per_request": "perRequest"},
    )
    class HttpTimeoutProperty:
        def __init__(
            self,
            *,
            idle: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]] = None,
            per_request: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]] = None,
        ) -> None:
            '''
            :param idle: ``CfnVirtualNode.HttpTimeoutProperty.Idle``.
            :param per_request: ``CfnVirtualNode.HttpTimeoutProperty.PerRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-httptimeout.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if idle is not None:
                self._values["idle"] = idle
            if per_request is not None:
                self._values["per_request"] = per_request

        @builtins.property
        def idle(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]]:
            '''``CfnVirtualNode.HttpTimeoutProperty.Idle``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-httptimeout.html#cfn-appmesh-virtualnode-httptimeout-idle
            '''
            result = self._values.get("idle")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]], result)

        @builtins.property
        def per_request(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]]:
            '''``CfnVirtualNode.HttpTimeoutProperty.PerRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-httptimeout.html#cfn-appmesh-virtualnode-httptimeout-perrequest
            '''
            result = self._values.get("per_request")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ListenerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "port_mapping": "portMapping",
            "connection_pool": "connectionPool",
            "health_check": "healthCheck",
            "outlier_detection": "outlierDetection",
            "timeout": "timeout",
            "tls": "tls",
        },
    )
    class ListenerProperty:
        def __init__(
            self,
            *,
            port_mapping: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.PortMappingProperty"],
            connection_pool: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeConnectionPoolProperty"]] = None,
            health_check: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.HealthCheckProperty"]] = None,
            outlier_detection: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.OutlierDetectionProperty"]] = None,
            timeout: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTimeoutProperty"]] = None,
            tls: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsProperty"]] = None,
        ) -> None:
            '''
            :param port_mapping: ``CfnVirtualNode.ListenerProperty.PortMapping``.
            :param connection_pool: ``CfnVirtualNode.ListenerProperty.ConnectionPool``.
            :param health_check: ``CfnVirtualNode.ListenerProperty.HealthCheck``.
            :param outlier_detection: ``CfnVirtualNode.ListenerProperty.OutlierDetection``.
            :param timeout: ``CfnVirtualNode.ListenerProperty.Timeout``.
            :param tls: ``CfnVirtualNode.ListenerProperty.TLS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "port_mapping": port_mapping,
            }
            if connection_pool is not None:
                self._values["connection_pool"] = connection_pool
            if health_check is not None:
                self._values["health_check"] = health_check
            if outlier_detection is not None:
                self._values["outlier_detection"] = outlier_detection
            if timeout is not None:
                self._values["timeout"] = timeout
            if tls is not None:
                self._values["tls"] = tls

        @builtins.property
        def port_mapping(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.PortMappingProperty"]:
            '''``CfnVirtualNode.ListenerProperty.PortMapping``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-portmapping
            '''
            result = self._values.get("port_mapping")
            assert result is not None, "Required property 'port_mapping' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.PortMappingProperty"], result)

        @builtins.property
        def connection_pool(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeConnectionPoolProperty"]]:
            '''``CfnVirtualNode.ListenerProperty.ConnectionPool``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-connectionpool
            '''
            result = self._values.get("connection_pool")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeConnectionPoolProperty"]], result)

        @builtins.property
        def health_check(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.HealthCheckProperty"]]:
            '''``CfnVirtualNode.ListenerProperty.HealthCheck``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-healthcheck
            '''
            result = self._values.get("health_check")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.HealthCheckProperty"]], result)

        @builtins.property
        def outlier_detection(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.OutlierDetectionProperty"]]:
            '''``CfnVirtualNode.ListenerProperty.OutlierDetection``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-outlierdetection
            '''
            result = self._values.get("outlier_detection")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.OutlierDetectionProperty"]], result)

        @builtins.property
        def timeout(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTimeoutProperty"]]:
            '''``CfnVirtualNode.ListenerProperty.Timeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTimeoutProperty"]], result)

        @builtins.property
        def tls(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsProperty"]]:
            '''``CfnVirtualNode.ListenerProperty.TLS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-tls
            '''
            result = self._values.get("tls")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ListenerTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"grpc": "grpc", "http": "http", "http2": "http2", "tcp": "tcp"},
    )
    class ListenerTimeoutProperty:
        def __init__(
            self,
            *,
            grpc: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.GrpcTimeoutProperty"]] = None,
            http: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.HttpTimeoutProperty"]] = None,
            http2: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.HttpTimeoutProperty"]] = None,
            tcp: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TcpTimeoutProperty"]] = None,
        ) -> None:
            '''
            :param grpc: ``CfnVirtualNode.ListenerTimeoutProperty.GRPC``.
            :param http: ``CfnVirtualNode.ListenerTimeoutProperty.HTTP``.
            :param http2: ``CfnVirtualNode.ListenerTimeoutProperty.HTTP2``.
            :param tcp: ``CfnVirtualNode.ListenerTimeoutProperty.TCP``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertimeout.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if grpc is not None:
                self._values["grpc"] = grpc
            if http is not None:
                self._values["http"] = http
            if http2 is not None:
                self._values["http2"] = http2
            if tcp is not None:
                self._values["tcp"] = tcp

        @builtins.property
        def grpc(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.GrpcTimeoutProperty"]]:
            '''``CfnVirtualNode.ListenerTimeoutProperty.GRPC``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertimeout.html#cfn-appmesh-virtualnode-listenertimeout-grpc
            '''
            result = self._values.get("grpc")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.GrpcTimeoutProperty"]], result)

        @builtins.property
        def http(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.HttpTimeoutProperty"]]:
            '''``CfnVirtualNode.ListenerTimeoutProperty.HTTP``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertimeout.html#cfn-appmesh-virtualnode-listenertimeout-http
            '''
            result = self._values.get("http")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.HttpTimeoutProperty"]], result)

        @builtins.property
        def http2(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.HttpTimeoutProperty"]]:
            '''``CfnVirtualNode.ListenerTimeoutProperty.HTTP2``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertimeout.html#cfn-appmesh-virtualnode-listenertimeout-http2
            '''
            result = self._values.get("http2")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.HttpTimeoutProperty"]], result)

        @builtins.property
        def tcp(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TcpTimeoutProperty"]]:
            '''``CfnVirtualNode.ListenerTimeoutProperty.TCP``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertimeout.html#cfn-appmesh-virtualnode-listenertimeout-tcp
            '''
            result = self._values.get("tcp")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TcpTimeoutProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ListenerTlsAcmCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_arn": "certificateArn"},
    )
    class ListenerTlsAcmCertificateProperty:
        def __init__(self, *, certificate_arn: builtins.str) -> None:
            '''
            :param certificate_arn: ``CfnVirtualNode.ListenerTlsAcmCertificateProperty.CertificateArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsacmcertificate.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "certificate_arn": certificate_arn,
            }

        @builtins.property
        def certificate_arn(self) -> builtins.str:
            '''``CfnVirtualNode.ListenerTlsAcmCertificateProperty.CertificateArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsacmcertificate.html#cfn-appmesh-virtualnode-listenertlsacmcertificate-certificatearn
            '''
            result = self._values.get("certificate_arn")
            assert result is not None, "Required property 'certificate_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTlsAcmCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ListenerTlsCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"acm": "acm", "file": "file", "sds": "sds"},
    )
    class ListenerTlsCertificateProperty:
        def __init__(
            self,
            *,
            acm: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsAcmCertificateProperty"]] = None,
            file: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsFileCertificateProperty"]] = None,
            sds: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsSdsCertificateProperty"]] = None,
        ) -> None:
            '''
            :param acm: ``CfnVirtualNode.ListenerTlsCertificateProperty.ACM``.
            :param file: ``CfnVirtualNode.ListenerTlsCertificateProperty.File``.
            :param sds: ``CfnVirtualNode.ListenerTlsCertificateProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlscertificate.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if acm is not None:
                self._values["acm"] = acm
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def acm(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsAcmCertificateProperty"]]:
            '''``CfnVirtualNode.ListenerTlsCertificateProperty.ACM``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlscertificate.html#cfn-appmesh-virtualnode-listenertlscertificate-acm
            '''
            result = self._values.get("acm")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsAcmCertificateProperty"]], result)

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsFileCertificateProperty"]]:
            '''``CfnVirtualNode.ListenerTlsCertificateProperty.File``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlscertificate.html#cfn-appmesh-virtualnode-listenertlscertificate-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsFileCertificateProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsSdsCertificateProperty"]]:
            '''``CfnVirtualNode.ListenerTlsCertificateProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlscertificate.html#cfn-appmesh-virtualnode-listenertlscertificate-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsSdsCertificateProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTlsCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ListenerTlsFileCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_chain": "certificateChain",
            "private_key": "privateKey",
        },
    )
    class ListenerTlsFileCertificateProperty:
        def __init__(
            self,
            *,
            certificate_chain: builtins.str,
            private_key: builtins.str,
        ) -> None:
            '''
            :param certificate_chain: ``CfnVirtualNode.ListenerTlsFileCertificateProperty.CertificateChain``.
            :param private_key: ``CfnVirtualNode.ListenerTlsFileCertificateProperty.PrivateKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsfilecertificate.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "certificate_chain": certificate_chain,
                "private_key": private_key,
            }

        @builtins.property
        def certificate_chain(self) -> builtins.str:
            '''``CfnVirtualNode.ListenerTlsFileCertificateProperty.CertificateChain``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsfilecertificate.html#cfn-appmesh-virtualnode-listenertlsfilecertificate-certificatechain
            '''
            result = self._values.get("certificate_chain")
            assert result is not None, "Required property 'certificate_chain' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def private_key(self) -> builtins.str:
            '''``CfnVirtualNode.ListenerTlsFileCertificateProperty.PrivateKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsfilecertificate.html#cfn-appmesh-virtualnode-listenertlsfilecertificate-privatekey
            '''
            result = self._values.get("private_key")
            assert result is not None, "Required property 'private_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTlsFileCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ListenerTlsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate": "certificate",
            "mode": "mode",
            "validation": "validation",
        },
    )
    class ListenerTlsProperty:
        def __init__(
            self,
            *,
            certificate: typing.Union["CfnVirtualNode.ListenerTlsCertificateProperty", aws_cdk.core.IResolvable],
            mode: builtins.str,
            validation: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsValidationContextProperty"]] = None,
        ) -> None:
            '''
            :param certificate: ``CfnVirtualNode.ListenerTlsProperty.Certificate``.
            :param mode: ``CfnVirtualNode.ListenerTlsProperty.Mode``.
            :param validation: ``CfnVirtualNode.ListenerTlsProperty.Validation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertls.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "certificate": certificate,
                "mode": mode,
            }
            if validation is not None:
                self._values["validation"] = validation

        @builtins.property
        def certificate(
            self,
        ) -> typing.Union["CfnVirtualNode.ListenerTlsCertificateProperty", aws_cdk.core.IResolvable]:
            '''``CfnVirtualNode.ListenerTlsProperty.Certificate``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertls.html#cfn-appmesh-virtualnode-listenertls-certificate
            '''
            result = self._values.get("certificate")
            assert result is not None, "Required property 'certificate' is missing"
            return typing.cast(typing.Union["CfnVirtualNode.ListenerTlsCertificateProperty", aws_cdk.core.IResolvable], result)

        @builtins.property
        def mode(self) -> builtins.str:
            '''``CfnVirtualNode.ListenerTlsProperty.Mode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertls.html#cfn-appmesh-virtualnode-listenertls-mode
            '''
            result = self._values.get("mode")
            assert result is not None, "Required property 'mode' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def validation(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsValidationContextProperty"]]:
            '''``CfnVirtualNode.ListenerTlsProperty.Validation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertls.html#cfn-appmesh-virtualnode-listenertls-validation
            '''
            result = self._values.get("validation")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsValidationContextProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ListenerTlsSdsCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_name": "secretName"},
    )
    class ListenerTlsSdsCertificateProperty:
        def __init__(self, *, secret_name: builtins.str) -> None:
            '''
            :param secret_name: ``CfnVirtualNode.ListenerTlsSdsCertificateProperty.SecretName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlssdscertificate.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "secret_name": secret_name,
            }

        @builtins.property
        def secret_name(self) -> builtins.str:
            '''``CfnVirtualNode.ListenerTlsSdsCertificateProperty.SecretName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlssdscertificate.html#cfn-appmesh-virtualnode-listenertlssdscertificate-secretname
            '''
            result = self._values.get("secret_name")
            assert result is not None, "Required property 'secret_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTlsSdsCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ListenerTlsValidationContextProperty",
        jsii_struct_bases=[],
        name_mapping={
            "trust": "trust",
            "subject_alternative_names": "subjectAlternativeNames",
        },
    )
    class ListenerTlsValidationContextProperty:
        def __init__(
            self,
            *,
            trust: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsValidationContextTrustProperty"],
            subject_alternative_names: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.SubjectAlternativeNamesProperty"]] = None,
        ) -> None:
            '''
            :param trust: ``CfnVirtualNode.ListenerTlsValidationContextProperty.Trust``.
            :param subject_alternative_names: ``CfnVirtualNode.ListenerTlsValidationContextProperty.SubjectAlternativeNames``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsvalidationcontext.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "trust": trust,
            }
            if subject_alternative_names is not None:
                self._values["subject_alternative_names"] = subject_alternative_names

        @builtins.property
        def trust(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsValidationContextTrustProperty"]:
            '''``CfnVirtualNode.ListenerTlsValidationContextProperty.Trust``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsvalidationcontext.html#cfn-appmesh-virtualnode-listenertlsvalidationcontext-trust
            '''
            result = self._values.get("trust")
            assert result is not None, "Required property 'trust' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ListenerTlsValidationContextTrustProperty"], result)

        @builtins.property
        def subject_alternative_names(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.SubjectAlternativeNamesProperty"]]:
            '''``CfnVirtualNode.ListenerTlsValidationContextProperty.SubjectAlternativeNames``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsvalidationcontext.html#cfn-appmesh-virtualnode-listenertlsvalidationcontext-subjectalternativenames
            '''
            result = self._values.get("subject_alternative_names")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.SubjectAlternativeNamesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTlsValidationContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ListenerTlsValidationContextTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"file": "file", "sds": "sds"},
    )
    class ListenerTlsValidationContextTrustProperty:
        def __init__(
            self,
            *,
            file: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextFileTrustProperty"]] = None,
            sds: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextSdsTrustProperty"]] = None,
        ) -> None:
            '''
            :param file: ``CfnVirtualNode.ListenerTlsValidationContextTrustProperty.File``.
            :param sds: ``CfnVirtualNode.ListenerTlsValidationContextTrustProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsvalidationcontexttrust.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextFileTrustProperty"]]:
            '''``CfnVirtualNode.ListenerTlsValidationContextTrustProperty.File``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsvalidationcontexttrust.html#cfn-appmesh-virtualnode-listenertlsvalidationcontexttrust-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextFileTrustProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextSdsTrustProperty"]]:
            '''``CfnVirtualNode.ListenerTlsValidationContextTrustProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsvalidationcontexttrust.html#cfn-appmesh-virtualnode-listenertlsvalidationcontexttrust-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextSdsTrustProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTlsValidationContextTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.LoggingProperty",
        jsii_struct_bases=[],
        name_mapping={"access_log": "accessLog"},
    )
    class LoggingProperty:
        def __init__(
            self,
            *,
            access_log: typing.Optional[typing.Union["CfnVirtualNode.AccessLogProperty", aws_cdk.core.IResolvable]] = None,
        ) -> None:
            '''
            :param access_log: ``CfnVirtualNode.LoggingProperty.AccessLog``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-logging.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if access_log is not None:
                self._values["access_log"] = access_log

        @builtins.property
        def access_log(
            self,
        ) -> typing.Optional[typing.Union["CfnVirtualNode.AccessLogProperty", aws_cdk.core.IResolvable]]:
            '''``CfnVirtualNode.LoggingProperty.AccessLog``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-logging.html#cfn-appmesh-virtualnode-logging-accesslog
            '''
            result = self._values.get("access_log")
            return typing.cast(typing.Optional[typing.Union["CfnVirtualNode.AccessLogProperty", aws_cdk.core.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.OutlierDetectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base_ejection_duration": "baseEjectionDuration",
            "interval": "interval",
            "max_ejection_percent": "maxEjectionPercent",
            "max_server_errors": "maxServerErrors",
        },
    )
    class OutlierDetectionProperty:
        def __init__(
            self,
            *,
            base_ejection_duration: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"],
            interval: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"],
            max_ejection_percent: jsii.Number,
            max_server_errors: jsii.Number,
        ) -> None:
            '''
            :param base_ejection_duration: ``CfnVirtualNode.OutlierDetectionProperty.BaseEjectionDuration``.
            :param interval: ``CfnVirtualNode.OutlierDetectionProperty.Interval``.
            :param max_ejection_percent: ``CfnVirtualNode.OutlierDetectionProperty.MaxEjectionPercent``.
            :param max_server_errors: ``CfnVirtualNode.OutlierDetectionProperty.MaxServerErrors``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-outlierdetection.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "base_ejection_duration": base_ejection_duration,
                "interval": interval,
                "max_ejection_percent": max_ejection_percent,
                "max_server_errors": max_server_errors,
            }

        @builtins.property
        def base_ejection_duration(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]:
            '''``CfnVirtualNode.OutlierDetectionProperty.BaseEjectionDuration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-outlierdetection.html#cfn-appmesh-virtualnode-outlierdetection-baseejectionduration
            '''
            result = self._values.get("base_ejection_duration")
            assert result is not None, "Required property 'base_ejection_duration' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"], result)

        @builtins.property
        def interval(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]:
            '''``CfnVirtualNode.OutlierDetectionProperty.Interval``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-outlierdetection.html#cfn-appmesh-virtualnode-outlierdetection-interval
            '''
            result = self._values.get("interval")
            assert result is not None, "Required property 'interval' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"], result)

        @builtins.property
        def max_ejection_percent(self) -> jsii.Number:
            '''``CfnVirtualNode.OutlierDetectionProperty.MaxEjectionPercent``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-outlierdetection.html#cfn-appmesh-virtualnode-outlierdetection-maxejectionpercent
            '''
            result = self._values.get("max_ejection_percent")
            assert result is not None, "Required property 'max_ejection_percent' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def max_server_errors(self) -> jsii.Number:
            '''``CfnVirtualNode.OutlierDetectionProperty.MaxServerErrors``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-outlierdetection.html#cfn-appmesh-virtualnode-outlierdetection-maxservererrors
            '''
            result = self._values.get("max_server_errors")
            assert result is not None, "Required property 'max_server_errors' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutlierDetectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.PortMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"port": "port", "protocol": "protocol"},
    )
    class PortMappingProperty:
        def __init__(self, *, port: jsii.Number, protocol: builtins.str) -> None:
            '''
            :param port: ``CfnVirtualNode.PortMappingProperty.Port``.
            :param protocol: ``CfnVirtualNode.PortMappingProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-portmapping.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "port": port,
                "protocol": protocol,
            }

        @builtins.property
        def port(self) -> jsii.Number:
            '''``CfnVirtualNode.PortMappingProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-portmapping.html#cfn-appmesh-virtualnode-portmapping-port
            '''
            result = self._values.get("port")
            assert result is not None, "Required property 'port' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def protocol(self) -> builtins.str:
            '''``CfnVirtualNode.PortMappingProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-portmapping.html#cfn-appmesh-virtualnode-portmapping-protocol
            '''
            result = self._values.get("protocol")
            assert result is not None, "Required property 'protocol' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ServiceDiscoveryProperty",
        jsii_struct_bases=[],
        name_mapping={"aws_cloud_map": "awsCloudMap", "dns": "dns"},
    )
    class ServiceDiscoveryProperty:
        def __init__(
            self,
            *,
            aws_cloud_map: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty"]] = None,
            dns: typing.Optional[typing.Union["CfnVirtualNode.DnsServiceDiscoveryProperty", aws_cdk.core.IResolvable]] = None,
        ) -> None:
            '''
            :param aws_cloud_map: ``CfnVirtualNode.ServiceDiscoveryProperty.AWSCloudMap``.
            :param dns: ``CfnVirtualNode.ServiceDiscoveryProperty.DNS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-servicediscovery.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if aws_cloud_map is not None:
                self._values["aws_cloud_map"] = aws_cloud_map
            if dns is not None:
                self._values["dns"] = dns

        @builtins.property
        def aws_cloud_map(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty"]]:
            '''``CfnVirtualNode.ServiceDiscoveryProperty.AWSCloudMap``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-servicediscovery.html#cfn-appmesh-virtualnode-servicediscovery-awscloudmap
            '''
            result = self._values.get("aws_cloud_map")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty"]], result)

        @builtins.property
        def dns(
            self,
        ) -> typing.Optional[typing.Union["CfnVirtualNode.DnsServiceDiscoveryProperty", aws_cdk.core.IResolvable]]:
            '''``CfnVirtualNode.ServiceDiscoveryProperty.DNS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-servicediscovery.html#cfn-appmesh-virtualnode-servicediscovery-dns
            '''
            result = self._values.get("dns")
            return typing.cast(typing.Optional[typing.Union["CfnVirtualNode.DnsServiceDiscoveryProperty", aws_cdk.core.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceDiscoveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.SubjectAlternativeNameMatchersProperty",
        jsii_struct_bases=[],
        name_mapping={"exact": "exact"},
    )
    class SubjectAlternativeNameMatchersProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            '''
            :param exact: ``CfnVirtualNode.SubjectAlternativeNameMatchersProperty.Exact``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-subjectalternativenamematchers.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact

        @builtins.property
        def exact(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnVirtualNode.SubjectAlternativeNameMatchersProperty.Exact``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-subjectalternativenamematchers.html#cfn-appmesh-virtualnode-subjectalternativenamematchers-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectAlternativeNameMatchersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.SubjectAlternativeNamesProperty",
        jsii_struct_bases=[],
        name_mapping={"match": "match"},
    )
    class SubjectAlternativeNamesProperty:
        def __init__(
            self,
            *,
            match: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.SubjectAlternativeNameMatchersProperty"],
        ) -> None:
            '''
            :param match: ``CfnVirtualNode.SubjectAlternativeNamesProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-subjectalternativenames.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "match": match,
            }

        @builtins.property
        def match(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.SubjectAlternativeNameMatchersProperty"]:
            '''``CfnVirtualNode.SubjectAlternativeNamesProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-subjectalternativenames.html#cfn-appmesh-virtualnode-subjectalternativenames-match
            '''
            result = self._values.get("match")
            assert result is not None, "Required property 'match' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.SubjectAlternativeNameMatchersProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectAlternativeNamesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.TcpTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"idle": "idle"},
    )
    class TcpTimeoutProperty:
        def __init__(
            self,
            *,
            idle: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]] = None,
        ) -> None:
            '''
            :param idle: ``CfnVirtualNode.TcpTimeoutProperty.Idle``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tcptimeout.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if idle is not None:
                self._values["idle"] = idle

        @builtins.property
        def idle(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]]:
            '''``CfnVirtualNode.TcpTimeoutProperty.Idle``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tcptimeout.html#cfn-appmesh-virtualnode-tcptimeout-idle
            '''
            result = self._values.get("idle")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.DurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TcpTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.TlsValidationContextAcmTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_authority_arns": "certificateAuthorityArns"},
    )
    class TlsValidationContextAcmTrustProperty:
        def __init__(
            self,
            *,
            certificate_authority_arns: typing.List[builtins.str],
        ) -> None:
            '''
            :param certificate_authority_arns: ``CfnVirtualNode.TlsValidationContextAcmTrustProperty.CertificateAuthorityArns``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextacmtrust.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "certificate_authority_arns": certificate_authority_arns,
            }

        @builtins.property
        def certificate_authority_arns(self) -> typing.List[builtins.str]:
            '''``CfnVirtualNode.TlsValidationContextAcmTrustProperty.CertificateAuthorityArns``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextacmtrust.html#cfn-appmesh-virtualnode-tlsvalidationcontextacmtrust-certificateauthorityarns
            '''
            result = self._values.get("certificate_authority_arns")
            assert result is not None, "Required property 'certificate_authority_arns' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TlsValidationContextAcmTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.TlsValidationContextFileTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_chain": "certificateChain"},
    )
    class TlsValidationContextFileTrustProperty:
        def __init__(self, *, certificate_chain: builtins.str) -> None:
            '''
            :param certificate_chain: ``CfnVirtualNode.TlsValidationContextFileTrustProperty.CertificateChain``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextfiletrust.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "certificate_chain": certificate_chain,
            }

        @builtins.property
        def certificate_chain(self) -> builtins.str:
            '''``CfnVirtualNode.TlsValidationContextFileTrustProperty.CertificateChain``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextfiletrust.html#cfn-appmesh-virtualnode-tlsvalidationcontextfiletrust-certificatechain
            '''
            result = self._values.get("certificate_chain")
            assert result is not None, "Required property 'certificate_chain' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TlsValidationContextFileTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.TlsValidationContextProperty",
        jsii_struct_bases=[],
        name_mapping={
            "trust": "trust",
            "subject_alternative_names": "subjectAlternativeNames",
        },
    )
    class TlsValidationContextProperty:
        def __init__(
            self,
            *,
            trust: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextTrustProperty"],
            subject_alternative_names: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.SubjectAlternativeNamesProperty"]] = None,
        ) -> None:
            '''
            :param trust: ``CfnVirtualNode.TlsValidationContextProperty.Trust``.
            :param subject_alternative_names: ``CfnVirtualNode.TlsValidationContextProperty.SubjectAlternativeNames``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontext.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "trust": trust,
            }
            if subject_alternative_names is not None:
                self._values["subject_alternative_names"] = subject_alternative_names

        @builtins.property
        def trust(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextTrustProperty"]:
            '''``CfnVirtualNode.TlsValidationContextProperty.Trust``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontext.html#cfn-appmesh-virtualnode-tlsvalidationcontext-trust
            '''
            result = self._values.get("trust")
            assert result is not None, "Required property 'trust' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextTrustProperty"], result)

        @builtins.property
        def subject_alternative_names(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.SubjectAlternativeNamesProperty"]]:
            '''``CfnVirtualNode.TlsValidationContextProperty.SubjectAlternativeNames``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontext.html#cfn-appmesh-virtualnode-tlsvalidationcontext-subjectalternativenames
            '''
            result = self._values.get("subject_alternative_names")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.SubjectAlternativeNamesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TlsValidationContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.TlsValidationContextSdsTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_name": "secretName"},
    )
    class TlsValidationContextSdsTrustProperty:
        def __init__(self, *, secret_name: builtins.str) -> None:
            '''
            :param secret_name: ``CfnVirtualNode.TlsValidationContextSdsTrustProperty.SecretName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextsdstrust.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "secret_name": secret_name,
            }

        @builtins.property
        def secret_name(self) -> builtins.str:
            '''``CfnVirtualNode.TlsValidationContextSdsTrustProperty.SecretName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextsdstrust.html#cfn-appmesh-virtualnode-tlsvalidationcontextsdstrust-secretname
            '''
            result = self._values.get("secret_name")
            assert result is not None, "Required property 'secret_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TlsValidationContextSdsTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.TlsValidationContextTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"acm": "acm", "file": "file", "sds": "sds"},
    )
    class TlsValidationContextTrustProperty:
        def __init__(
            self,
            *,
            acm: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextAcmTrustProperty"]] = None,
            file: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextFileTrustProperty"]] = None,
            sds: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextSdsTrustProperty"]] = None,
        ) -> None:
            '''
            :param acm: ``CfnVirtualNode.TlsValidationContextTrustProperty.ACM``.
            :param file: ``CfnVirtualNode.TlsValidationContextTrustProperty.File``.
            :param sds: ``CfnVirtualNode.TlsValidationContextTrustProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontexttrust.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if acm is not None:
                self._values["acm"] = acm
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def acm(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextAcmTrustProperty"]]:
            '''``CfnVirtualNode.TlsValidationContextTrustProperty.ACM``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontexttrust.html#cfn-appmesh-virtualnode-tlsvalidationcontexttrust-acm
            '''
            result = self._values.get("acm")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextAcmTrustProperty"]], result)

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextFileTrustProperty"]]:
            '''``CfnVirtualNode.TlsValidationContextTrustProperty.File``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontexttrust.html#cfn-appmesh-virtualnode-tlsvalidationcontexttrust-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextFileTrustProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextSdsTrustProperty"]]:
            '''``CfnVirtualNode.TlsValidationContextTrustProperty.SDS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontexttrust.html#cfn-appmesh-virtualnode-tlsvalidationcontexttrust-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.TlsValidationContextSdsTrustProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TlsValidationContextTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.VirtualNodeConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={"grpc": "grpc", "http": "http", "http2": "http2", "tcp": "tcp"},
    )
    class VirtualNodeConnectionPoolProperty:
        def __init__(
            self,
            *,
            grpc: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeGrpcConnectionPoolProperty"]] = None,
            http: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeHttpConnectionPoolProperty"]] = None,
            http2: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeHttp2ConnectionPoolProperty"]] = None,
            tcp: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeTcpConnectionPoolProperty"]] = None,
        ) -> None:
            '''
            :param grpc: ``CfnVirtualNode.VirtualNodeConnectionPoolProperty.GRPC``.
            :param http: ``CfnVirtualNode.VirtualNodeConnectionPoolProperty.HTTP``.
            :param http2: ``CfnVirtualNode.VirtualNodeConnectionPoolProperty.HTTP2``.
            :param tcp: ``CfnVirtualNode.VirtualNodeConnectionPoolProperty.TCP``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodeconnectionpool.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if grpc is not None:
                self._values["grpc"] = grpc
            if http is not None:
                self._values["http"] = http
            if http2 is not None:
                self._values["http2"] = http2
            if tcp is not None:
                self._values["tcp"] = tcp

        @builtins.property
        def grpc(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeGrpcConnectionPoolProperty"]]:
            '''``CfnVirtualNode.VirtualNodeConnectionPoolProperty.GRPC``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodeconnectionpool.html#cfn-appmesh-virtualnode-virtualnodeconnectionpool-grpc
            '''
            result = self._values.get("grpc")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeGrpcConnectionPoolProperty"]], result)

        @builtins.property
        def http(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeHttpConnectionPoolProperty"]]:
            '''``CfnVirtualNode.VirtualNodeConnectionPoolProperty.HTTP``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodeconnectionpool.html#cfn-appmesh-virtualnode-virtualnodeconnectionpool-http
            '''
            result = self._values.get("http")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeHttpConnectionPoolProperty"]], result)

        @builtins.property
        def http2(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeHttp2ConnectionPoolProperty"]]:
            '''``CfnVirtualNode.VirtualNodeConnectionPoolProperty.HTTP2``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodeconnectionpool.html#cfn-appmesh-virtualnode-virtualnodeconnectionpool-http2
            '''
            result = self._values.get("http2")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeHttp2ConnectionPoolProperty"]], result)

        @builtins.property
        def tcp(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeTcpConnectionPoolProperty"]]:
            '''``CfnVirtualNode.VirtualNodeConnectionPoolProperty.TCP``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodeconnectionpool.html#cfn-appmesh-virtualnode-virtualnodeconnectionpool-tcp
            '''
            result = self._values.get("tcp")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.VirtualNodeTcpConnectionPoolProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualNodeConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.VirtualNodeGrpcConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={"max_requests": "maxRequests"},
    )
    class VirtualNodeGrpcConnectionPoolProperty:
        def __init__(self, *, max_requests: jsii.Number) -> None:
            '''
            :param max_requests: ``CfnVirtualNode.VirtualNodeGrpcConnectionPoolProperty.MaxRequests``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodegrpcconnectionpool.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "max_requests": max_requests,
            }

        @builtins.property
        def max_requests(self) -> jsii.Number:
            '''``CfnVirtualNode.VirtualNodeGrpcConnectionPoolProperty.MaxRequests``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodegrpcconnectionpool.html#cfn-appmesh-virtualnode-virtualnodegrpcconnectionpool-maxrequests
            '''
            result = self._values.get("max_requests")
            assert result is not None, "Required property 'max_requests' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualNodeGrpcConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.VirtualNodeHttp2ConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={"max_requests": "maxRequests"},
    )
    class VirtualNodeHttp2ConnectionPoolProperty:
        def __init__(self, *, max_requests: jsii.Number) -> None:
            '''
            :param max_requests: ``CfnVirtualNode.VirtualNodeHttp2ConnectionPoolProperty.MaxRequests``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodehttp2connectionpool.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "max_requests": max_requests,
            }

        @builtins.property
        def max_requests(self) -> jsii.Number:
            '''``CfnVirtualNode.VirtualNodeHttp2ConnectionPoolProperty.MaxRequests``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodehttp2connectionpool.html#cfn-appmesh-virtualnode-virtualnodehttp2connectionpool-maxrequests
            '''
            result = self._values.get("max_requests")
            assert result is not None, "Required property 'max_requests' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualNodeHttp2ConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.VirtualNodeHttpConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_connections": "maxConnections",
            "max_pending_requests": "maxPendingRequests",
        },
    )
    class VirtualNodeHttpConnectionPoolProperty:
        def __init__(
            self,
            *,
            max_connections: jsii.Number,
            max_pending_requests: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param max_connections: ``CfnVirtualNode.VirtualNodeHttpConnectionPoolProperty.MaxConnections``.
            :param max_pending_requests: ``CfnVirtualNode.VirtualNodeHttpConnectionPoolProperty.MaxPendingRequests``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodehttpconnectionpool.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "max_connections": max_connections,
            }
            if max_pending_requests is not None:
                self._values["max_pending_requests"] = max_pending_requests

        @builtins.property
        def max_connections(self) -> jsii.Number:
            '''``CfnVirtualNode.VirtualNodeHttpConnectionPoolProperty.MaxConnections``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodehttpconnectionpool.html#cfn-appmesh-virtualnode-virtualnodehttpconnectionpool-maxconnections
            '''
            result = self._values.get("max_connections")
            assert result is not None, "Required property 'max_connections' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def max_pending_requests(self) -> typing.Optional[jsii.Number]:
            '''``CfnVirtualNode.VirtualNodeHttpConnectionPoolProperty.MaxPendingRequests``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodehttpconnectionpool.html#cfn-appmesh-virtualnode-virtualnodehttpconnectionpool-maxpendingrequests
            '''
            result = self._values.get("max_pending_requests")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualNodeHttpConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.VirtualNodeSpecProperty",
        jsii_struct_bases=[],
        name_mapping={
            "backend_defaults": "backendDefaults",
            "backends": "backends",
            "listeners": "listeners",
            "logging": "logging",
            "service_discovery": "serviceDiscovery",
        },
    )
    class VirtualNodeSpecProperty:
        def __init__(
            self,
            *,
            backend_defaults: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.BackendDefaultsProperty"]] = None,
            backends: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnVirtualNode.BackendProperty", aws_cdk.core.IResolvable]]]] = None,
            listeners: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnVirtualNode.ListenerProperty", aws_cdk.core.IResolvable]]]] = None,
            logging: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.LoggingProperty"]] = None,
            service_discovery: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ServiceDiscoveryProperty"]] = None,
        ) -> None:
            '''
            :param backend_defaults: ``CfnVirtualNode.VirtualNodeSpecProperty.BackendDefaults``.
            :param backends: ``CfnVirtualNode.VirtualNodeSpecProperty.Backends``.
            :param listeners: ``CfnVirtualNode.VirtualNodeSpecProperty.Listeners``.
            :param logging: ``CfnVirtualNode.VirtualNodeSpecProperty.Logging``.
            :param service_discovery: ``CfnVirtualNode.VirtualNodeSpecProperty.ServiceDiscovery``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if backend_defaults is not None:
                self._values["backend_defaults"] = backend_defaults
            if backends is not None:
                self._values["backends"] = backends
            if listeners is not None:
                self._values["listeners"] = listeners
            if logging is not None:
                self._values["logging"] = logging
            if service_discovery is not None:
                self._values["service_discovery"] = service_discovery

        @builtins.property
        def backend_defaults(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.BackendDefaultsProperty"]]:
            '''``CfnVirtualNode.VirtualNodeSpecProperty.BackendDefaults``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-backenddefaults
            '''
            result = self._values.get("backend_defaults")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.BackendDefaultsProperty"]], result)

        @builtins.property
        def backends(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnVirtualNode.BackendProperty", aws_cdk.core.IResolvable]]]]:
            '''``CfnVirtualNode.VirtualNodeSpecProperty.Backends``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-backends
            '''
            result = self._values.get("backends")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnVirtualNode.BackendProperty", aws_cdk.core.IResolvable]]]], result)

        @builtins.property
        def listeners(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnVirtualNode.ListenerProperty", aws_cdk.core.IResolvable]]]]:
            '''``CfnVirtualNode.VirtualNodeSpecProperty.Listeners``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-listeners
            '''
            result = self._values.get("listeners")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnVirtualNode.ListenerProperty", aws_cdk.core.IResolvable]]]], result)

        @builtins.property
        def logging(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.LoggingProperty"]]:
            '''``CfnVirtualNode.VirtualNodeSpecProperty.Logging``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-logging
            '''
            result = self._values.get("logging")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.LoggingProperty"]], result)

        @builtins.property
        def service_discovery(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ServiceDiscoveryProperty"]]:
            '''``CfnVirtualNode.VirtualNodeSpecProperty.ServiceDiscovery``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-servicediscovery
            '''
            result = self._values.get("service_discovery")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualNode.ServiceDiscoveryProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualNodeSpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.VirtualNodeTcpConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={"max_connections": "maxConnections"},
    )
    class VirtualNodeTcpConnectionPoolProperty:
        def __init__(self, *, max_connections: jsii.Number) -> None:
            '''
            :param max_connections: ``CfnVirtualNode.VirtualNodeTcpConnectionPoolProperty.MaxConnections``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodetcpconnectionpool.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "max_connections": max_connections,
            }

        @builtins.property
        def max_connections(self) -> jsii.Number:
            '''``CfnVirtualNode.VirtualNodeTcpConnectionPoolProperty.MaxConnections``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodetcpconnectionpool.html#cfn-appmesh-virtualnode-virtualnodetcpconnectionpool-maxconnections
            '''
            result = self._values.get("max_connections")
            assert result is not None, "Required property 'max_connections' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualNodeTcpConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.VirtualServiceBackendProperty",
        jsii_struct_bases=[],
        name_mapping={
            "virtual_service_name": "virtualServiceName",
            "client_policy": "clientPolicy",
        },
    )
    class VirtualServiceBackendProperty:
        def __init__(
            self,
            *,
            virtual_service_name: builtins.str,
            client_policy: typing.Optional[typing.Union["CfnVirtualNode.ClientPolicyProperty", aws_cdk.core.IResolvable]] = None,
        ) -> None:
            '''
            :param virtual_service_name: ``CfnVirtualNode.VirtualServiceBackendProperty.VirtualServiceName``.
            :param client_policy: ``CfnVirtualNode.VirtualServiceBackendProperty.ClientPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualservicebackend.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "virtual_service_name": virtual_service_name,
            }
            if client_policy is not None:
                self._values["client_policy"] = client_policy

        @builtins.property
        def virtual_service_name(self) -> builtins.str:
            '''``CfnVirtualNode.VirtualServiceBackendProperty.VirtualServiceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualservicebackend.html#cfn-appmesh-virtualnode-virtualservicebackend-virtualservicename
            '''
            result = self._values.get("virtual_service_name")
            assert result is not None, "Required property 'virtual_service_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnVirtualNode.ClientPolicyProperty", aws_cdk.core.IResolvable]]:
            '''``CfnVirtualNode.VirtualServiceBackendProperty.ClientPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualservicebackend.html#cfn-appmesh-virtualnode-virtualservicebackend-clientpolicy
            '''
            result = self._values.get("client_policy")
            return typing.cast(typing.Optional[typing.Union["CfnVirtualNode.ClientPolicyProperty", aws_cdk.core.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualServiceBackendProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNodeProps",
    jsii_struct_bases=[],
    name_mapping={
        "mesh_name": "meshName",
        "spec": "spec",
        "mesh_owner": "meshOwner",
        "tags": "tags",
        "virtual_node_name": "virtualNodeName",
    },
)
class CfnVirtualNodeProps:
    def __init__(
        self,
        *,
        mesh_name: builtins.str,
        spec: typing.Union[aws_cdk.core.IResolvable, CfnVirtualNode.VirtualNodeSpecProperty],
        mesh_owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        virtual_node_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::AppMesh::VirtualNode``.

        :param mesh_name: ``AWS::AppMesh::VirtualNode.MeshName``.
        :param spec: ``AWS::AppMesh::VirtualNode.Spec``.
        :param mesh_owner: ``AWS::AppMesh::VirtualNode.MeshOwner``.
        :param tags: ``AWS::AppMesh::VirtualNode.Tags``.
        :param virtual_node_name: ``AWS::AppMesh::VirtualNode.VirtualNodeName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "mesh_name": mesh_name,
            "spec": spec,
        }
        if mesh_owner is not None:
            self._values["mesh_owner"] = mesh_owner
        if tags is not None:
            self._values["tags"] = tags
        if virtual_node_name is not None:
            self._values["virtual_node_name"] = virtual_node_name

    @builtins.property
    def mesh_name(self) -> builtins.str:
        '''``AWS::AppMesh::VirtualNode.MeshName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-meshname
        '''
        result = self._values.get("mesh_name")
        assert result is not None, "Required property 'mesh_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnVirtualNode.VirtualNodeSpecProperty]:
        '''``AWS::AppMesh::VirtualNode.Spec``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-spec
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, CfnVirtualNode.VirtualNodeSpecProperty], result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::VirtualNode.MeshOwner``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-meshowner
        '''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::AppMesh::VirtualNode.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    @builtins.property
    def virtual_node_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::VirtualNode.VirtualNodeName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-virtualnodename
        '''
        result = self._values.get("virtual_node_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVirtualNodeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnVirtualRouter(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouter",
):
    '''A CloudFormation ``AWS::AppMesh::VirtualRouter``.

    :cloudformationResource: AWS::AppMesh::VirtualRouter
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        mesh_name: builtins.str,
        spec: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualRouter.VirtualRouterSpecProperty"],
        mesh_owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        virtual_router_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::AppMesh::VirtualRouter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param mesh_name: ``AWS::AppMesh::VirtualRouter.MeshName``.
        :param spec: ``AWS::AppMesh::VirtualRouter.Spec``.
        :param mesh_owner: ``AWS::AppMesh::VirtualRouter.MeshOwner``.
        :param tags: ``AWS::AppMesh::VirtualRouter.Tags``.
        :param virtual_router_name: ``AWS::AppMesh::VirtualRouter.VirtualRouterName``.
        '''
        props = CfnVirtualRouterProps(
            mesh_name=mesh_name,
            spec=spec,
            mesh_owner=mesh_owner,
            tags=tags,
            virtual_router_name=virtual_router_name,
        )

        jsii.create(CfnVirtualRouter, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrMeshName")
    def attr_mesh_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: MeshName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMeshName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrMeshOwner")
    def attr_mesh_owner(self) -> builtins.str:
        '''
        :cloudformationAttribute: MeshOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMeshOwner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrResourceOwner")
    def attr_resource_owner(self) -> builtins.str:
        '''
        :cloudformationAttribute: ResourceOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceOwner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrUid")
    def attr_uid(self) -> builtins.str:
        '''
        :cloudformationAttribute: Uid
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUid"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrVirtualRouterName")
    def attr_virtual_router_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: VirtualRouterName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVirtualRouterName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::AppMesh::VirtualRouter.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> builtins.str:
        '''``AWS::AppMesh::VirtualRouter.MeshName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-meshname
        '''
        return typing.cast(builtins.str, jsii.get(self, "meshName"))

    @mesh_name.setter
    def mesh_name(self, value: builtins.str) -> None:
        jsii.set(self, "meshName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="spec")
    def spec(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualRouter.VirtualRouterSpecProperty"]:
        '''``AWS::AppMesh::VirtualRouter.Spec``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-spec
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualRouter.VirtualRouterSpecProperty"], jsii.get(self, "spec"))

    @spec.setter
    def spec(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualRouter.VirtualRouterSpecProperty"],
    ) -> None:
        jsii.set(self, "spec", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshOwner")
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::VirtualRouter.MeshOwner``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-meshowner
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "meshOwner"))

    @mesh_owner.setter
    def mesh_owner(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "meshOwner", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualRouterName")
    def virtual_router_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::VirtualRouter.VirtualRouterName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-virtualroutername
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualRouterName"))

    @virtual_router_name.setter
    def virtual_router_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "virtualRouterName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouter.PortMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"port": "port", "protocol": "protocol"},
    )
    class PortMappingProperty:
        def __init__(self, *, port: jsii.Number, protocol: builtins.str) -> None:
            '''
            :param port: ``CfnVirtualRouter.PortMappingProperty.Port``.
            :param protocol: ``CfnVirtualRouter.PortMappingProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-portmapping.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "port": port,
                "protocol": protocol,
            }

        @builtins.property
        def port(self) -> jsii.Number:
            '''``CfnVirtualRouter.PortMappingProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-portmapping.html#cfn-appmesh-virtualrouter-portmapping-port
            '''
            result = self._values.get("port")
            assert result is not None, "Required property 'port' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def protocol(self) -> builtins.str:
            '''``CfnVirtualRouter.PortMappingProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-portmapping.html#cfn-appmesh-virtualrouter-portmapping-protocol
            '''
            result = self._values.get("protocol")
            assert result is not None, "Required property 'protocol' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouter.VirtualRouterListenerProperty",
        jsii_struct_bases=[],
        name_mapping={"port_mapping": "portMapping"},
    )
    class VirtualRouterListenerProperty:
        def __init__(
            self,
            *,
            port_mapping: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualRouter.PortMappingProperty"],
        ) -> None:
            '''
            :param port_mapping: ``CfnVirtualRouter.VirtualRouterListenerProperty.PortMapping``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterlistener.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "port_mapping": port_mapping,
            }

        @builtins.property
        def port_mapping(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualRouter.PortMappingProperty"]:
            '''``CfnVirtualRouter.VirtualRouterListenerProperty.PortMapping``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterlistener.html#cfn-appmesh-virtualrouter-virtualrouterlistener-portmapping
            '''
            result = self._values.get("port_mapping")
            assert result is not None, "Required property 'port_mapping' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualRouter.PortMappingProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualRouterListenerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouter.VirtualRouterSpecProperty",
        jsii_struct_bases=[],
        name_mapping={"listeners": "listeners"},
    )
    class VirtualRouterSpecProperty:
        def __init__(
            self,
            *,
            listeners: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnVirtualRouter.VirtualRouterListenerProperty", aws_cdk.core.IResolvable]]],
        ) -> None:
            '''
            :param listeners: ``CfnVirtualRouter.VirtualRouterSpecProperty.Listeners``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterspec.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "listeners": listeners,
            }

        @builtins.property
        def listeners(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnVirtualRouter.VirtualRouterListenerProperty", aws_cdk.core.IResolvable]]]:
            '''``CfnVirtualRouter.VirtualRouterSpecProperty.Listeners``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterspec.html#cfn-appmesh-virtualrouter-virtualrouterspec-listeners
            '''
            result = self._values.get("listeners")
            assert result is not None, "Required property 'listeners' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnVirtualRouter.VirtualRouterListenerProperty", aws_cdk.core.IResolvable]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualRouterSpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouterProps",
    jsii_struct_bases=[],
    name_mapping={
        "mesh_name": "meshName",
        "spec": "spec",
        "mesh_owner": "meshOwner",
        "tags": "tags",
        "virtual_router_name": "virtualRouterName",
    },
)
class CfnVirtualRouterProps:
    def __init__(
        self,
        *,
        mesh_name: builtins.str,
        spec: typing.Union[aws_cdk.core.IResolvable, CfnVirtualRouter.VirtualRouterSpecProperty],
        mesh_owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        virtual_router_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::AppMesh::VirtualRouter``.

        :param mesh_name: ``AWS::AppMesh::VirtualRouter.MeshName``.
        :param spec: ``AWS::AppMesh::VirtualRouter.Spec``.
        :param mesh_owner: ``AWS::AppMesh::VirtualRouter.MeshOwner``.
        :param tags: ``AWS::AppMesh::VirtualRouter.Tags``.
        :param virtual_router_name: ``AWS::AppMesh::VirtualRouter.VirtualRouterName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "mesh_name": mesh_name,
            "spec": spec,
        }
        if mesh_owner is not None:
            self._values["mesh_owner"] = mesh_owner
        if tags is not None:
            self._values["tags"] = tags
        if virtual_router_name is not None:
            self._values["virtual_router_name"] = virtual_router_name

    @builtins.property
    def mesh_name(self) -> builtins.str:
        '''``AWS::AppMesh::VirtualRouter.MeshName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-meshname
        '''
        result = self._values.get("mesh_name")
        assert result is not None, "Required property 'mesh_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnVirtualRouter.VirtualRouterSpecProperty]:
        '''``AWS::AppMesh::VirtualRouter.Spec``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-spec
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, CfnVirtualRouter.VirtualRouterSpecProperty], result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::VirtualRouter.MeshOwner``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-meshowner
        '''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::AppMesh::VirtualRouter.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    @builtins.property
    def virtual_router_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::VirtualRouter.VirtualRouterName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-virtualroutername
        '''
        result = self._values.get("virtual_router_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVirtualRouterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnVirtualService(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService",
):
    '''A CloudFormation ``AWS::AppMesh::VirtualService``.

    :cloudformationResource: AWS::AppMesh::VirtualService
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        mesh_name: builtins.str,
        spec: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualService.VirtualServiceSpecProperty"],
        virtual_service_name: builtins.str,
        mesh_owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Create a new ``AWS::AppMesh::VirtualService``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param mesh_name: ``AWS::AppMesh::VirtualService.MeshName``.
        :param spec: ``AWS::AppMesh::VirtualService.Spec``.
        :param virtual_service_name: ``AWS::AppMesh::VirtualService.VirtualServiceName``.
        :param mesh_owner: ``AWS::AppMesh::VirtualService.MeshOwner``.
        :param tags: ``AWS::AppMesh::VirtualService.Tags``.
        '''
        props = CfnVirtualServiceProps(
            mesh_name=mesh_name,
            spec=spec,
            virtual_service_name=virtual_service_name,
            mesh_owner=mesh_owner,
            tags=tags,
        )

        jsii.create(CfnVirtualService, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrMeshName")
    def attr_mesh_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: MeshName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMeshName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrMeshOwner")
    def attr_mesh_owner(self) -> builtins.str:
        '''
        :cloudformationAttribute: MeshOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMeshOwner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrResourceOwner")
    def attr_resource_owner(self) -> builtins.str:
        '''
        :cloudformationAttribute: ResourceOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceOwner"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrUid")
    def attr_uid(self) -> builtins.str:
        '''
        :cloudformationAttribute: Uid
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUid"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrVirtualServiceName")
    def attr_virtual_service_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: VirtualServiceName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVirtualServiceName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::AppMesh::VirtualService.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> builtins.str:
        '''``AWS::AppMesh::VirtualService.MeshName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-meshname
        '''
        return typing.cast(builtins.str, jsii.get(self, "meshName"))

    @mesh_name.setter
    def mesh_name(self, value: builtins.str) -> None:
        jsii.set(self, "meshName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="spec")
    def spec(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnVirtualService.VirtualServiceSpecProperty"]:
        '''``AWS::AppMesh::VirtualService.Spec``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-spec
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnVirtualService.VirtualServiceSpecProperty"], jsii.get(self, "spec"))

    @spec.setter
    def spec(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnVirtualService.VirtualServiceSpecProperty"],
    ) -> None:
        jsii.set(self, "spec", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualServiceName")
    def virtual_service_name(self) -> builtins.str:
        '''``AWS::AppMesh::VirtualService.VirtualServiceName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-virtualservicename
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualServiceName"))

    @virtual_service_name.setter
    def virtual_service_name(self, value: builtins.str) -> None:
        jsii.set(self, "virtualServiceName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshOwner")
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::VirtualService.MeshOwner``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-meshowner
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "meshOwner"))

    @mesh_owner.setter
    def mesh_owner(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "meshOwner", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService.VirtualNodeServiceProviderProperty",
        jsii_struct_bases=[],
        name_mapping={"virtual_node_name": "virtualNodeName"},
    )
    class VirtualNodeServiceProviderProperty:
        def __init__(self, *, virtual_node_name: builtins.str) -> None:
            '''
            :param virtual_node_name: ``CfnVirtualService.VirtualNodeServiceProviderProperty.VirtualNodeName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualnodeserviceprovider.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "virtual_node_name": virtual_node_name,
            }

        @builtins.property
        def virtual_node_name(self) -> builtins.str:
            '''``CfnVirtualService.VirtualNodeServiceProviderProperty.VirtualNodeName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualnodeserviceprovider.html#cfn-appmesh-virtualservice-virtualnodeserviceprovider-virtualnodename
            '''
            result = self._values.get("virtual_node_name")
            assert result is not None, "Required property 'virtual_node_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualNodeServiceProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService.VirtualRouterServiceProviderProperty",
        jsii_struct_bases=[],
        name_mapping={"virtual_router_name": "virtualRouterName"},
    )
    class VirtualRouterServiceProviderProperty:
        def __init__(self, *, virtual_router_name: builtins.str) -> None:
            '''
            :param virtual_router_name: ``CfnVirtualService.VirtualRouterServiceProviderProperty.VirtualRouterName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualrouterserviceprovider.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "virtual_router_name": virtual_router_name,
            }

        @builtins.property
        def virtual_router_name(self) -> builtins.str:
            '''``CfnVirtualService.VirtualRouterServiceProviderProperty.VirtualRouterName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualrouterserviceprovider.html#cfn-appmesh-virtualservice-virtualrouterserviceprovider-virtualroutername
            '''
            result = self._values.get("virtual_router_name")
            assert result is not None, "Required property 'virtual_router_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualRouterServiceProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService.VirtualServiceProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "virtual_node": "virtualNode",
            "virtual_router": "virtualRouter",
        },
    )
    class VirtualServiceProviderProperty:
        def __init__(
            self,
            *,
            virtual_node: typing.Optional[typing.Union["CfnVirtualService.VirtualNodeServiceProviderProperty", aws_cdk.core.IResolvable]] = None,
            virtual_router: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualService.VirtualRouterServiceProviderProperty"]] = None,
        ) -> None:
            '''
            :param virtual_node: ``CfnVirtualService.VirtualServiceProviderProperty.VirtualNode``.
            :param virtual_router: ``CfnVirtualService.VirtualServiceProviderProperty.VirtualRouter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualserviceprovider.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if virtual_node is not None:
                self._values["virtual_node"] = virtual_node
            if virtual_router is not None:
                self._values["virtual_router"] = virtual_router

        @builtins.property
        def virtual_node(
            self,
        ) -> typing.Optional[typing.Union["CfnVirtualService.VirtualNodeServiceProviderProperty", aws_cdk.core.IResolvable]]:
            '''``CfnVirtualService.VirtualServiceProviderProperty.VirtualNode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualserviceprovider.html#cfn-appmesh-virtualservice-virtualserviceprovider-virtualnode
            '''
            result = self._values.get("virtual_node")
            return typing.cast(typing.Optional[typing.Union["CfnVirtualService.VirtualNodeServiceProviderProperty", aws_cdk.core.IResolvable]], result)

        @builtins.property
        def virtual_router(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualService.VirtualRouterServiceProviderProperty"]]:
            '''``CfnVirtualService.VirtualServiceProviderProperty.VirtualRouter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualserviceprovider.html#cfn-appmesh-virtualservice-virtualserviceprovider-virtualrouter
            '''
            result = self._values.get("virtual_router")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualService.VirtualRouterServiceProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualServiceProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService.VirtualServiceSpecProperty",
        jsii_struct_bases=[],
        name_mapping={"provider": "provider"},
    )
    class VirtualServiceSpecProperty:
        def __init__(
            self,
            *,
            provider: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualService.VirtualServiceProviderProperty"]] = None,
        ) -> None:
            '''
            :param provider: ``CfnVirtualService.VirtualServiceSpecProperty.Provider``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualservicespec.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if provider is not None:
                self._values["provider"] = provider

        @builtins.property
        def provider(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualService.VirtualServiceProviderProperty"]]:
            '''``CfnVirtualService.VirtualServiceSpecProperty.Provider``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualservicespec.html#cfn-appmesh-virtualservice-virtualservicespec-provider
            '''
            result = self._values.get("provider")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnVirtualService.VirtualServiceProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualServiceSpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.CfnVirtualServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "mesh_name": "meshName",
        "spec": "spec",
        "virtual_service_name": "virtualServiceName",
        "mesh_owner": "meshOwner",
        "tags": "tags",
    },
)
class CfnVirtualServiceProps:
    def __init__(
        self,
        *,
        mesh_name: builtins.str,
        spec: typing.Union[aws_cdk.core.IResolvable, CfnVirtualService.VirtualServiceSpecProperty],
        virtual_service_name: builtins.str,
        mesh_owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::AppMesh::VirtualService``.

        :param mesh_name: ``AWS::AppMesh::VirtualService.MeshName``.
        :param spec: ``AWS::AppMesh::VirtualService.Spec``.
        :param virtual_service_name: ``AWS::AppMesh::VirtualService.VirtualServiceName``.
        :param mesh_owner: ``AWS::AppMesh::VirtualService.MeshOwner``.
        :param tags: ``AWS::AppMesh::VirtualService.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "mesh_name": mesh_name,
            "spec": spec,
            "virtual_service_name": virtual_service_name,
        }
        if mesh_owner is not None:
            self._values["mesh_owner"] = mesh_owner
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def mesh_name(self) -> builtins.str:
        '''``AWS::AppMesh::VirtualService.MeshName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-meshname
        '''
        result = self._values.get("mesh_name")
        assert result is not None, "Required property 'mesh_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnVirtualService.VirtualServiceSpecProperty]:
        '''``AWS::AppMesh::VirtualService.Spec``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-spec
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, CfnVirtualService.VirtualServiceSpecProperty], result)

    @builtins.property
    def virtual_service_name(self) -> builtins.str:
        '''``AWS::AppMesh::VirtualService.VirtualServiceName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-virtualservicename
        '''
        result = self._values.get("virtual_service_name")
        assert result is not None, "Required property 'virtual_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppMesh::VirtualService.MeshOwner``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-meshowner
        '''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::AppMesh::VirtualService.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVirtualServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClientPolicy(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-appmesh.ClientPolicy",
):
    '''(experimental) Defines the TLS validation context trust.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_ClientPolicyProxy"]:
        return _ClientPolicyProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(ClientPolicy, self, [])

    @jsii.member(jsii_name="acmTrust") # type: ignore[misc]
    @builtins.classmethod
    def acm_trust(
        cls,
        *,
        certificate_authorities: typing.List[aws_cdk.aws_acmpca.ICertificateAuthority],
        ports: typing.Optional[typing.List[jsii.Number]] = None,
    ) -> "ClientPolicy":
        '''(experimental) TLS validation context trust for ACM Private Certificate Authority (CA).

        :param certificate_authorities: (experimental) Contains information for your private certificate authority.
        :param ports: (experimental) TLS is enforced on the ports specified here. If no ports are specified, TLS will be enforced on all the ports. Default: - none

        :stability: experimental
        '''
        props = AcmTrustOptions(
            certificate_authorities=certificate_authorities, ports=ports
        )

        return typing.cast("ClientPolicy", jsii.sinvoke(cls, "acmTrust", [props]))

    @jsii.member(jsii_name="fileTrust") # type: ignore[misc]
    @builtins.classmethod
    def file_trust(
        cls,
        *,
        certificate_chain: builtins.str,
        ports: typing.Optional[typing.List[jsii.Number]] = None,
    ) -> "ClientPolicy":
        '''(experimental) Tells envoy where to fetch the validation context from.

        :param certificate_chain: (experimental) Path to the Certificate Chain file on the file system where the Envoy is deployed.
        :param ports: (experimental) TLS is enforced on the ports specified here. If no ports are specified, TLS will be enforced on all the ports. Default: - none

        :stability: experimental
        '''
        props = FileTrustOptions(certificate_chain=certificate_chain, ports=ports)

        return typing.cast("ClientPolicy", jsii.sinvoke(cls, "fileTrust", [props]))

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, scope: aws_cdk.core.Construct) -> "ClientPolicyConfig":
        '''(experimental) Returns Trust context based on trust type.

        :param scope: -

        :stability: experimental
        '''
        ...


class _ClientPolicyProxy(ClientPolicy):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> "ClientPolicyConfig":
        '''(experimental) Returns Trust context based on trust type.

        :param scope: -

        :stability: experimental
        '''
        return typing.cast("ClientPolicyConfig", jsii.invoke(self, "bind", [scope]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.ClientPolicyConfig",
    jsii_struct_bases=[],
    name_mapping={"client_policy": "clientPolicy"},
)
class ClientPolicyConfig:
    def __init__(self, *, client_policy: CfnVirtualNode.ClientPolicyProperty) -> None:
        '''(experimental) Properties of TLS Client Policy.

        :param client_policy: (experimental) Represents single Client Policy property.

        :stability: experimental
        '''
        if isinstance(client_policy, dict):
            client_policy = CfnVirtualNode.ClientPolicyProperty(**client_policy)
        self._values: typing.Dict[str, typing.Any] = {
            "client_policy": client_policy,
        }

    @builtins.property
    def client_policy(self) -> CfnVirtualNode.ClientPolicyProperty:
        '''(experimental) Represents single Client Policy property.

        :stability: experimental
        '''
        result = self._values.get("client_policy")
        assert result is not None, "Required property 'client_policy' is missing"
        return typing.cast(CfnVirtualNode.ClientPolicyProperty, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClientPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.ClientPolicyOptions",
    jsii_struct_bases=[],
    name_mapping={"ports": "ports"},
)
class ClientPolicyOptions:
    def __init__(
        self,
        *,
        ports: typing.Optional[typing.List[jsii.Number]] = None,
    ) -> None:
        '''(experimental) Represents the property needed to define a Client Policy.

        :param ports: (experimental) TLS is enforced on the ports specified here. If no ports are specified, TLS will be enforced on all the ports. Default: - none

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if ports is not None:
            self._values["ports"] = ports

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''(experimental) TLS is enforced on the ports specified here.

        If no ports are specified, TLS will be enforced on all the ports.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClientPolicyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.CloudMapServiceDiscoveryOptions",
    jsii_struct_bases=[],
    name_mapping={"service": "service", "instance_attributes": "instanceAttributes"},
)
class CloudMapServiceDiscoveryOptions:
    def __init__(
        self,
        *,
        service: aws_cdk.aws_servicediscovery.IService,
        instance_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Represents the properties needed to define CloudMap Service Discovery.

        :param service: (experimental) The AWS Cloud Map Service to use for service discovery.
        :param instance_attributes: (experimental) A string map that contains attributes with values that you can use to filter instances by any custom attribute that you specified when you registered the instance. Only instances that match all of the specified key/value pairs will be returned. Default: - no instance attributes

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "service": service,
        }
        if instance_attributes is not None:
            self._values["instance_attributes"] = instance_attributes

    @builtins.property
    def service(self) -> aws_cdk.aws_servicediscovery.IService:
        '''(experimental) The AWS Cloud Map Service to use for service discovery.

        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(aws_cdk.aws_servicediscovery.IService, result)

    @builtins.property
    def instance_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) A string map that contains attributes with values that you can use to filter instances by any custom attribute that you specified when you registered the instance.

        Only instances that match all of the specified
        key/value pairs will be returned.

        :default: - no instance attributes

        :stability: experimental
        '''
        result = self._values.get("instance_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudMapServiceDiscoveryOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.FileCertificateOptions",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_chain_path": "certificateChainPath",
        "private_key_path": "privateKeyPath",
        "tls_mode": "tlsMode",
    },
)
class FileCertificateOptions:
    def __init__(
        self,
        *,
        certificate_chain_path: builtins.str,
        private_key_path: builtins.str,
        tls_mode: "TlsMode",
    ) -> None:
        '''(experimental) File Certificate Properties.

        :param certificate_chain_path: (experimental) The file path of the certificate chain file.
        :param private_key_path: (experimental) The file path of the private key file.
        :param tls_mode: (experimental) The TLS mode.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "certificate_chain_path": certificate_chain_path,
            "private_key_path": private_key_path,
            "tls_mode": tls_mode,
        }

    @builtins.property
    def certificate_chain_path(self) -> builtins.str:
        '''(experimental) The file path of the certificate chain file.

        :stability: experimental
        '''
        result = self._values.get("certificate_chain_path")
        assert result is not None, "Required property 'certificate_chain_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_key_path(self) -> builtins.str:
        '''(experimental) The file path of the private key file.

        :stability: experimental
        '''
        result = self._values.get("private_key_path")
        assert result is not None, "Required property 'private_key_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tls_mode(self) -> "TlsMode":
        '''(experimental) The TLS mode.

        :stability: experimental
        '''
        result = self._values.get("tls_mode")
        assert result is not None, "Required property 'tls_mode' is missing"
        return typing.cast("TlsMode", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileCertificateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.FileTrustOptions",
    jsii_struct_bases=[ClientPolicyOptions],
    name_mapping={"ports": "ports", "certificate_chain": "certificateChain"},
)
class FileTrustOptions(ClientPolicyOptions):
    def __init__(
        self,
        *,
        ports: typing.Optional[typing.List[jsii.Number]] = None,
        certificate_chain: builtins.str,
    ) -> None:
        '''(experimental) File Trust Properties.

        :param ports: (experimental) TLS is enforced on the ports specified here. If no ports are specified, TLS will be enforced on all the ports. Default: - none
        :param certificate_chain: (experimental) Path to the Certificate Chain file on the file system where the Envoy is deployed.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "certificate_chain": certificate_chain,
        }
        if ports is not None:
            self._values["ports"] = ports

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''(experimental) TLS is enforced on the ports specified here.

        If no ports are specified, TLS will be enforced on all the ports.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def certificate_chain(self) -> builtins.str:
        '''(experimental) Path to the Certificate Chain file on the file system where the Envoy is deployed.

        :stability: experimental
        '''
        result = self._values.get("certificate_chain")
        assert result is not None, "Required property 'certificate_chain' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileTrustOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.GatewayRouteAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_route_name": "gatewayRouteName",
        "virtual_gateway": "virtualGateway",
    },
)
class GatewayRouteAttributes:
    def __init__(
        self,
        *,
        gateway_route_name: builtins.str,
        virtual_gateway: "IVirtualGateway",
    ) -> None:
        '''(experimental) Interface with properties necessary to import a reusable GatewayRoute.

        :param gateway_route_name: (experimental) The name of the GatewayRoute.
        :param virtual_gateway: (experimental) The VirtualGateway this GatewayRoute is associated with.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "gateway_route_name": gateway_route_name,
            "virtual_gateway": virtual_gateway,
        }

    @builtins.property
    def gateway_route_name(self) -> builtins.str:
        '''(experimental) The name of the GatewayRoute.

        :stability: experimental
        '''
        result = self._values.get("gateway_route_name")
        assert result is not None, "Required property 'gateway_route_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_gateway(self) -> "IVirtualGateway":
        '''(experimental) The VirtualGateway this GatewayRoute is associated with.

        :stability: experimental
        '''
        result = self._values.get("virtual_gateway")
        assert result is not None, "Required property 'virtual_gateway' is missing"
        return typing.cast("IVirtualGateway", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GatewayRouteAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.GatewayRouteBaseProps",
    jsii_struct_bases=[],
    name_mapping={"route_spec": "routeSpec", "gateway_route_name": "gatewayRouteName"},
)
class GatewayRouteBaseProps:
    def __init__(
        self,
        *,
        route_spec: "GatewayRouteSpec",
        gateway_route_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Basic configuration properties for a GatewayRoute.

        :param route_spec: (experimental) What protocol the route uses.
        :param gateway_route_name: (experimental) The name of the GatewayRoute. Default: - an automatically generated name

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "route_spec": route_spec,
        }
        if gateway_route_name is not None:
            self._values["gateway_route_name"] = gateway_route_name

    @builtins.property
    def route_spec(self) -> "GatewayRouteSpec":
        '''(experimental) What protocol the route uses.

        :stability: experimental
        '''
        result = self._values.get("route_spec")
        assert result is not None, "Required property 'route_spec' is missing"
        return typing.cast("GatewayRouteSpec", result)

    @builtins.property
    def gateway_route_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the GatewayRoute.

        :default: - an automatically generated name

        :stability: experimental
        '''
        result = self._values.get("gateway_route_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GatewayRouteBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.GatewayRouteProps",
    jsii_struct_bases=[GatewayRouteBaseProps],
    name_mapping={
        "route_spec": "routeSpec",
        "gateway_route_name": "gatewayRouteName",
        "virtual_gateway": "virtualGateway",
    },
)
class GatewayRouteProps(GatewayRouteBaseProps):
    def __init__(
        self,
        *,
        route_spec: "GatewayRouteSpec",
        gateway_route_name: typing.Optional[builtins.str] = None,
        virtual_gateway: "IVirtualGateway",
    ) -> None:
        '''(experimental) Properties to define a new GatewayRoute.

        :param route_spec: (experimental) What protocol the route uses.
        :param gateway_route_name: (experimental) The name of the GatewayRoute. Default: - an automatically generated name
        :param virtual_gateway: (experimental) The VirtualGateway this GatewayRoute is associated with.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "route_spec": route_spec,
            "virtual_gateway": virtual_gateway,
        }
        if gateway_route_name is not None:
            self._values["gateway_route_name"] = gateway_route_name

    @builtins.property
    def route_spec(self) -> "GatewayRouteSpec":
        '''(experimental) What protocol the route uses.

        :stability: experimental
        '''
        result = self._values.get("route_spec")
        assert result is not None, "Required property 'route_spec' is missing"
        return typing.cast("GatewayRouteSpec", result)

    @builtins.property
    def gateway_route_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the GatewayRoute.

        :default: - an automatically generated name

        :stability: experimental
        '''
        result = self._values.get("gateway_route_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_gateway(self) -> "IVirtualGateway":
        '''(experimental) The VirtualGateway this GatewayRoute is associated with.

        :stability: experimental
        '''
        result = self._values.get("virtual_gateway")
        assert result is not None, "Required property 'virtual_gateway' is missing"
        return typing.cast("IVirtualGateway", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GatewayRouteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GatewayRouteSpec(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-appmesh.GatewayRouteSpec",
):
    '''(experimental) Used to generate specs with different protocols for a GatewayRoute.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_GatewayRouteSpecProxy"]:
        return _GatewayRouteSpecProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(GatewayRouteSpec, self, [])

    @jsii.member(jsii_name="grpc") # type: ignore[misc]
    @builtins.classmethod
    def grpc(
        cls,
        *,
        match: "GrpcGatewayRouteMatch",
        route_target: "IVirtualService",
    ) -> "GatewayRouteSpec":
        '''(experimental) Creates an GRPC Based GatewayRoute.

        :param match: (experimental) The criterion for determining a request match for this GatewayRoute.
        :param route_target: (experimental) The VirtualService this GatewayRoute directs traffic to.

        :stability: experimental
        '''
        options = GrpcGatewayRouteSpecOptions(match=match, route_target=route_target)

        return typing.cast("GatewayRouteSpec", jsii.sinvoke(cls, "grpc", [options]))

    @jsii.member(jsii_name="http") # type: ignore[misc]
    @builtins.classmethod
    def http(
        cls,
        *,
        route_target: "IVirtualService",
        match: typing.Optional["HttpGatewayRouteMatch"] = None,
    ) -> "GatewayRouteSpec":
        '''(experimental) Creates an HTTP Based GatewayRoute.

        :param route_target: (experimental) The VirtualService this GatewayRoute directs traffic to.
        :param match: (experimental) The criterion for determining a request match for this GatewayRoute. Default: - matches on '/'

        :stability: experimental
        '''
        options = HttpGatewayRouteSpecOptions(route_target=route_target, match=match)

        return typing.cast("GatewayRouteSpec", jsii.sinvoke(cls, "http", [options]))

    @jsii.member(jsii_name="http2") # type: ignore[misc]
    @builtins.classmethod
    def http2(
        cls,
        *,
        route_target: "IVirtualService",
        match: typing.Optional["HttpGatewayRouteMatch"] = None,
    ) -> "GatewayRouteSpec":
        '''(experimental) Creates an HTTP2 Based GatewayRoute.

        :param route_target: (experimental) The VirtualService this GatewayRoute directs traffic to.
        :param match: (experimental) The criterion for determining a request match for this GatewayRoute. Default: - matches on '/'

        :stability: experimental
        '''
        options = HttpGatewayRouteSpecOptions(route_target=route_target, match=match)

        return typing.cast("GatewayRouteSpec", jsii.sinvoke(cls, "http2", [options]))

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, scope: aws_cdk.core.Construct) -> "GatewayRouteSpecConfig":
        '''(experimental) Called when the GatewayRouteSpec type is initialized.

        Can be used to enforce
        mutual exclusivity with future properties

        :param scope: -

        :stability: experimental
        '''
        ...


class _GatewayRouteSpecProxy(GatewayRouteSpec):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> "GatewayRouteSpecConfig":
        '''(experimental) Called when the GatewayRouteSpec type is initialized.

        Can be used to enforce
        mutual exclusivity with future properties

        :param scope: -

        :stability: experimental
        '''
        return typing.cast("GatewayRouteSpecConfig", jsii.invoke(self, "bind", [scope]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.GatewayRouteSpecConfig",
    jsii_struct_bases=[],
    name_mapping={
        "grpc_spec_config": "grpcSpecConfig",
        "http2_spec_config": "http2SpecConfig",
        "http_spec_config": "httpSpecConfig",
    },
)
class GatewayRouteSpecConfig:
    def __init__(
        self,
        *,
        grpc_spec_config: typing.Optional[CfnGatewayRoute.GrpcGatewayRouteProperty] = None,
        http2_spec_config: typing.Optional[CfnGatewayRoute.HttpGatewayRouteProperty] = None,
        http_spec_config: typing.Optional[CfnGatewayRoute.HttpGatewayRouteProperty] = None,
    ) -> None:
        '''(experimental) All Properties for GatewayRoute Specs.

        :param grpc_spec_config: (experimental) The spec for a grpc gateway route. Default: - no grpc spec
        :param http2_spec_config: (experimental) The spec for an http2 gateway route. Default: - no http2 spec
        :param http_spec_config: (experimental) The spec for an http gateway route. Default: - no http spec

        :stability: experimental
        '''
        if isinstance(grpc_spec_config, dict):
            grpc_spec_config = CfnGatewayRoute.GrpcGatewayRouteProperty(**grpc_spec_config)
        if isinstance(http2_spec_config, dict):
            http2_spec_config = CfnGatewayRoute.HttpGatewayRouteProperty(**http2_spec_config)
        if isinstance(http_spec_config, dict):
            http_spec_config = CfnGatewayRoute.HttpGatewayRouteProperty(**http_spec_config)
        self._values: typing.Dict[str, typing.Any] = {}
        if grpc_spec_config is not None:
            self._values["grpc_spec_config"] = grpc_spec_config
        if http2_spec_config is not None:
            self._values["http2_spec_config"] = http2_spec_config
        if http_spec_config is not None:
            self._values["http_spec_config"] = http_spec_config

    @builtins.property
    def grpc_spec_config(
        self,
    ) -> typing.Optional[CfnGatewayRoute.GrpcGatewayRouteProperty]:
        '''(experimental) The spec for a grpc gateway route.

        :default: - no grpc spec

        :stability: experimental
        '''
        result = self._values.get("grpc_spec_config")
        return typing.cast(typing.Optional[CfnGatewayRoute.GrpcGatewayRouteProperty], result)

    @builtins.property
    def http2_spec_config(
        self,
    ) -> typing.Optional[CfnGatewayRoute.HttpGatewayRouteProperty]:
        '''(experimental) The spec for an http2 gateway route.

        :default: - no http2 spec

        :stability: experimental
        '''
        result = self._values.get("http2_spec_config")
        return typing.cast(typing.Optional[CfnGatewayRoute.HttpGatewayRouteProperty], result)

    @builtins.property
    def http_spec_config(
        self,
    ) -> typing.Optional[CfnGatewayRoute.HttpGatewayRouteProperty]:
        '''(experimental) The spec for an http gateway route.

        :default: - no http spec

        :stability: experimental
        '''
        result = self._values.get("http_spec_config")
        return typing.cast(typing.Optional[CfnGatewayRoute.HttpGatewayRouteProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GatewayRouteSpecConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.GrpcGatewayListenerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "health_check": "healthCheck",
        "port": "port",
        "tls_certificate": "tlsCertificate",
    },
)
class GrpcGatewayListenerOptions:
    def __init__(
        self,
        *,
        health_check: typing.Optional["HealthCheck"] = None,
        port: typing.Optional[jsii.Number] = None,
        tls_certificate: typing.Optional["TlsCertificate"] = None,
    ) -> None:
        '''(experimental) Represents the properties needed to define GRPC Listeners for a VirtualGateway.

        :param health_check: (experimental) The health check information for the listener. Default: - no healthcheck
        :param port: (experimental) Port to listen for connections on. Default: - 8080
        :param tls_certificate: (experimental) Represents the listener certificate. Default: - none

        :stability: experimental
        '''
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        self._values: typing.Dict[str, typing.Any] = {}
        if health_check is not None:
            self._values["health_check"] = health_check
        if port is not None:
            self._values["port"] = port
        if tls_certificate is not None:
            self._values["tls_certificate"] = tls_certificate

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        '''(experimental) The health check information for the listener.

        :default: - no healthcheck

        :stability: experimental
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional["HealthCheck"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Port to listen for connections on.

        :default: - 8080

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tls_certificate(self) -> typing.Optional["TlsCertificate"]:
        '''(experimental) Represents the listener certificate.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("tls_certificate")
        return typing.cast(typing.Optional["TlsCertificate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrpcGatewayListenerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.GrpcGatewayRouteMatch",
    jsii_struct_bases=[],
    name_mapping={"service_name": "serviceName"},
)
class GrpcGatewayRouteMatch:
    def __init__(self, *, service_name: builtins.str) -> None:
        '''(experimental) The criterion for determining a request match for this GatewayRoute.

        :param service_name: (experimental) The fully qualified domain name for the service to match from the request.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "service_name": service_name,
        }

    @builtins.property
    def service_name(self) -> builtins.str:
        '''(experimental) The fully qualified domain name for the service to match from the request.

        :stability: experimental
        '''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrpcGatewayRouteMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.GrpcGatewayRouteSpecOptions",
    jsii_struct_bases=[],
    name_mapping={"match": "match", "route_target": "routeTarget"},
)
class GrpcGatewayRouteSpecOptions:
    def __init__(
        self,
        *,
        match: GrpcGatewayRouteMatch,
        route_target: "IVirtualService",
    ) -> None:
        '''(experimental) Properties specific for a GRPC GatewayRoute.

        :param match: (experimental) The criterion for determining a request match for this GatewayRoute.
        :param route_target: (experimental) The VirtualService this GatewayRoute directs traffic to.

        :stability: experimental
        '''
        if isinstance(match, dict):
            match = GrpcGatewayRouteMatch(**match)
        self._values: typing.Dict[str, typing.Any] = {
            "match": match,
            "route_target": route_target,
        }

    @builtins.property
    def match(self) -> GrpcGatewayRouteMatch:
        '''(experimental) The criterion for determining a request match for this GatewayRoute.

        :stability: experimental
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast(GrpcGatewayRouteMatch, result)

    @builtins.property
    def route_target(self) -> "IVirtualService":
        '''(experimental) The VirtualService this GatewayRoute directs traffic to.

        :stability: experimental
        '''
        result = self._values.get("route_target")
        assert result is not None, "Required property 'route_target' is missing"
        return typing.cast("IVirtualService", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrpcGatewayRouteSpecOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-appmesh.GrpcRetryEvent")
class GrpcRetryEvent(enum.Enum):
    '''(experimental) gRPC events.

    :stability: experimental
    '''

    CANCELLED = "CANCELLED"
    '''(experimental) Request was cancelled.

    :see: https://grpc.github.io/grpc/core/md_doc_statuscodes.html
    :stability: experimental
    '''
    DEADLINE_EXCEEDED = "DEADLINE_EXCEEDED"
    '''(experimental) The deadline was exceeded.

    :see: https://grpc.github.io/grpc/core/md_doc_statuscodes.html
    :stability: experimental
    '''
    INTERNAL_ERROR = "INTERNAL_ERROR"
    '''(experimental) Internal error.

    :see: https://grpc.github.io/grpc/core/md_doc_statuscodes.html
    :stability: experimental
    '''
    RESOURCE_EXHAUSTED = "RESOURCE_EXHAUSTED"
    '''(experimental) A resource was exhausted.

    :see: https://grpc.github.io/grpc/core/md_doc_statuscodes.html
    :stability: experimental
    '''
    UNAVAILABLE = "UNAVAILABLE"
    '''(experimental) The service is unavailable.

    :see: https://grpc.github.io/grpc/core/md_doc_statuscodes.html
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.GrpcRouteMatch",
    jsii_struct_bases=[],
    name_mapping={"service_name": "serviceName"},
)
class GrpcRouteMatch:
    def __init__(self, *, service_name: builtins.str) -> None:
        '''(experimental) The criterion for determining a request match for this GatewayRoute.

        :param service_name: (experimental) The fully qualified domain name for the service to match from the request.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "service_name": service_name,
        }

    @builtins.property
    def service_name(self) -> builtins.str:
        '''(experimental) The fully qualified domain name for the service to match from the request.

        :stability: experimental
        '''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrpcRouteMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.GrpcTimeout",
    jsii_struct_bases=[],
    name_mapping={"idle": "idle", "per_request": "perRequest"},
)
class GrpcTimeout:
    def __init__(
        self,
        *,
        idle: typing.Optional[aws_cdk.core.Duration] = None,
        per_request: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        '''(experimental) Represents timeouts for GRPC protocols.

        :param idle: (experimental) Represents an idle timeout. The amount of time that a connection may be idle. Default: - none
        :param per_request: (experimental) Represents per request timeout. Default: - 15 s

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if idle is not None:
            self._values["idle"] = idle
        if per_request is not None:
            self._values["per_request"] = per_request

    @builtins.property
    def idle(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''(experimental) Represents an idle timeout.

        The amount of time that a connection may be idle.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("idle")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def per_request(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''(experimental) Represents per request timeout.

        :default: - 15 s

        :stability: experimental
        '''
        result = self._values.get("per_request")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrpcTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.GrpcVirtualNodeListenerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "health_check": "healthCheck",
        "port": "port",
        "timeout": "timeout",
        "tls_certificate": "tlsCertificate",
    },
)
class GrpcVirtualNodeListenerOptions:
    def __init__(
        self,
        *,
        health_check: typing.Optional["HealthCheck"] = None,
        port: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[GrpcTimeout] = None,
        tls_certificate: typing.Optional["TlsCertificate"] = None,
    ) -> None:
        '''(experimental) Represent the GRPC Node Listener prorperty.

        :param health_check: (experimental) The health check information for the listener. Default: - no healthcheck
        :param port: (experimental) Port to listen for connections on. Default: - 8080
        :param timeout: (experimental) Timeout for GRPC protocol. Default: - None
        :param tls_certificate: (experimental) Represents the configuration for enabling TLS on a listener. Default: - none

        :stability: experimental
        '''
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        if isinstance(timeout, dict):
            timeout = GrpcTimeout(**timeout)
        self._values: typing.Dict[str, typing.Any] = {}
        if health_check is not None:
            self._values["health_check"] = health_check
        if port is not None:
            self._values["port"] = port
        if timeout is not None:
            self._values["timeout"] = timeout
        if tls_certificate is not None:
            self._values["tls_certificate"] = tls_certificate

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        '''(experimental) The health check information for the listener.

        :default: - no healthcheck

        :stability: experimental
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional["HealthCheck"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Port to listen for connections on.

        :default: - 8080

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[GrpcTimeout]:
        '''(experimental) Timeout for GRPC protocol.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[GrpcTimeout], result)

    @builtins.property
    def tls_certificate(self) -> typing.Optional["TlsCertificate"]:
        '''(experimental) Represents the configuration for enabling TLS on a listener.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("tls_certificate")
        return typing.cast(typing.Optional["TlsCertificate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrpcVirtualNodeListenerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.HealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "healthy_threshold": "healthyThreshold",
        "interval": "interval",
        "path": "path",
        "port": "port",
        "protocol": "protocol",
        "timeout": "timeout",
        "unhealthy_threshold": "unhealthyThreshold",
    },
)
class HealthCheck:
    def __init__(
        self,
        *,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[aws_cdk.core.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional["Protocol"] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        unhealthy_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties used to define healthchecks when creating virtual nodes.

        All values have a default if only specified as {} when creating.
        If property not set, then no healthchecks will be defined.

        :param healthy_threshold: (experimental) Number of successful attempts before considering the node UP. Default: 2
        :param interval: (experimental) Interval in milliseconds to re-check. Default: 5 seconds
        :param path: (experimental) The path where the application expects any health-checks, this can also be the application path. Default: /
        :param port: (experimental) The TCP port number for the healthcheck. Default: - same as corresponding port mapping
        :param protocol: (experimental) The protocol to use for the healthcheck, for convinience a const enum has been defined. Protocol.HTTP or Protocol.TCP Default: - same as corresponding port mapping
        :param timeout: (experimental) Timeout in milli-seconds for the healthcheck to be considered a fail. Default: 2 seconds
        :param unhealthy_threshold: (experimental) Number of failed attempts before considering the node DOWN. Default: 2

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if healthy_threshold is not None:
            self._values["healthy_threshold"] = healthy_threshold
        if interval is not None:
            self._values["interval"] = interval
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if timeout is not None:
            self._values["timeout"] = timeout
        if unhealthy_threshold is not None:
            self._values["unhealthy_threshold"] = unhealthy_threshold

    @builtins.property
    def healthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of successful attempts before considering the node UP.

        :default: 2

        :stability: experimental
        '''
        result = self._values.get("healthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''(experimental) Interval in milliseconds to re-check.

        :default: 5 seconds

        :stability: experimental
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path where the application expects any health-checks, this can also be the application path.

        :default: /

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The TCP port number for the healthcheck.

        :default: - same as corresponding port mapping

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        '''(experimental) The protocol to use for the healthcheck, for convinience a const enum has been defined.

        Protocol.HTTP or Protocol.TCP

        :default: - same as corresponding port mapping

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional["Protocol"], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''(experimental) Timeout in milli-seconds for the healthcheck to be considered a fail.

        :default: 2 seconds

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of failed attempts before considering the node DOWN.

        :default: 2

        :stability: experimental
        '''
        result = self._values.get("unhealthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.HttpGatewayListenerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "health_check": "healthCheck",
        "port": "port",
        "tls_certificate": "tlsCertificate",
    },
)
class HttpGatewayListenerOptions:
    def __init__(
        self,
        *,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        tls_certificate: typing.Optional["TlsCertificate"] = None,
    ) -> None:
        '''(experimental) Represents the properties needed to define HTTP Listeners for a VirtualGateway.

        :param health_check: (experimental) The health check information for the listener. Default: - no healthcheck
        :param port: (experimental) Port to listen for connections on. Default: - 8080
        :param tls_certificate: (experimental) Represents the configuration for enabling TLS on a listener. Default: - none

        :stability: experimental
        '''
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        self._values: typing.Dict[str, typing.Any] = {}
        if health_check is not None:
            self._values["health_check"] = health_check
        if port is not None:
            self._values["port"] = port
        if tls_certificate is not None:
            self._values["tls_certificate"] = tls_certificate

    @builtins.property
    def health_check(self) -> typing.Optional[HealthCheck]:
        '''(experimental) The health check information for the listener.

        :default: - no healthcheck

        :stability: experimental
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[HealthCheck], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Port to listen for connections on.

        :default: - 8080

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tls_certificate(self) -> typing.Optional["TlsCertificate"]:
        '''(experimental) Represents the configuration for enabling TLS on a listener.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("tls_certificate")
        return typing.cast(typing.Optional["TlsCertificate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpGatewayListenerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.HttpGatewayRouteMatch",
    jsii_struct_bases=[],
    name_mapping={"prefix_path": "prefixPath"},
)
class HttpGatewayRouteMatch:
    def __init__(self, *, prefix_path: builtins.str) -> None:
        '''(experimental) The criterion for determining a request match for this GatewayRoute.

        :param prefix_path: (experimental) Specifies the path to match requests with. This parameter must always start with /, which by itself matches all requests to the virtual service name. You can also match for path-based routing of requests. For example, if your virtual service name is my-service.local and you want the route to match requests to my-service.local/metrics, your prefix should be /metrics.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "prefix_path": prefix_path,
        }

    @builtins.property
    def prefix_path(self) -> builtins.str:
        '''(experimental) Specifies the path to match requests with.

        This parameter must always start with /, which by itself matches all requests to the virtual service name.
        You can also match for path-based routing of requests. For example, if your virtual service name is my-service.local
        and you want the route to match requests to my-service.local/metrics, your prefix should be /metrics.

        :stability: experimental
        '''
        result = self._values.get("prefix_path")
        assert result is not None, "Required property 'prefix_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpGatewayRouteMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.HttpGatewayRouteSpecOptions",
    jsii_struct_bases=[],
    name_mapping={"route_target": "routeTarget", "match": "match"},
)
class HttpGatewayRouteSpecOptions:
    def __init__(
        self,
        *,
        route_target: "IVirtualService",
        match: typing.Optional[HttpGatewayRouteMatch] = None,
    ) -> None:
        '''(experimental) Properties specific for HTTP Based GatewayRoutes.

        :param route_target: (experimental) The VirtualService this GatewayRoute directs traffic to.
        :param match: (experimental) The criterion for determining a request match for this GatewayRoute. Default: - matches on '/'

        :stability: experimental
        '''
        if isinstance(match, dict):
            match = HttpGatewayRouteMatch(**match)
        self._values: typing.Dict[str, typing.Any] = {
            "route_target": route_target,
        }
        if match is not None:
            self._values["match"] = match

    @builtins.property
    def route_target(self) -> "IVirtualService":
        '''(experimental) The VirtualService this GatewayRoute directs traffic to.

        :stability: experimental
        '''
        result = self._values.get("route_target")
        assert result is not None, "Required property 'route_target' is missing"
        return typing.cast("IVirtualService", result)

    @builtins.property
    def match(self) -> typing.Optional[HttpGatewayRouteMatch]:
        '''(experimental) The criterion for determining a request match for this GatewayRoute.

        :default: - matches on '/'

        :stability: experimental
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional[HttpGatewayRouteMatch], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpGatewayRouteSpecOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HttpHeaderMatch(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-appmesh.HttpHeaderMatch",
):
    '''(experimental) Used to generate header matching methods.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_HttpHeaderMatchProxy"]:
        return _HttpHeaderMatchProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(HttpHeaderMatch, self, [])

    @jsii.member(jsii_name="valueDoesNotEndWith") # type: ignore[misc]
    @builtins.classmethod
    def value_does_not_end_with(
        cls,
        header_name: builtins.str,
        suffix: builtins.str,
    ) -> "HttpHeaderMatch":
        '''(experimental) The value of the header with the given name in the request must not end with the specified characters.

        :param header_name: the name of the HTTP header to match against.
        :param suffix: The suffix to test against.

        :stability: experimental
        '''
        return typing.cast("HttpHeaderMatch", jsii.sinvoke(cls, "valueDoesNotEndWith", [header_name, suffix]))

    @jsii.member(jsii_name="valueDoesNotMatchRegex") # type: ignore[misc]
    @builtins.classmethod
    def value_does_not_match_regex(
        cls,
        header_name: builtins.str,
        regex: builtins.str,
    ) -> "HttpHeaderMatch":
        '''(experimental) The value of the header with the given name in the request must not include the specified characters.

        :param header_name: the name of the HTTP header to match against.
        :param regex: The regex to test against.

        :stability: experimental
        '''
        return typing.cast("HttpHeaderMatch", jsii.sinvoke(cls, "valueDoesNotMatchRegex", [header_name, regex]))

    @jsii.member(jsii_name="valueDoesNotStartWith") # type: ignore[misc]
    @builtins.classmethod
    def value_does_not_start_with(
        cls,
        header_name: builtins.str,
        prefix: builtins.str,
    ) -> "HttpHeaderMatch":
        '''(experimental) The value of the header with the given name in the request must not start with the specified characters.

        :param header_name: the name of the HTTP header to match against.
        :param prefix: The prefix to test against.

        :stability: experimental
        '''
        return typing.cast("HttpHeaderMatch", jsii.sinvoke(cls, "valueDoesNotStartWith", [header_name, prefix]))

    @jsii.member(jsii_name="valueEndsWith") # type: ignore[misc]
    @builtins.classmethod
    def value_ends_with(
        cls,
        header_name: builtins.str,
        suffix: builtins.str,
    ) -> "HttpHeaderMatch":
        '''(experimental) The value of the header with the given name in the request must end with the specified characters.

        :param header_name: the name of the HTTP header to match against.
        :param suffix: The suffix to test against.

        :stability: experimental
        '''
        return typing.cast("HttpHeaderMatch", jsii.sinvoke(cls, "valueEndsWith", [header_name, suffix]))

    @jsii.member(jsii_name="valueIs") # type: ignore[misc]
    @builtins.classmethod
    def value_is(
        cls,
        header_name: builtins.str,
        header_value: builtins.str,
    ) -> "HttpHeaderMatch":
        '''(experimental) The value of the header with the given name in the request must match the specified value exactly.

        :param header_name: the name of the HTTP header to match against.
        :param header_value: The exact value to test against.

        :stability: experimental
        '''
        return typing.cast("HttpHeaderMatch", jsii.sinvoke(cls, "valueIs", [header_name, header_value]))

    @jsii.member(jsii_name="valueIsNot") # type: ignore[misc]
    @builtins.classmethod
    def value_is_not(
        cls,
        header_name: builtins.str,
        header_value: builtins.str,
    ) -> "HttpHeaderMatch":
        '''(experimental) The value of the header with the given name in the request must not match the specified value exactly.

        :param header_name: the name of the HTTP header to match against.
        :param header_value: The exact value to test against.

        :stability: experimental
        '''
        return typing.cast("HttpHeaderMatch", jsii.sinvoke(cls, "valueIsNot", [header_name, header_value]))

    @jsii.member(jsii_name="valueMatchesRegex") # type: ignore[misc]
    @builtins.classmethod
    def value_matches_regex(
        cls,
        header_name: builtins.str,
        regex: builtins.str,
    ) -> "HttpHeaderMatch":
        '''(experimental) The value of the header with the given name in the request must include the specified characters.

        :param header_name: the name of the HTTP header to match against.
        :param regex: The regex to test against.

        :stability: experimental
        '''
        return typing.cast("HttpHeaderMatch", jsii.sinvoke(cls, "valueMatchesRegex", [header_name, regex]))

    @jsii.member(jsii_name="valuesIsInRange") # type: ignore[misc]
    @builtins.classmethod
    def values_is_in_range(
        cls,
        header_name: builtins.str,
        start: jsii.Number,
        end: jsii.Number,
    ) -> "HttpHeaderMatch":
        '''(experimental) The value of the header with the given name in the request must be in a range of values.

        :param header_name: the name of the HTTP header to match against.
        :param start: Match on values starting at and including this value.
        :param end: Match on values up to but not including this value.

        :stability: experimental
        '''
        return typing.cast("HttpHeaderMatch", jsii.sinvoke(cls, "valuesIsInRange", [header_name, start, end]))

    @jsii.member(jsii_name="valuesIsNotInRange") # type: ignore[misc]
    @builtins.classmethod
    def values_is_not_in_range(
        cls,
        header_name: builtins.str,
        start: jsii.Number,
        end: jsii.Number,
    ) -> "HttpHeaderMatch":
        '''(experimental) The value of the header with the given name in the request must not be in a range of values.

        :param header_name: the name of the HTTP header to match against.
        :param start: Match on values starting at and including this value.
        :param end: Match on values up to but not including this value.

        :stability: experimental
        '''
        return typing.cast("HttpHeaderMatch", jsii.sinvoke(cls, "valuesIsNotInRange", [header_name, start, end]))

    @jsii.member(jsii_name="valueStartsWith") # type: ignore[misc]
    @builtins.classmethod
    def value_starts_with(
        cls,
        header_name: builtins.str,
        prefix: builtins.str,
    ) -> "HttpHeaderMatch":
        '''(experimental) The value of the header with the given name in the request must start with the specified characters.

        :param header_name: the name of the HTTP header to match against.
        :param prefix: The prefix to test against.

        :stability: experimental
        '''
        return typing.cast("HttpHeaderMatch", jsii.sinvoke(cls, "valueStartsWith", [header_name, prefix]))

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, scope: aws_cdk.core.Construct) -> "HttpHeaderMatchConfig":
        '''(experimental) Returns the header match configuration.

        :param scope: -

        :stability: experimental
        '''
        ...


class _HttpHeaderMatchProxy(HttpHeaderMatch):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> "HttpHeaderMatchConfig":
        '''(experimental) Returns the header match configuration.

        :param scope: -

        :stability: experimental
        '''
        return typing.cast("HttpHeaderMatchConfig", jsii.invoke(self, "bind", [scope]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.HttpHeaderMatchConfig",
    jsii_struct_bases=[],
    name_mapping={"http_route_header": "httpRouteHeader"},
)
class HttpHeaderMatchConfig:
    def __init__(self, *, http_route_header: CfnRoute.HttpRouteHeaderProperty) -> None:
        '''(experimental) Configuration for ``HeaderMatch``.

        :param http_route_header: (experimental) The HTTP route header.

        :stability: experimental
        '''
        if isinstance(http_route_header, dict):
            http_route_header = CfnRoute.HttpRouteHeaderProperty(**http_route_header)
        self._values: typing.Dict[str, typing.Any] = {
            "http_route_header": http_route_header,
        }

    @builtins.property
    def http_route_header(self) -> CfnRoute.HttpRouteHeaderProperty:
        '''(experimental) The HTTP route header.

        :stability: experimental
        '''
        result = self._values.get("http_route_header")
        assert result is not None, "Required property 'http_route_header' is missing"
        return typing.cast(CfnRoute.HttpRouteHeaderProperty, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpHeaderMatchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-appmesh.HttpRetryEvent")
class HttpRetryEvent(enum.Enum):
    '''(experimental) HTTP events on which to retry.

    :stability: experimental
    '''

    SERVER_ERROR = "SERVER_ERROR"
    '''(experimental) HTTP status codes 500, 501, 502, 503, 504, 505, 506, 507, 508, 510, and 511.

    :stability: experimental
    '''
    GATEWAY_ERROR = "GATEWAY_ERROR"
    '''(experimental) HTTP status codes 502, 503, and 504.

    :stability: experimental
    '''
    CLIENT_ERROR = "CLIENT_ERROR"
    '''(experimental) HTTP status code 409.

    :stability: experimental
    '''
    STREAM_ERROR = "STREAM_ERROR"
    '''(experimental) Retry on refused stream.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.HttpRetryPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "retry_attempts": "retryAttempts",
        "retry_timeout": "retryTimeout",
        "http_retry_events": "httpRetryEvents",
        "tcp_retry_events": "tcpRetryEvents",
    },
)
class HttpRetryPolicy:
    def __init__(
        self,
        *,
        retry_attempts: jsii.Number,
        retry_timeout: aws_cdk.core.Duration,
        http_retry_events: typing.Optional[typing.List[HttpRetryEvent]] = None,
        tcp_retry_events: typing.Optional[typing.List["TcpRetryEvent"]] = None,
    ) -> None:
        '''(experimental) HTTP retry policy.

        :param retry_attempts: (experimental) The maximum number of retry attempts.
        :param retry_timeout: (experimental) The timeout for each retry attempt.
        :param http_retry_events: (experimental) Specify HTTP events on which to retry. You must specify at least one value for at least one types of retry events. Default: - no retries for http events
        :param tcp_retry_events: (experimental) TCP events on which to retry. The event occurs before any processing of a request has started and is encountered when the upstream is temporarily or permanently unavailable. You must specify at least one value for at least one types of retry events. Default: - no retries for tcp events

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "retry_attempts": retry_attempts,
            "retry_timeout": retry_timeout,
        }
        if http_retry_events is not None:
            self._values["http_retry_events"] = http_retry_events
        if tcp_retry_events is not None:
            self._values["tcp_retry_events"] = tcp_retry_events

    @builtins.property
    def retry_attempts(self) -> jsii.Number:
        '''(experimental) The maximum number of retry attempts.

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        assert result is not None, "Required property 'retry_attempts' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def retry_timeout(self) -> aws_cdk.core.Duration:
        '''(experimental) The timeout for each retry attempt.

        :stability: experimental
        '''
        result = self._values.get("retry_timeout")
        assert result is not None, "Required property 'retry_timeout' is missing"
        return typing.cast(aws_cdk.core.Duration, result)

    @builtins.property
    def http_retry_events(self) -> typing.Optional[typing.List[HttpRetryEvent]]:
        '''(experimental) Specify HTTP events on which to retry.

        You must specify at least one value
        for at least one types of retry events.

        :default: - no retries for http events

        :stability: experimental
        '''
        result = self._values.get("http_retry_events")
        return typing.cast(typing.Optional[typing.List[HttpRetryEvent]], result)

    @builtins.property
    def tcp_retry_events(self) -> typing.Optional[typing.List["TcpRetryEvent"]]:
        '''(experimental) TCP events on which to retry.

        The event occurs before any processing of a
        request has started and is encountered when the upstream is temporarily or
        permanently unavailable. You must specify at least one value for at least
        one types of retry events.

        :default: - no retries for tcp events

        :stability: experimental
        '''
        result = self._values.get("tcp_retry_events")
        return typing.cast(typing.Optional[typing.List["TcpRetryEvent"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpRetryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.HttpRouteMatch",
    jsii_struct_bases=[],
    name_mapping={
        "prefix_path": "prefixPath",
        "headers": "headers",
        "method": "method",
        "protocol": "protocol",
    },
)
class HttpRouteMatch:
    def __init__(
        self,
        *,
        prefix_path: builtins.str,
        headers: typing.Optional[typing.List[HttpHeaderMatch]] = None,
        method: typing.Optional["HttpRouteMatchMethod"] = None,
        protocol: typing.Optional["HttpRouteProtocol"] = None,
    ) -> None:
        '''(experimental) The criterion for determining a request match for this GatewayRoute.

        :param prefix_path: (experimental) Specifies the path to match requests with. This parameter must always start with /, which by itself matches all requests to the virtual service name. You can also match for path-based routing of requests. For example, if your virtual service name is my-service.local and you want the route to match requests to my-service.local/metrics, your prefix should be /metrics.
        :param headers: (experimental) Specifies the client request headers to match on. All specified headers must match for the route to match. Default: - do not match on headers
        :param method: (experimental) The HTTP client request method to match on. Default: - do not match on request method
        :param protocol: (experimental) The client request protocol to match on. Applicable only for HTTP2 routes. Default: - do not match on HTTP2 request protocol

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "prefix_path": prefix_path,
        }
        if headers is not None:
            self._values["headers"] = headers
        if method is not None:
            self._values["method"] = method
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def prefix_path(self) -> builtins.str:
        '''(experimental) Specifies the path to match requests with.

        This parameter must always start with /, which by itself matches all requests to the virtual service name.
        You can also match for path-based routing of requests. For example, if your virtual service name is my-service.local
        and you want the route to match requests to my-service.local/metrics, your prefix should be /metrics.

        :stability: experimental
        '''
        result = self._values.get("prefix_path")
        assert result is not None, "Required property 'prefix_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.List[HttpHeaderMatch]]:
        '''(experimental) Specifies the client request headers to match on.

        All specified headers
        must match for the route to match.

        :default: - do not match on headers

        :stability: experimental
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.List[HttpHeaderMatch]], result)

    @builtins.property
    def method(self) -> typing.Optional["HttpRouteMatchMethod"]:
        '''(experimental) The HTTP client request method to match on.

        :default: - do not match on request method

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional["HttpRouteMatchMethod"], result)

    @builtins.property
    def protocol(self) -> typing.Optional["HttpRouteProtocol"]:
        '''(experimental) The client request protocol to match on.

        Applicable only for HTTP2 routes.

        :default: - do not match on HTTP2 request protocol

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional["HttpRouteProtocol"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpRouteMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-appmesh.HttpRouteMatchMethod")
class HttpRouteMatchMethod(enum.Enum):
    '''(experimental) Supported values for matching routes based on the HTTP request method.

    :stability: experimental
    '''

    GET = "GET"
    '''(experimental) GET request.

    :stability: experimental
    '''
    HEAD = "HEAD"
    '''(experimental) HEAD request.

    :stability: experimental
    '''
    POST = "POST"
    '''(experimental) POST request.

    :stability: experimental
    '''
    PUT = "PUT"
    '''(experimental) PUT request.

    :stability: experimental
    '''
    DELETE = "DELETE"
    '''(experimental) DELETE request.

    :stability: experimental
    '''
    CONNECT = "CONNECT"
    '''(experimental) CONNECT request.

    :stability: experimental
    '''
    OPTIONS = "OPTIONS"
    '''(experimental) OPTIONS request.

    :stability: experimental
    '''
    TRACE = "TRACE"
    '''(experimental) TRACE request.

    :stability: experimental
    '''
    PATCH = "PATCH"
    '''(experimental) PATCH request.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-appmesh.HttpRouteProtocol")
class HttpRouteProtocol(enum.Enum):
    '''(experimental) Supported :scheme options for HTTP2.

    :stability: experimental
    '''

    HTTP = "HTTP"
    '''(experimental) Match HTTP requests.

    :stability: experimental
    '''
    HTTPS = "HTTPS"
    '''(experimental) Match HTTPS requests.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.HttpTimeout",
    jsii_struct_bases=[],
    name_mapping={"idle": "idle", "per_request": "perRequest"},
)
class HttpTimeout:
    def __init__(
        self,
        *,
        idle: typing.Optional[aws_cdk.core.Duration] = None,
        per_request: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        '''(experimental) Represents timeouts for HTTP protocols.

        :param idle: (experimental) Represents an idle timeout. The amount of time that a connection may be idle. Default: - none
        :param per_request: (experimental) Represents per request timeout. Default: - 15 s

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if idle is not None:
            self._values["idle"] = idle
        if per_request is not None:
            self._values["per_request"] = per_request

    @builtins.property
    def idle(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''(experimental) Represents an idle timeout.

        The amount of time that a connection may be idle.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("idle")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def per_request(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''(experimental) Represents per request timeout.

        :default: - 15 s

        :stability: experimental
        '''
        result = self._values.get("per_request")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.HttpVirtualNodeListenerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "health_check": "healthCheck",
        "port": "port",
        "timeout": "timeout",
        "tls_certificate": "tlsCertificate",
    },
)
class HttpVirtualNodeListenerOptions:
    def __init__(
        self,
        *,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[HttpTimeout] = None,
        tls_certificate: typing.Optional["TlsCertificate"] = None,
    ) -> None:
        '''(experimental) Represent the HTTP Node Listener prorperty.

        :param health_check: (experimental) The health check information for the listener. Default: - no healthcheck
        :param port: (experimental) Port to listen for connections on. Default: - 8080
        :param timeout: (experimental) Timeout for HTTP protocol. Default: - None
        :param tls_certificate: (experimental) Represents the configuration for enabling TLS on a listener. Default: - none

        :stability: experimental
        '''
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        if isinstance(timeout, dict):
            timeout = HttpTimeout(**timeout)
        self._values: typing.Dict[str, typing.Any] = {}
        if health_check is not None:
            self._values["health_check"] = health_check
        if port is not None:
            self._values["port"] = port
        if timeout is not None:
            self._values["timeout"] = timeout
        if tls_certificate is not None:
            self._values["tls_certificate"] = tls_certificate

    @builtins.property
    def health_check(self) -> typing.Optional[HealthCheck]:
        '''(experimental) The health check information for the listener.

        :default: - no healthcheck

        :stability: experimental
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[HealthCheck], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Port to listen for connections on.

        :default: - 8080

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[HttpTimeout]:
        '''(experimental) Timeout for HTTP protocol.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[HttpTimeout], result)

    @builtins.property
    def tls_certificate(self) -> typing.Optional["TlsCertificate"]:
        '''(experimental) Represents the configuration for enabling TLS on a listener.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("tls_certificate")
        return typing.cast(typing.Optional["TlsCertificate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpVirtualNodeListenerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-appmesh.IGatewayRoute")
class IGatewayRoute(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Interface for which all GatewayRoute based classes MUST implement.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IGatewayRouteProxy"]:
        return _IGatewayRouteProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="gatewayRouteArn")
    def gateway_route_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the GatewayRoute.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="gatewayRouteName")
    def gateway_route_name(self) -> builtins.str:
        '''(experimental) The name of the GatewayRoute.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualGateway")
    def virtual_gateway(self) -> "IVirtualGateway":
        '''(experimental) The VirtualGateway the GatewayRoute belongs to.

        :stability: experimental
        '''
        ...


class _IGatewayRouteProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''(experimental) Interface for which all GatewayRoute based classes MUST implement.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-appmesh.IGatewayRoute"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="gatewayRouteArn")
    def gateway_route_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the GatewayRoute.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "gatewayRouteArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="gatewayRouteName")
    def gateway_route_name(self) -> builtins.str:
        '''(experimental) The name of the GatewayRoute.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "gatewayRouteName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualGateway")
    def virtual_gateway(self) -> "IVirtualGateway":
        '''(experimental) The VirtualGateway the GatewayRoute belongs to.

        :stability: experimental
        '''
        return typing.cast("IVirtualGateway", jsii.get(self, "virtualGateway"))


@jsii.interface(jsii_type="@aws-cdk/aws-appmesh.IMesh")
class IMesh(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Interface wich all Mesh based classes MUST implement.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IMeshProxy"]:
        return _IMeshProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshArn")
    def mesh_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the AppMesh mesh.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> builtins.str:
        '''(experimental) The name of the AppMesh mesh.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addVirtualGateway")
    def add_virtual_gateway(
        self,
        id: builtins.str,
        *,
        access_log: typing.Optional[AccessLog] = None,
        backend_defaults: typing.Optional[BackendDefaults] = None,
        listeners: typing.Optional[typing.List["VirtualGatewayListener"]] = None,
        virtual_gateway_name: typing.Optional[builtins.str] = None,
    ) -> "VirtualGateway":
        '''(experimental) Adds a VirtualGateway to the Mesh.

        :param id: -
        :param access_log: (experimental) Access Logging Configuration for the VirtualGateway. Default: - no access logging
        :param backend_defaults: (experimental) Default Configuration Virtual Node uses to communicate with Virtual Service. Default: - No Config
        :param listeners: (experimental) Listeners for the VirtualGateway. Only one is supported. Default: - Single HTTP listener on port 8080
        :param virtual_gateway_name: (experimental) Name of the VirtualGateway. Default: - A name is automatically determined

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addVirtualNode")
    def add_virtual_node(
        self,
        id: builtins.str,
        *,
        access_log: typing.Optional[AccessLog] = None,
        backend_defaults: typing.Optional[BackendDefaults] = None,
        backends: typing.Optional[typing.List[Backend]] = None,
        listeners: typing.Optional[typing.List["VirtualNodeListener"]] = None,
        service_discovery: typing.Optional["ServiceDiscovery"] = None,
        virtual_node_name: typing.Optional[builtins.str] = None,
    ) -> "VirtualNode":
        '''(experimental) Adds a VirtualNode to the Mesh.

        :param id: -
        :param access_log: (experimental) Access Logging Configuration for the virtual node. Default: - No access logging
        :param backend_defaults: (experimental) Default Configuration Virtual Node uses to communicate with Virtual Service. Default: - No Config
        :param backends: (experimental) Virtual Services that this is node expected to send outbound traffic to. Default: - No backends
        :param listeners: (experimental) Initial listener for the virtual node. Default: - No listeners
        :param service_discovery: (experimental) Defines how upstream clients will discover this VirtualNode. Default: - No Service Discovery
        :param virtual_node_name: (experimental) The name of the VirtualNode. Default: - A name is automatically determined

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addVirtualRouter")
    def add_virtual_router(
        self,
        id: builtins.str,
        *,
        listeners: typing.Optional[typing.List["VirtualRouterListener"]] = None,
        virtual_router_name: typing.Optional[builtins.str] = None,
    ) -> "VirtualRouter":
        '''(experimental) Adds a VirtualRouter to the Mesh with the given id and props.

        :param id: -
        :param listeners: (experimental) Listener specification for the VirtualRouter. Default: - A listener on HTTP port 8080
        :param virtual_router_name: (experimental) The name of the VirtualRouter. Default: - A name is automatically determined

        :stability: experimental
        '''
        ...


class _IMeshProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''(experimental) Interface wich all Mesh based classes MUST implement.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-appmesh.IMesh"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshArn")
    def mesh_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the AppMesh mesh.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "meshArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> builtins.str:
        '''(experimental) The name of the AppMesh mesh.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "meshName"))

    @jsii.member(jsii_name="addVirtualGateway")
    def add_virtual_gateway(
        self,
        id: builtins.str,
        *,
        access_log: typing.Optional[AccessLog] = None,
        backend_defaults: typing.Optional[BackendDefaults] = None,
        listeners: typing.Optional[typing.List["VirtualGatewayListener"]] = None,
        virtual_gateway_name: typing.Optional[builtins.str] = None,
    ) -> "VirtualGateway":
        '''(experimental) Adds a VirtualGateway to the Mesh.

        :param id: -
        :param access_log: (experimental) Access Logging Configuration for the VirtualGateway. Default: - no access logging
        :param backend_defaults: (experimental) Default Configuration Virtual Node uses to communicate with Virtual Service. Default: - No Config
        :param listeners: (experimental) Listeners for the VirtualGateway. Only one is supported. Default: - Single HTTP listener on port 8080
        :param virtual_gateway_name: (experimental) Name of the VirtualGateway. Default: - A name is automatically determined

        :stability: experimental
        '''
        props = VirtualGatewayBaseProps(
            access_log=access_log,
            backend_defaults=backend_defaults,
            listeners=listeners,
            virtual_gateway_name=virtual_gateway_name,
        )

        return typing.cast("VirtualGateway", jsii.invoke(self, "addVirtualGateway", [id, props]))

    @jsii.member(jsii_name="addVirtualNode")
    def add_virtual_node(
        self,
        id: builtins.str,
        *,
        access_log: typing.Optional[AccessLog] = None,
        backend_defaults: typing.Optional[BackendDefaults] = None,
        backends: typing.Optional[typing.List[Backend]] = None,
        listeners: typing.Optional[typing.List["VirtualNodeListener"]] = None,
        service_discovery: typing.Optional["ServiceDiscovery"] = None,
        virtual_node_name: typing.Optional[builtins.str] = None,
    ) -> "VirtualNode":
        '''(experimental) Adds a VirtualNode to the Mesh.

        :param id: -
        :param access_log: (experimental) Access Logging Configuration for the virtual node. Default: - No access logging
        :param backend_defaults: (experimental) Default Configuration Virtual Node uses to communicate with Virtual Service. Default: - No Config
        :param backends: (experimental) Virtual Services that this is node expected to send outbound traffic to. Default: - No backends
        :param listeners: (experimental) Initial listener for the virtual node. Default: - No listeners
        :param service_discovery: (experimental) Defines how upstream clients will discover this VirtualNode. Default: - No Service Discovery
        :param virtual_node_name: (experimental) The name of the VirtualNode. Default: - A name is automatically determined

        :stability: experimental
        '''
        props = VirtualNodeBaseProps(
            access_log=access_log,
            backend_defaults=backend_defaults,
            backends=backends,
            listeners=listeners,
            service_discovery=service_discovery,
            virtual_node_name=virtual_node_name,
        )

        return typing.cast("VirtualNode", jsii.invoke(self, "addVirtualNode", [id, props]))

    @jsii.member(jsii_name="addVirtualRouter")
    def add_virtual_router(
        self,
        id: builtins.str,
        *,
        listeners: typing.Optional[typing.List["VirtualRouterListener"]] = None,
        virtual_router_name: typing.Optional[builtins.str] = None,
    ) -> "VirtualRouter":
        '''(experimental) Adds a VirtualRouter to the Mesh with the given id and props.

        :param id: -
        :param listeners: (experimental) Listener specification for the VirtualRouter. Default: - A listener on HTTP port 8080
        :param virtual_router_name: (experimental) The name of the VirtualRouter. Default: - A name is automatically determined

        :stability: experimental
        '''
        props = VirtualRouterBaseProps(
            listeners=listeners, virtual_router_name=virtual_router_name
        )

        return typing.cast("VirtualRouter", jsii.invoke(self, "addVirtualRouter", [id, props]))


@jsii.interface(jsii_type="@aws-cdk/aws-appmesh.IRoute")
class IRoute(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Interface for which all Route based classes MUST implement.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IRouteProxy"]:
        return _IRouteProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="routeArn")
    def route_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the route.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="routeName")
    def route_name(self) -> builtins.str:
        '''(experimental) The name of the route.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualRouter")
    def virtual_router(self) -> "IVirtualRouter":
        '''(experimental) The VirtualRouter the Route belongs to.

        :stability: experimental
        '''
        ...


class _IRouteProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''(experimental) Interface for which all Route based classes MUST implement.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-appmesh.IRoute"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="routeArn")
    def route_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the route.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="routeName")
    def route_name(self) -> builtins.str:
        '''(experimental) The name of the route.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualRouter")
    def virtual_router(self) -> "IVirtualRouter":
        '''(experimental) The VirtualRouter the Route belongs to.

        :stability: experimental
        '''
        return typing.cast("IVirtualRouter", jsii.get(self, "virtualRouter"))


@jsii.interface(jsii_type="@aws-cdk/aws-appmesh.IVirtualGateway")
class IVirtualGateway(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Interface which all Virtual Gateway based classes must implement.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IVirtualGatewayProxy"]:
        return _IVirtualGatewayProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualGateway belongs to.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualGatewayArn")
    def virtual_gateway_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the VirtualGateway.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualGatewayName")
    def virtual_gateway_name(self) -> builtins.str:
        '''(experimental) Name of the VirtualGateway.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addGatewayRoute")
    def add_gateway_route(
        self,
        id: builtins.str,
        *,
        route_spec: GatewayRouteSpec,
        gateway_route_name: typing.Optional[builtins.str] = None,
    ) -> "GatewayRoute":
        '''(experimental) Utility method to add a new GatewayRoute to the VirtualGateway.

        :param id: -
        :param route_spec: (experimental) What protocol the route uses.
        :param gateway_route_name: (experimental) The name of the GatewayRoute. Default: - an automatically generated name

        :stability: experimental
        '''
        ...


class _IVirtualGatewayProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''(experimental) Interface which all Virtual Gateway based classes must implement.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-appmesh.IVirtualGateway"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualGateway belongs to.

        :stability: experimental
        '''
        return typing.cast(IMesh, jsii.get(self, "mesh"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualGatewayArn")
    def virtual_gateway_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the VirtualGateway.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualGatewayArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualGatewayName")
    def virtual_gateway_name(self) -> builtins.str:
        '''(experimental) Name of the VirtualGateway.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualGatewayName"))

    @jsii.member(jsii_name="addGatewayRoute")
    def add_gateway_route(
        self,
        id: builtins.str,
        *,
        route_spec: GatewayRouteSpec,
        gateway_route_name: typing.Optional[builtins.str] = None,
    ) -> "GatewayRoute":
        '''(experimental) Utility method to add a new GatewayRoute to the VirtualGateway.

        :param id: -
        :param route_spec: (experimental) What protocol the route uses.
        :param gateway_route_name: (experimental) The name of the GatewayRoute. Default: - an automatically generated name

        :stability: experimental
        '''
        route = GatewayRouteBaseProps(
            route_spec=route_spec, gateway_route_name=gateway_route_name
        )

        return typing.cast("GatewayRoute", jsii.invoke(self, "addGatewayRoute", [id, route]))


@jsii.interface(jsii_type="@aws-cdk/aws-appmesh.IVirtualNode")
class IVirtualNode(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Interface which all VirtualNode based classes must implement.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IVirtualNodeProxy"]:
        return _IVirtualNodeProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualNode belongs to.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualNodeArn")
    def virtual_node_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name belonging to the VirtualNode.

        Set this value as the APPMESH_VIRTUAL_NODE_NAME environment variable for
        your task group's Envoy proxy container in your task definition or pod
        spec.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualNodeName")
    def virtual_node_name(self) -> builtins.str:
        '''(experimental) The name of the VirtualNode.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IVirtualNodeProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''(experimental) Interface which all VirtualNode based classes must implement.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-appmesh.IVirtualNode"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualNode belongs to.

        :stability: experimental
        '''
        return typing.cast(IMesh, jsii.get(self, "mesh"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualNodeArn")
    def virtual_node_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name belonging to the VirtualNode.

        Set this value as the APPMESH_VIRTUAL_NODE_NAME environment variable for
        your task group's Envoy proxy container in your task definition or pod
        spec.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualNodeArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualNodeName")
    def virtual_node_name(self) -> builtins.str:
        '''(experimental) The name of the VirtualNode.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualNodeName"))


@jsii.interface(jsii_type="@aws-cdk/aws-appmesh.IVirtualRouter")
class IVirtualRouter(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Interface which all VirtualRouter based classes MUST implement.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IVirtualRouterProxy"]:
        return _IVirtualRouterProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualRouter belongs to.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualRouterArn")
    def virtual_router_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the VirtualRouter.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualRouterName")
    def virtual_router_name(self) -> builtins.str:
        '''(experimental) The name of the VirtualRouter.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addRoute")
    def add_route(
        self,
        id: builtins.str,
        *,
        route_spec: "RouteSpec",
        route_name: typing.Optional[builtins.str] = None,
    ) -> "Route":
        '''(experimental) Add a single route to the router.

        :param id: -
        :param route_spec: (experimental) Protocol specific spec.
        :param route_name: (experimental) The name of the route. Default: - An automatically generated name

        :stability: experimental
        '''
        ...


class _IVirtualRouterProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''(experimental) Interface which all VirtualRouter based classes MUST implement.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-appmesh.IVirtualRouter"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualRouter belongs to.

        :stability: experimental
        '''
        return typing.cast(IMesh, jsii.get(self, "mesh"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualRouterArn")
    def virtual_router_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the VirtualRouter.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualRouterArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualRouterName")
    def virtual_router_name(self) -> builtins.str:
        '''(experimental) The name of the VirtualRouter.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualRouterName"))

    @jsii.member(jsii_name="addRoute")
    def add_route(
        self,
        id: builtins.str,
        *,
        route_spec: "RouteSpec",
        route_name: typing.Optional[builtins.str] = None,
    ) -> "Route":
        '''(experimental) Add a single route to the router.

        :param id: -
        :param route_spec: (experimental) Protocol specific spec.
        :param route_name: (experimental) The name of the route. Default: - An automatically generated name

        :stability: experimental
        '''
        props = RouteBaseProps(route_spec=route_spec, route_name=route_name)

        return typing.cast("Route", jsii.invoke(self, "addRoute", [id, props]))


@jsii.interface(jsii_type="@aws-cdk/aws-appmesh.IVirtualService")
class IVirtualService(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Represents the interface which all VirtualService based classes MUST implement.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IVirtualServiceProxy"]:
        return _IVirtualServiceProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualService belongs to.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualServiceArn")
    def virtual_service_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the virtual service.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualServiceName")
    def virtual_service_name(self) -> builtins.str:
        '''(experimental) The name of the VirtualService.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IVirtualServiceProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''(experimental) Represents the interface which all VirtualService based classes MUST implement.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-appmesh.IVirtualService"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualService belongs to.

        :stability: experimental
        '''
        return typing.cast(IMesh, jsii.get(self, "mesh"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualServiceArn")
    def virtual_service_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the virtual service.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualServiceArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualServiceName")
    def virtual_service_name(self) -> builtins.str:
        '''(experimental) The name of the VirtualService.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualServiceName"))


@jsii.implements(IMesh)
class Mesh(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appmesh.Mesh",
):
    '''(experimental) Define a new AppMesh mesh.

    :see: https://docs.aws.amazon.com/app-mesh/latest/userguide/meshes.html
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        egress_filter: typing.Optional["MeshFilterType"] = None,
        mesh_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param egress_filter: (experimental) Egress filter to be applied to the Mesh. Default: DROP_ALL
        :param mesh_name: (experimental) The name of the Mesh being defined. Default: - A name is autmoatically generated

        :stability: experimental
        '''
        props = MeshProps(egress_filter=egress_filter, mesh_name=mesh_name)

        jsii.create(Mesh, self, [scope, id, props])

    @jsii.member(jsii_name="fromMeshArn") # type: ignore[misc]
    @builtins.classmethod
    def from_mesh_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        mesh_arn: builtins.str,
    ) -> IMesh:
        '''(experimental) Import an existing mesh by arn.

        :param scope: -
        :param id: -
        :param mesh_arn: -

        :stability: experimental
        '''
        return typing.cast(IMesh, jsii.sinvoke(cls, "fromMeshArn", [scope, id, mesh_arn]))

    @jsii.member(jsii_name="fromMeshName") # type: ignore[misc]
    @builtins.classmethod
    def from_mesh_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        mesh_name: builtins.str,
    ) -> IMesh:
        '''(experimental) Import an existing mesh by name.

        :param scope: -
        :param id: -
        :param mesh_name: -

        :stability: experimental
        '''
        return typing.cast(IMesh, jsii.sinvoke(cls, "fromMeshName", [scope, id, mesh_name]))

    @jsii.member(jsii_name="addVirtualGateway")
    def add_virtual_gateway(
        self,
        id: builtins.str,
        *,
        access_log: typing.Optional[AccessLog] = None,
        backend_defaults: typing.Optional[BackendDefaults] = None,
        listeners: typing.Optional[typing.List["VirtualGatewayListener"]] = None,
        virtual_gateway_name: typing.Optional[builtins.str] = None,
    ) -> "VirtualGateway":
        '''(experimental) Adds a VirtualGateway to the Mesh.

        :param id: -
        :param access_log: (experimental) Access Logging Configuration for the VirtualGateway. Default: - no access logging
        :param backend_defaults: (experimental) Default Configuration Virtual Node uses to communicate with Virtual Service. Default: - No Config
        :param listeners: (experimental) Listeners for the VirtualGateway. Only one is supported. Default: - Single HTTP listener on port 8080
        :param virtual_gateway_name: (experimental) Name of the VirtualGateway. Default: - A name is automatically determined

        :stability: experimental
        '''
        props = VirtualGatewayBaseProps(
            access_log=access_log,
            backend_defaults=backend_defaults,
            listeners=listeners,
            virtual_gateway_name=virtual_gateway_name,
        )

        return typing.cast("VirtualGateway", jsii.invoke(self, "addVirtualGateway", [id, props]))

    @jsii.member(jsii_name="addVirtualNode")
    def add_virtual_node(
        self,
        id: builtins.str,
        *,
        access_log: typing.Optional[AccessLog] = None,
        backend_defaults: typing.Optional[BackendDefaults] = None,
        backends: typing.Optional[typing.List[Backend]] = None,
        listeners: typing.Optional[typing.List["VirtualNodeListener"]] = None,
        service_discovery: typing.Optional["ServiceDiscovery"] = None,
        virtual_node_name: typing.Optional[builtins.str] = None,
    ) -> "VirtualNode":
        '''(experimental) Adds a VirtualNode to the Mesh.

        :param id: -
        :param access_log: (experimental) Access Logging Configuration for the virtual node. Default: - No access logging
        :param backend_defaults: (experimental) Default Configuration Virtual Node uses to communicate with Virtual Service. Default: - No Config
        :param backends: (experimental) Virtual Services that this is node expected to send outbound traffic to. Default: - No backends
        :param listeners: (experimental) Initial listener for the virtual node. Default: - No listeners
        :param service_discovery: (experimental) Defines how upstream clients will discover this VirtualNode. Default: - No Service Discovery
        :param virtual_node_name: (experimental) The name of the VirtualNode. Default: - A name is automatically determined

        :stability: experimental
        '''
        props = VirtualNodeBaseProps(
            access_log=access_log,
            backend_defaults=backend_defaults,
            backends=backends,
            listeners=listeners,
            service_discovery=service_discovery,
            virtual_node_name=virtual_node_name,
        )

        return typing.cast("VirtualNode", jsii.invoke(self, "addVirtualNode", [id, props]))

    @jsii.member(jsii_name="addVirtualRouter")
    def add_virtual_router(
        self,
        id: builtins.str,
        *,
        listeners: typing.Optional[typing.List["VirtualRouterListener"]] = None,
        virtual_router_name: typing.Optional[builtins.str] = None,
    ) -> "VirtualRouter":
        '''(experimental) Adds a VirtualRouter to the Mesh with the given id and props.

        :param id: -
        :param listeners: (experimental) Listener specification for the VirtualRouter. Default: - A listener on HTTP port 8080
        :param virtual_router_name: (experimental) The name of the VirtualRouter. Default: - A name is automatically determined

        :stability: experimental
        '''
        props = VirtualRouterBaseProps(
            listeners=listeners, virtual_router_name=virtual_router_name
        )

        return typing.cast("VirtualRouter", jsii.invoke(self, "addVirtualRouter", [id, props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshArn")
    def mesh_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the AppMesh mesh.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "meshArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> builtins.str:
        '''(experimental) The name of the AppMesh mesh.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "meshName"))


@jsii.enum(jsii_type="@aws-cdk/aws-appmesh.MeshFilterType")
class MeshFilterType(enum.Enum):
    '''(experimental) A utility enum defined for the egressFilter type property, the default of DROP_ALL, allows traffic only to other resources inside the mesh, or API calls to amazon resources.

    :default: DROP_ALL

    :stability: experimental
    '''

    ALLOW_ALL = "ALLOW_ALL"
    '''(experimental) Allows all outbound traffic.

    :stability: experimental
    '''
    DROP_ALL = "DROP_ALL"
    '''(experimental) Allows traffic only to other resources inside the mesh, or API calls to amazon resources.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.MeshProps",
    jsii_struct_bases=[],
    name_mapping={"egress_filter": "egressFilter", "mesh_name": "meshName"},
)
class MeshProps:
    def __init__(
        self,
        *,
        egress_filter: typing.Optional[MeshFilterType] = None,
        mesh_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The set of properties used when creating a Mesh.

        :param egress_filter: (experimental) Egress filter to be applied to the Mesh. Default: DROP_ALL
        :param mesh_name: (experimental) The name of the Mesh being defined. Default: - A name is autmoatically generated

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if egress_filter is not None:
            self._values["egress_filter"] = egress_filter
        if mesh_name is not None:
            self._values["mesh_name"] = mesh_name

    @builtins.property
    def egress_filter(self) -> typing.Optional[MeshFilterType]:
        '''(experimental) Egress filter to be applied to the Mesh.

        :default: DROP_ALL

        :stability: experimental
        '''
        result = self._values.get("egress_filter")
        return typing.cast(typing.Optional[MeshFilterType], result)

    @builtins.property
    def mesh_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the Mesh being defined.

        :default: - A name is autmoatically generated

        :stability: experimental
        '''
        result = self._values.get("mesh_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MeshProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-appmesh.Protocol")
class Protocol(enum.Enum):
    '''(experimental) Enum of supported AppMesh protocols.

    :stability: experimental
    '''

    HTTP = "HTTP"
    '''
    :stability: experimental
    '''
    TCP = "TCP"
    '''
    :stability: experimental
    '''
    HTTP2 = "HTTP2"
    '''
    :stability: experimental
    '''
    GRPC = "GRPC"
    '''
    :stability: experimental
    '''


@jsii.implements(IRoute)
class Route(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appmesh.Route",
):
    '''(experimental) Route represents a new or existing route attached to a VirtualRouter and Mesh.

    :see: https://docs.aws.amazon.com/app-mesh/latest/userguide/routes.html
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        mesh: IMesh,
        virtual_router: IVirtualRouter,
        route_spec: "RouteSpec",
        route_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param mesh: (experimental) The service mesh to define the route in.
        :param virtual_router: (experimental) The VirtualRouter the Route belongs to.
        :param route_spec: (experimental) Protocol specific spec.
        :param route_name: (experimental) The name of the route. Default: - An automatically generated name

        :stability: experimental
        '''
        props = RouteProps(
            mesh=mesh,
            virtual_router=virtual_router,
            route_spec=route_spec,
            route_name=route_name,
        )

        jsii.create(Route, self, [scope, id, props])

    @jsii.member(jsii_name="fromRouteArn") # type: ignore[misc]
    @builtins.classmethod
    def from_route_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        route_arn: builtins.str,
    ) -> IRoute:
        '''(experimental) Import an existing Route given an ARN.

        :param scope: -
        :param id: -
        :param route_arn: -

        :stability: experimental
        '''
        return typing.cast(IRoute, jsii.sinvoke(cls, "fromRouteArn", [scope, id, route_arn]))

    @jsii.member(jsii_name="fromRouteAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_route_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        route_name: builtins.str,
        virtual_router: IVirtualRouter,
    ) -> IRoute:
        '''(experimental) Import an existing Route given attributes.

        :param scope: -
        :param id: -
        :param route_name: (experimental) The name of the Route.
        :param virtual_router: (experimental) The VirtualRouter the Route belongs to.

        :stability: experimental
        '''
        attrs = RouteAttributes(route_name=route_name, virtual_router=virtual_router)

        return typing.cast(IRoute, jsii.sinvoke(cls, "fromRouteAttributes", [scope, id, attrs]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="routeArn")
    def route_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the route.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="routeName")
    def route_name(self) -> builtins.str:
        '''(experimental) The name of the Route.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualRouter")
    def virtual_router(self) -> IVirtualRouter:
        '''(experimental) The VirtualRouter the Route belongs to.

        :stability: experimental
        '''
        return typing.cast(IVirtualRouter, jsii.get(self, "virtualRouter"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.RouteAttributes",
    jsii_struct_bases=[],
    name_mapping={"route_name": "routeName", "virtual_router": "virtualRouter"},
)
class RouteAttributes:
    def __init__(
        self,
        *,
        route_name: builtins.str,
        virtual_router: IVirtualRouter,
    ) -> None:
        '''(experimental) Interface with properties ncecessary to import a reusable Route.

        :param route_name: (experimental) The name of the Route.
        :param virtual_router: (experimental) The VirtualRouter the Route belongs to.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "route_name": route_name,
            "virtual_router": virtual_router,
        }

    @builtins.property
    def route_name(self) -> builtins.str:
        '''(experimental) The name of the Route.

        :stability: experimental
        '''
        result = self._values.get("route_name")
        assert result is not None, "Required property 'route_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_router(self) -> IVirtualRouter:
        '''(experimental) The VirtualRouter the Route belongs to.

        :stability: experimental
        '''
        result = self._values.get("virtual_router")
        assert result is not None, "Required property 'virtual_router' is missing"
        return typing.cast(IVirtualRouter, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RouteAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.RouteBaseProps",
    jsii_struct_bases=[],
    name_mapping={"route_spec": "routeSpec", "route_name": "routeName"},
)
class RouteBaseProps:
    def __init__(
        self,
        *,
        route_spec: "RouteSpec",
        route_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Base interface properties for all Routes.

        :param route_spec: (experimental) Protocol specific spec.
        :param route_name: (experimental) The name of the route. Default: - An automatically generated name

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "route_spec": route_spec,
        }
        if route_name is not None:
            self._values["route_name"] = route_name

    @builtins.property
    def route_spec(self) -> "RouteSpec":
        '''(experimental) Protocol specific spec.

        :stability: experimental
        '''
        result = self._values.get("route_spec")
        assert result is not None, "Required property 'route_spec' is missing"
        return typing.cast("RouteSpec", result)

    @builtins.property
    def route_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the route.

        :default: - An automatically generated name

        :stability: experimental
        '''
        result = self._values.get("route_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RouteBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.RouteProps",
    jsii_struct_bases=[RouteBaseProps],
    name_mapping={
        "route_spec": "routeSpec",
        "route_name": "routeName",
        "mesh": "mesh",
        "virtual_router": "virtualRouter",
    },
)
class RouteProps(RouteBaseProps):
    def __init__(
        self,
        *,
        route_spec: "RouteSpec",
        route_name: typing.Optional[builtins.str] = None,
        mesh: IMesh,
        virtual_router: IVirtualRouter,
    ) -> None:
        '''(experimental) Properties to define new Routes.

        :param route_spec: (experimental) Protocol specific spec.
        :param route_name: (experimental) The name of the route. Default: - An automatically generated name
        :param mesh: (experimental) The service mesh to define the route in.
        :param virtual_router: (experimental) The VirtualRouter the Route belongs to.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "route_spec": route_spec,
            "mesh": mesh,
            "virtual_router": virtual_router,
        }
        if route_name is not None:
            self._values["route_name"] = route_name

    @builtins.property
    def route_spec(self) -> "RouteSpec":
        '''(experimental) Protocol specific spec.

        :stability: experimental
        '''
        result = self._values.get("route_spec")
        assert result is not None, "Required property 'route_spec' is missing"
        return typing.cast("RouteSpec", result)

    @builtins.property
    def route_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the route.

        :default: - An automatically generated name

        :stability: experimental
        '''
        result = self._values.get("route_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh(self) -> IMesh:
        '''(experimental) The service mesh to define the route in.

        :stability: experimental
        '''
        result = self._values.get("mesh")
        assert result is not None, "Required property 'mesh' is missing"
        return typing.cast(IMesh, result)

    @builtins.property
    def virtual_router(self) -> IVirtualRouter:
        '''(experimental) The VirtualRouter the Route belongs to.

        :stability: experimental
        '''
        result = self._values.get("virtual_router")
        assert result is not None, "Required property 'virtual_router' is missing"
        return typing.cast(IVirtualRouter, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RouteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RouteSpec(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-appmesh.RouteSpec",
):
    '''(experimental) Used to generate specs with different protocols for a RouteSpec.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_RouteSpecProxy"]:
        return _RouteSpecProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(RouteSpec, self, [])

    @jsii.member(jsii_name="grpc") # type: ignore[misc]
    @builtins.classmethod
    def grpc(
        cls,
        *,
        match: GrpcRouteMatch,
        weighted_targets: typing.List["WeightedTarget"],
        retry_policy: typing.Optional["GrpcRetryPolicy"] = None,
        timeout: typing.Optional[GrpcTimeout] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> "RouteSpec":
        '''(experimental) Creates a GRPC Based RouteSpec.

        :param match: (experimental) The criterion for determining a request match for this Route.
        :param weighted_targets: (experimental) List of targets that traffic is routed to when a request matches the route.
        :param retry_policy: (experimental) The retry policy. Default: - no retry policy
        :param timeout: (experimental) An object that represents a grpc timeout. Default: - None
        :param priority: (experimental) The priority for the route. Routes are matched based on the specified value, where 0 is the highest priority. Default: - no particular priority

        :stability: experimental
        '''
        options = GrpcRouteSpecOptions(
            match=match,
            weighted_targets=weighted_targets,
            retry_policy=retry_policy,
            timeout=timeout,
            priority=priority,
        )

        return typing.cast("RouteSpec", jsii.sinvoke(cls, "grpc", [options]))

    @jsii.member(jsii_name="http") # type: ignore[misc]
    @builtins.classmethod
    def http(
        cls,
        *,
        weighted_targets: typing.List["WeightedTarget"],
        match: typing.Optional[HttpRouteMatch] = None,
        retry_policy: typing.Optional[HttpRetryPolicy] = None,
        timeout: typing.Optional[HttpTimeout] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> "RouteSpec":
        '''(experimental) Creates an HTTP Based RouteSpec.

        :param weighted_targets: (experimental) List of targets that traffic is routed to when a request matches the route.
        :param match: (experimental) The criterion for determining a request match for this Route. Default: - matches on '/'
        :param retry_policy: (experimental) The retry policy. Default: - no retry policy
        :param timeout: (experimental) An object that represents a http timeout. Default: - None
        :param priority: (experimental) The priority for the route. Routes are matched based on the specified value, where 0 is the highest priority. Default: - no particular priority

        :stability: experimental
        '''
        options = HttpRouteSpecOptions(
            weighted_targets=weighted_targets,
            match=match,
            retry_policy=retry_policy,
            timeout=timeout,
            priority=priority,
        )

        return typing.cast("RouteSpec", jsii.sinvoke(cls, "http", [options]))

    @jsii.member(jsii_name="http2") # type: ignore[misc]
    @builtins.classmethod
    def http2(
        cls,
        *,
        weighted_targets: typing.List["WeightedTarget"],
        match: typing.Optional[HttpRouteMatch] = None,
        retry_policy: typing.Optional[HttpRetryPolicy] = None,
        timeout: typing.Optional[HttpTimeout] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> "RouteSpec":
        '''(experimental) Creates an HTTP2 Based RouteSpec.

        :param weighted_targets: (experimental) List of targets that traffic is routed to when a request matches the route.
        :param match: (experimental) The criterion for determining a request match for this Route. Default: - matches on '/'
        :param retry_policy: (experimental) The retry policy. Default: - no retry policy
        :param timeout: (experimental) An object that represents a http timeout. Default: - None
        :param priority: (experimental) The priority for the route. Routes are matched based on the specified value, where 0 is the highest priority. Default: - no particular priority

        :stability: experimental
        '''
        options = HttpRouteSpecOptions(
            weighted_targets=weighted_targets,
            match=match,
            retry_policy=retry_policy,
            timeout=timeout,
            priority=priority,
        )

        return typing.cast("RouteSpec", jsii.sinvoke(cls, "http2", [options]))

    @jsii.member(jsii_name="tcp") # type: ignore[misc]
    @builtins.classmethod
    def tcp(
        cls,
        *,
        weighted_targets: typing.List["WeightedTarget"],
        timeout: typing.Optional["TcpTimeout"] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> "RouteSpec":
        '''(experimental) Creates a TCP Based RouteSpec.

        :param weighted_targets: (experimental) List of targets that traffic is routed to when a request matches the route.
        :param timeout: (experimental) An object that represents a tcp timeout. Default: - None
        :param priority: (experimental) The priority for the route. Routes are matched based on the specified value, where 0 is the highest priority. Default: - no particular priority

        :stability: experimental
        '''
        options = TcpRouteSpecOptions(
            weighted_targets=weighted_targets, timeout=timeout, priority=priority
        )

        return typing.cast("RouteSpec", jsii.sinvoke(cls, "tcp", [options]))

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, scope: aws_cdk.core.Construct) -> "RouteSpecConfig":
        '''(experimental) Called when the GatewayRouteSpec type is initialized.

        Can be used to enforce
        mutual exclusivity with future properties

        :param scope: -

        :stability: experimental
        '''
        ...


class _RouteSpecProxy(RouteSpec):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> "RouteSpecConfig":
        '''(experimental) Called when the GatewayRouteSpec type is initialized.

        Can be used to enforce
        mutual exclusivity with future properties

        :param scope: -

        :stability: experimental
        '''
        return typing.cast("RouteSpecConfig", jsii.invoke(self, "bind", [scope]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.RouteSpecConfig",
    jsii_struct_bases=[],
    name_mapping={
        "grpc_route_spec": "grpcRouteSpec",
        "http2_route_spec": "http2RouteSpec",
        "http_route_spec": "httpRouteSpec",
        "priority": "priority",
        "tcp_route_spec": "tcpRouteSpec",
    },
)
class RouteSpecConfig:
    def __init__(
        self,
        *,
        grpc_route_spec: typing.Optional[CfnRoute.GrpcRouteProperty] = None,
        http2_route_spec: typing.Optional[CfnRoute.HttpRouteProperty] = None,
        http_route_spec: typing.Optional[CfnRoute.HttpRouteProperty] = None,
        priority: typing.Optional[jsii.Number] = None,
        tcp_route_spec: typing.Optional[CfnRoute.TcpRouteProperty] = None,
    ) -> None:
        '''(experimental) All Properties for GatewayRoute Specs.

        :param grpc_route_spec: (experimental) The spec for a grpc route. Default: - no grpc spec
        :param http2_route_spec: (experimental) The spec for an http2 route. Default: - no http2 spec
        :param http_route_spec: (experimental) The spec for an http route. Default: - no http spec
        :param priority: (experimental) The priority for the route. Routes are matched based on the specified value, where 0 is the highest priority. Default: - no particular priority
        :param tcp_route_spec: (experimental) The spec for a tcp route. Default: - no tcp spec

        :stability: experimental
        '''
        if isinstance(grpc_route_spec, dict):
            grpc_route_spec = CfnRoute.GrpcRouteProperty(**grpc_route_spec)
        if isinstance(http2_route_spec, dict):
            http2_route_spec = CfnRoute.HttpRouteProperty(**http2_route_spec)
        if isinstance(http_route_spec, dict):
            http_route_spec = CfnRoute.HttpRouteProperty(**http_route_spec)
        if isinstance(tcp_route_spec, dict):
            tcp_route_spec = CfnRoute.TcpRouteProperty(**tcp_route_spec)
        self._values: typing.Dict[str, typing.Any] = {}
        if grpc_route_spec is not None:
            self._values["grpc_route_spec"] = grpc_route_spec
        if http2_route_spec is not None:
            self._values["http2_route_spec"] = http2_route_spec
        if http_route_spec is not None:
            self._values["http_route_spec"] = http_route_spec
        if priority is not None:
            self._values["priority"] = priority
        if tcp_route_spec is not None:
            self._values["tcp_route_spec"] = tcp_route_spec

    @builtins.property
    def grpc_route_spec(self) -> typing.Optional[CfnRoute.GrpcRouteProperty]:
        '''(experimental) The spec for a grpc route.

        :default: - no grpc spec

        :stability: experimental
        '''
        result = self._values.get("grpc_route_spec")
        return typing.cast(typing.Optional[CfnRoute.GrpcRouteProperty], result)

    @builtins.property
    def http2_route_spec(self) -> typing.Optional[CfnRoute.HttpRouteProperty]:
        '''(experimental) The spec for an http2 route.

        :default: - no http2 spec

        :stability: experimental
        '''
        result = self._values.get("http2_route_spec")
        return typing.cast(typing.Optional[CfnRoute.HttpRouteProperty], result)

    @builtins.property
    def http_route_spec(self) -> typing.Optional[CfnRoute.HttpRouteProperty]:
        '''(experimental) The spec for an http route.

        :default: - no http spec

        :stability: experimental
        '''
        result = self._values.get("http_route_spec")
        return typing.cast(typing.Optional[CfnRoute.HttpRouteProperty], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority for the route.

        Routes are matched based on the specified
        value, where 0 is the highest priority.

        :default: - no particular priority

        :stability: experimental
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_route_spec(self) -> typing.Optional[CfnRoute.TcpRouteProperty]:
        '''(experimental) The spec for a tcp route.

        :default: - no tcp spec

        :stability: experimental
        '''
        result = self._values.get("tcp_route_spec")
        return typing.cast(typing.Optional[CfnRoute.TcpRouteProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RouteSpecConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.RouteSpecOptionsBase",
    jsii_struct_bases=[],
    name_mapping={"priority": "priority"},
)
class RouteSpecOptionsBase:
    def __init__(self, *, priority: typing.Optional[jsii.Number] = None) -> None:
        '''(experimental) Base options for all route specs.

        :param priority: (experimental) The priority for the route. Routes are matched based on the specified value, where 0 is the highest priority. Default: - no particular priority

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority for the route.

        Routes are matched based on the specified
        value, where 0 is the highest priority.

        :default: - no particular priority

        :stability: experimental
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RouteSpecOptionsBase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceDiscovery(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-appmesh.ServiceDiscovery",
):
    '''(experimental) Provides the Service Discovery method a VirtualNode uses.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_ServiceDiscoveryProxy"]:
        return _ServiceDiscoveryProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(ServiceDiscovery, self, [])

    @jsii.member(jsii_name="cloudMap") # type: ignore[misc]
    @builtins.classmethod
    def cloud_map(
        cls,
        *,
        service: aws_cdk.aws_servicediscovery.IService,
        instance_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> "ServiceDiscovery":
        '''(experimental) Returns Cloud Map based service discovery.

        :param service: (experimental) The AWS Cloud Map Service to use for service discovery.
        :param instance_attributes: (experimental) A string map that contains attributes with values that you can use to filter instances by any custom attribute that you specified when you registered the instance. Only instances that match all of the specified key/value pairs will be returned. Default: - no instance attributes

        :stability: experimental
        '''
        options = CloudMapServiceDiscoveryOptions(
            service=service, instance_attributes=instance_attributes
        )

        return typing.cast("ServiceDiscovery", jsii.sinvoke(cls, "cloudMap", [options]))

    @jsii.member(jsii_name="dns") # type: ignore[misc]
    @builtins.classmethod
    def dns(cls, hostname: builtins.str) -> "ServiceDiscovery":
        '''(experimental) Returns DNS based service discovery.

        :param hostname: -

        :stability: experimental
        '''
        return typing.cast("ServiceDiscovery", jsii.sinvoke(cls, "dns", [hostname]))

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, scope: aws_cdk.core.Construct) -> "ServiceDiscoveryConfig":
        '''(experimental) Binds the current object when adding Service Discovery to a VirtualNode.

        :param scope: -

        :stability: experimental
        '''
        ...


class _ServiceDiscoveryProxy(ServiceDiscovery):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> "ServiceDiscoveryConfig":
        '''(experimental) Binds the current object when adding Service Discovery to a VirtualNode.

        :param scope: -

        :stability: experimental
        '''
        return typing.cast("ServiceDiscoveryConfig", jsii.invoke(self, "bind", [scope]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.ServiceDiscoveryConfig",
    jsii_struct_bases=[],
    name_mapping={"cloudmap": "cloudmap", "dns": "dns"},
)
class ServiceDiscoveryConfig:
    def __init__(
        self,
        *,
        cloudmap: typing.Optional[CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty] = None,
        dns: typing.Optional[CfnVirtualNode.DnsServiceDiscoveryProperty] = None,
    ) -> None:
        '''(experimental) Properties for VirtualNode Service Discovery.

        :param cloudmap: (experimental) Cloud Map based Service Discovery. Default: - no Cloud Map based service discovery
        :param dns: (experimental) DNS based Service Discovery. Default: - no DNS based service discovery

        :stability: experimental
        '''
        if isinstance(cloudmap, dict):
            cloudmap = CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty(**cloudmap)
        if isinstance(dns, dict):
            dns = CfnVirtualNode.DnsServiceDiscoveryProperty(**dns)
        self._values: typing.Dict[str, typing.Any] = {}
        if cloudmap is not None:
            self._values["cloudmap"] = cloudmap
        if dns is not None:
            self._values["dns"] = dns

    @builtins.property
    def cloudmap(
        self,
    ) -> typing.Optional[CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty]:
        '''(experimental) Cloud Map based Service Discovery.

        :default: - no Cloud Map based service discovery

        :stability: experimental
        '''
        result = self._values.get("cloudmap")
        return typing.cast(typing.Optional[CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty], result)

    @builtins.property
    def dns(self) -> typing.Optional[CfnVirtualNode.DnsServiceDiscoveryProperty]:
        '''(experimental) DNS based Service Discovery.

        :default: - no DNS based service discovery

        :stability: experimental
        '''
        result = self._values.get("dns")
        return typing.cast(typing.Optional[CfnVirtualNode.DnsServiceDiscoveryProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceDiscoveryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-appmesh.TcpRetryEvent")
class TcpRetryEvent(enum.Enum):
    '''(experimental) TCP events on which you may retry.

    :stability: experimental
    '''

    CONNECTION_ERROR = "CONNECTION_ERROR"
    '''(experimental) A connection error.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.TcpRouteSpecOptions",
    jsii_struct_bases=[RouteSpecOptionsBase],
    name_mapping={
        "priority": "priority",
        "weighted_targets": "weightedTargets",
        "timeout": "timeout",
    },
)
class TcpRouteSpecOptions(RouteSpecOptionsBase):
    def __init__(
        self,
        *,
        priority: typing.Optional[jsii.Number] = None,
        weighted_targets: typing.List["WeightedTarget"],
        timeout: typing.Optional["TcpTimeout"] = None,
    ) -> None:
        '''(experimental) Properties specific for a TCP Based Routes.

        :param priority: (experimental) The priority for the route. Routes are matched based on the specified value, where 0 is the highest priority. Default: - no particular priority
        :param weighted_targets: (experimental) List of targets that traffic is routed to when a request matches the route.
        :param timeout: (experimental) An object that represents a tcp timeout. Default: - None

        :stability: experimental
        '''
        if isinstance(timeout, dict):
            timeout = TcpTimeout(**timeout)
        self._values: typing.Dict[str, typing.Any] = {
            "weighted_targets": weighted_targets,
        }
        if priority is not None:
            self._values["priority"] = priority
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority for the route.

        Routes are matched based on the specified
        value, where 0 is the highest priority.

        :default: - no particular priority

        :stability: experimental
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weighted_targets(self) -> typing.List["WeightedTarget"]:
        '''(experimental) List of targets that traffic is routed to when a request matches the route.

        :stability: experimental
        '''
        result = self._values.get("weighted_targets")
        assert result is not None, "Required property 'weighted_targets' is missing"
        return typing.cast(typing.List["WeightedTarget"], result)

    @builtins.property
    def timeout(self) -> typing.Optional["TcpTimeout"]:
        '''(experimental) An object that represents a tcp timeout.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["TcpTimeout"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TcpRouteSpecOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.TcpTimeout",
    jsii_struct_bases=[],
    name_mapping={"idle": "idle"},
)
class TcpTimeout:
    def __init__(self, *, idle: typing.Optional[aws_cdk.core.Duration] = None) -> None:
        '''(experimental) Represents timeouts for TCP protocols.

        :param idle: (experimental) Represents an idle timeout. The amount of time that a connection may be idle. Default: - none

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if idle is not None:
            self._values["idle"] = idle

    @builtins.property
    def idle(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''(experimental) Represents an idle timeout.

        The amount of time that a connection may be idle.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("idle")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TcpTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.TcpVirtualNodeListenerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "health_check": "healthCheck",
        "port": "port",
        "timeout": "timeout",
        "tls_certificate": "tlsCertificate",
    },
)
class TcpVirtualNodeListenerOptions:
    def __init__(
        self,
        *,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[TcpTimeout] = None,
        tls_certificate: typing.Optional["TlsCertificate"] = None,
    ) -> None:
        '''(experimental) Represent the TCP Node Listener prorperty.

        :param health_check: (experimental) The health check information for the listener. Default: - no healthcheck
        :param port: (experimental) Port to listen for connections on. Default: - 8080
        :param timeout: (experimental) Timeout for TCP protocol. Default: - None
        :param tls_certificate: (experimental) Represents the configuration for enabling TLS on a listener. Default: - none

        :stability: experimental
        '''
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        if isinstance(timeout, dict):
            timeout = TcpTimeout(**timeout)
        self._values: typing.Dict[str, typing.Any] = {}
        if health_check is not None:
            self._values["health_check"] = health_check
        if port is not None:
            self._values["port"] = port
        if timeout is not None:
            self._values["timeout"] = timeout
        if tls_certificate is not None:
            self._values["tls_certificate"] = tls_certificate

    @builtins.property
    def health_check(self) -> typing.Optional[HealthCheck]:
        '''(experimental) The health check information for the listener.

        :default: - no healthcheck

        :stability: experimental
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[HealthCheck], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Port to listen for connections on.

        :default: - 8080

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[TcpTimeout]:
        '''(experimental) Timeout for TCP protocol.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[TcpTimeout], result)

    @builtins.property
    def tls_certificate(self) -> typing.Optional["TlsCertificate"]:
        '''(experimental) Represents the configuration for enabling TLS on a listener.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("tls_certificate")
        return typing.cast(typing.Optional["TlsCertificate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TcpVirtualNodeListenerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TlsCertificate(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-appmesh.TlsCertificate",
):
    '''(experimental) Represents a TLS certificate.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_TlsCertificateProxy"]:
        return _TlsCertificateProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(TlsCertificate, self, [])

    @jsii.member(jsii_name="acm") # type: ignore[misc]
    @builtins.classmethod
    def acm(
        cls,
        *,
        certificate: aws_cdk.aws_certificatemanager.ICertificate,
        tls_mode: "TlsMode",
    ) -> "TlsCertificate":
        '''(experimental) Returns an ACM TLS Certificate.

        :param certificate: (experimental) The ACM certificate.
        :param tls_mode: (experimental) The TLS mode.

        :stability: experimental
        '''
        props = AcmCertificateOptions(certificate=certificate, tls_mode=tls_mode)

        return typing.cast("TlsCertificate", jsii.sinvoke(cls, "acm", [props]))

    @jsii.member(jsii_name="file") # type: ignore[misc]
    @builtins.classmethod
    def file(
        cls,
        *,
        certificate_chain_path: builtins.str,
        private_key_path: builtins.str,
        tls_mode: "TlsMode",
    ) -> "TlsCertificate":
        '''(experimental) Returns an File TLS Certificate.

        :param certificate_chain_path: (experimental) The file path of the certificate chain file.
        :param private_key_path: (experimental) The file path of the private key file.
        :param tls_mode: (experimental) The TLS mode.

        :stability: experimental
        '''
        props = FileCertificateOptions(
            certificate_chain_path=certificate_chain_path,
            private_key_path=private_key_path,
            tls_mode=tls_mode,
        )

        return typing.cast("TlsCertificate", jsii.sinvoke(cls, "file", [props]))

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, _scope: aws_cdk.core.Construct) -> "TlsCertificateConfig":
        '''(experimental) Returns TLS certificate based provider.

        :param _scope: -

        :stability: experimental
        '''
        ...


class _TlsCertificateProxy(TlsCertificate):
    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct) -> "TlsCertificateConfig":
        '''(experimental) Returns TLS certificate based provider.

        :param _scope: -

        :stability: experimental
        '''
        return typing.cast("TlsCertificateConfig", jsii.invoke(self, "bind", [_scope]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.TlsCertificateConfig",
    jsii_struct_bases=[],
    name_mapping={"tls_certificate": "tlsCertificate", "tls_mode": "tlsMode"},
)
class TlsCertificateConfig:
    def __init__(
        self,
        *,
        tls_certificate: CfnVirtualNode.ListenerTlsCertificateProperty,
        tls_mode: "TlsMode",
    ) -> None:
        '''(experimental) A wrapper for the tls config returned by {@link TlsCertificate.bind}.

        :param tls_certificate: (experimental) The CFN shape for a listener TLS certificate.
        :param tls_mode: (experimental) The TLS mode.

        :stability: experimental
        '''
        if isinstance(tls_certificate, dict):
            tls_certificate = CfnVirtualNode.ListenerTlsCertificateProperty(**tls_certificate)
        self._values: typing.Dict[str, typing.Any] = {
            "tls_certificate": tls_certificate,
            "tls_mode": tls_mode,
        }

    @builtins.property
    def tls_certificate(self) -> CfnVirtualNode.ListenerTlsCertificateProperty:
        '''(experimental) The CFN shape for a listener TLS certificate.

        :stability: experimental
        '''
        result = self._values.get("tls_certificate")
        assert result is not None, "Required property 'tls_certificate' is missing"
        return typing.cast(CfnVirtualNode.ListenerTlsCertificateProperty, result)

    @builtins.property
    def tls_mode(self) -> "TlsMode":
        '''(experimental) The TLS mode.

        :stability: experimental
        '''
        result = self._values.get("tls_mode")
        assert result is not None, "Required property 'tls_mode' is missing"
        return typing.cast("TlsMode", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TlsCertificateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-appmesh.TlsMode")
class TlsMode(enum.Enum):
    '''(experimental) Enum of supported TLS modes.

    :stability: experimental
    '''

    STRICT = "STRICT"
    '''(experimental) Only accept encrypted traffic.

    :stability: experimental
    '''
    PERMISSIVE = "PERMISSIVE"
    '''(experimental) Accept encrypted and plaintext traffic.

    :stability: experimental
    '''
    DISABLED = "DISABLED"
    '''(experimental) TLS is disabled, only accept plaintext traffic.

    :stability: experimental
    '''


@jsii.implements(IVirtualGateway)
class VirtualGateway(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appmesh.VirtualGateway",
):
    '''(experimental) VirtualGateway represents a newly defined App Mesh Virtual Gateway.

    A virtual gateway allows resources that are outside of your mesh to communicate to resources that
    are inside of your mesh.

    :see: https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_gateways.html
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        mesh: IMesh,
        access_log: typing.Optional[AccessLog] = None,
        backend_defaults: typing.Optional[BackendDefaults] = None,
        listeners: typing.Optional[typing.List["VirtualGatewayListener"]] = None,
        virtual_gateway_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param mesh: (experimental) The Mesh which the VirtualGateway belongs to.
        :param access_log: (experimental) Access Logging Configuration for the VirtualGateway. Default: - no access logging
        :param backend_defaults: (experimental) Default Configuration Virtual Node uses to communicate with Virtual Service. Default: - No Config
        :param listeners: (experimental) Listeners for the VirtualGateway. Only one is supported. Default: - Single HTTP listener on port 8080
        :param virtual_gateway_name: (experimental) Name of the VirtualGateway. Default: - A name is automatically determined

        :stability: experimental
        '''
        props = VirtualGatewayProps(
            mesh=mesh,
            access_log=access_log,
            backend_defaults=backend_defaults,
            listeners=listeners,
            virtual_gateway_name=virtual_gateway_name,
        )

        jsii.create(VirtualGateway, self, [scope, id, props])

    @jsii.member(jsii_name="fromVirtualGatewayArn") # type: ignore[misc]
    @builtins.classmethod
    def from_virtual_gateway_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        virtual_gateway_arn: builtins.str,
    ) -> IVirtualGateway:
        '''(experimental) Import an existing VirtualGateway given an ARN.

        :param scope: -
        :param id: -
        :param virtual_gateway_arn: -

        :stability: experimental
        '''
        return typing.cast(IVirtualGateway, jsii.sinvoke(cls, "fromVirtualGatewayArn", [scope, id, virtual_gateway_arn]))

    @jsii.member(jsii_name="fromVirtualGatewayAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_virtual_gateway_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        mesh: IMesh,
        virtual_gateway_name: builtins.str,
    ) -> IVirtualGateway:
        '''(experimental) Import an existing VirtualGateway given its attributes.

        :param scope: -
        :param id: -
        :param mesh: (experimental) The Mesh that the VirtualGateway belongs to.
        :param virtual_gateway_name: (experimental) The name of the VirtualGateway.

        :stability: experimental
        '''
        attrs = VirtualGatewayAttributes(
            mesh=mesh, virtual_gateway_name=virtual_gateway_name
        )

        return typing.cast(IVirtualGateway, jsii.sinvoke(cls, "fromVirtualGatewayAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addGatewayRoute")
    def add_gateway_route(
        self,
        id: builtins.str,
        *,
        route_spec: GatewayRouteSpec,
        gateway_route_name: typing.Optional[builtins.str] = None,
    ) -> "GatewayRoute":
        '''(experimental) Utility method to add a new GatewayRoute to the VirtualGateway.

        :param id: -
        :param route_spec: (experimental) What protocol the route uses.
        :param gateway_route_name: (experimental) The name of the GatewayRoute. Default: - an automatically generated name

        :stability: experimental
        '''
        props = GatewayRouteBaseProps(
            route_spec=route_spec, gateway_route_name=gateway_route_name
        )

        return typing.cast("GatewayRoute", jsii.invoke(self, "addGatewayRoute", [id, props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listeners")
    def _listeners(self) -> typing.List["VirtualGatewayListenerConfig"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List["VirtualGatewayListenerConfig"], jsii.get(self, "listeners"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh that the VirtualGateway belongs to.

        :stability: experimental
        '''
        return typing.cast(IMesh, jsii.get(self, "mesh"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualGatewayArn")
    def virtual_gateway_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the VirtualGateway.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualGatewayArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualGatewayName")
    def virtual_gateway_name(self) -> builtins.str:
        '''(experimental) The name of the VirtualGateway.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualGatewayName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualGatewayAttributes",
    jsii_struct_bases=[],
    name_mapping={"mesh": "mesh", "virtual_gateway_name": "virtualGatewayName"},
)
class VirtualGatewayAttributes:
    def __init__(self, *, mesh: IMesh, virtual_gateway_name: builtins.str) -> None:
        '''(experimental) Unterface with properties necessary to import a reusable VirtualGateway.

        :param mesh: (experimental) The Mesh that the VirtualGateway belongs to.
        :param virtual_gateway_name: (experimental) The name of the VirtualGateway.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "mesh": mesh,
            "virtual_gateway_name": virtual_gateway_name,
        }

    @builtins.property
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh that the VirtualGateway belongs to.

        :stability: experimental
        '''
        result = self._values.get("mesh")
        assert result is not None, "Required property 'mesh' is missing"
        return typing.cast(IMesh, result)

    @builtins.property
    def virtual_gateway_name(self) -> builtins.str:
        '''(experimental) The name of the VirtualGateway.

        :stability: experimental
        '''
        result = self._values.get("virtual_gateway_name")
        assert result is not None, "Required property 'virtual_gateway_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualGatewayAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualGatewayBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_log": "accessLog",
        "backend_defaults": "backendDefaults",
        "listeners": "listeners",
        "virtual_gateway_name": "virtualGatewayName",
    },
)
class VirtualGatewayBaseProps:
    def __init__(
        self,
        *,
        access_log: typing.Optional[AccessLog] = None,
        backend_defaults: typing.Optional[BackendDefaults] = None,
        listeners: typing.Optional[typing.List["VirtualGatewayListener"]] = None,
        virtual_gateway_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Basic configuration properties for a VirtualGateway.

        :param access_log: (experimental) Access Logging Configuration for the VirtualGateway. Default: - no access logging
        :param backend_defaults: (experimental) Default Configuration Virtual Node uses to communicate with Virtual Service. Default: - No Config
        :param listeners: (experimental) Listeners for the VirtualGateway. Only one is supported. Default: - Single HTTP listener on port 8080
        :param virtual_gateway_name: (experimental) Name of the VirtualGateway. Default: - A name is automatically determined

        :stability: experimental
        '''
        if isinstance(backend_defaults, dict):
            backend_defaults = BackendDefaults(**backend_defaults)
        self._values: typing.Dict[str, typing.Any] = {}
        if access_log is not None:
            self._values["access_log"] = access_log
        if backend_defaults is not None:
            self._values["backend_defaults"] = backend_defaults
        if listeners is not None:
            self._values["listeners"] = listeners
        if virtual_gateway_name is not None:
            self._values["virtual_gateway_name"] = virtual_gateway_name

    @builtins.property
    def access_log(self) -> typing.Optional[AccessLog]:
        '''(experimental) Access Logging Configuration for the VirtualGateway.

        :default: - no access logging

        :stability: experimental
        '''
        result = self._values.get("access_log")
        return typing.cast(typing.Optional[AccessLog], result)

    @builtins.property
    def backend_defaults(self) -> typing.Optional[BackendDefaults]:
        '''(experimental) Default Configuration Virtual Node uses to communicate with Virtual Service.

        :default: - No Config

        :stability: experimental
        '''
        result = self._values.get("backend_defaults")
        return typing.cast(typing.Optional[BackendDefaults], result)

    @builtins.property
    def listeners(self) -> typing.Optional[typing.List["VirtualGatewayListener"]]:
        '''(experimental) Listeners for the VirtualGateway.

        Only one is supported.

        :default: - Single HTTP listener on port 8080

        :stability: experimental
        '''
        result = self._values.get("listeners")
        return typing.cast(typing.Optional[typing.List["VirtualGatewayListener"]], result)

    @builtins.property
    def virtual_gateway_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the VirtualGateway.

        :default: - A name is automatically determined

        :stability: experimental
        '''
        result = self._values.get("virtual_gateway_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualGatewayBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualGatewayListener(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-appmesh.VirtualGatewayListener",
):
    '''(experimental) Represents the properties needed to define listeners for a VirtualGateway.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_VirtualGatewayListenerProxy"]:
        return _VirtualGatewayListenerProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(VirtualGatewayListener, self, [])

    @jsii.member(jsii_name="grpc") # type: ignore[misc]
    @builtins.classmethod
    def grpc(
        cls,
        *,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        tls_certificate: typing.Optional[TlsCertificate] = None,
    ) -> "VirtualGatewayListener":
        '''(experimental) Returns a GRPC Listener for a VirtualGateway.

        :param health_check: (experimental) The health check information for the listener. Default: - no healthcheck
        :param port: (experimental) Port to listen for connections on. Default: - 8080
        :param tls_certificate: (experimental) Represents the listener certificate. Default: - none

        :stability: experimental
        '''
        options = GrpcGatewayListenerOptions(
            health_check=health_check, port=port, tls_certificate=tls_certificate
        )

        return typing.cast("VirtualGatewayListener", jsii.sinvoke(cls, "grpc", [options]))

    @jsii.member(jsii_name="http") # type: ignore[misc]
    @builtins.classmethod
    def http(
        cls,
        *,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        tls_certificate: typing.Optional[TlsCertificate] = None,
    ) -> "VirtualGatewayListener":
        '''(experimental) Returns an HTTP Listener for a VirtualGateway.

        :param health_check: (experimental) The health check information for the listener. Default: - no healthcheck
        :param port: (experimental) Port to listen for connections on. Default: - 8080
        :param tls_certificate: (experimental) Represents the configuration for enabling TLS on a listener. Default: - none

        :stability: experimental
        '''
        options = HttpGatewayListenerOptions(
            health_check=health_check, port=port, tls_certificate=tls_certificate
        )

        return typing.cast("VirtualGatewayListener", jsii.sinvoke(cls, "http", [options]))

    @jsii.member(jsii_name="http2") # type: ignore[misc]
    @builtins.classmethod
    def http2(
        cls,
        *,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        tls_certificate: typing.Optional[TlsCertificate] = None,
    ) -> "VirtualGatewayListener":
        '''(experimental) Returns an HTTP2 Listener for a VirtualGateway.

        :param health_check: (experimental) The health check information for the listener. Default: - no healthcheck
        :param port: (experimental) Port to listen for connections on. Default: - 8080
        :param tls_certificate: (experimental) Represents the configuration for enabling TLS on a listener. Default: - none

        :stability: experimental
        '''
        options = HttpGatewayListenerOptions(
            health_check=health_check, port=port, tls_certificate=tls_certificate
        )

        return typing.cast("VirtualGatewayListener", jsii.sinvoke(cls, "http2", [options]))

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, scope: aws_cdk.core.Construct) -> "VirtualGatewayListenerConfig":
        '''(experimental) Called when the GatewayListener type is initialized.

        Can be used to enforce
        mutual exclusivity

        :param scope: -

        :stability: experimental
        '''
        ...


class _VirtualGatewayListenerProxy(VirtualGatewayListener):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> "VirtualGatewayListenerConfig":
        '''(experimental) Called when the GatewayListener type is initialized.

        Can be used to enforce
        mutual exclusivity

        :param scope: -

        :stability: experimental
        '''
        return typing.cast("VirtualGatewayListenerConfig", jsii.invoke(self, "bind", [scope]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualGatewayListenerConfig",
    jsii_struct_bases=[],
    name_mapping={"listener": "listener"},
)
class VirtualGatewayListenerConfig:
    def __init__(
        self,
        *,
        listener: CfnVirtualGateway.VirtualGatewayListenerProperty,
    ) -> None:
        '''(experimental) Properties for a VirtualGateway listener.

        :param listener: (experimental) Single listener config for a VirtualGateway.

        :stability: experimental
        '''
        if isinstance(listener, dict):
            listener = CfnVirtualGateway.VirtualGatewayListenerProperty(**listener)
        self._values: typing.Dict[str, typing.Any] = {
            "listener": listener,
        }

    @builtins.property
    def listener(self) -> CfnVirtualGateway.VirtualGatewayListenerProperty:
        '''(experimental) Single listener config for a VirtualGateway.

        :stability: experimental
        '''
        result = self._values.get("listener")
        assert result is not None, "Required property 'listener' is missing"
        return typing.cast(CfnVirtualGateway.VirtualGatewayListenerProperty, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualGatewayListenerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualGatewayProps",
    jsii_struct_bases=[VirtualGatewayBaseProps],
    name_mapping={
        "access_log": "accessLog",
        "backend_defaults": "backendDefaults",
        "listeners": "listeners",
        "virtual_gateway_name": "virtualGatewayName",
        "mesh": "mesh",
    },
)
class VirtualGatewayProps(VirtualGatewayBaseProps):
    def __init__(
        self,
        *,
        access_log: typing.Optional[AccessLog] = None,
        backend_defaults: typing.Optional[BackendDefaults] = None,
        listeners: typing.Optional[typing.List[VirtualGatewayListener]] = None,
        virtual_gateway_name: typing.Optional[builtins.str] = None,
        mesh: IMesh,
    ) -> None:
        '''(experimental) Properties used when creating a new VirtualGateway.

        :param access_log: (experimental) Access Logging Configuration for the VirtualGateway. Default: - no access logging
        :param backend_defaults: (experimental) Default Configuration Virtual Node uses to communicate with Virtual Service. Default: - No Config
        :param listeners: (experimental) Listeners for the VirtualGateway. Only one is supported. Default: - Single HTTP listener on port 8080
        :param virtual_gateway_name: (experimental) Name of the VirtualGateway. Default: - A name is automatically determined
        :param mesh: (experimental) The Mesh which the VirtualGateway belongs to.

        :stability: experimental
        '''
        if isinstance(backend_defaults, dict):
            backend_defaults = BackendDefaults(**backend_defaults)
        self._values: typing.Dict[str, typing.Any] = {
            "mesh": mesh,
        }
        if access_log is not None:
            self._values["access_log"] = access_log
        if backend_defaults is not None:
            self._values["backend_defaults"] = backend_defaults
        if listeners is not None:
            self._values["listeners"] = listeners
        if virtual_gateway_name is not None:
            self._values["virtual_gateway_name"] = virtual_gateway_name

    @builtins.property
    def access_log(self) -> typing.Optional[AccessLog]:
        '''(experimental) Access Logging Configuration for the VirtualGateway.

        :default: - no access logging

        :stability: experimental
        '''
        result = self._values.get("access_log")
        return typing.cast(typing.Optional[AccessLog], result)

    @builtins.property
    def backend_defaults(self) -> typing.Optional[BackendDefaults]:
        '''(experimental) Default Configuration Virtual Node uses to communicate with Virtual Service.

        :default: - No Config

        :stability: experimental
        '''
        result = self._values.get("backend_defaults")
        return typing.cast(typing.Optional[BackendDefaults], result)

    @builtins.property
    def listeners(self) -> typing.Optional[typing.List[VirtualGatewayListener]]:
        '''(experimental) Listeners for the VirtualGateway.

        Only one is supported.

        :default: - Single HTTP listener on port 8080

        :stability: experimental
        '''
        result = self._values.get("listeners")
        return typing.cast(typing.Optional[typing.List[VirtualGatewayListener]], result)

    @builtins.property
    def virtual_gateway_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the VirtualGateway.

        :default: - A name is automatically determined

        :stability: experimental
        '''
        result = self._values.get("virtual_gateway_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualGateway belongs to.

        :stability: experimental
        '''
        result = self._values.get("mesh")
        assert result is not None, "Required property 'mesh' is missing"
        return typing.cast(IMesh, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IVirtualNode)
class VirtualNode(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appmesh.VirtualNode",
):
    '''(experimental) VirtualNode represents a newly defined AppMesh VirtualNode.

    Any inbound traffic that your virtual node expects should be specified as a
    listener. Any outbound traffic that your virtual node expects to reach
    should be specified as a backend.

    :see: https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_nodes.html
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        mesh: IMesh,
        access_log: typing.Optional[AccessLog] = None,
        backend_defaults: typing.Optional[BackendDefaults] = None,
        backends: typing.Optional[typing.List[Backend]] = None,
        listeners: typing.Optional[typing.List["VirtualNodeListener"]] = None,
        service_discovery: typing.Optional[ServiceDiscovery] = None,
        virtual_node_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param mesh: (experimental) The Mesh which the VirtualNode belongs to.
        :param access_log: (experimental) Access Logging Configuration for the virtual node. Default: - No access logging
        :param backend_defaults: (experimental) Default Configuration Virtual Node uses to communicate with Virtual Service. Default: - No Config
        :param backends: (experimental) Virtual Services that this is node expected to send outbound traffic to. Default: - No backends
        :param listeners: (experimental) Initial listener for the virtual node. Default: - No listeners
        :param service_discovery: (experimental) Defines how upstream clients will discover this VirtualNode. Default: - No Service Discovery
        :param virtual_node_name: (experimental) The name of the VirtualNode. Default: - A name is automatically determined

        :stability: experimental
        '''
        props = VirtualNodeProps(
            mesh=mesh,
            access_log=access_log,
            backend_defaults=backend_defaults,
            backends=backends,
            listeners=listeners,
            service_discovery=service_discovery,
            virtual_node_name=virtual_node_name,
        )

        jsii.create(VirtualNode, self, [scope, id, props])

    @jsii.member(jsii_name="fromVirtualNodeArn") # type: ignore[misc]
    @builtins.classmethod
    def from_virtual_node_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        virtual_node_arn: builtins.str,
    ) -> IVirtualNode:
        '''(experimental) Import an existing VirtualNode given an ARN.

        :param scope: -
        :param id: -
        :param virtual_node_arn: -

        :stability: experimental
        '''
        return typing.cast(IVirtualNode, jsii.sinvoke(cls, "fromVirtualNodeArn", [scope, id, virtual_node_arn]))

    @jsii.member(jsii_name="fromVirtualNodeAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_virtual_node_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        mesh: IMesh,
        virtual_node_name: builtins.str,
    ) -> IVirtualNode:
        '''(experimental) Import an existing VirtualNode given its name.

        :param scope: -
        :param id: -
        :param mesh: (experimental) The Mesh that the VirtualNode belongs to.
        :param virtual_node_name: (experimental) The name of the VirtualNode.

        :stability: experimental
        '''
        attrs = VirtualNodeAttributes(mesh=mesh, virtual_node_name=virtual_node_name)

        return typing.cast(IVirtualNode, jsii.sinvoke(cls, "fromVirtualNodeAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addBackend")
    def add_backend(self, backend: Backend) -> None:
        '''(experimental) Add a Virtual Services that this node is expected to send outbound traffic to.

        :param backend: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addBackend", [backend]))

    @jsii.member(jsii_name="addListener")
    def add_listener(self, listener: "VirtualNodeListener") -> None:
        '''(experimental) Utility method to add an inbound listener for this VirtualNode.

        Note: At this time, Virtual Nodes support at most one listener. Adding
        more than one will result in a failure to deploy the CloudFormation stack.
        However, the App Mesh team has plans to add support for multiple listeners
        on Virtual Nodes and Virtual Routers.

        :param listener: -

        :see: https://github.com/aws/aws-app-mesh-roadmap/issues/120
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addListener", [listener]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualNode belongs to.

        :stability: experimental
        '''
        return typing.cast(IMesh, jsii.get(self, "mesh"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualNodeArn")
    def virtual_node_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name belonging to the VirtualNode.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualNodeArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualNodeName")
    def virtual_node_name(self) -> builtins.str:
        '''(experimental) The name of the VirtualNode.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualNodeName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualNodeAttributes",
    jsii_struct_bases=[],
    name_mapping={"mesh": "mesh", "virtual_node_name": "virtualNodeName"},
)
class VirtualNodeAttributes:
    def __init__(self, *, mesh: IMesh, virtual_node_name: builtins.str) -> None:
        '''(experimental) Interface with properties necessary to import a reusable VirtualNode.

        :param mesh: (experimental) The Mesh that the VirtualNode belongs to.
        :param virtual_node_name: (experimental) The name of the VirtualNode.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "mesh": mesh,
            "virtual_node_name": virtual_node_name,
        }

    @builtins.property
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh that the VirtualNode belongs to.

        :stability: experimental
        '''
        result = self._values.get("mesh")
        assert result is not None, "Required property 'mesh' is missing"
        return typing.cast(IMesh, result)

    @builtins.property
    def virtual_node_name(self) -> builtins.str:
        '''(experimental) The name of the VirtualNode.

        :stability: experimental
        '''
        result = self._values.get("virtual_node_name")
        assert result is not None, "Required property 'virtual_node_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNodeAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualNodeBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_log": "accessLog",
        "backend_defaults": "backendDefaults",
        "backends": "backends",
        "listeners": "listeners",
        "service_discovery": "serviceDiscovery",
        "virtual_node_name": "virtualNodeName",
    },
)
class VirtualNodeBaseProps:
    def __init__(
        self,
        *,
        access_log: typing.Optional[AccessLog] = None,
        backend_defaults: typing.Optional[BackendDefaults] = None,
        backends: typing.Optional[typing.List[Backend]] = None,
        listeners: typing.Optional[typing.List["VirtualNodeListener"]] = None,
        service_discovery: typing.Optional[ServiceDiscovery] = None,
        virtual_node_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Basic configuration properties for a VirtualNode.

        :param access_log: (experimental) Access Logging Configuration for the virtual node. Default: - No access logging
        :param backend_defaults: (experimental) Default Configuration Virtual Node uses to communicate with Virtual Service. Default: - No Config
        :param backends: (experimental) Virtual Services that this is node expected to send outbound traffic to. Default: - No backends
        :param listeners: (experimental) Initial listener for the virtual node. Default: - No listeners
        :param service_discovery: (experimental) Defines how upstream clients will discover this VirtualNode. Default: - No Service Discovery
        :param virtual_node_name: (experimental) The name of the VirtualNode. Default: - A name is automatically determined

        :stability: experimental
        '''
        if isinstance(backend_defaults, dict):
            backend_defaults = BackendDefaults(**backend_defaults)
        self._values: typing.Dict[str, typing.Any] = {}
        if access_log is not None:
            self._values["access_log"] = access_log
        if backend_defaults is not None:
            self._values["backend_defaults"] = backend_defaults
        if backends is not None:
            self._values["backends"] = backends
        if listeners is not None:
            self._values["listeners"] = listeners
        if service_discovery is not None:
            self._values["service_discovery"] = service_discovery
        if virtual_node_name is not None:
            self._values["virtual_node_name"] = virtual_node_name

    @builtins.property
    def access_log(self) -> typing.Optional[AccessLog]:
        '''(experimental) Access Logging Configuration for the virtual node.

        :default: - No access logging

        :stability: experimental
        '''
        result = self._values.get("access_log")
        return typing.cast(typing.Optional[AccessLog], result)

    @builtins.property
    def backend_defaults(self) -> typing.Optional[BackendDefaults]:
        '''(experimental) Default Configuration Virtual Node uses to communicate with Virtual Service.

        :default: - No Config

        :stability: experimental
        '''
        result = self._values.get("backend_defaults")
        return typing.cast(typing.Optional[BackendDefaults], result)

    @builtins.property
    def backends(self) -> typing.Optional[typing.List[Backend]]:
        '''(experimental) Virtual Services that this is node expected to send outbound traffic to.

        :default: - No backends

        :stability: experimental
        '''
        result = self._values.get("backends")
        return typing.cast(typing.Optional[typing.List[Backend]], result)

    @builtins.property
    def listeners(self) -> typing.Optional[typing.List["VirtualNodeListener"]]:
        '''(experimental) Initial listener for the virtual node.

        :default: - No listeners

        :stability: experimental
        '''
        result = self._values.get("listeners")
        return typing.cast(typing.Optional[typing.List["VirtualNodeListener"]], result)

    @builtins.property
    def service_discovery(self) -> typing.Optional[ServiceDiscovery]:
        '''(experimental) Defines how upstream clients will discover this VirtualNode.

        :default: - No Service Discovery

        :stability: experimental
        '''
        result = self._values.get("service_discovery")
        return typing.cast(typing.Optional[ServiceDiscovery], result)

    @builtins.property
    def virtual_node_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the VirtualNode.

        :default: - A name is automatically determined

        :stability: experimental
        '''
        result = self._values.get("virtual_node_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNodeBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualNodeListener(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-appmesh.VirtualNodeListener",
):
    '''(experimental) Defines listener for a VirtualNode.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_VirtualNodeListenerProxy"]:
        return _VirtualNodeListenerProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(VirtualNodeListener, self, [])

    @jsii.member(jsii_name="grpc") # type: ignore[misc]
    @builtins.classmethod
    def grpc(
        cls,
        *,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[GrpcTimeout] = None,
        tls_certificate: typing.Optional[TlsCertificate] = None,
    ) -> "VirtualNodeListener":
        '''(experimental) Returns an GRPC Listener for a VirtualNode.

        :param health_check: (experimental) The health check information for the listener. Default: - no healthcheck
        :param port: (experimental) Port to listen for connections on. Default: - 8080
        :param timeout: (experimental) Timeout for GRPC protocol. Default: - None
        :param tls_certificate: (experimental) Represents the configuration for enabling TLS on a listener. Default: - none

        :stability: experimental
        '''
        props = GrpcVirtualNodeListenerOptions(
            health_check=health_check,
            port=port,
            timeout=timeout,
            tls_certificate=tls_certificate,
        )

        return typing.cast("VirtualNodeListener", jsii.sinvoke(cls, "grpc", [props]))

    @jsii.member(jsii_name="http") # type: ignore[misc]
    @builtins.classmethod
    def http(
        cls,
        *,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[HttpTimeout] = None,
        tls_certificate: typing.Optional[TlsCertificate] = None,
    ) -> "VirtualNodeListener":
        '''(experimental) Returns an HTTP Listener for a VirtualNode.

        :param health_check: (experimental) The health check information for the listener. Default: - no healthcheck
        :param port: (experimental) Port to listen for connections on. Default: - 8080
        :param timeout: (experimental) Timeout for HTTP protocol. Default: - None
        :param tls_certificate: (experimental) Represents the configuration for enabling TLS on a listener. Default: - none

        :stability: experimental
        '''
        props = HttpVirtualNodeListenerOptions(
            health_check=health_check,
            port=port,
            timeout=timeout,
            tls_certificate=tls_certificate,
        )

        return typing.cast("VirtualNodeListener", jsii.sinvoke(cls, "http", [props]))

    @jsii.member(jsii_name="http2") # type: ignore[misc]
    @builtins.classmethod
    def http2(
        cls,
        *,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[HttpTimeout] = None,
        tls_certificate: typing.Optional[TlsCertificate] = None,
    ) -> "VirtualNodeListener":
        '''(experimental) Returns an HTTP2 Listener for a VirtualNode.

        :param health_check: (experimental) The health check information for the listener. Default: - no healthcheck
        :param port: (experimental) Port to listen for connections on. Default: - 8080
        :param timeout: (experimental) Timeout for HTTP protocol. Default: - None
        :param tls_certificate: (experimental) Represents the configuration for enabling TLS on a listener. Default: - none

        :stability: experimental
        '''
        props = HttpVirtualNodeListenerOptions(
            health_check=health_check,
            port=port,
            timeout=timeout,
            tls_certificate=tls_certificate,
        )

        return typing.cast("VirtualNodeListener", jsii.sinvoke(cls, "http2", [props]))

    @jsii.member(jsii_name="tcp") # type: ignore[misc]
    @builtins.classmethod
    def tcp(
        cls,
        *,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[TcpTimeout] = None,
        tls_certificate: typing.Optional[TlsCertificate] = None,
    ) -> "VirtualNodeListener":
        '''(experimental) Returns an TCP Listener for a VirtualNode.

        :param health_check: (experimental) The health check information for the listener. Default: - no healthcheck
        :param port: (experimental) Port to listen for connections on. Default: - 8080
        :param timeout: (experimental) Timeout for TCP protocol. Default: - None
        :param tls_certificate: (experimental) Represents the configuration for enabling TLS on a listener. Default: - none

        :stability: experimental
        '''
        props = TcpVirtualNodeListenerOptions(
            health_check=health_check,
            port=port,
            timeout=timeout,
            tls_certificate=tls_certificate,
        )

        return typing.cast("VirtualNodeListener", jsii.sinvoke(cls, "tcp", [props]))

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, scope: aws_cdk.core.Construct) -> "VirtualNodeListenerConfig":
        '''(experimental) Binds the current object when adding Listener to a VirtualNode.

        :param scope: -

        :stability: experimental
        '''
        ...


class _VirtualNodeListenerProxy(VirtualNodeListener):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> "VirtualNodeListenerConfig":
        '''(experimental) Binds the current object when adding Listener to a VirtualNode.

        :param scope: -

        :stability: experimental
        '''
        return typing.cast("VirtualNodeListenerConfig", jsii.invoke(self, "bind", [scope]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualNodeListenerConfig",
    jsii_struct_bases=[],
    name_mapping={"listener": "listener"},
)
class VirtualNodeListenerConfig:
    def __init__(self, *, listener: CfnVirtualNode.ListenerProperty) -> None:
        '''(experimental) Properties for a VirtualNode listener.

        :param listener: (experimental) Single listener config for a VirtualNode.

        :stability: experimental
        '''
        if isinstance(listener, dict):
            listener = CfnVirtualNode.ListenerProperty(**listener)
        self._values: typing.Dict[str, typing.Any] = {
            "listener": listener,
        }

    @builtins.property
    def listener(self) -> CfnVirtualNode.ListenerProperty:
        '''(experimental) Single listener config for a VirtualNode.

        :stability: experimental
        '''
        result = self._values.get("listener")
        assert result is not None, "Required property 'listener' is missing"
        return typing.cast(CfnVirtualNode.ListenerProperty, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNodeListenerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualNodeProps",
    jsii_struct_bases=[VirtualNodeBaseProps],
    name_mapping={
        "access_log": "accessLog",
        "backend_defaults": "backendDefaults",
        "backends": "backends",
        "listeners": "listeners",
        "service_discovery": "serviceDiscovery",
        "virtual_node_name": "virtualNodeName",
        "mesh": "mesh",
    },
)
class VirtualNodeProps(VirtualNodeBaseProps):
    def __init__(
        self,
        *,
        access_log: typing.Optional[AccessLog] = None,
        backend_defaults: typing.Optional[BackendDefaults] = None,
        backends: typing.Optional[typing.List[Backend]] = None,
        listeners: typing.Optional[typing.List[VirtualNodeListener]] = None,
        service_discovery: typing.Optional[ServiceDiscovery] = None,
        virtual_node_name: typing.Optional[builtins.str] = None,
        mesh: IMesh,
    ) -> None:
        '''(experimental) The properties used when creating a new VirtualNode.

        :param access_log: (experimental) Access Logging Configuration for the virtual node. Default: - No access logging
        :param backend_defaults: (experimental) Default Configuration Virtual Node uses to communicate with Virtual Service. Default: - No Config
        :param backends: (experimental) Virtual Services that this is node expected to send outbound traffic to. Default: - No backends
        :param listeners: (experimental) Initial listener for the virtual node. Default: - No listeners
        :param service_discovery: (experimental) Defines how upstream clients will discover this VirtualNode. Default: - No Service Discovery
        :param virtual_node_name: (experimental) The name of the VirtualNode. Default: - A name is automatically determined
        :param mesh: (experimental) The Mesh which the VirtualNode belongs to.

        :stability: experimental
        '''
        if isinstance(backend_defaults, dict):
            backend_defaults = BackendDefaults(**backend_defaults)
        self._values: typing.Dict[str, typing.Any] = {
            "mesh": mesh,
        }
        if access_log is not None:
            self._values["access_log"] = access_log
        if backend_defaults is not None:
            self._values["backend_defaults"] = backend_defaults
        if backends is not None:
            self._values["backends"] = backends
        if listeners is not None:
            self._values["listeners"] = listeners
        if service_discovery is not None:
            self._values["service_discovery"] = service_discovery
        if virtual_node_name is not None:
            self._values["virtual_node_name"] = virtual_node_name

    @builtins.property
    def access_log(self) -> typing.Optional[AccessLog]:
        '''(experimental) Access Logging Configuration for the virtual node.

        :default: - No access logging

        :stability: experimental
        '''
        result = self._values.get("access_log")
        return typing.cast(typing.Optional[AccessLog], result)

    @builtins.property
    def backend_defaults(self) -> typing.Optional[BackendDefaults]:
        '''(experimental) Default Configuration Virtual Node uses to communicate with Virtual Service.

        :default: - No Config

        :stability: experimental
        '''
        result = self._values.get("backend_defaults")
        return typing.cast(typing.Optional[BackendDefaults], result)

    @builtins.property
    def backends(self) -> typing.Optional[typing.List[Backend]]:
        '''(experimental) Virtual Services that this is node expected to send outbound traffic to.

        :default: - No backends

        :stability: experimental
        '''
        result = self._values.get("backends")
        return typing.cast(typing.Optional[typing.List[Backend]], result)

    @builtins.property
    def listeners(self) -> typing.Optional[typing.List[VirtualNodeListener]]:
        '''(experimental) Initial listener for the virtual node.

        :default: - No listeners

        :stability: experimental
        '''
        result = self._values.get("listeners")
        return typing.cast(typing.Optional[typing.List[VirtualNodeListener]], result)

    @builtins.property
    def service_discovery(self) -> typing.Optional[ServiceDiscovery]:
        '''(experimental) Defines how upstream clients will discover this VirtualNode.

        :default: - No Service Discovery

        :stability: experimental
        '''
        result = self._values.get("service_discovery")
        return typing.cast(typing.Optional[ServiceDiscovery], result)

    @builtins.property
    def virtual_node_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the VirtualNode.

        :default: - A name is automatically determined

        :stability: experimental
        '''
        result = self._values.get("virtual_node_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualNode belongs to.

        :stability: experimental
        '''
        result = self._values.get("mesh")
        assert result is not None, "Required property 'mesh' is missing"
        return typing.cast(IMesh, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNodeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IVirtualRouter)
class VirtualRouter(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appmesh.VirtualRouter",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        mesh: IMesh,
        listeners: typing.Optional[typing.List["VirtualRouterListener"]] = None,
        virtual_router_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param mesh: (experimental) The Mesh which the VirtualRouter belongs to.
        :param listeners: (experimental) Listener specification for the VirtualRouter. Default: - A listener on HTTP port 8080
        :param virtual_router_name: (experimental) The name of the VirtualRouter. Default: - A name is automatically determined

        :stability: experimental
        '''
        props = VirtualRouterProps(
            mesh=mesh, listeners=listeners, virtual_router_name=virtual_router_name
        )

        jsii.create(VirtualRouter, self, [scope, id, props])

    @jsii.member(jsii_name="fromVirtualRouterArn") # type: ignore[misc]
    @builtins.classmethod
    def from_virtual_router_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        virtual_router_arn: builtins.str,
    ) -> IVirtualRouter:
        '''(experimental) Import an existing VirtualRouter given an ARN.

        :param scope: -
        :param id: -
        :param virtual_router_arn: -

        :stability: experimental
        '''
        return typing.cast(IVirtualRouter, jsii.sinvoke(cls, "fromVirtualRouterArn", [scope, id, virtual_router_arn]))

    @jsii.member(jsii_name="fromVirtualRouterAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_virtual_router_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        mesh: IMesh,
        virtual_router_name: builtins.str,
    ) -> IVirtualRouter:
        '''(experimental) Import an existing VirtualRouter given attributes.

        :param scope: -
        :param id: -
        :param mesh: (experimental) The Mesh which the VirtualRouter belongs to.
        :param virtual_router_name: (experimental) The name of the VirtualRouter.

        :stability: experimental
        '''
        attrs = VirtualRouterAttributes(
            mesh=mesh, virtual_router_name=virtual_router_name
        )

        return typing.cast(IVirtualRouter, jsii.sinvoke(cls, "fromVirtualRouterAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addRoute")
    def add_route(
        self,
        id: builtins.str,
        *,
        route_spec: RouteSpec,
        route_name: typing.Optional[builtins.str] = None,
    ) -> Route:
        '''(experimental) Add a single route to the router.

        :param id: -
        :param route_spec: (experimental) Protocol specific spec.
        :param route_name: (experimental) The name of the route. Default: - An automatically generated name

        :stability: experimental
        '''
        props = RouteBaseProps(route_spec=route_spec, route_name=route_name)

        return typing.cast(Route, jsii.invoke(self, "addRoute", [id, props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualRouter belongs to.

        :stability: experimental
        '''
        return typing.cast(IMesh, jsii.get(self, "mesh"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualRouterArn")
    def virtual_router_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the VirtualRouter.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualRouterArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualRouterName")
    def virtual_router_name(self) -> builtins.str:
        '''(experimental) The name of the VirtualRouter.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualRouterName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualRouterAttributes",
    jsii_struct_bases=[],
    name_mapping={"mesh": "mesh", "virtual_router_name": "virtualRouterName"},
)
class VirtualRouterAttributes:
    def __init__(self, *, mesh: IMesh, virtual_router_name: builtins.str) -> None:
        '''(experimental) Interface with properties ncecessary to import a reusable VirtualRouter.

        :param mesh: (experimental) The Mesh which the VirtualRouter belongs to.
        :param virtual_router_name: (experimental) The name of the VirtualRouter.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "mesh": mesh,
            "virtual_router_name": virtual_router_name,
        }

    @builtins.property
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualRouter belongs to.

        :stability: experimental
        '''
        result = self._values.get("mesh")
        assert result is not None, "Required property 'mesh' is missing"
        return typing.cast(IMesh, result)

    @builtins.property
    def virtual_router_name(self) -> builtins.str:
        '''(experimental) The name of the VirtualRouter.

        :stability: experimental
        '''
        result = self._values.get("virtual_router_name")
        assert result is not None, "Required property 'virtual_router_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualRouterAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualRouterBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "listeners": "listeners",
        "virtual_router_name": "virtualRouterName",
    },
)
class VirtualRouterBaseProps:
    def __init__(
        self,
        *,
        listeners: typing.Optional[typing.List["VirtualRouterListener"]] = None,
        virtual_router_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Interface with base properties all routers willl inherit.

        :param listeners: (experimental) Listener specification for the VirtualRouter. Default: - A listener on HTTP port 8080
        :param virtual_router_name: (experimental) The name of the VirtualRouter. Default: - A name is automatically determined

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if listeners is not None:
            self._values["listeners"] = listeners
        if virtual_router_name is not None:
            self._values["virtual_router_name"] = virtual_router_name

    @builtins.property
    def listeners(self) -> typing.Optional[typing.List["VirtualRouterListener"]]:
        '''(experimental) Listener specification for the VirtualRouter.

        :default: - A listener on HTTP port 8080

        :stability: experimental
        '''
        result = self._values.get("listeners")
        return typing.cast(typing.Optional[typing.List["VirtualRouterListener"]], result)

    @builtins.property
    def virtual_router_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the VirtualRouter.

        :default: - A name is automatically determined

        :stability: experimental
        '''
        result = self._values.get("virtual_router_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualRouterBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualRouterListener(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-appmesh.VirtualRouterListener",
):
    '''(experimental) Represents the properties needed to define listeners for a VirtualRouter.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_VirtualRouterListenerProxy"]:
        return _VirtualRouterListenerProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(VirtualRouterListener, self, [])

    @jsii.member(jsii_name="grpc") # type: ignore[misc]
    @builtins.classmethod
    def grpc(cls, port: typing.Optional[jsii.Number] = None) -> "VirtualRouterListener":
        '''(experimental) Returns a GRPC Listener for a VirtualRouter.

        :param port: the optional port of the listener, 8080 by default.

        :stability: experimental
        '''
        return typing.cast("VirtualRouterListener", jsii.sinvoke(cls, "grpc", [port]))

    @jsii.member(jsii_name="http") # type: ignore[misc]
    @builtins.classmethod
    def http(cls, port: typing.Optional[jsii.Number] = None) -> "VirtualRouterListener":
        '''(experimental) Returns an HTTP Listener for a VirtualRouter.

        :param port: the optional port of the listener, 8080 by default.

        :stability: experimental
        '''
        return typing.cast("VirtualRouterListener", jsii.sinvoke(cls, "http", [port]))

    @jsii.member(jsii_name="http2") # type: ignore[misc]
    @builtins.classmethod
    def http2(
        cls,
        port: typing.Optional[jsii.Number] = None,
    ) -> "VirtualRouterListener":
        '''(experimental) Returns an HTTP2 Listener for a VirtualRouter.

        :param port: the optional port of the listener, 8080 by default.

        :stability: experimental
        '''
        return typing.cast("VirtualRouterListener", jsii.sinvoke(cls, "http2", [port]))

    @jsii.member(jsii_name="tcp") # type: ignore[misc]
    @builtins.classmethod
    def tcp(cls, port: typing.Optional[jsii.Number] = None) -> "VirtualRouterListener":
        '''(experimental) Returns a TCP Listener for a VirtualRouter.

        :param port: the optional port of the listener, 8080 by default.

        :stability: experimental
        '''
        return typing.cast("VirtualRouterListener", jsii.sinvoke(cls, "tcp", [port]))

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, scope: aws_cdk.core.Construct) -> "VirtualRouterListenerConfig":
        '''(experimental) Called when the VirtualRouterListener type is initialized.

        Can be used to enforce
        mutual exclusivity

        :param scope: -

        :stability: experimental
        '''
        ...


class _VirtualRouterListenerProxy(VirtualRouterListener):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> "VirtualRouterListenerConfig":
        '''(experimental) Called when the VirtualRouterListener type is initialized.

        Can be used to enforce
        mutual exclusivity

        :param scope: -

        :stability: experimental
        '''
        return typing.cast("VirtualRouterListenerConfig", jsii.invoke(self, "bind", [scope]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualRouterListenerConfig",
    jsii_struct_bases=[],
    name_mapping={"listener": "listener"},
)
class VirtualRouterListenerConfig:
    def __init__(
        self,
        *,
        listener: CfnVirtualRouter.VirtualRouterListenerProperty,
    ) -> None:
        '''(experimental) Properties for a VirtualRouter listener.

        :param listener: (experimental) Single listener config for a VirtualRouter.

        :stability: experimental
        '''
        if isinstance(listener, dict):
            listener = CfnVirtualRouter.VirtualRouterListenerProperty(**listener)
        self._values: typing.Dict[str, typing.Any] = {
            "listener": listener,
        }

    @builtins.property
    def listener(self) -> CfnVirtualRouter.VirtualRouterListenerProperty:
        '''(experimental) Single listener config for a VirtualRouter.

        :stability: experimental
        '''
        result = self._values.get("listener")
        assert result is not None, "Required property 'listener' is missing"
        return typing.cast(CfnVirtualRouter.VirtualRouterListenerProperty, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualRouterListenerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualRouterProps",
    jsii_struct_bases=[VirtualRouterBaseProps],
    name_mapping={
        "listeners": "listeners",
        "virtual_router_name": "virtualRouterName",
        "mesh": "mesh",
    },
)
class VirtualRouterProps(VirtualRouterBaseProps):
    def __init__(
        self,
        *,
        listeners: typing.Optional[typing.List[VirtualRouterListener]] = None,
        virtual_router_name: typing.Optional[builtins.str] = None,
        mesh: IMesh,
    ) -> None:
        '''(experimental) The properties used when creating a new VirtualRouter.

        :param listeners: (experimental) Listener specification for the VirtualRouter. Default: - A listener on HTTP port 8080
        :param virtual_router_name: (experimental) The name of the VirtualRouter. Default: - A name is automatically determined
        :param mesh: (experimental) The Mesh which the VirtualRouter belongs to.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "mesh": mesh,
        }
        if listeners is not None:
            self._values["listeners"] = listeners
        if virtual_router_name is not None:
            self._values["virtual_router_name"] = virtual_router_name

    @builtins.property
    def listeners(self) -> typing.Optional[typing.List[VirtualRouterListener]]:
        '''(experimental) Listener specification for the VirtualRouter.

        :default: - A listener on HTTP port 8080

        :stability: experimental
        '''
        result = self._values.get("listeners")
        return typing.cast(typing.Optional[typing.List[VirtualRouterListener]], result)

    @builtins.property
    def virtual_router_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the VirtualRouter.

        :default: - A name is automatically determined

        :stability: experimental
        '''
        result = self._values.get("virtual_router_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualRouter belongs to.

        :stability: experimental
        '''
        result = self._values.get("mesh")
        assert result is not None, "Required property 'mesh' is missing"
        return typing.cast(IMesh, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualRouterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IVirtualService)
class VirtualService(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appmesh.VirtualService",
):
    '''(experimental) VirtualService represents a service inside an AppMesh.

    It routes traffic either to a Virtual Node or to a Virtual Router.

    :see: https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_services.html
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        virtual_service_provider: "VirtualServiceProvider",
        virtual_service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param virtual_service_provider: (experimental) The VirtualNode or VirtualRouter which the VirtualService uses as its provider.
        :param virtual_service_name: (experimental) The name of the VirtualService. It is recommended this follows the fully-qualified domain name format, such as "my-service.default.svc.cluster.local". Default: - A name is automatically generated

        :stability: experimental
        '''
        props = VirtualServiceProps(
            virtual_service_provider=virtual_service_provider,
            virtual_service_name=virtual_service_name,
        )

        jsii.create(VirtualService, self, [scope, id, props])

    @jsii.member(jsii_name="fromVirtualServiceArn") # type: ignore[misc]
    @builtins.classmethod
    def from_virtual_service_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        virtual_service_arn: builtins.str,
    ) -> IVirtualService:
        '''(experimental) Import an existing VirtualService given an ARN.

        :param scope: -
        :param id: -
        :param virtual_service_arn: -

        :stability: experimental
        '''
        return typing.cast(IVirtualService, jsii.sinvoke(cls, "fromVirtualServiceArn", [scope, id, virtual_service_arn]))

    @jsii.member(jsii_name="fromVirtualServiceAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_virtual_service_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        mesh: IMesh,
        virtual_service_name: builtins.str,
    ) -> IVirtualService:
        '''(experimental) Import an existing VirtualService given its attributes.

        :param scope: -
        :param id: -
        :param mesh: (experimental) The Mesh which the VirtualService belongs to.
        :param virtual_service_name: (experimental) The name of the VirtualService, it is recommended this follows the fully-qualified domain name format.

        :stability: experimental
        '''
        attrs = VirtualServiceAttributes(
            mesh=mesh, virtual_service_name=virtual_service_name
        )

        return typing.cast(IVirtualService, jsii.sinvoke(cls, "fromVirtualServiceAttributes", [scope, id, attrs]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualService belongs to.

        :stability: experimental
        '''
        return typing.cast(IMesh, jsii.get(self, "mesh"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualServiceArn")
    def virtual_service_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the virtual service.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualServiceArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualServiceName")
    def virtual_service_name(self) -> builtins.str:
        '''(experimental) The name of the VirtualService, it is recommended this follows the fully-qualified domain name format.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "virtualServiceName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualServiceAttributes",
    jsii_struct_bases=[],
    name_mapping={"mesh": "mesh", "virtual_service_name": "virtualServiceName"},
)
class VirtualServiceAttributes:
    def __init__(self, *, mesh: IMesh, virtual_service_name: builtins.str) -> None:
        '''(experimental) Interface with properties ncecessary to import a reusable VirtualService.

        :param mesh: (experimental) The Mesh which the VirtualService belongs to.
        :param virtual_service_name: (experimental) The name of the VirtualService, it is recommended this follows the fully-qualified domain name format.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "mesh": mesh,
            "virtual_service_name": virtual_service_name,
        }

    @builtins.property
    def mesh(self) -> IMesh:
        '''(experimental) The Mesh which the VirtualService belongs to.

        :stability: experimental
        '''
        result = self._values.get("mesh")
        assert result is not None, "Required property 'mesh' is missing"
        return typing.cast(IMesh, result)

    @builtins.property
    def virtual_service_name(self) -> builtins.str:
        '''(experimental) The name of the VirtualService, it is recommended this follows the fully-qualified domain name format.

        :stability: experimental
        '''
        result = self._values.get("virtual_service_name")
        assert result is not None, "Required property 'virtual_service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualServiceAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualServiceBackendOptions",
    jsii_struct_bases=[],
    name_mapping={"client_policy": "clientPolicy"},
)
class VirtualServiceBackendOptions:
    def __init__(self, *, client_policy: typing.Optional[ClientPolicy] = None) -> None:
        '''(experimental) Represents the properties needed to define a Virtual Service backend.

        :param client_policy: (experimental) Client policy for the backend. Default: none

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if client_policy is not None:
            self._values["client_policy"] = client_policy

    @builtins.property
    def client_policy(self) -> typing.Optional[ClientPolicy]:
        '''(experimental) Client policy for the backend.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("client_policy")
        return typing.cast(typing.Optional[ClientPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualServiceBackendOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "virtual_service_provider": "virtualServiceProvider",
        "virtual_service_name": "virtualServiceName",
    },
)
class VirtualServiceProps:
    def __init__(
        self,
        *,
        virtual_service_provider: "VirtualServiceProvider",
        virtual_service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The properties applied to the VirtualService being defined.

        :param virtual_service_provider: (experimental) The VirtualNode or VirtualRouter which the VirtualService uses as its provider.
        :param virtual_service_name: (experimental) The name of the VirtualService. It is recommended this follows the fully-qualified domain name format, such as "my-service.default.svc.cluster.local". Default: - A name is automatically generated

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "virtual_service_provider": virtual_service_provider,
        }
        if virtual_service_name is not None:
            self._values["virtual_service_name"] = virtual_service_name

    @builtins.property
    def virtual_service_provider(self) -> "VirtualServiceProvider":
        '''(experimental) The VirtualNode or VirtualRouter which the VirtualService uses as its provider.

        :stability: experimental
        '''
        result = self._values.get("virtual_service_provider")
        assert result is not None, "Required property 'virtual_service_provider' is missing"
        return typing.cast("VirtualServiceProvider", result)

    @builtins.property
    def virtual_service_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the VirtualService.

        It is recommended this follows the fully-qualified domain name format,
        such as "my-service.default.svc.cluster.local".

        :default: - A name is automatically generated

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            service.domain.local
        '''
        result = self._values.get("virtual_service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualServiceProvider(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-appmesh.VirtualServiceProvider",
):
    '''(experimental) Represents the properties needed to define the provider for a VirtualService.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_VirtualServiceProviderProxy"]:
        return _VirtualServiceProviderProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(VirtualServiceProvider, self, [])

    @jsii.member(jsii_name="none") # type: ignore[misc]
    @builtins.classmethod
    def none(cls, mesh: IMesh) -> "VirtualServiceProvider":
        '''(experimental) Returns an Empty Provider for a VirtualService.

        This provides no routing capabilities
        and should only be used as a placeholder

        :param mesh: -

        :stability: experimental
        '''
        return typing.cast("VirtualServiceProvider", jsii.sinvoke(cls, "none", [mesh]))

    @jsii.member(jsii_name="virtualNode") # type: ignore[misc]
    @builtins.classmethod
    def virtual_node(cls, virtual_node: IVirtualNode) -> "VirtualServiceProvider":
        '''(experimental) Returns a VirtualNode based Provider for a VirtualService.

        :param virtual_node: -

        :stability: experimental
        '''
        return typing.cast("VirtualServiceProvider", jsii.sinvoke(cls, "virtualNode", [virtual_node]))

    @jsii.member(jsii_name="virtualRouter") # type: ignore[misc]
    @builtins.classmethod
    def virtual_router(cls, virtual_router: IVirtualRouter) -> "VirtualServiceProvider":
        '''(experimental) Returns a VirtualRouter based Provider for a VirtualService.

        :param virtual_router: -

        :stability: experimental
        '''
        return typing.cast("VirtualServiceProvider", jsii.sinvoke(cls, "virtualRouter", [virtual_router]))

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, _construct: constructs.Construct) -> "VirtualServiceProviderConfig":
        '''(experimental) Enforces mutual exclusivity for VirtualService provider types.

        :param _construct: -

        :stability: experimental
        '''
        ...


class _VirtualServiceProviderProxy(VirtualServiceProvider):
    @jsii.member(jsii_name="bind")
    def bind(self, _construct: constructs.Construct) -> "VirtualServiceProviderConfig":
        '''(experimental) Enforces mutual exclusivity for VirtualService provider types.

        :param _construct: -

        :stability: experimental
        '''
        return typing.cast("VirtualServiceProviderConfig", jsii.invoke(self, "bind", [_construct]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.VirtualServiceProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "mesh": "mesh",
        "virtual_node_provider": "virtualNodeProvider",
        "virtual_router_provider": "virtualRouterProvider",
    },
)
class VirtualServiceProviderConfig:
    def __init__(
        self,
        *,
        mesh: IMesh,
        virtual_node_provider: typing.Optional[CfnVirtualService.VirtualNodeServiceProviderProperty] = None,
        virtual_router_provider: typing.Optional[CfnVirtualService.VirtualRouterServiceProviderProperty] = None,
    ) -> None:
        '''(experimental) Properties for a VirtualService provider.

        :param mesh: (experimental) Mesh the Provider is using. Default: - none
        :param virtual_node_provider: (experimental) Virtual Node based provider. Default: - none
        :param virtual_router_provider: (experimental) Virtual Router based provider. Default: - none

        :stability: experimental
        '''
        if isinstance(virtual_node_provider, dict):
            virtual_node_provider = CfnVirtualService.VirtualNodeServiceProviderProperty(**virtual_node_provider)
        if isinstance(virtual_router_provider, dict):
            virtual_router_provider = CfnVirtualService.VirtualRouterServiceProviderProperty(**virtual_router_provider)
        self._values: typing.Dict[str, typing.Any] = {
            "mesh": mesh,
        }
        if virtual_node_provider is not None:
            self._values["virtual_node_provider"] = virtual_node_provider
        if virtual_router_provider is not None:
            self._values["virtual_router_provider"] = virtual_router_provider

    @builtins.property
    def mesh(self) -> IMesh:
        '''(experimental) Mesh the Provider is using.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("mesh")
        assert result is not None, "Required property 'mesh' is missing"
        return typing.cast(IMesh, result)

    @builtins.property
    def virtual_node_provider(
        self,
    ) -> typing.Optional[CfnVirtualService.VirtualNodeServiceProviderProperty]:
        '''(experimental) Virtual Node based provider.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("virtual_node_provider")
        return typing.cast(typing.Optional[CfnVirtualService.VirtualNodeServiceProviderProperty], result)

    @builtins.property
    def virtual_router_provider(
        self,
    ) -> typing.Optional[CfnVirtualService.VirtualRouterServiceProviderProperty]:
        '''(experimental) Virtual Router based provider.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("virtual_router_provider")
        return typing.cast(typing.Optional[CfnVirtualService.VirtualRouterServiceProviderProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualServiceProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.WeightedTarget",
    jsii_struct_bases=[],
    name_mapping={"virtual_node": "virtualNode", "weight": "weight"},
)
class WeightedTarget:
    def __init__(
        self,
        *,
        virtual_node: IVirtualNode,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for the Weighted Targets in the route.

        :param virtual_node: (experimental) The VirtualNode the route points to.
        :param weight: (experimental) The weight for the target. Default: 1

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "virtual_node": virtual_node,
        }
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def virtual_node(self) -> IVirtualNode:
        '''(experimental) The VirtualNode the route points to.

        :stability: experimental
        '''
        result = self._values.get("virtual_node")
        assert result is not None, "Required property 'virtual_node' is missing"
        return typing.cast(IVirtualNode, result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The weight for the target.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WeightedTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.AcmTrustOptions",
    jsii_struct_bases=[ClientPolicyOptions],
    name_mapping={
        "ports": "ports",
        "certificate_authorities": "certificateAuthorities",
    },
)
class AcmTrustOptions(ClientPolicyOptions):
    def __init__(
        self,
        *,
        ports: typing.Optional[typing.List[jsii.Number]] = None,
        certificate_authorities: typing.List[aws_cdk.aws_acmpca.ICertificateAuthority],
    ) -> None:
        '''(experimental) ACM Trust Properties.

        :param ports: (experimental) TLS is enforced on the ports specified here. If no ports are specified, TLS will be enforced on all the ports. Default: - none
        :param certificate_authorities: (experimental) Contains information for your private certificate authority.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "certificate_authorities": certificate_authorities,
        }
        if ports is not None:
            self._values["ports"] = ports

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''(experimental) TLS is enforced on the ports specified here.

        If no ports are specified, TLS will be enforced on all the ports.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def certificate_authorities(
        self,
    ) -> typing.List[aws_cdk.aws_acmpca.ICertificateAuthority]:
        '''(experimental) Contains information for your private certificate authority.

        :stability: experimental
        '''
        result = self._values.get("certificate_authorities")
        assert result is not None, "Required property 'certificate_authorities' is missing"
        return typing.cast(typing.List[aws_cdk.aws_acmpca.ICertificateAuthority], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcmTrustOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IGatewayRoute)
class GatewayRoute(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appmesh.GatewayRoute",
):
    '''(experimental) GatewayRoute represents a new or existing gateway route attached to a VirtualGateway and Mesh.

    :see: https://docs.aws.amazon.com/app-mesh/latest/userguide/gateway-routes.html
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        virtual_gateway: IVirtualGateway,
        route_spec: GatewayRouteSpec,
        gateway_route_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param virtual_gateway: (experimental) The VirtualGateway this GatewayRoute is associated with.
        :param route_spec: (experimental) What protocol the route uses.
        :param gateway_route_name: (experimental) The name of the GatewayRoute. Default: - an automatically generated name

        :stability: experimental
        '''
        props = GatewayRouteProps(
            virtual_gateway=virtual_gateway,
            route_spec=route_spec,
            gateway_route_name=gateway_route_name,
        )

        jsii.create(GatewayRoute, self, [scope, id, props])

    @jsii.member(jsii_name="fromGatewayRouteArn") # type: ignore[misc]
    @builtins.classmethod
    def from_gateway_route_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        gateway_route_arn: builtins.str,
    ) -> IGatewayRoute:
        '''(experimental) Import an existing GatewayRoute given an ARN.

        :param scope: -
        :param id: -
        :param gateway_route_arn: -

        :stability: experimental
        '''
        return typing.cast(IGatewayRoute, jsii.sinvoke(cls, "fromGatewayRouteArn", [scope, id, gateway_route_arn]))

    @jsii.member(jsii_name="fromGatewayRouteAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_gateway_route_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        gateway_route_name: builtins.str,
        virtual_gateway: IVirtualGateway,
    ) -> IGatewayRoute:
        '''(experimental) Import an existing GatewayRoute given attributes.

        :param scope: -
        :param id: -
        :param gateway_route_name: (experimental) The name of the GatewayRoute.
        :param virtual_gateway: (experimental) The VirtualGateway this GatewayRoute is associated with.

        :stability: experimental
        '''
        attrs = GatewayRouteAttributes(
            gateway_route_name=gateway_route_name, virtual_gateway=virtual_gateway
        )

        return typing.cast(IGatewayRoute, jsii.sinvoke(cls, "fromGatewayRouteAttributes", [scope, id, attrs]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="gatewayRouteArn")
    def gateway_route_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) for the GatewayRoute.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "gatewayRouteArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="gatewayRouteName")
    def gateway_route_name(self) -> builtins.str:
        '''(experimental) The name of the GatewayRoute.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "gatewayRouteName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="virtualGateway")
    def virtual_gateway(self) -> IVirtualGateway:
        '''(experimental) The VirtualGateway this GatewayRoute is a part of.

        :stability: experimental
        '''
        return typing.cast(IVirtualGateway, jsii.get(self, "virtualGateway"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.GrpcRetryPolicy",
    jsii_struct_bases=[HttpRetryPolicy],
    name_mapping={
        "retry_attempts": "retryAttempts",
        "retry_timeout": "retryTimeout",
        "http_retry_events": "httpRetryEvents",
        "tcp_retry_events": "tcpRetryEvents",
        "grpc_retry_events": "grpcRetryEvents",
    },
)
class GrpcRetryPolicy(HttpRetryPolicy):
    def __init__(
        self,
        *,
        retry_attempts: jsii.Number,
        retry_timeout: aws_cdk.core.Duration,
        http_retry_events: typing.Optional[typing.List[HttpRetryEvent]] = None,
        tcp_retry_events: typing.Optional[typing.List[TcpRetryEvent]] = None,
        grpc_retry_events: typing.Optional[typing.List[GrpcRetryEvent]] = None,
    ) -> None:
        '''(experimental) gRPC retry policy.

        :param retry_attempts: (experimental) The maximum number of retry attempts.
        :param retry_timeout: (experimental) The timeout for each retry attempt.
        :param http_retry_events: (experimental) Specify HTTP events on which to retry. You must specify at least one value for at least one types of retry events. Default: - no retries for http events
        :param tcp_retry_events: (experimental) TCP events on which to retry. The event occurs before any processing of a request has started and is encountered when the upstream is temporarily or permanently unavailable. You must specify at least one value for at least one types of retry events. Default: - no retries for tcp events
        :param grpc_retry_events: (experimental) gRPC events on which to retry. You must specify at least one value for at least one types of retry events. Default: - no retries for gRPC events

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "retry_attempts": retry_attempts,
            "retry_timeout": retry_timeout,
        }
        if http_retry_events is not None:
            self._values["http_retry_events"] = http_retry_events
        if tcp_retry_events is not None:
            self._values["tcp_retry_events"] = tcp_retry_events
        if grpc_retry_events is not None:
            self._values["grpc_retry_events"] = grpc_retry_events

    @builtins.property
    def retry_attempts(self) -> jsii.Number:
        '''(experimental) The maximum number of retry attempts.

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        assert result is not None, "Required property 'retry_attempts' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def retry_timeout(self) -> aws_cdk.core.Duration:
        '''(experimental) The timeout for each retry attempt.

        :stability: experimental
        '''
        result = self._values.get("retry_timeout")
        assert result is not None, "Required property 'retry_timeout' is missing"
        return typing.cast(aws_cdk.core.Duration, result)

    @builtins.property
    def http_retry_events(self) -> typing.Optional[typing.List[HttpRetryEvent]]:
        '''(experimental) Specify HTTP events on which to retry.

        You must specify at least one value
        for at least one types of retry events.

        :default: - no retries for http events

        :stability: experimental
        '''
        result = self._values.get("http_retry_events")
        return typing.cast(typing.Optional[typing.List[HttpRetryEvent]], result)

    @builtins.property
    def tcp_retry_events(self) -> typing.Optional[typing.List[TcpRetryEvent]]:
        '''(experimental) TCP events on which to retry.

        The event occurs before any processing of a
        request has started and is encountered when the upstream is temporarily or
        permanently unavailable. You must specify at least one value for at least
        one types of retry events.

        :default: - no retries for tcp events

        :stability: experimental
        '''
        result = self._values.get("tcp_retry_events")
        return typing.cast(typing.Optional[typing.List[TcpRetryEvent]], result)

    @builtins.property
    def grpc_retry_events(self) -> typing.Optional[typing.List[GrpcRetryEvent]]:
        '''(experimental) gRPC events on which to retry.

        You must specify at least one value
        for at least one types of retry events.

        :default: - no retries for gRPC events

        :stability: experimental
        '''
        result = self._values.get("grpc_retry_events")
        return typing.cast(typing.Optional[typing.List[GrpcRetryEvent]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrpcRetryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.GrpcRouteSpecOptions",
    jsii_struct_bases=[RouteSpecOptionsBase],
    name_mapping={
        "priority": "priority",
        "match": "match",
        "weighted_targets": "weightedTargets",
        "retry_policy": "retryPolicy",
        "timeout": "timeout",
    },
)
class GrpcRouteSpecOptions(RouteSpecOptionsBase):
    def __init__(
        self,
        *,
        priority: typing.Optional[jsii.Number] = None,
        match: GrpcRouteMatch,
        weighted_targets: typing.List[WeightedTarget],
        retry_policy: typing.Optional[GrpcRetryPolicy] = None,
        timeout: typing.Optional[GrpcTimeout] = None,
    ) -> None:
        '''(experimental) Properties specific for a GRPC Based Routes.

        :param priority: (experimental) The priority for the route. Routes are matched based on the specified value, where 0 is the highest priority. Default: - no particular priority
        :param match: (experimental) The criterion for determining a request match for this Route.
        :param weighted_targets: (experimental) List of targets that traffic is routed to when a request matches the route.
        :param retry_policy: (experimental) The retry policy. Default: - no retry policy
        :param timeout: (experimental) An object that represents a grpc timeout. Default: - None

        :stability: experimental
        '''
        if isinstance(match, dict):
            match = GrpcRouteMatch(**match)
        if isinstance(retry_policy, dict):
            retry_policy = GrpcRetryPolicy(**retry_policy)
        if isinstance(timeout, dict):
            timeout = GrpcTimeout(**timeout)
        self._values: typing.Dict[str, typing.Any] = {
            "match": match,
            "weighted_targets": weighted_targets,
        }
        if priority is not None:
            self._values["priority"] = priority
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority for the route.

        Routes are matched based on the specified
        value, where 0 is the highest priority.

        :default: - no particular priority

        :stability: experimental
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def match(self) -> GrpcRouteMatch:
        '''(experimental) The criterion for determining a request match for this Route.

        :stability: experimental
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast(GrpcRouteMatch, result)

    @builtins.property
    def weighted_targets(self) -> typing.List[WeightedTarget]:
        '''(experimental) List of targets that traffic is routed to when a request matches the route.

        :stability: experimental
        '''
        result = self._values.get("weighted_targets")
        assert result is not None, "Required property 'weighted_targets' is missing"
        return typing.cast(typing.List[WeightedTarget], result)

    @builtins.property
    def retry_policy(self) -> typing.Optional[GrpcRetryPolicy]:
        '''(experimental) The retry policy.

        :default: - no retry policy

        :stability: experimental
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional[GrpcRetryPolicy], result)

    @builtins.property
    def timeout(self) -> typing.Optional[GrpcTimeout]:
        '''(experimental) An object that represents a grpc timeout.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[GrpcTimeout], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrpcRouteSpecOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appmesh.HttpRouteSpecOptions",
    jsii_struct_bases=[RouteSpecOptionsBase],
    name_mapping={
        "priority": "priority",
        "weighted_targets": "weightedTargets",
        "match": "match",
        "retry_policy": "retryPolicy",
        "timeout": "timeout",
    },
)
class HttpRouteSpecOptions(RouteSpecOptionsBase):
    def __init__(
        self,
        *,
        priority: typing.Optional[jsii.Number] = None,
        weighted_targets: typing.List[WeightedTarget],
        match: typing.Optional[HttpRouteMatch] = None,
        retry_policy: typing.Optional[HttpRetryPolicy] = None,
        timeout: typing.Optional[HttpTimeout] = None,
    ) -> None:
        '''(experimental) Properties specific for HTTP Based Routes.

        :param priority: (experimental) The priority for the route. Routes are matched based on the specified value, where 0 is the highest priority. Default: - no particular priority
        :param weighted_targets: (experimental) List of targets that traffic is routed to when a request matches the route.
        :param match: (experimental) The criterion for determining a request match for this Route. Default: - matches on '/'
        :param retry_policy: (experimental) The retry policy. Default: - no retry policy
        :param timeout: (experimental) An object that represents a http timeout. Default: - None

        :stability: experimental
        '''
        if isinstance(match, dict):
            match = HttpRouteMatch(**match)
        if isinstance(retry_policy, dict):
            retry_policy = HttpRetryPolicy(**retry_policy)
        if isinstance(timeout, dict):
            timeout = HttpTimeout(**timeout)
        self._values: typing.Dict[str, typing.Any] = {
            "weighted_targets": weighted_targets,
        }
        if priority is not None:
            self._values["priority"] = priority
        if match is not None:
            self._values["match"] = match
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority for the route.

        Routes are matched based on the specified
        value, where 0 is the highest priority.

        :default: - no particular priority

        :stability: experimental
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weighted_targets(self) -> typing.List[WeightedTarget]:
        '''(experimental) List of targets that traffic is routed to when a request matches the route.

        :stability: experimental
        '''
        result = self._values.get("weighted_targets")
        assert result is not None, "Required property 'weighted_targets' is missing"
        return typing.cast(typing.List[WeightedTarget], result)

    @builtins.property
    def match(self) -> typing.Optional[HttpRouteMatch]:
        '''(experimental) The criterion for determining a request match for this Route.

        :default: - matches on '/'

        :stability: experimental
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional[HttpRouteMatch], result)

    @builtins.property
    def retry_policy(self) -> typing.Optional[HttpRetryPolicy]:
        '''(experimental) The retry policy.

        :default: - no retry policy

        :stability: experimental
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional[HttpRetryPolicy], result)

    @builtins.property
    def timeout(self) -> typing.Optional[HttpTimeout]:
        '''(experimental) An object that represents a http timeout.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[HttpTimeout], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpRouteSpecOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AccessLog",
    "AccessLogConfig",
    "AcmCertificateOptions",
    "AcmTrustOptions",
    "Backend",
    "BackendConfig",
    "BackendDefaults",
    "CfnGatewayRoute",
    "CfnGatewayRouteProps",
    "CfnMesh",
    "CfnMeshProps",
    "CfnRoute",
    "CfnRouteProps",
    "CfnVirtualGateway",
    "CfnVirtualGatewayProps",
    "CfnVirtualNode",
    "CfnVirtualNodeProps",
    "CfnVirtualRouter",
    "CfnVirtualRouterProps",
    "CfnVirtualService",
    "CfnVirtualServiceProps",
    "ClientPolicy",
    "ClientPolicyConfig",
    "ClientPolicyOptions",
    "CloudMapServiceDiscoveryOptions",
    "FileCertificateOptions",
    "FileTrustOptions",
    "GatewayRoute",
    "GatewayRouteAttributes",
    "GatewayRouteBaseProps",
    "GatewayRouteProps",
    "GatewayRouteSpec",
    "GatewayRouteSpecConfig",
    "GrpcGatewayListenerOptions",
    "GrpcGatewayRouteMatch",
    "GrpcGatewayRouteSpecOptions",
    "GrpcRetryEvent",
    "GrpcRetryPolicy",
    "GrpcRouteMatch",
    "GrpcRouteSpecOptions",
    "GrpcTimeout",
    "GrpcVirtualNodeListenerOptions",
    "HealthCheck",
    "HttpGatewayListenerOptions",
    "HttpGatewayRouteMatch",
    "HttpGatewayRouteSpecOptions",
    "HttpHeaderMatch",
    "HttpHeaderMatchConfig",
    "HttpRetryEvent",
    "HttpRetryPolicy",
    "HttpRouteMatch",
    "HttpRouteMatchMethod",
    "HttpRouteProtocol",
    "HttpRouteSpecOptions",
    "HttpTimeout",
    "HttpVirtualNodeListenerOptions",
    "IGatewayRoute",
    "IMesh",
    "IRoute",
    "IVirtualGateway",
    "IVirtualNode",
    "IVirtualRouter",
    "IVirtualService",
    "Mesh",
    "MeshFilterType",
    "MeshProps",
    "Protocol",
    "Route",
    "RouteAttributes",
    "RouteBaseProps",
    "RouteProps",
    "RouteSpec",
    "RouteSpecConfig",
    "RouteSpecOptionsBase",
    "ServiceDiscovery",
    "ServiceDiscoveryConfig",
    "TcpRetryEvent",
    "TcpRouteSpecOptions",
    "TcpTimeout",
    "TcpVirtualNodeListenerOptions",
    "TlsCertificate",
    "TlsCertificateConfig",
    "TlsMode",
    "VirtualGateway",
    "VirtualGatewayAttributes",
    "VirtualGatewayBaseProps",
    "VirtualGatewayListener",
    "VirtualGatewayListenerConfig",
    "VirtualGatewayProps",
    "VirtualNode",
    "VirtualNodeAttributes",
    "VirtualNodeBaseProps",
    "VirtualNodeListener",
    "VirtualNodeListenerConfig",
    "VirtualNodeProps",
    "VirtualRouter",
    "VirtualRouterAttributes",
    "VirtualRouterBaseProps",
    "VirtualRouterListener",
    "VirtualRouterListenerConfig",
    "VirtualRouterProps",
    "VirtualService",
    "VirtualServiceAttributes",
    "VirtualServiceBackendOptions",
    "VirtualServiceProps",
    "VirtualServiceProvider",
    "VirtualServiceProviderConfig",
    "WeightedTarget",
]

publication.publish()
