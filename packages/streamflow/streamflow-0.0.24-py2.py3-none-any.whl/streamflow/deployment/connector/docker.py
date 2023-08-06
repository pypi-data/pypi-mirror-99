import asyncio
import json
import os
import shlex
from abc import ABC
from typing import MutableSequence, MutableMapping, Any, Tuple, Optional, Union

from typing_extensions import Text

from streamflow.core.exception import WorkflowExecutionException
from streamflow.core.scheduling import Resource
from streamflow.deployment.connector.base import BaseConnector
from streamflow.log_handler import logger


async def _check_effective_resource(common_paths: MutableMapping[Text, Any],
                                    effective_resources: MutableSequence[Text],
                                    resource: Text,
                                    path: Text,
                                    source_remote: Optional[Text] = None
                                    ) -> Tuple[MutableMapping[Text, Any], MutableSequence[Text]]:
    # Get all container mounts
    volumes = await _get_volumes(resource)
    for volume in volumes:
        # If path is in a persistent volume
        if path.startswith(volume['Destination']):
            if path not in common_paths:
                common_paths[path] = []
            # Check if path is shared with another resource that has been already processed
            for i, common_path in enumerate(common_paths[path]):
                if common_path['source'] == volume['Source']:
                    # If path has already been processed, but the current resource is the source, substitute it
                    if resource == source_remote:
                        effective_resources.remove(common_path['resource'])
                        common_path['resource'] = resource
                        common_paths[path][i] = common_path
                        effective_resources.append(resource)
                        return common_paths, effective_resources
                    # Otherwise simply skip current resource
                    else:
                        return common_paths, effective_resources
            # If this is the first resource encountered with the persistent path, add it to the list
            effective_resources.append(resource)
            common_paths[path].append({'source': volume['Source'], 'resource': resource})
            return common_paths, effective_resources
    # If path is not in a persistent volume, add the current resource to the list
    effective_resources.append(resource)
    return common_paths, effective_resources


async def _copy_local_to_remote_single(src: Text,
                                       dst: Text,
                                       resource: Text) -> None:
    dst = resource + ":" + dst
    proc = await asyncio.create_subprocess_exec(*shlex.split(_get_copy_command(src, dst)))
    await proc.wait()


