import click
import yaml
import os
import subprocess
from pathlib import Path
import time
import webbrowser

from halo import Halo

from spell.cli.exceptions import (
    api_client_exception_handler,
    ExitException,
    SPELL_INVALID_CONFIG,
)
from spell.cli.utils import (
    tabulate_rows,
    convert_to_local_time,
    with_emoji,
    git_utils,
    ellipses,
    parse_utils,
    prettify_time,
    require_install,
    get_star_spinner_frames,
)
from spell.cli.log import logger
from spell.cli.utils import group
from spell.cli.utils.command_options import (
    dependency_params,
    workspace_spec_params,
    cli_params,
    description_param,
    mount_params,
)
from spell.cli.utils.parse_utils import validate_attached_resources
from spell.client.utils import (
    get_conda_contents,
    get_requirements_file,
    format_pip_apt_versions,
)
from spell.api.models import (
    ContainerResourceRequirements,
    PodAutoscaleConfig,
    ResourceRequirement,
    ModelServerUpdateRequest,
    ModelServerCreateRequest,
    Environment,
    BatchingConfig,
)

RM_MAX_WAIT_TIME_S = 300
RM_CHECK_PERIOD_S = 5
RM_TOTAL_CHECKS = int(RM_MAX_WAIT_TIME_S / RM_CHECK_PERIOD_S)


@group(
    name="server",
    short_help="Manage model servers",
    help="Manage model servers",
    docs="https://spell.ml/docs/model_servers/"
)
@click.option(
    "--raw", help="display output in raw format", is_flag=True, default=False, hidden=True
)
@click.pass_context
def server(ctx, raw):
    pass


@server.command(name="list", short_help="List all your model servers")
@click.pass_context
@click.option(
    "--raw", help="display output in raw format", is_flag=True, default=False, hidden=True
)
def list_servers(ctx, raw):
    client = ctx.obj["client"]
    list_model_servers(client, raw)


def with_autoscaler_options(with_defaults=True):
    def decorator(f):
        f = click.option(
            "--target-cpu-utilization",
            type=float,
            help="If average pod CPU usage goes higher than this times the cpu-request the autoscaler "
            "will spin up a new pod.",
        )(f)
        f = click.option(
            "--target-requests-per-second",
            type=float,
            help="The autoscaler will scale up pods if the average number of HTTP(S) requests per second "
            "to a pod exceeds this value.",
        )(f)
        f = click.option(
            "--max-pods",
            type=int,
            default=5 if with_defaults else None,
            help="The autoscaler will never scale to more pods than this.",
        )(f)
        return click.option(
            "--min-pods",
            type=int,
            default=1 if with_defaults else None,
            help="The autoscaler will never scale to fewer pods than this.",
        )(f)

    return decorator


def with_resource_requirements_options(with_defaults=True):
    def decorator(f):
        f = click.option(
            "--gpu-limit",
            type=int,
            help=(
                "Maximum number of GPUs allowable to each pod. "
                "This defaults to 1 if the node group has GPUs"
            ),
        )(f)
        f = click.option(
            "--ram-limit",
            type=int,
            help="The maximum amount of RAM a pod can use in MB. It will be terminated if it exceeds this.",
        )(f)
        f = click.option(
            "--ram-request", type=int, help="The amount of RAM you expect each pod to use in MB",
        )(f)
        f = click.option(
            "--cpu-limit", type=float, help="The maximum amount of vCPU cores a pod can use"
        )(f)
        return click.option(
            "--cpu-request",
            type=float,
            default=0.9 if with_defaults else None,
            help="The amount of vCPU cores you expect each pod to use",
        )(f)

    return decorator


def with_batching_options(f):
    f = click.option(
        "--request-timeout",
        type=int,
        help=(
            "The maximum amount of time in milliseconds to wait before processing a request. "
            "Default is {}ms. By using this flag, you will enable batching.".format(
                BatchingConfig.DEFAULT_REQUEST_TIMEOUT
            )
        ),
    )(f)
    return click.option(
        "--max-batch-size",
        type=int,
        help=(
            "The maximum batch size. Default is {}. ".format(BatchingConfig.DEFAULT_MAX_BATCH_SIZE)
            + "By using this flag, you will enable batching."
        ),
    )(f)


