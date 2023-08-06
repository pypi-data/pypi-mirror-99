import click
from spell.cli.exceptions import api_client_exception_handler, ExitException
from spell.cli.utils import command, prettify_time, tabulate_rows
from spell.cli.utils.command import docs_option


def get_available_instances(provider, region):
    if provider == "aws":
        options = ["cpu", "cpu-big", "cpu-huge", "ram-big", "ram-huge"]
        if region in [
            "ap-northeast-1",
            "ap-northeast-2",
            "ap-southeast-1",
            "ap-southeast-2",
            "ca-central-1",
            "cn-north-1",
            "cn-northwest-1",
            "eu-central-1",
            "eu-west-1",
            "eu-west-2",
            "us-east-1",
            "us-east-2",
            "us-west-2",
        ]:
            options.extend(
                [
                    "K80",
                    "K80x8",
                    "T4",
                    "T4-big",
                    "T4-huge",
                    "T4x4",
                    "V100",
                    "V100x4",
                    "V100x8",
                    "V100x8-big",
                ]
            )
        return options

    # GCP supports different GPUs in different regions
    options = ["cpu", "cpu-big", "cpu-huge"]
    if region in ["us-west1", "us-central1", "us-east1", "europe-west1", "asia-east1"]:
        options.extend(["K80", "K80x2", "K80x4", "K80x8"])
    if region in ["us-west1", "us-central1", "europe-west4", "asia-east1"]:
        options.extend(["V100", "V100x4", "V100x8"])
    if region in [
        "us-west1",
        "us-central1",
        "us-east1",
        "europe-west1",
        "europe-west4",
        "asia-east1",
        "australia-southeast1",
    ]:
        options.extend(["P100", "P100x2", "P100x4"])
    if region in [
        "asia-east1",
        "asia-northeast1",
        "asia-northeast3",
        "asia-south1",
        "asia-southeast1",
        "europe-west2",
        "europe-west3",
        "europe-west4",
        "southamerica-east1",
        "us-central1",
        "us-east1",
        "us-west1",
    ]:
        options.extend(["T4", "T4x2", "T4x4"])
    return options


# Maps the name used by the client to a display name
FRAMEWORKS = {
    "tensorflow1": "TensorFlow 1",
    "tensorflow2": "TensorFlow 2",
}


@command(name="list", short_help="List all your machine types")
@click.pass_context
def list_machine_types(ctx):
    def create_row(machine_type):
        machines = machine_type["machines"]
        return (
            machine_type["name"],
            machine_type["spell_type"],
            machine_type["is_spot"],
            machine_type["instance_spec"].get("storage_size"),
            ", ".join(machine_type["warm_frameworks"]),
            prettify_time(machine_type["created_at"]),
            prettify_time(machine_type["updated_at"]),
            machine_type["min_instances"],
            machine_type["max_instances"],
            machine_type["idle_timeout_seconds"] / 60,
            len([m for m in machines if m["status"] == "Starting"]),
            len([m for m in machines if m["status"] == "Idle"]),
            len([m for m in machines if m["status"] == "In use"]),
        )

    machine_types = ctx.obj["cluster"]["machine_types"]
    tabulate_rows(
        [create_row(mt) for mt in machine_types],
        headers=[
            "NAME",
            "TYPE",
            "SPOT",
            "DISK SIZE",
            "IMAGES",
            "CREATED",
            "LAST MODIFIED",
            "MIN",
            "MAX",
            "IDLE TIMEOUT",
            "STARTING",
            "IDLE",
            "IN USE",
        ],
    )


@command(
    name="add",
    short_help="Creates a new machine type for executing Spell Runs and Workspaces",
    docs="https://spell.ml/docs/ownvpc_machine_types/#creating-a-new-machine-type",
)
@click.pass_context
@click.option("--name", help="Name to give this machine type", prompt=True)
@click.option(
    "--instance-type",
    help="The type of machine to use e.g. 'CPU', 'K80'. "
    "If you skip this you will be prompted with options",
    default=None,
)
@click.option(
    "--spot",
    is_flag=True,
    default=False,
    help="Spot/Preemptible instances can be significantly cheaper than on demand instances, "
    "however AWS/GCP can terminate them at any time. If your run is terminated prematurely we "
    "will keep all data and save it for you with a final run status of Interrupted.",
)
@click.option(
    "--default-auto-resume",
    is_flag=True,
    default=False,
    help="Configure the default auto resume behavior for runs on this machine type. "
    "Runs can explicitly opt in or out of auto resume, this will be the default used for "
    "runs that don't specify. NOTE: This is only supported for spot instances currently.",
)
@click.option("--storage-size", default=80, type=int, help="Disk size in GB")
@click.option(
    "--additional-images",
    multiple=True,
    type=click.Choice(FRAMEWORKS.values()),
    help="By default all machines support TensorFlow 1, PyTorch, and Conda. "
    "If you require any additional frameworks you can select them here. "
    "Additional frameworks will increase the time it takes to spin up new machines.",
)
@click.option(
    "--min-machines",
    default=0,
    type=int,
    help="Minimum number of machines to keep available at all times regardless of demand",
)
@click.option(
    "--max-machines", default=2, type=int, help="Maximum number of machines of this machine type",
)
@click.option(
    "--idle-timeout",
    default=30,
    type=int,
    help="Grace period to wait before terminating idle machines (minutes)",
)
def add_machine_type(
    ctx,
    name,
    instance_type,
    spot,
    default_auto_resume,
    storage_size,
    additional_images,
    min_machines,
    max_machines,
    idle_timeout,
):
    cluster = ctx.obj["cluster"]

    # Prompt for instance type
    provider = cluster["cloud_provider"].lower()
    region = cluster["networking"][provider]["region"]
    instance_types = [i.lower() for i in get_available_instances(provider, region)]
    while not instance_type or instance_type.lower() not in instance_types:
        instance_type = click.prompt(
            "Please select an instance type from: {}".format(instance_types)
        )

    if default_auto_resume and not spot:
        raise ExitException(
            "Auto-resume is only supported on spot instances. "
            "Use --spot to specify a spot instance."
        )

    # Map display names to server names
    additional_images = [k for (k, v) in FRAMEWORKS.items() if v in additional_images]

    with api_client_exception_handler():
        ctx.obj["client"].create_machine_type(
            cluster["name"],
            name,
            instance_type.lower(),
            spot,
            default_auto_resume,
            storage_size,
            additional_images,
            min_machines,
            max_machines,
            idle_timeout,
        )
    click.echo("Successfully created new machine type {}".format(name))


