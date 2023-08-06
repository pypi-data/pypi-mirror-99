// This file was auto-generated from a YAML file

package v1_0

func init() {
	Profile["/tosca/kubernetes/1.0/capabilities.yaml"] = `
tosca_definitions_version: tosca_simple_yaml_1_3

imports:

- data.yaml

capability_types:

  # Resources

  # https://github.com/kubernetes/community/blob/master/contributors/devel/api-conventions.md#metadata
  # https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.10/#objectmeta-v1-meta
  Metadata:
    description: >-
      ObjectMeta is metadata that all persisted resources must have, which includes all objects
      users must create.
    properties:
      # Identification
      name:
        description: >-
          Name must be unique within a namespace. Is required when creating resources, although some
          resources may allow a client to request the generation of an appropriate name
          automatically. Name is primarily intended for creation idempotence and configuration
          definition. Cannot be updated.
        type: string
        required: false
      generateName:
        description: >-
          GenerateName is an optional prefix, used by the server, to generate a unique name ONLY IF
          the Name field has not been provided. If this field is used, the name returned to the
          client will be different than the name passed. This value will also be combined with a
          unique suffix. The provided value has the same validation rules as the Name field, and may
          be truncated by the length of the suffix required to make the value unique on the server.
          If this field is specified and the generated name exists, the server will NOT return a 409
          - instead, it will either return 201 Created or 500 with Reason ServerTimeout indicating a
          unique name could not be found in the time allotted, and the client should retry
          (optionally after the time indicated in the Retry-After header). Applied only if Name is
          not specified.
        type: string
        required: false
      namespace:
        description: >-
          Namespace defines the space within each name must be unique. An empty namespace is
          equivalent to the "default" namespace, but "default" is the canonical representation. Not
          all objects are required to be scoped to a namespace - the value of this field for those
          objects will be empty. Must be a DNS_LABEL. Cannot be updated.
        type: string
        required: false
      labels:
        description: >-
          Map of string keys and values that can be used to organize and categorize (scope and
          select) objects. May match selectors of replication controllers and services.
        type: map
        entry_schema: string
        required: false

      # Extra
      annotations:
        description: >-
          Annotations is an unstructured key value map stored with a resource that may be set by
          external tools to store and retrieve arbitrary metadata. They are not queryable and should
          be preserved when modifying objects.
        type: map
        entry_schema: string # TODO
        required: false

      # Lifecycle
      initializers:
        description: >-
          An initializer is a controller which enforces some system invariant at object creation
          time. This field is a list of initializers that have not yet acted on this object. If nil
          or empty, this object has been completely initialized. Otherwise, the object is considered
          uninitialized and is hidden (in list/watch and get calls) from clients that haven't
          explicitly asked to observe uninitialized objects. When an object is created, the system
          will populate this list with the current set of initializers. Only privileged users may
          set or modify this list. Once it is empty, it may not be modified further by any user.
        type: list
        entry_schema: string # TODO
        required: false
      finalizers:
        description: >-
          Must be empty before the object is deleted from the registry. Each entry is an identifier
          for the responsible component that will remove the entry from the list. If the
          deletionTimestamp of the object is non-nil, entries in this list can only be removed.
        type: list
        entry_schema: string # TODO
        required: false
      ownerReferences:
        description: >-
          List of objects depended by this object. If ALL objects in the list have been deleted,
          this object will be garbage collected. If this object is managed by a controller, then an
          entry in this list will point to this controller, with the controller field set to true.
          There cannot be more than one managing controller.
        type: list
        entry_schema: string # TODO
        required: false

    attributes:
      # Identification
      uid:
        description: >-
          UID is the unique in time and space value for this object. It is typically generated by
          the server on successful creation of a resource and is not allowed to change on PUT
          operations. Populated by the system. Read-only.
        type: string
      selfLink:
        description: >-
          SelfLink is a URL representing this object. Populated by the system. Read-only.
        type: string
      resourceVersion:
        description: >-
          An opaque value that represents the internal version of this object that can be used by
          clients to determine when objects have changed. May be used for optimistic concurrency,
          change detection, and the watch operation on a resource or set of resources. Clients must
          treat these values as opaque and passed unmodified back to the server. They may only be
          valid for a particular resource or set of resources. Populated by the system. Read-only.
          Value must be treated as opaque by clients.
        type: string
      clusterName:
        description: >-
          The name of the cluster which the object belongs to. This is used to distinguish resources
          with same name and namespace in different clusters. This field is not set anywhere right
          now and apiserver is going to ignore it if set in create or update request.
        type: string
      generation:
        description: >-
          A sequence number representing a specific generation of the desired state. Populated by
          the system. Read-only.
        type: Count
        default: 0

      # Lifecycle
      creationTimestamp:
        description: >-
          CreationTimestamp is a timestamp representing the server time when this object was
          created. It is not guaranteed to be set in happens-before order across separate
          operations. Clients may not set this value. It is represented in RFC3339 form and is in
          UTC. Populated by the system. Read-only. Null for lists.
        type: timestamp
      deletionTimestamp:
        description: >-
          DeletionTimestamp is RFC 3339 date and time at which this resource will be deleted. This
          field is set by the server when a graceful deletion is requested by the user, and is not
          directly settable by a client. The resource is expected to be deleted (no longer visible
          from resource lists, and not reachable by name) after the time in this field, once the
          finalizers list is empty. As long as the finalizers list contains items, deletion is
          blocked. Once the deletionTimestamp is set, this value may not be unset or be set further
          into the future, although it may be shortened or the resource may be deleted prior to this
          time. For example, a user may request that a pod is deleted in 30 seconds. The Kubelet
          will react by sending a graceful termination signal to the containers in the pod. After
          that 30 seconds, the Kubelet will send a hard termination signal (SIGKILL) to the
          container and after cleanup, remove the pod from the API. In the presence of network
          partitions, this object may still exist after this timestamp, until an administrator or
          automated process can determine the resource is fully terminated. If not set, graceful
          deletion of the object has not been requested. Populated by the system when a graceful
          deletion is requested. Read-only.
        type: timestamp
      deletionGracePeriodSeconds:
        description: >-
          Number of seconds allowed for this object to gracefully terminate before it will be
          removed from the system. Only set when deletionTimestamp is also set. May only be
          shortened. Read-only.
        type: scalar-unit.time
        default: 0 s

  # https://kubernetes.io/docs/concepts/services-networking/service/
  # https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.10/#service-v1-core
  Service:
    description: >-
      Service is a named abstraction of software service (for example, mysql) consisting of local
      port (for example 3306) that the proxy listens on, and the selector that determines which pods
      will answer requests sent through the proxy.
    properties:
      ports:
        description: >-
          The list of ports that are exposed by this service.
        type: list
        entry_schema: ServicePort

      # Pods
      selector:
        description: >-
          Route service traffic to pods with label keys and values matching this selector. If empty
          or not present, the service is assumed to have an external process managing its endpoints,
          which Kubernetes will not modify. Only applies to types ClusterIP, NodePort, and
          LoadBalancer. Ignored if type is ExternalName.
        type: map
        entry_schema: string
        required: false

      # DNS
      publishNotReadyAddresses:
        description: >-
          publishNotReadyAddresses, when set to true, indicates that DNS implementations must
          publish the notReadyAddresses of subsets for the Endpoints associated with the Service.
          The default value is false. The primary use case for setting this field is to use a
          StatefulSet's Headless Service to propagate SRV records for its Pods without respect to
          their readiness for purpose of peer discovery.
        type: boolean
        default: false

      # External
      externalIPs:
        description: >-
          externalIPs is a list of IP addresses for which nodes in the cluster will also accept
          traffic for this service. These IPs are not managed by Kubernetes. The user is responsible
          for ensuring that traffic arrives at a node with this IP. A common example is external
          load-balancers that are not part of the Kubernetes system.
        type: map
        entry_schema: IP
        required: false
      externalTrafficPolicy:
        description: >-
          externalTrafficPolicy denotes if this Service desires to route external traffic to
          node-local or cluster-wide endpoints. "Local" preserves the client source IP and avoids a
          second hop for LoadBalancer and Nodeport type services, but risks potentially imbalanced
          traffic spreading. "Cluster" obscures the client source IP and may cause a second hop to
          another node, but should have good overall load-spreading.
        type: string
        constraints:
        - valid_values: [ Local, Cluster ]
        required: false

      # Session
      sessionAffinity:
        description: >-
          Supports "ClientIP" and "None". Used to maintain session affinity. Enable client IP based
          session affinity. Must be ClientIP or None. Defaults to None.
        type: string
        default: None
        constraints:
        - valid_values: [ ClientIP, None ]
      # TODO: sessionAffinityConfig
    attributes:
      status:
        description: >-
          Most recently observed status of the service. Populated by the system. Read-only.
        type: string # TODO

  ClusterIP:
    description: >-
      "ClusterIP" allocates a cluster-internal IP address for load-balancing to endpoints. Endpoints
      are determined by the selector or if that is not specified, by manual construction of an
      Endpoints object. If clusterIP is "None", no virtual IP is allocated and the endpoints are
      published as a set of endpoints rather than a stable IP.
    derived_from: Service
    attributes:
      clusterIP:
        description: >-
          clusterIP is the IP address of the service and is usually assigned randomly by the master.
          If an address is specified manually and is not in use by others, it will be allocated to
          the service; otherwise, creation of the service will fail. This field can not be changed
          through updates. Valid values are "None", empty string (""), or a valid IP address.
          "None" can be specified for headless services when proxying is not required.
        type: IP

  NodePort:
    description: >-
      "NodePort" builds on ClusterIP and allocates a port on every node which routes to the
      clusterIP.
    derived_from: ClusterIP

  LoadBalancer:
    description: >-
      "LoadBalancer" builds on NodePort and creates an external load-balancer (if supported in the
      current cloud) which routes to the clusterIP.
    derived_from: NodePort
    properties:
      loadBalancerIP:
        description: >-
          LoadBalancer will get created with the IP specified in this field. This feature depends on
          whether the underlying cloud-provider supports specifying the loadBalancerIP when a load
          balancer is created. This field will be ignored if the cloud-provider does not support the
          feature.
        type: IP
      loadBalancerSourceRanges:
        description: >-
          If specified and supported by the platform, this will restrict traffic through the
          cloud-provider load-balancer will be restricted to the specified client IPs. This field
          will be ignored if the cloud-provider does not support the feature.
        type: list
        entry_schema: IP
    attributes:
      healthCheckNodePort:
        description: >-
          healthCheckNodePort specifies the healthcheck nodePort for the service. If not specified,
          HealthCheckNodePort is created by the service api backend with the allocated nodePort.
          Will use user-specified nodePort value if specified by the client. Only effects when
          ExternalTrafficPolicy is set to Local.
        type: Port

  ExternalName:
    description: >-
      "ExternalName" maps to the specified externalName.
    derived_from: Service
    properties:
      externalName:
        description: >-
          externalName is the external reference that kubedns or equivalent will return as a CNAME
          record for this service. No proxying will be involved. Must be a valid RFC-1123 hostname.
        type: Hostname

  # Controllers

  Controller:
    description: >-
      Controller

  # https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
  # https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.10/#deployment-v1-apps
  Deployment:
    description: >-
      Deployment enables declarative updates for Pods and ReplicaSets.
    derived_from: Controller
    properties:
      # Resources
      template:
        description: >-
          Template describes the pods that will be created.
        type: Pod
      selector:
        description: >-
          Label selector for pods. Existing ReplicaSets whose pods are selected by this will be the
          ones affected by this deployment. It must match the pod template's labels.
        type: LabelSelector
        default: {}

      # Deployment
      replicas:
        description: >-
          Number of desired pods. This is a pointer to distinguish between explicit zero and not
          specified. Defaults to 1.
        type: Count
        default: 1
      revisionHistoryLimit:
        description: >-
          The number of old ReplicaSets to retain to allow rollback. This is a pointer to
          distinguish between explicit zero and not specified. Defaults to 10.
        type: Count
        default: 10
      strategy:
        description: >-
          The deployment strategy to use to replace existing pods with new ones.
        type: DeploymentStrategy
        default: {}

      # Lifecycle
      minReadySeconds:
        description: >-
          Minimum number of seconds for which a newly created pod should be ready without any of its
          container crashing, for it to be considered available. Defaults to 0 (pod will be
          considered available as soon as it is ready).
        type: scalar-unit.time
        default: 0s
      progressDeadlineSeconds:
        description: >-
          The maximum time in seconds for a deployment to make progress before it is considered to
          be failed. The deployment controller will continue to process failed deployments and a
          condition with a ProgressDeadlineExceeded reason will be surfaced in the deployment
          status. Note that progress will not be estimated during the time a deployment is paused.
          Defaults to 600s.
        type: scalar-unit.time
        default: 600s

    attributes:
      paused:
        description: >-
          Indicates that the deployment is paused.
        type: boolean

  VirtualService:
    metadata:
      puccini.kubernetes.plugins.1: js/plugins/istio.js
    description: >-
      Creates a DestinationRule subset with the name of the node template
      Adds to VirtualService (with HttpRoute) for that subset
    derived_from: Service
`
}