def list_model_servers(client, raw):
    with api_client_exception_handler():
        model_servers = client.get_model_servers()
    if len(model_servers) == 0:
        click.echo("There are no model servers to display.")
    else:

        data = [
            (ms.server_name, ms.url, get_display_status(ms), ms.get_age(),) for ms in model_servers
        ]
        tabulate_rows(data, headers=["NAME", "URL", "PODS (READY/TOTAL)", "AGE"], raw=raw)


def get_display_status(model_server):
    if model_server.status not in ("running"):
        return model_server.status.capitalize()

    runningPods = [p for p in model_server.pods if not p.deleted_at]
    return f"{len([p for p in runningPods if p.ready_at])}/{len(runningPods)}"


@server.command(
    name="serve",
    short_help="Create a new model server using a model",
    help="""Create a new model server based on an existing model and entrypoint
            to a Python predictor able to serve said model.""",
    docs="https://spell.ml/docs/model_servers/#creating-model-servers"
)
@click.argument("model", metavar="MODEL:VERSION")
@click.argument("entrypoint")
@click.option("--name", help="Name of the model server. Defaults to the model name.")
@click.option(
    "--config",
    type=click.File(),
    help="Path to a YAML for JSON file which wil be passed through to the Predictor",
)
@click.option(
    "--node-group", help="Node group to schedule the server to. Defaults to initial node group.",
)
@click.option(
    "--classname",
    help="Name of the Predictor class to use. Only required if more than one predictor exist in the Python module used",
)
@dependency_params(include_docker=False, resource_type="model server")
@workspace_spec_params
@description_param(resource_type="model server")
@cli_params
@mount_params
@with_autoscaler_options()
@with_resource_requirements_options()
@click.option(
    "--num-processes",
    type=int,
    help=(
        "The number of processes to run the model server on. "
        "By default this is (2 * numberOfCores) + 1 or equal to the available GPUs if applicable"
    ),
)
@click.option(
    "--enable-batching",
    is_flag=True,
    help=(
        "Enable server-side batching. "
        "Without specifying further options this enables batching with the default options"
    ),
)
@with_batching_options
@click.option(
    "--validate",
    is_flag=True,
    help="Validate the structure of your predictor class. All Python packages required to import"
    " your predictor must be in your Python environment",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Launch the server in debug mode. For security purposes, this should not be used in production",
)
@click.option(
    "--open/--no-open", default=True, help="Open the server's webpage in a browser after creation",
)
@click.pass_context
def serve(
    ctx,
    model,
    entrypoint,
    name,
    config,
    node_group,
    classname,
    github_url,
    github_ref,
    pip_packages,
    requirements_file,
    apt_packages,
    commit_ref,
    description,
    envvars,
    force,
    verbose,
    conda_file,
    raw_resources,
    min_pods,
    max_pods,
    target_cpu_utilization,
    target_requests_per_second,
    cpu_request,
    cpu_limit,
    ram_request,
    ram_limit,
    gpu_limit,
    num_processes,
    enable_batching,
    max_batch_size,
    request_timeout,
    debug,
    validate,
    open,
    **kwargs,
):
    model_name, tag = parse_utils.get_name_and_tag(model)
    if tag is None:
        raise ExitException("A model tag must be specified in the form model_name:version")
    model_version_id, model_version_name = parse_utils.parse_tag(tag)
    if name is None:
        name = model_name
    if github_url and validate:
        raise ExitException("Cannot use --validate with --github-url")
    config = read_config(config)
    server_req = make_modelserver_create_request(
        ctx,
        model_name,
        model_version_id,
        model_version_name,
        entrypoint,
        name,
        config,
        node_group,
        classname,
        pip_packages,
        requirements_file,
        apt_packages,
        commit_ref,
        description,
        envvars,
        force,
        verbose,
        github_url,
        github_ref,
        conda_file,
        raw_resources,
        min_pods,
        max_pods,
        target_cpu_utilization,
        target_requests_per_second,
        cpu_request,
        cpu_limit,
        ram_request,
        ram_limit,
        gpu_limit,
        num_processes,
        enable_batching,
        max_batch_size,
        request_timeout,
        debug,
        validate,
        **kwargs,
    )
    client = ctx.obj["client"]
    logger.info("sending model server request to api")
    with api_client_exception_handler():
        server = client.new_model_server(server_req)

    utf8 = ctx.obj["utf8"]
    click.echo(
        with_emoji("💫", "Starting server {}".format(server.server_name), utf8) + ellipses(utf8)
    )
    if open:
        url = "{}/web_redirect/{}/model-servers/{}".format(
            ctx.obj["client_args"]["base_url"], ctx.obj["owner"], server.server_name
        )
        webbrowser.open(url)