async def _exists_image(image_name: Text) -> bool:
    exists_command = "".join(
        "docker "
        "image "
        "inspect "
        "{image_name}"
    ).format(
        image_name=image_name
    )
    proc = await asyncio.create_subprocess_exec(
        *shlex.split(exists_command),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    await proc.wait()
    return proc.returncode == 0


def _get_copy_command(src: Text, dst: Text):
    return "".join([
        "docker ",
        "cp ",
        "{src} ",
        "{dst}"
    ]).format(
        src=src,
        dst=dst
    )


async def _get_effective_resources(resources: MutableSequence[Text],
                                   dest_path: Text,
                                   source_remote: Optional[Text] = None) -> MutableSequence[Text]:
    common_paths = {}
    effective_resources = []
    for resource in resources:
        common_paths, effective_resources = await _check_effective_resource(
            common_paths,
            effective_resources,
            resource,
            dest_path,
            source_remote)
    return effective_resources


async def _get_resource(resource_name: Text) -> Resource:
    inspect_command = "".join([
        "docker ",
        "inspect ",
        "--format ",
        "'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ",
        resource_name])
    proc = await asyncio.create_subprocess_exec(
        *shlex.split(inspect_command),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    return Resource(name=resource_name, hostname=stdout.decode().strip())


async def _get_volumes(resource: Text) -> MutableSequence[MutableMapping[Text, Text]]:
    inspect_command = "".join([
        "docker ",
        "inspect ",
        "--format ",
        "'{{json .Mounts }}' ",
        resource])
    proc = await asyncio.create_subprocess_exec(
        *shlex.split(inspect_command),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    return json.loads(stdout.decode().strip())


async def _pull_image(image_name: Text) -> None:
    exists_command = "".join(
        "docker "
        "pull "
        "--quiet "
        "{image_name}"
    ).format(
        image_name=image_name
    )
    proc = await asyncio.create_subprocess_exec(*shlex.split(exists_command))
    await proc.wait()


class DockerBaseConnector(BaseConnector, ABC):

    async def _copy_local_to_remote(self,
                                    src: Text,
                                    dst: Text,
                                    resources: MutableSequence[Text]) -> None:
        effective_resources = await _get_effective_resources(resources, dst)
        await asyncio.gather(*[asyncio.create_task(
            _copy_local_to_remote_single(src, dst, resource)
        ) for resource in effective_resources])

    async def _copy_remote_to_local(self,
                                    src: Text,
                                    dst: Text,
                                    resource: Text) -> None:
        src = resource + ":" + src
        proc = await asyncio.create_subprocess_exec(*shlex.split(_get_copy_command(src, dst)))
        await proc.wait()

    async def _copy_remote_to_remote(self,
                                     src: Text,
                                     dst: Text,
                                     resources: MutableSequence[Text],
                                     source_remote: Text) -> None:
        effective_resources = await _get_effective_resources(resources, dst, source_remote)
        await super()._copy_remote_to_remote(src, dst, effective_resources, source_remote)

    async def run(self,
                  resource: Text,
                  command: MutableSequence[Text],
                  environment: MutableMapping[Text, Text] = None,
                  workdir: Optional[Text] = None,
                  stdin: Optional[Union[int, Text]] = None,
                  stdout: Union[int, Text] = asyncio.subprocess.STDOUT,
                  stderr: Union[int, Text] = asyncio.subprocess.STDOUT,
                  capture_output: bool = False,
                  job_name: Optional[Text] = None) -> Optional[Tuple[Optional[Any], int]]:
        encoded_command = self.create_encoded_command(
            command, resource, environment, workdir, stdin, stdout, stderr)
        run_command = "".join([
            "docker "
            "exec ",
            "-t ",
            "{service} ",
            "sh -c '{command}'"
        ]).format(
            service=resource,
            command=encoded_command
        )
        proc = await asyncio.create_subprocess_exec(
            *shlex.split(run_command),
            stdout=asyncio.subprocess.PIPE if capture_output else None,
            stderr=asyncio.subprocess.PIPE if capture_output else None)
        if capture_output:
            stdout, _ = await proc.communicate()
            return stdout.decode().strip(), proc.returncode
        else:
            await proc.wait()

class DockerConnector(DockerBaseConnector):

    def __init__(self,
                 streamflow_config_dir: Text,
                 image: Text,
                 addHost: Optional[MutableSequence[Text]] = None,
                 blkioWeight: Optional[int] = None,
                 blkioWeightDevice: Optional[MutableSequence[int]] = None,
                 capAdd: Optional[MutableSequence[Text]] = None,
                 capDrop: Optional[MutableSequence[Text]] = None,
                 cgroupParent: Optional[Text] = None,
                 cidfile: Optional[Text] = None,
                 containerIds: Optional[MutableSequence] = None,
                 cpuPeriod: Optional[int] = None,
                 cpuQuota: Optional[int] = None,
                 cpuRTPeriod: Optional[int] = None,
                 cpuRTRuntime: Optional[int] = None,
                 cpuShares: Optional[int] = None,
                 cpus: Optional[float] = None,
                 cpusetCpus: Optional[Text] = None,
                 cpusetMems: Optional[Text] = None,
                 detachKeys: Optional[Text] = None,
                 device: Optional[MutableSequence[Text]] = None,
                 deviceCgroupRule: Optional[MutableSequence[Text]] = None,
                 deviceReadBps: Optional[MutableSequence[Text]] = None,
                 deviceReadIops: Optional[MutableSequence[Text]] = None,
                 deviceWriteBps: Optional[MutableSequence[Text]] = None,
                 deviceWriteIops: Optional[MutableSequence[Text]] = None,
                 disableContentTrust: bool = True,
                 dns: Optional[MutableSequence[Text]] = None,
                 dnsOptions: Optional[MutableSequence[Text]] = None,
                 dnsSearch: Optional[MutableSequence[Text]] = None,
                 domainname: Optional[Text] = None,
                 entrypoint: Optional[Text] = None,
                 env: Optional[MutableSequence[Text]] = None,
                 envFile: Optional[MutableSequence[Text]] = None,
                 expose: Optional[MutableSequence[Text]] = None,
                 gpus: Optional[MutableSequence[Text]] = None,
                 groupAdd: Optional[MutableSequence[Text]] = None,
                 healthCmd: Optional[Text] = None,
                 healthInterval: Optional[Text] = None,
                 healthRetries: Optional[int] = None,
                 healthStartPeriod: Optional[Text] = None,
                 healthTimeout: Optional[Text] = None,
                 hostname: Optional[Text] = None,
                 init: bool = True,
                 ip: Optional[Text] = None,
                 ip6: Optional[Text] = None,
                 ipc: Optional[Text] = None,
                 isolation: Optional[Text] = None,
                 kernelMemory: Optional[int] = None,
                 label: Optional[MutableSequence[Text]] = None,
                 labelFile: Optional[MutableSequence[Text]] = None,
                 link: Optional[MutableSequence[Text]] = None,
                 linkLocalIP: Optional[MutableSequence[Text]] = None,
                 logDriver: Optional[Text] = None,
                 logOpts: Optional[MutableSequence[Text]] = None,
                 macAddress: Optional[Text] = None,
                 memory: Optional[int] = None,
                 memoryReservation: Optional[int] = None,
                 memorySwap: Optional[int] = None,
                 memorySwappiness: Optional[int] = None,
                 mount: Optional[MutableSequence[Text]] = None,
                 network: Optional[MutableSequence[Text]] = None,
                 networkAlias: Optional[MutableSequence[Text]] = None,
                 noHealthcheck: bool = False,
                 oomKillDisable: bool = False,
                 oomScoreAdj: Optional[int] = None,
                 pid: Optional[Text] = None,
                 pidsLimit: Optional[int] = None,
                 privileged: bool = False,
                 publish: Optional[MutableSequence[Text]] = None,
                 publishAll: bool = False,
                 readOnly: bool = False,
                 replicas: int = 1,
                 restart: Optional[Text] = None,
                 rm: bool = True,
                 runtime: Optional[Text] = None,
                 securityOpts: Optional[MutableSequence[Text]] = None,
                 shmSize: Optional[int] = None,
                 sigProxy: bool = True,
                 stopSignal: Optional[Text] = None,
                 stopTimeout: Optional[int] = None,
                 storageOpts: Optional[MutableSequence[Text]] = None,
                 sysctl: Optional[MutableSequence[Text]] = None,
                 tmpfs: Optional[MutableSequence[Text]] = None,
                 ulimit: Optional[MutableSequence[Text]] = None,
                 user: Optional[Text] = None,
                 userns: Optional[Text] = None,
                 uts: Optional[Text] = None,
                 volume: Optional[MutableSequence[Text]] = None,
                 volumeDriver: Optional[Text] = None,
                 volumesFrom: Optional[MutableSequence[Text]] = None,
                 workdir: Optional[Text] = None):
        super().__init__(streamflow_config_dir)
        self.image: Text = image
        self.addHost: Optional[MutableSequence[Text]] = addHost
        self.blkioWeight: Optional[int] = blkioWeight
        self.blkioWeightDevice: Optional[MutableSequence[int]] = blkioWeightDevice
        self.capAdd: Optional[MutableSequence[Text]] = capAdd
        self.capDrop: Optional[MutableSequence[Text]] = capDrop
        self.cgroupParent: Optional[Text] = cgroupParent
        self.cidfile: Optional[Text] = cidfile
        self.containerIds: MutableSequence[Text] = containerIds or []
        self.cpuPeriod: Optional[int] = cpuPeriod
        self.cpuQuota: Optional[int] = cpuQuota
        self.cpuRTPeriod: Optional[int] = cpuRTPeriod
        self.cpuRTRuntime: Optional[int] = cpuRTRuntime
        self.cpuShares: Optional[int] = cpuShares
        self.cpus: Optional[float] = cpus
        self.cpusetCpus: Optional[Text] = cpusetCpus
        self.cpusetMems: Optional[Text] = cpusetMems
        self.detachKeys: Optional[Text] = detachKeys
        self.device: Optional[MutableSequence[Text]] = device
        self.deviceCgroupRule: Optional[MutableSequence[Text]] = deviceCgroupRule
        self.deviceReadBps: Optional[MutableSequence[Text]] = deviceReadBps
        self.deviceReadIops: Optional[MutableSequence[Text]] = deviceReadIops
        self.deviceWriteBps: Optional[MutableSequence[Text]] = deviceWriteBps
        self.deviceWriteIops: Optional[MutableSequence[Text]] = deviceWriteIops
        self.disableContentTrust: bool = disableContentTrust
        self.dns: Optional[MutableSequence[Text]] = dns
        self.dnsOptions: Optional[MutableSequence[Text]] = dnsOptions
        self.dnsSearch: Optional[MutableSequence[Text]] = dnsSearch
        self.domainname: Optional[Text] = domainname
        self.entrypoint: Optional[Text] = entrypoint
        self.env: Optional[MutableSequence[Text]] = env
        self.envFile: Optional[MutableSequence[Text]] = envFile
        self.expose: Optional[MutableSequence[Text]] = expose
        self.gpus: Optional[MutableSequence[Text]] = gpus
        self.groupAdd: Optional[MutableSequence[Text]] = groupAdd
        self.healthCmd: Optional[Text] = healthCmd
        self.healthInterval: Optional[Text] = healthInterval
        self.healthRetries: Optional[int] = healthRetries
        self.healthStartPeriod: Optional[Text] = healthStartPeriod
        self.healthTimeout: Optional[Text] = healthTimeout
        self.hostname: Optional[Text] = hostname
        self.init: bool = init
        self.ip: Optional[Text] = ip
        self.ip6: Optional[Text] = ip6
        self.ipc: Optional[Text] = ipc
        self.isolation: Optional[Text] = isolation
        self.kernelMemory: Optional[int] = kernelMemory
        self.label: Optional[MutableSequence[Text]] = label
        self.labelFile: Optional[MutableSequence[Text]] = labelFile
        self.link: Optional[MutableSequence[Text]] = link
        self.linkLocalIP: Optional[MutableSequence[Text]] = linkLocalIP
        self.logDriver: Optional[Text] = logDriver
        self.logOpts: Optional[MutableSequence[Text]] = logOpts
        self.macAddress: Optional[Text] = macAddress
        self.memory: Optional[int] = memory
        self.memoryReservation: Optional[int] = memoryReservation
        self.memorySwap: Optional[int] = memorySwap
        self.memorySwappiness: Optional[int] = memorySwappiness
        self.mount: Optional[MutableSequence[Text]] = mount
        self.network: Optional[MutableSequence[Text]] = network
        self.networkAlias: Optional[MutableSequence[Text]] = networkAlias
        self.noHealthcheck: bool = noHealthcheck
        self.oomKillDisable: bool = oomKillDisable
        self.oomScoreAdj: Optional[int] = oomScoreAdj
        self.pid: Optional[Text] = pid
        self.pidsLimit: Optional[int] = pidsLimit
        self.privileged: bool = privileged
        self.publish: Optional[MutableSequence[Text]] = publish
        self.publishAll: bool = publishAll
        self.readOnly: bool = readOnly
        self.replicas: int = replicas
        self.restart: Optional[Text] = restart
        self.rm: bool = rm
        self.runtime: Optional[Text] = runtime
        self.securityOpts: Optional[MutableSequence[Text]] = securityOpts
        self.shmSize: Optional[int] = shmSize
        self.sigProxy: bool = sigProxy
        self.stopSignal: Optional[Text] = stopSignal
        self.stopTimeout: Optional[int] = stopTimeout
        self.storageOpts: Optional[MutableSequence[Text]] = storageOpts
        self.sysctl: Optional[MutableSequence[Text]] = sysctl
        self.tmpfs: Optional[MutableSequence[Text]] = tmpfs
        self.ulimit: Optional[MutableSequence[Text]] = ulimit
        self.user: Optional[Text] = user
        self.userns: Optional[Text] = userns
        self.uts: Optional[Text] = uts
        self.volume: Optional[MutableSequence[Text]] = volume
        self.volumeDriver: Optional[Text] = volumeDriver
        self.volumesFrom: Optional[MutableSequence[Text]] = volumesFrom
        self.workdir: Optional[Text] = workdir

    async def deploy(self, external: bool) -> None:
        if not external:
            # Pull image if it doesn't exist
            if not await _exists_image(self.image):
                await _pull_image(self.image)
            # Deploy the Docker container
            for _ in range(0, self.replicas):
                deploy_command = "".join([
                    "docker ",
                    "run "
                    "--detach "
                    "--interactive "
                    "{addHost}"
                    "{blkioWeight}"
                    "{blkioWeightDevice}"
                    "{capAdd}"
                    "{capDrop}"
                    "{cgroupParent}"
                    "{cidfile}"
                    "{cpuPeriod}"
                    "{cpuQuota}"
                    "{cpuRTPeriod}"
                    "{cpuRTRuntime}"
                    "{cpuShares}"
                    "{cpus}"
                    "{cpusetCpus}"
                    "{cpusetMems}"
                    "{detachKeys}"
                    "{device}"
                    "{deviceCgroupRule}"
                    "{deviceReadBps}"
                    "{deviceReadIops}"
                    "{deviceWriteBps}"
                    "{deviceWriteIops}"
                    "{disableContentTrust}"
                    "{dns}"
                    "{dnsOptions}"
                    "{dnsSearch}"
                    "{domainname}"
                    "{entrypoint}"
                    "{env}"
                    "{envFile}"
                    "{expose}"
                    "{gpus}"
                    "{groupAdd}"
                    "{healthCmd}"
                    "{healthInterval}"
                    "{healthRetries}"
                    "{healthStartPeriod}"
                    "{healthTimeout}"
                    "{hostname}"
                    "{init}"
                    "{ip}"
                    "{ip6}"
                    "{ipc}"
                    "{isolation}"
                    "{kernelMemory}"
                    "{label}"
                    "{labelFile}"
                    "{link}"
                    "{linkLocalIP}"
                    "{logDriver}"
                    "{logOpts}"
                    "{macAddress}"
                    "{memory}"
                    "{memoryReservation}"
                    "{memorySwap}"
                    "{memorySwappiness}"
                    "{mount}"
                    "{network}"
                    "{networkAlias}"
                    "{noHealthcheck}"
                    "{oomKillDisable}"
                    "{oomScoreAdj}"
                    "{pid}"
                    "{pidsLimit}"
                    "{privileged}"
                    "{publish}"
                    "{publishAll}"
                    "{readOnly}"
                    "{restart}"
                    "{rm}"
                    "{runtime}"
                    "{securityOpts}"
                    "{shmSize}"
                    "{sigProxy}"
                    "{stopSignal}"
                    "{stopTimeout}"
                    "{storageOpts}"
                    "{sysctl}"
                    "{tmpfs}"
                    "{ulimit}"
                    "{user}"
                    "{userns}"
                    "{uts}"
                    "{volume}"
                    "{volumeDriver}"
                    "{volumesFrom}"
                    "{workdir}"
                    "{image}"
                ]).format(
                    addHost=self.get_option("add-host", self.addHost),
                    blkioWeight=self.get_option("blkio-weight", self.addHost),
                    blkioWeightDevice=self.get_option("blkio-weight-device", self.blkioWeightDevice),
                    capAdd=self.get_option("cap-add", self.capAdd),
                    capDrop=self.get_option("cap-drop", self.capDrop),
                    cgroupParent=self.get_option("cgroup-parent", self.cgroupParent),
                    cidfile=self.get_option("cidfile", self.cidfile),
                    cpuPeriod=self.get_option("cpu-period", self.cpuPeriod),
                    cpuQuota=self.get_option("cpu-quota", self.cpuQuota),
                    cpuRTPeriod=self.get_option("cpu-rt-period", self.cpuRTPeriod),
                    cpuRTRuntime=self.get_option("cpu-rt-runtime", self.cpuRTRuntime),
                    cpuShares=self.get_option("cpu-shares", self.cpuShares),
                    cpus=self.get_option("cpus", self.cpus),
                    cpusetCpus=self.get_option("cpuset-cpus", self.cpusetCpus),
                    cpusetMems=self.get_option("cpuset-mems", self.cpusetMems),
                    detachKeys=self.get_option("detach-keys", self.detachKeys),
                    device=self.get_option("device", self.device),
                    deviceCgroupRule=self.get_option("device-cgroup-rule", self.deviceCgroupRule),
                    deviceReadBps=self.get_option("device-read-bps", self.deviceReadBps),
                    deviceReadIops=self.get_option("device-read-iops", self.deviceReadIops),
                    deviceWriteBps=self.get_option("device-write-bps", self.deviceWriteBps),
                    deviceWriteIops=self.get_option("device-write-iops", self.deviceWriteIops),
                    disableContentTrust="--disable-content-trust={disableContentTrust} ".format(
                        disableContentTrust="true" if self.disableContentTrust else "false"),
                    dns=self.get_option("dns", self.dns),
                    dnsOptions=self.get_option("dns-option", self.dnsOptions),
                    dnsSearch=self.get_option("dns-search", self.dnsSearch),
                    domainname=self.get_option("domainname", self.domainname),
                    entrypoint=self.get_option("entrypoint", self.entrypoint),
                    env=self.get_option("env", self.env),
                    envFile=self.get_option("env-file", self.envFile),
                    expose=self.get_option("expose", self.expose),
                    gpus=self.get_option("gpus", self.gpus),
                    groupAdd=self.get_option("group-add", self.groupAdd),
                    healthCmd=self.get_option("health-cmd", self.healthCmd),
                    healthInterval=self.get_option("health-interval", self.healthInterval),
                    healthRetries=self.get_option("health-retries", self.healthRetries),
                    healthStartPeriod=self.get_option("health-start-period", self.healthStartPeriod),
                    healthTimeout=self.get_option("health-timeout", self.healthTimeout),
                    hostname=self.get_option("hostname", self.hostname),
                    init=self.get_option("init", self.init),
                    ip=self.get_option("ip", self.ip),
                    ip6=self.get_option("ip6", self.ip6),
                    ipc=self.get_option("ipc", self.ipc),
                    isolation=self.get_option("isolation", self.isolation),
                    kernelMemory=self.get_option("kernel-memory", self.kernelMemory),
                    label=self.get_option("label", self.label),
                    labelFile=self.get_option("label-file", self.labelFile),
                    link=self.get_option("link", self.link),
                    linkLocalIP=self.get_option("link-local-ip", self.linkLocalIP),
                    logDriver=self.get_option("log-driver", self.logDriver),
                    logOpts=self.get_option("log-opt", self.logOpts),
                    macAddress=self.get_option("mac-address", self.macAddress),
                    memory=self.get_option("memory", self.memory),
                    memoryReservation=self.get_option("memory-reservation", self.memoryReservation),
                    memorySwap=self.get_option("memory-swap", self.memorySwap),
                    memorySwappiness=self.get_option("memory-swappiness", self.memorySwappiness),
                    mount=self.get_option("mount", self.mount),
                    network=self.get_option("network", self.network),
                    networkAlias=self.get_option("network-alias", self.networkAlias),
                    noHealthcheck=self.get_option("no-healthcheck", self.noHealthcheck),
                    oomKillDisable=self.get_option("oom-kill-disable", self.oomKillDisable),
                    oomScoreAdj=self.get_option("oom-score-adj", self.oomScoreAdj),
                    pid=self.get_option("pid", self.pid),
                    pidsLimit=self.get_option("pids-limit", self.pidsLimit),
                    privileged=self.get_option("privileged", self.privileged),
                    publish=self.get_option("publish", self.publish),
                    publishAll=self.get_option("publish-all", self.publishAll),
                    readOnly=self.get_option("read-only", self.readOnly),
                    restart=self.get_option("restart", self.restart),
                    rm=self.get_option("rm", self.rm),
                    runtime=self.get_option("runtime", self.runtime),
                    securityOpts=self.get_option("security-opt", self.securityOpts),
                    shmSize=self.get_option("shm-size", self.shmSize),
                    sigProxy="--sig-proxy={sigProxy} ".format(sigProxy="true" if self.sigProxy else "false"),
                    stopSignal=self.get_option("stop-signal", self.stopSignal),
                    stopTimeout=self.get_option("stop-timeout", self.stopTimeout),
                    storageOpts=self.get_option("storage-opt", self.storageOpts),
                    sysctl=self.get_option("sysctl", self.sysctl),
                    tmpfs=self.get_option("tmpfs", self.tmpfs),
                    ulimit=self.get_option("ulimit", self.ulimit),
                    user=self.get_option("user", self.user),
                    userns=self.get_option("userns", self.userns),
                    uts=self.get_option("uts", self.uts),
                    volume=self.get_option("volume", self.volume),
                    volumeDriver=self.get_option("volume-driver", self.volumeDriver),
                    volumesFrom=self.get_option("volumes-from", self.volumesFrom),
                    workdir=self.get_option("workdir", self.workdir),
                    image=self.image
                )
                logger.debug("Executing command {command}".format(command=deploy_command))
                proc = await asyncio.create_subprocess_exec(
                    *shlex.split(deploy_command),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE)
                stdout, stderr = await proc.communicate()
                if proc.returncode == 0:
                    self.containerIds.append(stdout.decode().strip())
                else:
                    raise WorkflowExecutionException(stderr.decode().strip())

    async def get_available_resources(self, service: Text) -> MutableMapping[Text, Resource]:
        return {container_id: await _get_resource(container_id) for container_id in self.containerIds}

    async def undeploy(self, external: bool) -> None:
        if not external and self.containerIds:
            for container_id in self.containerIds:
                undeploy_command = "".join([
                    "docker ",
                    "stop "
                    "{containerId}"
                ]).format(
                    containerId=container_id
                )
                logger.debug("Executing command {command}".format(command=undeploy_command))
                proc = await asyncio.create_subprocess_exec(
                    *shlex.split(undeploy_command),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE)
                await proc.wait()
            self.containerIds = []


class DockerComposeConnector(DockerBaseConnector):

    def __init__(self,
                 streamflow_config_dir: Text,
                 files: MutableSequence[Text],
                 projectName: Optional[Text] = None,
                 verbose: Optional[bool] = False,
                 logLevel: Optional[Text] = None,
                 noAnsi: Optional[bool] = False,
                 host: Optional[Text] = None,
                 tls: Optional[bool] = False,
                 tlscacert: Optional[Text] = None,
                 tlscert: Optional[Text] = None,
                 tlskey: Optional[Text] = None,
                 tlsverify: Optional[bool] = False,
                 skipHostnameCheck: Optional[bool] = False,
                 projectDirectory: Optional[Text] = None,
                 compatibility: Optional[bool] = False,
                 noDeps: Optional[bool] = False,
                 forceRecreate: Optional[bool] = False,
                 alwaysRecreateDeps: Optional[bool] = False,
                 noRecreate: Optional[bool] = False,
                 noBuild: Optional[bool] = False,
                 noStart: Optional[bool] = False,
                 build: Optional[bool] = False,
                 timeout: Optional[int] = None,
                 renewAnonVolumes: Optional[bool] = False,
                 removeOrphans: Optional[bool] = False,
                 removeVolumes: Optional[bool] = False
                 ) -> None:
        super().__init__(streamflow_config_dir)
        self.files = [os.path.join(streamflow_config_dir, file) for file in files]
        self.projectName = projectName
        self.verbose = verbose
        self.logLevel = logLevel
        self.noAnsi = noAnsi
        self.host = host
        self.noDeps = noDeps
        self.forceRecreate = forceRecreate
        self.alwaysRecreateDeps = alwaysRecreateDeps
        self.noRecreate = noRecreate
        self.noBuild = noBuild
        self.noStart = noStart
        self.build = build
        self.renewAnonVolumes = renewAnonVolumes
        self.removeOrphans = removeOrphans
        self.removeVolumes = removeVolumes
        self.skipHostnameCheck = skipHostnameCheck
        self.projectDirectory = projectDirectory
        self.compatibility = compatibility
        self.timeout = timeout
        self.tls = tls
        self.tlscacert = tlscacert
        self.tlscert = tlscert
        self.tlskey = tlskey
        self.tlsverify = tlsverify

    def base_command(self) -> Text:
        return "".join([
            "docker-compose ",
            "{files}",
            "{projectName}",
            "{verbose}",
            "{logLevel}",
            "{noAnsi}",
            "{host}",
            "{tls}",
            "{tlscacert}",
            "{tlscert}",
            "{tlskey}",
            "{tlsverify}",
            "{skipHostnameCheck}",
            "{projectDirectory}",
            "{compatibility} "
        ]).format(
            files=self.get_option("file", self.files),
            projectName=self.get_option("project-name", self.projectName),
            verbose=self.get_option("verbose", self.verbose),
            logLevel=self.get_option("log-level", self.logLevel),
            noAnsi=self.get_option("no-ansi", self.noAnsi),
            host=self.get_option("host", self.host),
            tls=self.get_option("tls", self.tls),
            tlscacert=self.get_option("tlscacert", self.tlscacert),
            tlscert=self.get_option("tlscert", self.tlscert),
            tlskey=self.get_option("tlskey", self.tlskey),
            tlsverify=self.get_option("tlsverify", self.tlsverify),
            skipHostnameCheck=self.get_option("skip-hostname-check", self.skipHostnameCheck),
            projectDirectory=self.get_option("project-directory", self.projectDirectory),
            compatibility=self.get_option("compatibility", self.compatibility)
        )

    async def deploy(self, external: bool) -> None:
        if not external:
            deploy_command = self.base_command() + "".join([
                "up ",
                "--detach ",
                "{noDeps}",
                "{forceRecreate}",
                "{alwaysRecreateDeps}",
                "{noRecreate}",
                "{noBuild}",
                "{noStart}"
            ]).format(
                noDeps=self.get_option("no-deps ", self.noDeps),
                forceRecreate=self.get_option("force-recreate", self.forceRecreate),
                alwaysRecreateDeps=self.get_option("always-recreate-deps", self.alwaysRecreateDeps),
                noRecreate=self.get_option("no-recreate", self.noRecreate),
                noBuild=self.get_option("no-build", self.noBuild),
                noStart=self.get_option("no-start", self.noStart)
            )
            logger.debug("Executing command {command}".format(command=deploy_command))
            proc = await asyncio.create_subprocess_exec(*shlex.split(deploy_command))
            await proc.wait()

    async def get_available_resources(self, service: Text) -> MutableMapping[Text, Resource]:
        ps_command = self.base_command() + "".join([
            "ps ",
            "--filter \"com.docker.compose.service\"=\"{service}\"".format(service=service)
        ])
        logger.debug("Executing command {command}".format(command=ps_command))
        proc = await asyncio.create_subprocess_exec(
            *shlex.split(ps_command),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, _ = await proc.communicate()
        lines = (line for line in stdout.decode().strip().split('\n'))
        resources = {}
        for line in lines:
            if line.startswith("---------"):
                break
        for line in lines:
            resource_name = line.split()[0].strip()
            resources[resource_name] = await _get_resource(resource_name)
        return resources

    async def undeploy(self, external: bool) -> None:
        if not external:
            undeploy_command = self.base_command() + "".join([
                "down ",
                "{removeVolumes}"
            ]).format(
                removeVolumes=self.get_option("volumes", self.removeVolumes)
            )
            logger.debug("Executing command {command}".format(command=undeploy_command))
            proc = await asyncio.create_subprocess_exec(*shlex.split(undeploy_command))
            await proc.wait()