def get_machine_type(ctx, name):
    machine_types = ctx.obj["cluster"]["machine_types"]
    machine_type_names = [mt["name"] for mt in machine_types]
    if name not in machine_type_names:
        raise ExitException(
            "Unknown machine type {} choose from {}".format(name, machine_type_names)
        )
    matching = [mt for mt in machine_types if mt["name"] == name]
    if len(matching) > 1:
        raise ExitException(
            "Unexpectedly found {} machine types with the name {}".format(len(matching), name)
        )
    return matching[0]


@command(
    name="scale", short_help="Change the limits for number of machines of this machine type",
)
@click.argument("name")
@click.option(
    "--min-machines",
    type=int,
    help="Minimum number of machines to keep available at all times regardless of demand. Omit to leave unchanged",
)
@click.option(
    "--max-machines",
    type=int,
    help="Maximum number of machines of this machine type. Omit to leave unchanged",
)
@click.option(
    "--idle-timeout",
    type=int,
    help="Grace period to wait before terminating idle machines (minutes). Omit to leave unchanged",
)
@click.option(
    "--default-auto-resume/--disable-default-auto-resume",
    default=None,
    hidden=True,
    help="Configure the default auto resume behavior for runs on this machine type. "
    "Runs can explicitly opt in or out of auto resume, this will be the default used for "
    "runs that don't specify. NOTE: This is only supported for spot instances currently.",
)
@click.pass_context
def scale_machine_type(ctx, name, min_machines, max_machines, idle_timeout, default_auto_resume):
    machine_type = get_machine_type(ctx, name)
    if default_auto_resume and not machine_type["is_spot"]:
        raise ExitException("Auto-resume is only supported on spot instances")
    if min_machines is None:
        min_machines = click.prompt(
            "Enter new value for minimum machines", default=machine_type["min_instances"],
        )
    if max_machines is None:
        max_machines = click.prompt(
            "Enter new value for maximum machines", default=machine_type["max_instances"],
        )
    if idle_timeout is None:
        idle_timeout = click.prompt(
            "Enter new value for idle timeout (minutes)",
            default=round(machine_type["idle_timeout_seconds"] / 60),
        )
    with api_client_exception_handler():
        ctx.obj["client"].scale_machine_type(
            ctx.obj["cluster"]["name"],
            machine_type["id"],
            min_machines,
            max_machines,
            idle_timeout,
            default_auto_resume,
        )
    click.echo("Successfully updated {}!".format(name))


@click.command(name="delete", short_help="Delete a machine type")
@click.argument("name")
@click.option("-f", "--force", is_flag=True, help="Do not prompt for confirmation")
@docs_option("https://spell.ml/docs/ownvpc_machine_types/#deleting-a-machine-type")
@click.pass_context
def delete_machine_type(ctx, name, force):
    machine_type = get_machine_type(ctx, name)
    if not force and not click.confirm("Are you sure you want to delete {}?".format(name)):
        return
    with api_client_exception_handler():
        cluster_name = ctx.obj["cluster"]["name"]
        mt_id = machine_type["id"]
        ctx.obj["client"].delete_machine_type(cluster_name, mt_id)
    click.echo("Successfully deleted {}!".format(name))


@click.command(name="get-token", short_help="Gets the auth token for a Private machine type")
@click.argument("name")
@click.option("--renew", is_flag=True, help="Renew token. This will invalidate the previous token")
@click.pass_context
def get_machine_type_token(ctx, name, renew):
    machine_type = get_machine_type(ctx, name)
    if machine_type["spell_type"] != "Customer":
        raise ExitException("Can only get-token for Private machine types")
    if renew:
        if not click.confirm(
            "Are you sure you want to renew the token for {}? "
            "Note this will invalidate the previous token".format(name)
        ):
            return
        with api_client_exception_handler():
            cluster_name = ctx.obj["cluster"]["name"]
            mt_id = machine_type["id"]
            click.echo("Renewing token for machine-type {}".format(name))
            machine_type = ctx.obj["client"].renew_token_machine_type(cluster_name, mt_id)
    click.echo("Token for machine-type {}: {}".format(name, machine_type["auth_token"]))