def make_modelserver_create_request(
    ctx,
    model_name,
    model_version_id,
    model_version_name,
    entrypoint,
    name,
    config,
    node_group,
    classname,
    pip_packages,
    requirements_file,
    apt_packages,
    commit_ref,
    description,
    envvars,
    force,
    verbose,
    github_url,
    github_ref,
    conda_file,
    raw_resources,
    min_pods,
    max_pods,
    target_cpu_utilization,
    target_requests_per_second,
    cpu_request,
    cpu_limit,
    ram_request,
    ram_limit,
    gpu_limit,
    num_processes,
    enable_batching,
    max_batch_size,
    request_timeout,
    debug,
    validate,
    **kwargs,
):
    repo = git_utils.detect_repo(
        ctx,
        github_url=github_url,
        github_ref=github_ref,
        force=force,
        description=description,
        commit_ref=commit_ref,
        allow_missing=False,
        resource_type="model server",
    )
    if github_url is None and entrypoint is not None:
        validate_entrypoint(repo, entrypoint)
        entrypoint = git_utils.get_tracked_repo_path(repo, entrypoint)
    if validate:
        validate_predictor(entrypoint, repo, classname=classname)
    environment = create_environment(
        conda_file, pip_packages, requirements_file, apt_packages, envvars
    )
    attached_resources = validate_attached_resources(raw_resources)
    pod_autoscale_config = create_pod_autoscale_config(
        min_pods, max_pods, target_cpu_utilization, target_requests_per_second
    )
    resource_requirements = create_resource_requirements(
        ram_request, cpu_request, ram_limit, cpu_limit, gpu_limit,
    )
    if enable_batching or max_batch_size or request_timeout:
        batching_config = BatchingConfig(
            max_batch_size=max_batch_size or BatchingConfig.DEFAULT_MAX_BATCH_SIZE,
            request_timeout_ms=request_timeout or BatchingConfig.DEFAULT_REQUEST_TIMEOUT,
            is_enabled=True,
        )
    else:
        batching_config = BatchingConfig(is_enabled=False)

    return ModelServerCreateRequest(
        model_name=model_name,
        model_version_id=model_version_id,
        model_version_name=model_version_name,
        server_name=name,
        config=config,
        node_group=node_group,
        entrypoint=entrypoint,
        predictor_class=classname,
        environment=environment,
        attached_resources=attached_resources,
        description=repo.description,
        repository=repo,
        pod_autoscale_config=pod_autoscale_config,
        resource_requirements=resource_requirements,
        num_processes=num_processes,
        batching_config=batching_config,
        debug=debug,
    )


