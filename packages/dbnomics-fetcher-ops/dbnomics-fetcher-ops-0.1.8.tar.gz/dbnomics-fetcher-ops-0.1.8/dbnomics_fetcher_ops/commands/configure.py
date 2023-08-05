# dbnomics-fetcher-ops -- Manage DBnomics fetchers
# By: Christophe Benz <christophe.benz@cepremap.org>
#
# Copyright (C) 2020 Cepremap
# https://git.nomics.world/dbnomics/dbnomics-fetcher-ops
#
# dbnomics-fetcher-ops is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# dbnomics-fetcher-ops is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from dataclasses import dataclass
from io import StringIO
from typing import Dict, Optional, Tuple

import daiquiri
import gitlab
import typer
from gitlab.v4.objects import VISIBILITY_PUBLIC, DeployKey, Project, ProjectPipelineSchedule
from gitlab.v4.objects.variables import Variable
from ruamel.yaml import YAML

from dbnomics_fetcher_ops.model import FetcherMetadata

from ..model import FetcherDef, ProjectRef, ScheduleDef
from ..ssh import generate_ssh_key_pair

logger = daiquiri.getLogger(__name__)

CI_JOBS_KEY = "CI jobs"
SSH_PRIVATE_KEY = "SSH_PRIVATE_KEY"


def configure_command(
    provider_slug: str,
    gitlab_url: str = typer.Option(..., envvar="GITLAB_URL", help="Base URL of GitLab instance"),
    gitlab_private_token: str = typer.Option(
        ..., envvar="GITLAB_PRIVATE_TOKEN", help="Private access token used to authenticate to GitLab API"
    ),
    debug_gitlab: bool = typer.Option(False, help="Show logging debug messages of Python GitLab"),
):
    """Configure a fetcher."""
    # Defer import to let the cli.callback function write the variable and avoid importing None.
    from ..app_args import app_args

    assert app_args is not None

    if provider_slug != provider_slug.lower():
        logger.error("Invalid PROVIDER_SLUG %r: must be lowercase", provider_slug)
        raise typer.Exit(1)

    fetcher_by_slug: Dict[str, FetcherDef] = {
        fetcher.provider_slug: fetcher for fetcher in app_args.fetcher_metadata.fetchers
    }

    fetcher_def: Optional[FetcherDef] = fetcher_by_slug.get(provider_slug)
    if fetcher_def is None:
        logger.error("Could not find any fetcher in fetchers.yml for provider %r, exit", provider_slug)
        raise typer.Exit(1)

    if fetcher_def.legacy_pipeline:
        logger.error(
            "Provider %r still declares `legacy_pipeline: true` in fetchers.yml, exit", provider_slug,
        )
        raise typer.Exit(1)

    # Create GitLab client.
    gitlab_url = gitlab_url.rstrip("/")
    gl = gitlab.Gitlab(gitlab_url, private_token=gitlab_private_token, api_version=4)
    gl.auth()
    if debug_gitlab:
        gl.enable_debug()

    ctx = Context(gitlab_url=gitlab_url, gl=gl, provider_slug=provider_slug)

    fetcher_project = load_fetcher_project(gl, app_args.fetcher_metadata, provider_slug)
    source_data_project = load_or_create_source_data_project(gl, app_args.fetcher_metadata, ctx)
    json_data_project = load_or_create_json_data_project(gl, app_args.fetcher_metadata, ctx)

    # Setup CI conf.
    ensure_ci_conf(fetcher_project, source_data_project, json_data_project, app_args.fetcher_metadata, ctx)
    setup_pipeline_schedules(fetcher_project, fetcher_def)
    ensure_ssh_key_pairs(fetcher_project, source_data_project, json_data_project, ctx)


@dataclass
class Context:
    gitlab_url: str
    gl: gitlab.Gitlab
    provider_slug: str


def load_fetcher_project(gl: gitlab.Gitlab, fetcher_metadata: FetcherMetadata, provider_slug: str) -> Project:
    fetcher_group_name, fetcher_project_name = resolve_project_ref(fetcher_metadata.gitlab.fetcher, provider_slug)
    project_name_with_namespace = f"{fetcher_group_name}/{fetcher_project_name}"
    try:
        fetcher_project = gl.projects.get(project_name_with_namespace)
    except gitlab.exceptions.GitlabGetError:
        logger.error(
            "Could not find project %r for fetcher source code of provider %r",
            project_name_with_namespace,
            provider_slug,
        )
        raise typer.Abort()
    return fetcher_project