def make_modelserver_update_request(
    ctx,
    model_name,
    model_version_id,
    model_version_name,
    entrypoint,
    config,
    node_group,
    classname,
    pip_packages,
    requirements_file,
    apt_packages,
    commit_ref,
    description,
    envvars,
    force,
    verbose,
    github_url,
    github_ref,
    conda_file,
    update_spell_version,
    raw_resources,
    min_pods,
    max_pods,
    target_cpu_utilization,
    target_requests_per_second,
    cpu_request,
    cpu_limit,
    ram_request,
    ram_limit,
    gpu_limit,
    num_processes,
    batching_flag,
    max_batch_size,
    request_timeout,
    debug,
    validate,
    **kwargs,
):
    repo = None
    environment = None
    attached_resources = None
    pod_autoscale_config = None
    resource_requirements = None
    new_entrypoint = None
    if any((entrypoint, github_url, description, github_url, github_ref)) or commit_ref != "HEAD":
        repo = git_utils.detect_repo(
            ctx,
            github_url=github_url,
            github_ref=github_ref,
            force=force,
            description=description,
            commit_ref=commit_ref,
            allow_missing=False,
            resource_type="model server",
        )
        repo.description = None
        if github_url is None and entrypoint is not None:
            new_entrypoint = git_utils.get_tracked_repo_path(repo, entrypoint)
            validate_entrypoint(repo, new_entrypoint)
        if validate:
            validate_predictor(new_entrypoint, repo, classname=classname)
    if any((conda_file, pip_packages, requirements_file, apt_packages, envvars)):
        environment = create_environment(
            conda_file, pip_packages, requirements_file, apt_packages, envvars
        )

    if raw_resources:
        attached_resources = validate_attached_resources(raw_resources)

    if any(
        x is not None
        for x in (min_pods, max_pods, target_cpu_utilization, target_requests_per_second)
    ):
        pod_autoscale_config = create_pod_autoscale_config(
            min_pods, max_pods, target_cpu_utilization, target_requests_per_second
        )

    if any(x is not None for x in (ram_request, cpu_request, ram_limit, cpu_limit, gpu_limit)):
        resource_requirements = create_resource_requirements(
            ram_request, cpu_request, ram_limit, cpu_limit, gpu_limit
        )

    # TODO(Justin): This is ugly, and may warrant redoing this object using JSON PATCH specification
    batching_config = None
    if batching_flag is None:
        if max_batch_size or request_timeout:
            batching_config = BatchingConfig(
                max_batch_size=max_batch_size, request_timeout_ms=request_timeout, is_enabled=True
            )
    elif batching_flag or max_batch_size or request_timeout:
        batching_config = BatchingConfig(
            max_batch_size=max_batch_size, request_timeout_ms=request_timeout, is_enabled=True
        )
    else:
        batching_config = BatchingConfig(is_enabled=False)
    return ModelServerUpdateRequest(
        model_name=model_name,
        model_version_id=model_version_id,
        model_version_name=model_version_name,
        entrypoint=new_entrypoint,
        config=config,
        node_group=node_group,
        predictor_class=classname,
        environment=environment,
        update_spell_version=update_spell_version,
        attached_resources=attached_resources,
        description=description,
        repository=repo,
        pod_autoscale_config=pod_autoscale_config,
        resource_requirements=resource_requirements,
        num_processes=num_processes,
        batching_config=batching_config,
        debug=debug,
    )


def validate_entrypoint(repo, entrypoint):
    if not os.path.isfile(entrypoint):
        raise ExitException(
            "ENTRYPOINT {} file not found.".format(entrypoint), SPELL_INVALID_CONFIG
        )
    entrypoint = git_utils.get_tracked_repo_path(repo, entrypoint)
    if entrypoint is None:
        raise ExitException(
            "ENTRYPOINT must be a path within the repository.", SPELL_INVALID_CONFIG,
        )


def create_environment(conda_file, pip_packages, requirements_file, apt_packages, envvars):
    # TODO(ian) remove when we support custom docker images
    docker_image = None
    if docker_image is not None and (pip_packages or apt_packages or requirements_file):
        raise ExitException(
            "--apt, --pip, or --pip-req cannot be specified when --from is provided."
            " Please install packages in the specified Dockerfile.",
            SPELL_INVALID_CONFIG,
        )

    conda_file = get_conda_contents(conda_file)

    # grab pip packages from requirements file
    pip_packages = list(pip_packages)
    pip_packages.extend(get_requirements_file(requirements_file))

    # extract envvars into a dictionary
    curr_envvars = parse_utils.parse_env_vars(envvars)
    pip, apt = format_pip_apt_versions(pip_packages, apt_packages)
    return Environment(
        pip=pip, apt=apt, docker_image=docker_image, env_vars=curr_envvars, conda_file=conda_file,
    )


def create_pod_autoscale_config(
    min_pods, max_pods, target_cpu_utilization, target_requests_per_second
):
    pod_autoscale_config = PodAutoscaleConfig(min_pods=min_pods, max_pods=max_pods)
    if target_cpu_utilization is not None:
        pod_autoscale_config.target_cpu_utilization = int(target_cpu_utilization * 100)
    if target_requests_per_second is not None:
        pod_autoscale_config.target_avg_requests_per_sec_millicores = int(
            target_requests_per_second * 1000
        )
    return pod_autoscale_config


def create_resource_requirements(ram_request, cpu_request, ram_limit, cpu_limit, gpu_limit):
    resource_request = ResourceRequirement(memory_mebibytes=ram_request)
    if cpu_request is not None:
        resource_request.cpu_millicores = int(cpu_request * 1000)
    resource_limit = ResourceRequirement(memory_mebibytes=ram_limit, gpu=gpu_limit)
    if cpu_limit is not None:
        resource_limit.cpu_millicores = int(cpu_limit * 1000)
    return ContainerResourceRequirements(
        resource_request=resource_request, resource_limit=resource_limit,
    )


@server.command(
    name="rm",
    short_help="Remove a model server",
    help="""Remove the model server with the specified NAME""",
    docs="https://spell.ml/docs/model_servers/#stopping-or-deleting-model-servers"
)
@click.pass_context
@click.argument("name")
@click.option("-f", "--force", is_flag=True, help="Remove the server even if it is running")
def remove(ctx, name, force):
    parse_utils.validate_server_name(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        ms = client.get_model_server(server_name=name)
    spinner = None
    is_utf8_enabled = ctx.obj["utf8"]
    if ctx.obj["interactive"]:
        spinner = Halo(spinner=get_star_spinner_frames(is_utf8_enabled))
    if ms.status not in ("stopping", "stopped", "failed"):
        if not force:
            raise ExitException("Model server must be stopped before it can be removed")
        with api_client_exception_handler():
            client.stop_model_server(server_name=name)
        ms.status = "stopping"
    if ms.status == "stopping":
        waiting_text = "Waiting for server {} to complete stopping...".format(name)
        if spinner:
            spinner.text = waiting_text
            spinner.start()
        else:
            click.echo(waiting_text)
        is_stopped = False
        for _ in range(RM_TOTAL_CHECKS):
            with api_client_exception_handler():
                ms = client.get_model_server(server_name=name)
            if ms.status == "stopped":
                is_stopped = True
                break
            time.sleep(RM_CHECK_PERIOD_S)
        if not is_stopped:
            if spinner:
                spinner.stop()
            raise ExitException(
                "Model server is still not stopped after {} seconds. Try again later".format(
                    RM_MAX_WAIT_TIME_S
                )
            )
    with api_client_exception_handler():
        client.delete_model_server(server_name=name)
    removed_text = "Successfully removed model server {}".format(name)
    if spinner:
        spinner.stop_and_persist(
            text="Successfully removed model server {}".format(name), symbol="🎉"
        )
    else:
        click.echo(with_emoji("🎉", removed_text, is_utf8_enabled))


@server.command(
    name="start",
    short_help="Start a model server",
    help="""Start the model server with the specified NAME""",
)
@click.pass_context
@click.argument("name")
def start(ctx, name):
    parse_utils.validate_server_name(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        client.start_model_server(server_name=name)
    click.echo("Successfully started model server {}".format(name))


@server.command(
    name="stop",
    short_help="Stop a model server",
    help="""Stop the model server with the specified NAME""",
    docs="https://spell.ml/docs/model_servers/#stopping-or-deleting-model-servers"
)
@click.pass_context
@click.argument("name")
def stop(ctx, name):
    parse_utils.validate_server_name(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        client.stop_model_server(server_name=name)
    click.echo("Successfully began stopping model server {}".format(name))


@server.command(docs="https://spell.ml/docs/model_servers/#updating-model-servers")
@click.argument("server-name")
@click.option("--model", help="New model to use", metavar="NAME:VERSION")
@click.option("--entrypoint", help="Choose a new entrypoint for the server")
@click.option(
    "--config",
    type=click.File(),
    help="Path to a YAML for JSON file which wil be passed through to the Predictor",
)
@click.option(
    "--node-group", help="Node group to schedule the server to. Defaults to initial node group.",
)
@click.option(
    "--classname",
    help="Name of the Predictor class to use. Only required if more than one predictor exist in the Python module used",
)
@dependency_params(include_docker=False, resource_type="model server")
@workspace_spec_params
@click.option(
    "--update-spell-version",
    "update_spell_version",
    is_flag=True,
    default=False,
    help="Update the version of Spell running the model server",
)
@description_param(resource_type="model server")
@cli_params
@mount_params
@with_autoscaler_options(with_defaults=False)
@with_resource_requirements_options(with_defaults=False)
@click.option(
    "--num-processes",
    help=(
        "The number of processes to run the model server on. By default this is (2 * numberOfCores) + 1"
        ' or equal to the number of available GPUs if applicable. To use the default, enter "default"'
    ),
)
@click.option(
    "--enable-batching/--disable-batching",
    "batching_flag",
    default=None,
    help="Enable or disable server-side batching",
)
@with_batching_options
@click.option(
    "--validate",
    is_flag=True,
    help="Validate the structure of your predictor class. All Python packages required to import"
    " your predictor must be in your Python environment",
)
@click.option(
    "--debug-on/--debug-off",
    "debug",
    default=None,  # This default makes it a three-way flag
    help="Launch the server in debug mode. For security purposes, this should not be used in production",
)
@click.pass_context
def update(
    ctx,
    server_name,
    model,
    entrypoint,
    config,
    node_group,
    classname,
    github_url,
    github_ref,
    pip_packages,
    requirements_file,
    apt_packages,
    commit_ref,
    description,
    envvars,
    force,
    verbose,
    conda_file,
    update_spell_version,
    raw_resources,
    min_pods,
    max_pods,
    target_cpu_utilization,
    target_requests_per_second,
    cpu_request,
    cpu_limit,
    ram_request,
    ram_limit,
    gpu_limit,
    num_processes,
    batching_flag,
    max_batch_size,
    request_timeout,
    debug,
    validate,
    **kwargs,
):
    """Update a custom model server"""
    model_name, model_version_id, model_version_name = None, None, None
    if model:
        model_name, tag = parse_utils.get_name_and_tag(model)
        if tag is None:
            raise ExitException("A model tag must be specified in the form model_name:version")
        model_version_id, model_version_name = parse_utils.parse_tag(tag)
    if max_batch_size and not request_timeout:
        raise ExitException("--request-timeout must be specified if --max-batch-size is provided")
    if not max_batch_size and request_timeout:
        raise ExitException("--max-batch-size must be specified if --request-timeout is provided")
    if github_url and validate:
        raise ExitException("Cannot use --validate with --github-url")
    if validate and not entrypoint:
        raise ExitException("Cannot use --validate without --entrypoint")
    config = read_config(config)
    server_req = make_modelserver_update_request(
        ctx,
        model_name,
        model_version_id,
        model_version_name,
        entrypoint,
        config,
        node_group,
        classname,
        pip_packages,
        requirements_file,
        apt_packages,
        commit_ref,
        description,
        envvars,
        force,
        verbose,
        github_url,
        github_ref,
        conda_file,
        update_spell_version,
        raw_resources,
        min_pods,
        max_pods,
        target_cpu_utilization,
        target_requests_per_second,
        cpu_request,
        cpu_limit,
        ram_request,
        ram_limit,
        gpu_limit,
        num_processes,
        batching_flag,
        max_batch_size,
        request_timeout,
        debug,
        validate,
        **kwargs,
    )
    client = ctx.obj["client"]
    logger.info("sending model server update request to api")
    with api_client_exception_handler():
        client.update_model_server(server_name, server_req)

    utf8 = ctx.obj["utf8"]
    click.echo(with_emoji("💫", "Updating server {}".format(server_name), utf8) + ellipses(utf8))


@server.command(
    short_help="Describe a model server",
    help="""Describe a model server with the specified NAME""",
)
@click.pass_context
@click.argument("name")
def describe(ctx, name):
    parse_utils.validate_server_name(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        ms = client.get_model_server(server_name=name)
    lines = [("Server Name", ms.server_name)]
    if ms.model_version:
        lines.extend(get_custom_model_server_info_lines(ms))
    else:
        lines.append(("Resource", ms.resource_path))
    lines.append(("Date Created", convert_to_local_time(ms.created_at)))
    lines.append(("Time Running", ms.get_age()))
    lines.append(("URL", ms.url))
    lines.append(("Node Group", ms.node_group_name))
    if not ms.cluster.get("is_serving_cluster_public", False):
        lines.append(("*NOTE*", "This will only be accessible within the same VPC of the cluster"))
    if len(ms.additional_resources) > 0:
        lines.append(("Mounts", ""))
        for resource, destination in ms.additional_resources.items():
            lines.append(("\t", "{} at {}".format(resource, destination)))
    if ms.environment:
        lines.extend(get_model_server_env_lines(ms.environment))
    click.echo("Server Info:")
    tabulate_rows(lines)
    lines = [("Pods (Ready/Total)", get_display_status(ms))]
    if ms.resource_requirements:
        request = ms.resource_requirements.request
        limit = ms.resource_requirements.limit
        if request and request.cpu_millicores:
            lines.append(("CPU Request", "{}m".format(request.cpu_millicores)))
        if limit and limit.cpu_millicores:
            lines.append(("CPU Limit", "{}m".format(limit.cpu_millicores)))
        if request and request.memory_mebibytes:
            lines.append(("Memory Request", "{} MiB".format(request.memory_mebibytes)))
        if limit and limit.memory_mebibytes:
            lines.append(("Memory Limit", "{}MiB".format(limit.memory_mebibytes)))

    if ms.pod_autoscale_config:
        config = ms.pod_autoscale_config
        if config.min_pods:
            lines.append(("Min Pods", config.min_pods))
        if config.max_pods:
            lines.append(("Max Pods", config.max_pods))
        if config.target_cpu_utilization:
            lines.append(("Target Pod CPU", "{}%".format(config.target_cpu_utilization)))
        if config.target_avg_requests_per_sec_millicores:
            lines.append(
                (
                    "Target Req per Second",
                    "{}".format(config.target_avg_requests_per_sec_millicores / 1000),
                )
            )
    if ms.num_processes is not None:
        lines.append(("Number of Worker Processes", ms.num_processes))
    lines.extend(get_batching_config_lines(ms.batching_config))

    click.echo("\nPerformance Info:")
    tabulate_rows(lines)


def get_custom_model_server_info_lines(ms):
    lines = []
    specifier = ms.model_version.specifier
    if specifier:
        lines.append(("Model", specifier))
    lines.append(("Resource", ms.model_version.resource))
    if ms.workspace:
        lines.append(("Repository", ms.workspace.name))
    if ms.github_url:
        lines.append(("GitHub URL", ms.github_url))
    if ms.debug:
        lines.append(("Debug", ms.debug))
    if ms.git_commit_hash:
        formatted_hash = ms.git_commit_hash
        if ms.has_uncommitted:
            formatted_hash += "[Uncommitted]"
        lines.append(("GitCommitHash", formatted_hash))
    if ms.entrypoint:
        lines.append(("Entrypoint", ms.entrypoint))
    if ms.predictor_class:
        lines.append(("Predictor Class", ms.predictor_class))
    return lines


def get_model_server_env_lines(environment):
    lines = []
    if environment.apt:
        lines.append(("Apt", ""))
        for a in environment.apt:
            lines.append(("\t", str(a)))
    if environment.pip:
        lines.append(("Pip", ""))
        for p in environment.pip:
            lines.append(("\t", str(p)))
    if environment.env_vars:
        lines.append(("Environment Vars", ""))
        for name, value in environment.env_vars.items():
            lines.append(("\t", "{}={}".format(name, value)))
    if environment.conda_file:
        lines.append(("Conda File", environment.conda_file))
    return lines


def get_batching_config_lines(config):
    lines = []
    if config and config.is_enabled:
        lines.append(("Batching Enabled", "Yes"))
        lines.append(("Batch Timeout", f"{config.request_timeout_ms}ms"))
        lines.append(("Max Batch Size", config.max_batch_size))
    else:
        lines.append(("Batching Enabled", "No"))
    return lines


@server.command(name="status", help="Get the status of all pods for this server.")
@click.pass_context
@click.argument("name")
def status(ctx, name):
    parse_utils.validate_server_name(name)
    with api_client_exception_handler():
        ms = ctx.obj["client"].get_model_server(server_name=name)
    print_pod_statuses(ms)


def print_pod_statuses(model_server):
    rows = []
    for p in model_server.pods:
        ready_at = prettify_time(p.ready_at) if p.ready_at else "-"
        rows.append([p.id, prettify_time(p.created_at), ready_at])
    tabulate_rows(rows, headers=["POD ID", "CREATED AT", "READY AT"])


@server.command(
    name="logs",
    short_help="Get logs from a model server",
    help="""Get logs for the model server with the specified NAME""",
    docs="https://spell.ml/docs/model_servers/#viewing-model-server-logs"
)
@click.pass_context
@click.option("-f", "--follow", is_flag=True, help="Follow log output")
@click.option(
    "-p", "--pod", help="The ID of the pod you would like logs for. Omit to get a list of all pods."
)
@click.argument("name")
def logs(ctx, name, pod, follow):
    parse_utils.validate_server_name(name)
    client = ctx.obj["client"]

    # Prompt with all pods so user can select one
    if not pod:
        with api_client_exception_handler():
            ms = client.get_model_server(server_name=name)
        if len(ms.pods) == 0:
            click.echo("There are no active pods for this server.")
            return
        if len(ms.pods) == 1:
            pod = str(ms.pods[0].id)
        else:
            print_pod_statuses(ms)
            pod_ids = [str(pod.id) for pod in ms.pods]
            pod = click.prompt(
                "Enter the ID of the pod you would like logs for", type=click.Choice(pod_ids)
            )

    utf8 = ctx.obj["utf8"]
    with api_client_exception_handler():
        try:
            for entry in client.get_model_server_log_entries(name, pod, follow=follow):
                click.echo(entry.log)
        except KeyboardInterrupt:
            if follow:
                click.echo()
                click.echo(
                    with_emoji(
                        "✨",
                        "Use 'spell model-servers logs -f {}' to view logs again".format(name),
                        utf8,
                    )
                )


@server.command(short_help="cURL the predict URL of a model server")
@require_install("curl")
@click.argument("name")
@click.argument("curl_args", nargs=-1)
@click.option(
    "--json",
    "json_arg",
    help="Pass a json object to the predict URL. If a path to a file is provided, it will be read and passed",
)
@click.pass_context
def predict(ctx, name, curl_args, json_arg):
    """Issue a cURL command against the predict endpoint of a model server

    This is a POST request. Further cURL arguments can be provided using "--". Example:
    spell server predict myserver -- -H "Content-Type: appliation/json" -d '{data: [1,2,3]}'
    """
    cmd = ["curl", "-X", "POST"]
    if json_arg:
        cmd.extend(["-H", "Content-Type: application/json", "-d"])
        json_file = Path(json_arg)
        if json_file.exists():
            cmd.append("@" + json_arg)
        else:
            cmd.append(json_arg)
    parse_utils.validate_server_name(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        server = client.get_model_server(server_name=name)
    cmd.extend(curl_args)
    cmd.append(server.url)
    click.echo(subprocess.check_output(cmd))


@server.command(short_help="cURL the health URL of a model server")
@require_install("curl")
@click.argument("name")
@click.argument("curl_args", nargs=-1)
@click.pass_context
def healthcheck(ctx, name, curl_args):
    """Issue a cURL command against the health endpoint of a model server

    This is a GET request. Further cURL arguments can be provided using "--". Example:
    spell server healthcheck myserver -- -H "Content-Type: appliation/json" -d '{data: [1,2,3]}'
    """
    parse_utils.validate_server_name(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        server = client.get_model_server(server_name=name)
    cmd = ["curl"]
    cmd.extend(curl_args)
    url = server.url[: -len("predict")] + "health"
    cmd.append(url)
    click.echo(subprocess.check_output(cmd))


def get_config_info(config, owner, cluster_name):
    server_name = config["specifier"]
    parse_utils.validate_server_name(server_name)
    owner = owner if "owner" not in config else config["owner"]
    cluster_name = cluster_name if "clusterName" not in config else config["clusterName"]
    return server_name, owner, cluster_name


def read_config(config_file):
    """This function loads, then dumps the config. This both ensures it's valid YAML and
    standardizes the string representation so it can be more easily manipulated.
    """
    if not config_file:
        return ""
    try:
        config = yaml.safe_load(config_file)
        return yaml.dump(config)
    except yaml.scanner.ScannerError:
        raise ExitException("Config file is not valid YAML")


def validate_predictor(entrypoint, repo, classname=None):
    try:
        from spell.serving.api import API
        from spell.serving.exceptions import InvalidPredictor
    except ImportError:
        raise ExitException(
            "Could not import required packages to validate your predictor. "
            "Please run `pip install --upgrade 'spell[serving]'` and rerun this command"
        )
    try:
        API.from_entrypoint(Path(entrypoint), classname=classname, root=Path(repo.local_root))
    except InvalidPredictor as e:
        raise ExitException(str(e))