def load_or_create_source_data_project(gl: gitlab.Gitlab, fetcher_metadata: FetcherMetadata, ctx: Context) -> Project:
    source_data_group_name, source_data_project_name = resolve_project_ref(
        fetcher_metadata.gitlab.source_data, ctx.provider_slug
    )
    try:
        source_data_project = gl.projects.get(f"{source_data_group_name}/{source_data_project_name}")
    except gitlab.exceptions.GitlabGetError:
        logger.info("Source data project does not exist, creating...")
        source_data_description = f"Source data as downloaded from provider {ctx.provider_slug}"
        source_data_project = create_project(
            source_data_group_name, source_data_project_name, source_data_description, ctx
        )
    return source_data_project


def load_or_create_json_data_project(gl: gitlab.Gitlab, fetcher_metadata: FetcherMetadata, ctx: Context) -> Project:

    json_data_group_name, json_data_project_name = resolve_project_ref(
        fetcher_metadata.gitlab.json_data, ctx.provider_slug
    )
    try:
        json_data_project = gl.projects.get(f"{json_data_group_name}/{json_data_project_name}")
    except gitlab.exceptions.GitlabGetError:
        logger.info("JSON data project does not exist, creating...")
        json_data_description = "Data following DBnomics data model, converted from provider data"
        json_data_project = create_project(json_data_group_name, json_data_project_name, json_data_description, ctx)
    return json_data_project


def resolve_project_ref(project_ref: ProjectRef, provider_slug: str) -> Tuple[str, str]:
    variables = {"PROVIDER_SLUG": provider_slug}
    group = project_ref.group
    name = project_ref.name
    for k, v in variables.items():
        group = group.replace("{" + k + "}", v)
        name = name.replace("{" + k + "}", v)
    return group, name


def get_deploy_key_title(ctx: Context):
    return f"{ctx.provider_slug} {CI_JOBS_KEY}"


def find_variable_by_name(project: Project, name: str) -> Optional[Variable]:
    try:
        return project.variables.get(name)
    except gitlab.exceptions.GitlabGetError:
        return None


def find_deploy_key_by_title(ctx: Context, title: str) -> Optional[DeployKey]:
    for key in ctx.gl.deploykeys.list(as_list=False):
        if key.title == title:
            return key
    return None


def find_project_deploy_key_by_title(project: Project, title: str) -> Optional[DeployKey]:
    for key in project.keys.list(as_list=False):
        if key.title == title:
            return key
    return None


def delete_env_variable(project: Project, name: str, ctx: Context):
    logger.info("Deleting environment variable %r of %r...", name, project.path_with_namespace)
    try:
        variable = project.variables.get(name)
    except gitlab.exceptions.GitlabGetError:
        logger.info("%r was not found in %r", name, project.path_with_namespace)
        return
    variable.delete()
    logger.info("%r deleted from %r", variable, project.path_with_namespace)


def delete_deploy_keys(project: Project, ctx: Context):
    logger.info("Deleting deploy keys of %r...", project.path_with_namespace)
    for key in project.keys.list(as_list=False):
        if key.title != get_deploy_key_title(ctx):
            logger.warning("%r ignored, title: %r", key, key.title)
            continue
        key.delete()
        logger.info("%r deleted from %r", key, project.path_with_namespace)
    else:
        logger.info("No deploy key found for %r", project.path_with_namespace)


def ensure_ssh_key_pairs(
    fetcher_project: Project, source_data_project: Project, json_data_project: Project, ctx: Context,
):
    """Checks that the SSH key pairs are configured, otherwise configure them.

    In particular ensure that the fetcher project has a SSH_PRIVATE_KEY masked variable,
    and that source-data and json-data projects have a deploy key.
    """
    ssh_private_key_variable = find_variable_by_name(fetcher_project, SSH_PRIVATE_KEY)
    deploy_key_title = get_deploy_key_title(ctx)
    source_data_deploy_key = find_project_deploy_key_by_title(source_data_project, deploy_key_title)
    json_data_deploy_key = find_project_deploy_key_by_title(json_data_project, deploy_key_title)
    if not ssh_private_key_variable or not source_data_deploy_key or not json_data_deploy_key:
        # Do some cleanup.
        delete_env_variable(fetcher_project, SSH_PRIVATE_KEY, ctx)
        delete_deploy_keys(source_data_project, ctx)
        delete_deploy_keys(json_data_project, ctx)

        # Generate a new SSH key pair, set private key to a fetcher project variable,
        # and create a deploy key from SSH public key used by both source-data
        # and json-data projects.
        ssh_public_key, ssh_private_key = generate_ssh_key_pair(ctx.provider_slug)
        fetcher_project.variables.create({"key": SSH_PRIVATE_KEY, "value": ssh_private_key})
        # Do not display private key value.
        logger.info("%r added to %r", SSH_PRIVATE_KEY, fetcher_project.path_with_namespace)
        deploy_key = source_data_project.keys.create(
            {"title": deploy_key_title, "key": ssh_public_key, "can_push": True}
        )
        logger.info("%r enabled for %r", deploy_key, source_data_project.path_with_namespace)
        json_data_project.keys.enable(deploy_key.id)
        json_data_project.keys.update(deploy_key.id, {"can_push": True})
        logger.info("%r enabled for %r", deploy_key, json_data_project.path_with_namespace)
    else:
        logger.info("SSH key pair is already configured for this fetcher")


def ensure_ci_conf(
    fetcher_project: Project,
    source_data_project: Project,
    json_data_project: Project,
    fetcher_metadata: FetcherMetadata,
    ctx: Context,
):
    """Configure a fetcher project to run a CI pipeline.

    Add a .gitlab-ci.yml if it does not exist, create it from a template in fetchers.yml,
    and add the PROVIDER_SLUG variable.
    """
    ensure_gitlab_ci_yml_exists(fetcher_project, fetcher_metadata, ctx)

    computed_variables = {
        "JSON_DATA_REMOTE_SSH_URL": json_data_project.ssh_url_to_repo,
        "SOURCE_DATA_REMOTE_SSH_URL": source_data_project.ssh_url_to_repo,
    }
    variables = computed_variables | fetcher_metadata.gitlab.fetcher.variables
    ensure_pipeline_variables_exist(fetcher_project, variables)


def ensure_gitlab_ci_yml_exists(project: Project, fetcher_metadata: FetcherMetadata, ctx: Context):
    def get_pipeline_content():
        template = fetcher_metadata.pipeline.template
        template["variables"] = {"PROVIDER_SLUG": ctx.provider_slug}
        template_io = StringIO()
        yaml = YAML(typ="safe")
        yaml.default_flow_style = False
        yaml.dump(template, template_io)
        return template_io.getvalue()

    try:
        gitlab_ci_file = project.files.get(file_path=".gitlab-ci.yml", ref="master")
    except gitlab.exceptions.GitlabGetError:
        logger.info("GitLab CI file not found, creating it from the shared pipeline template...")
        gitlab_ci_file = project.files.create(
            {
                "file_path": ".gitlab-ci.yml",
                "branch": "master",
                "content": get_pipeline_content(),
                "author_email": "dbnomics-fetcher-ops@localhost",
                "author_name": "dbnomics-fetcher-ops",
                "commit_message": "Add shared pipeline",
            }
        )
        logger.info(".gitlab-ci.yml file %r created in %r", gitlab_ci_file, project.path_with_namespace)
    else:
        logger.info(".gitlab-ci.yml found, doing nothing")


def ensure_pipeline_variables_exist(fetcher_project: Project, variables: dict):
    for k, v in variables.items():
        logger.info("Configuring variable %r for project %r", k, fetcher_project.path_with_namespace)
        variable = find_variable_by_name(fetcher_project, k)
        if variable is None:
            logger.info("Variable %r was not found, creating it", k)
            fetcher_project.variables.create({"key": k, "value": v})
        elif variable.value != v:
            logger.info("Variable %r was found with a different value, update it", k)
            variable.value = v
            variable.save()


def create_pipeline_schedule(project: Project, schedule_def: ScheduleDef) -> ProjectPipelineSchedule:
    schedule = project.pipelineschedules.create(
        {
            "active": True,
            "description": "Run fetcher",
            "ref": "master",
            "cron": schedule_def.cron,
            "cron_timezone": schedule_def.timezone,
        }
    )
    logger.info("%r created for %r", schedule, project.path_with_namespace)
    return schedule


def setup_pipeline_schedules(project: Project, fetcher_def: FetcherDef):
    logger.info("Deleting all pipeline schedules of project %r...", project.path_with_namespace)
    for schedule in project.pipelineschedules.list(as_list=False):
        schedule.delete()

    logger.info("Configuring pipeline schedules for project %r...", project.path_with_namespace)
    for schedule_def in fetcher_def.schedules:
        create_pipeline_schedule(project, schedule_def)


def create_project(group_name: str, project_name: str, description: str, ctx: Context):
    gl = ctx.gl
    groups = gl.groups.list(search=group_name)
    assert len(groups) == 1, groups
    group = groups[0]

    project = gl.projects.create(
        {"name": project_name, "namespace_id": group.id, "description": description, "visibility": VISIBILITY_PUBLIC}
    )
    logger.info("Project created: %r", project.path_with_namespace)
    return project
