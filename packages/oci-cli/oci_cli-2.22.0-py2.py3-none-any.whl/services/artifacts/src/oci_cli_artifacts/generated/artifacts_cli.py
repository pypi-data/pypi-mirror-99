# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from __future__ import print_function
import click
import oci  # noqa: F401
import six  # noqa: F401
import sys  # noqa: F401
from oci_cli.cli_root import cli
from oci_cli import cli_constants  # noqa: F401
from oci_cli import cli_util
from oci_cli import json_skeleton_utils
from oci_cli import custom_types  # noqa: F401
from oci_cli.aliasing import CommandGroupWithAlias


@cli.command(cli_util.override('artifacts.artifacts_root_group.command_name', 'artifacts'), cls=CommandGroupWithAlias, help=cli_util.override('artifacts.artifacts_root_group.help', """API covering the [Registry] services.
Use this API to manage resources such as container images and repositories."""), short_help=cli_util.override('artifacts.artifacts_root_group.short_help', """Container Images API"""))
@cli_util.help_option_group
def artifacts_root_group():
    pass


@click.command(cli_util.override('artifacts.container_image_summary_group.command_name', 'container-image-summary'), cls=CommandGroupWithAlias, help="""Container image summary.""")
@cli_util.help_option_group
def container_image_summary_group():
    pass


@click.command(cli_util.override('artifacts.container_configuration_group.command_name', 'container-configuration'), cls=CommandGroupWithAlias, help="""Container configuration.""")
@cli_util.help_option_group
def container_configuration_group():
    pass


@click.command(cli_util.override('artifacts.container_repository_group.command_name', 'container-repository'), cls=CommandGroupWithAlias, help="""Container repository metadata.""")
@cli_util.help_option_group
def container_repository_group():
    pass


@click.command(cli_util.override('artifacts.container_image_group.command_name', 'container-image'), cls=CommandGroupWithAlias, help="""Container image metadata.""")
@cli_util.help_option_group
def container_image_group():
    pass


artifacts_root_group.add_command(container_image_summary_group)
artifacts_root_group.add_command(container_configuration_group)
artifacts_root_group.add_command(container_repository_group)
artifacts_root_group.add_command(container_image_group)


@container_repository_group.command(name=cli_util.override('artifacts.change_container_repository_compartment.command_name', 'change-compartment'), help=u"""Moves a container repository into a different compartment within the same tenancy. For information about moving resources between compartments, see [Moving Resources to a Different Compartment]. \n[Command Reference](changeContainerRepositoryCompartment)""")
@cli_util.option('--repository-id', required=True, help=u"""The [OCID] of the container repository.

Example: `ocid1.containerrepo.oc1..exampleuniqueID`""")
@cli_util.option('--compartment-id', required=True, help=u"""The [OCID] of the compartment into which to move the resource.""")
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `if-match` parameter to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def change_container_repository_compartment(ctx, from_json, repository_id, compartment_id, if_match):

    if isinstance(repository_id, six.string_types) and len(repository_id.strip()) == 0:
        raise click.UsageError('Parameter --repository-id cannot be whitespace or empty string')

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    _details = {}
    _details['compartmentId'] = compartment_id

    client = cli_util.build_client('artifacts', 'artifacts', ctx)
    result = client.change_container_repository_compartment(
        repository_id=repository_id,
        change_container_repository_compartment_details=_details,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@container_repository_group.command(name=cli_util.override('artifacts.create_container_repository.command_name', 'create'), help=u"""Create a new empty container repository. Avoid entering confidential information. \n[Command Reference](createContainerRepository)""")
@cli_util.option('--compartment-id', required=True, help=u"""The [OCID] of the compartment in which to create the resource.""")
@cli_util.option('--display-name', required=True, help=u"""The container repository name.""")
@cli_util.option('--is-immutable', type=click.BOOL, help=u"""Whether the repository is immutable. Images cannot be overwritten in an immutable repository.""")
@cli_util.option('--is-public', type=click.BOOL, help=u"""Whether the repository is public. A public repository allows unauthenticated access.""")
@cli_util.option('--readme', type=custom_types.CLI_COMPLEX_TYPE, help=u"""""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["AVAILABLE", "DELETING", "DELETED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({'readme': {'module': 'artifacts', 'class': 'ContainerRepositoryReadme'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'readme': {'module': 'artifacts', 'class': 'ContainerRepositoryReadme'}}, output_type={'module': 'artifacts', 'class': 'ContainerRepository'})
@cli_util.wrap_exceptions
def create_container_repository(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, compartment_id, display_name, is_immutable, is_public, readme):

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    _details = {}
    _details['compartmentId'] = compartment_id
    _details['displayName'] = display_name

    if is_immutable is not None:
        _details['isImmutable'] = is_immutable

    if is_public is not None:
        _details['isPublic'] = is_public

    if readme is not None:
        _details['readme'] = cli_util.parse_json_parameter("readme", readme)

    client = cli_util.build_client('artifacts', 'artifacts', ctx)
    result = client.create_container_repository(
        create_container_repository_details=_details,
        **kwargs
    )
    if wait_for_state:

        if hasattr(client, 'get_container_repository') and callable(getattr(client, 'get_container_repository')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_container_repository(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@container_image_group.command(name=cli_util.override('artifacts.delete_container_image.command_name', 'delete'), help=u"""Delete a container image. \n[Command Reference](deleteContainerImage)""")
@cli_util.option('--image-id', required=True, help=u"""The [OCID] of the container image.

Example: `ocid1.containerimage.oc1..exampleuniqueID`""")
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `if-match` parameter to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@cli_util.confirm_delete_option
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["AVAILABLE", "DELETED", "DELETING"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def delete_container_image(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, image_id, if_match):

    if isinstance(image_id, six.string_types) and len(image_id.strip()) == 0:
        raise click.UsageError('Parameter --image-id cannot be whitespace or empty string')

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('artifacts', 'artifacts', ctx)
    result = client.delete_container_image(
        image_id=image_id,
        **kwargs
    )
    if wait_for_state:

        if hasattr(client, 'get_container_image') and callable(getattr(client, 'get_container_image')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                oci.wait_until(client, client.get_container_image(image_id), 'lifecycle_state', wait_for_state, succeed_on_not_found=True, **wait_period_kwargs)
            except oci.exceptions.ServiceError as e:
                # We make an initial service call so we can pass the result to oci.wait_until(), however if we are waiting on the
                # outcome of a delete operation it is possible that the resource is already gone and so the initial service call
                # will result in an exception that reflects a HTTP 404. In this case, we can exit with success (rather than raising
                # the exception) since this would have been the behaviour in the waiter anyway (as for delete we provide the argument
                # succeed_on_not_found=True to the waiter).
                #
                # Any non-404 should still result in the exception being thrown.
                if e.status == 404:
                    pass
                else:
                    raise
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Please retrieve the resource to find its current state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@container_repository_group.command(name=cli_util.override('artifacts.delete_container_repository.command_name', 'delete'), help=u"""Delete container repository. \n[Command Reference](deleteContainerRepository)""")
@cli_util.option('--repository-id', required=True, help=u"""The [OCID] of the container repository.

Example: `ocid1.containerrepo.oc1..exampleuniqueID`""")
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `if-match` parameter to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@cli_util.confirm_delete_option
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["AVAILABLE", "DELETING", "DELETED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def delete_container_repository(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, repository_id, if_match):

    if isinstance(repository_id, six.string_types) and len(repository_id.strip()) == 0:
        raise click.UsageError('Parameter --repository-id cannot be whitespace or empty string')

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('artifacts', 'artifacts', ctx)
    result = client.delete_container_repository(
        repository_id=repository_id,
        **kwargs
    )
    if wait_for_state:

        if hasattr(client, 'get_container_repository') and callable(getattr(client, 'get_container_repository')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                oci.wait_until(client, client.get_container_repository(repository_id), 'lifecycle_state', wait_for_state, succeed_on_not_found=True, **wait_period_kwargs)
            except oci.exceptions.ServiceError as e:
                # We make an initial service call so we can pass the result to oci.wait_until(), however if we are waiting on the
                # outcome of a delete operation it is possible that the resource is already gone and so the initial service call
                # will result in an exception that reflects a HTTP 404. In this case, we can exit with success (rather than raising
                # the exception) since this would have been the behaviour in the waiter anyway (as for delete we provide the argument
                # succeed_on_not_found=True to the waiter).
                #
                # Any non-404 should still result in the exception being thrown.
                if e.status == 404:
                    pass
                else:
                    raise
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Please retrieve the resource to find its current state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@container_configuration_group.command(name=cli_util.override('artifacts.get_container_configuration.command_name', 'get'), help=u"""Get container configuration. \n[Command Reference](getContainerConfiguration)""")
@cli_util.option('--compartment-id', required=True, help=u"""The [OCID] of the compartment.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'artifacts', 'class': 'ContainerConfiguration'})
@cli_util.wrap_exceptions
def get_container_configuration(ctx, from_json, compartment_id):

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('artifacts', 'artifacts', ctx)
    result = client.get_container_configuration(
        compartment_id=compartment_id,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@container_image_group.command(name=cli_util.override('artifacts.get_container_image.command_name', 'get'), help=u"""Get container image metadata. \n[Command Reference](getContainerImage)""")
@cli_util.option('--image-id', required=True, help=u"""The [OCID] of the container image.

Example: `ocid1.containerimage.oc1..exampleuniqueID`""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'artifacts', 'class': 'ContainerImage'})
@cli_util.wrap_exceptions
def get_container_image(ctx, from_json, image_id):

    if isinstance(image_id, six.string_types) and len(image_id.strip()) == 0:
        raise click.UsageError('Parameter --image-id cannot be whitespace or empty string')

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('artifacts', 'artifacts', ctx)
    result = client.get_container_image(
        image_id=image_id,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@container_repository_group.command(name=cli_util.override('artifacts.get_container_repository.command_name', 'get'), help=u"""Get container repository. \n[Command Reference](getContainerRepository)""")
@cli_util.option('--repository-id', required=True, help=u"""The [OCID] of the container repository.

Example: `ocid1.containerrepo.oc1..exampleuniqueID`""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'artifacts', 'class': 'ContainerRepository'})
@cli_util.wrap_exceptions
def get_container_repository(ctx, from_json, repository_id):

    if isinstance(repository_id, six.string_types) and len(repository_id.strip()) == 0:
        raise click.UsageError('Parameter --repository-id cannot be whitespace or empty string')

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('artifacts', 'artifacts', ctx)
    result = client.get_container_repository(
        repository_id=repository_id,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@container_image_summary_group.command(name=cli_util.override('artifacts.list_container_images.command_name', 'list-container-images'), help=u"""List container images in a compartment. \n[Command Reference](listContainerImages)""")
@cli_util.option('--compartment-id', required=True, help=u"""The [OCID] of the compartment.""")
@cli_util.option('--compartment-id-in-subtree', type=click.BOOL, help=u"""When set to true, the hierarchy of compartments is traversed and all compartments and subcompartments in the tenancy are inspected depending on the the setting of `accessLevel`. Default is false. Can only be set to true when calling the API on the tenancy (root compartment).""")
@cli_util.option('--display-name', help=u"""A filter to return only resources that match the given display name exactly.""")
@cli_util.option('--image-id', help=u"""A filter to return a container image summary only for the specified container image OCID.""")
@cli_util.option('--is-versioned', type=click.BOOL, help=u"""A filter to return container images based on whether there are any associated versions.""")
@cli_util.option('--repository-id', help=u"""A filter to return container images only for the specified container repository OCID.""")
@cli_util.option('--repository-name', help=u"""A filter to return container images or container image signatures that match the repository name.

Example: `foo` or `foo*`""")
@cli_util.option('--version-parameterconflict', help=u"""A filter to return container images that match the version.

Example: `foo` or `foo*`""")
@cli_util.option('--lifecycle-state', help=u"""A filter to return only resources that match the given lifecycle state name exactly.""")
@cli_util.option('--limit', type=click.INT, help=u"""For list pagination. The maximum number of results per page, or items to return in a paginated \"List\" call. For important details about how pagination works, see [List Pagination].

Example: `50`""")
@cli_util.option('--page', help=u"""For list pagination. The value of the `opc-next-page` response header from the previous \"List\" call. For important details about how pagination works, see [List Pagination].""")
@cli_util.option('--sort-by', type=custom_types.CliCaseInsensitiveChoice(["TIMECREATED", "DISPLAYNAME"]), help=u"""The field to sort by. You can provide one sort order (`sortOrder`). Default order for TIMECREATED is descending. Default order for DISPLAYNAME is ascending. The DISPLAYNAME sort order is case sensitive.

**Note:** In general, some \"List\" operations (for example, `ListInstances`) let you optionally filter by availability domain if the scope of the resource type is within a single availability domain. If you call one of these \"List\" operations without specifying an availability domain, the resources are grouped by availability domain, then sorted.""")
@cli_util.option('--sort-order', type=custom_types.CliCaseInsensitiveChoice(["ASC", "DESC"]), help=u"""The sort order to use, either ascending (`ASC`) or descending (`DESC`). The DISPLAYNAME sort order is case sensitive.""")
@cli_util.option('--all', 'all_pages', is_flag=True, help="""Fetches all pages of results. If you provide this option, then you cannot provide the --limit option.""")
@cli_util.option('--page-size', type=click.INT, help="""When fetching results, the number of results to fetch per call. Only valid when used with --all or --limit, and ignored otherwise.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'artifacts', 'class': 'ContainerImageCollection'})
@cli_util.wrap_exceptions
def list_container_images(ctx, from_json, all_pages, page_size, compartment_id, compartment_id_in_subtree, display_name, image_id, is_versioned, repository_id, repository_name, version_parameterconflict, lifecycle_state, limit, page, sort_by, sort_order):

    if all_pages and limit:
        raise click.UsageError('If you provide the --all option you cannot provide the --limit option')

    kwargs = {}
    if compartment_id_in_subtree is not None:
        kwargs['compartment_id_in_subtree'] = compartment_id_in_subtree
    if display_name is not None:
        kwargs['display_name'] = display_name
    if image_id is not None:
        kwargs['image_id'] = image_id
    if is_versioned is not None:
        kwargs['is_versioned'] = is_versioned
    if repository_id is not None:
        kwargs['repository_id'] = repository_id
    if repository_name is not None:
        kwargs['repository_name'] = repository_name
    if version_parameterconflict is not None:
        kwargs['version'] = version_parameterconflict
    if lifecycle_state is not None:
        kwargs['lifecycle_state'] = lifecycle_state
    if limit is not None:
        kwargs['limit'] = limit
    if page is not None:
        kwargs['page'] = page
    if sort_by is not None:
        kwargs['sort_by'] = sort_by
    if sort_order is not None:
        kwargs['sort_order'] = sort_order
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('artifacts', 'artifacts', ctx)
    if all_pages:
        if page_size:
            kwargs['limit'] = page_size

        result = cli_util.list_call_get_all_results(
            client.list_container_images,
            compartment_id=compartment_id,
            **kwargs
        )
    elif limit is not None:
        result = cli_util.list_call_get_up_to_limit(
            client.list_container_images,
            limit,
            page_size,
            compartment_id=compartment_id,
            **kwargs
        )
    else:
        result = client.list_container_images(
            compartment_id=compartment_id,
            **kwargs
        )
    cli_util.render_response(result, ctx)


@container_repository_group.command(name=cli_util.override('artifacts.list_container_repositories.command_name', 'list'), help=u"""List container repositories in a compartment. \n[Command Reference](listContainerRepositories)""")
@cli_util.option('--compartment-id', required=True, help=u"""The [OCID] of the compartment.""")
@cli_util.option('--compartment-id-in-subtree', type=click.BOOL, help=u"""When set to true, the hierarchy of compartments is traversed and all compartments and subcompartments in the tenancy are inspected depending on the the setting of `accessLevel`. Default is false. Can only be set to true when calling the API on the tenancy (root compartment).""")
@cli_util.option('--repository-id', help=u"""A filter to return container images only for the specified container repository OCID.""")
@cli_util.option('--display-name', help=u"""A filter to return only resources that match the given display name exactly.""")
@cli_util.option('--is-public', type=click.BOOL, help=u"""A filter to return resources that match the isPublic value.""")
@cli_util.option('--lifecycle-state', help=u"""A filter to return only resources that match the given lifecycle state name exactly.""")
@cli_util.option('--limit', type=click.INT, help=u"""For list pagination. The maximum number of results per page, or items to return in a paginated \"List\" call. For important details about how pagination works, see [List Pagination].

Example: `50`""")
@cli_util.option('--page', help=u"""For list pagination. The value of the `opc-next-page` response header from the previous \"List\" call. For important details about how pagination works, see [List Pagination].""")
@cli_util.option('--sort-by', type=custom_types.CliCaseInsensitiveChoice(["TIMECREATED", "DISPLAYNAME"]), help=u"""The field to sort by. You can provide one sort order (`sortOrder`). Default order for TIMECREATED is descending. Default order for DISPLAYNAME is ascending. The DISPLAYNAME sort order is case sensitive.

**Note:** In general, some \"List\" operations (for example, `ListInstances`) let you optionally filter by availability domain if the scope of the resource type is within a single availability domain. If you call one of these \"List\" operations without specifying an availability domain, the resources are grouped by availability domain, then sorted.""")
@cli_util.option('--sort-order', type=custom_types.CliCaseInsensitiveChoice(["ASC", "DESC"]), help=u"""The sort order to use, either ascending (`ASC`) or descending (`DESC`). The DISPLAYNAME sort order is case sensitive.""")
@cli_util.option('--all', 'all_pages', is_flag=True, help="""Fetches all pages of results. If you provide this option, then you cannot provide the --limit option.""")
@cli_util.option('--page-size', type=click.INT, help="""When fetching results, the number of results to fetch per call. Only valid when used with --all or --limit, and ignored otherwise.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'artifacts', 'class': 'ContainerRepositoryCollection'})
@cli_util.wrap_exceptions
def list_container_repositories(ctx, from_json, all_pages, page_size, compartment_id, compartment_id_in_subtree, repository_id, display_name, is_public, lifecycle_state, limit, page, sort_by, sort_order):

    if all_pages and limit:
        raise click.UsageError('If you provide the --all option you cannot provide the --limit option')

    kwargs = {}
    if compartment_id_in_subtree is not None:
        kwargs['compartment_id_in_subtree'] = compartment_id_in_subtree
    if repository_id is not None:
        kwargs['repository_id'] = repository_id
    if display_name is not None:
        kwargs['display_name'] = display_name
    if is_public is not None:
        kwargs['is_public'] = is_public
    if lifecycle_state is not None:
        kwargs['lifecycle_state'] = lifecycle_state
    if limit is not None:
        kwargs['limit'] = limit
    if page is not None:
        kwargs['page'] = page
    if sort_by is not None:
        kwargs['sort_by'] = sort_by
    if sort_order is not None:
        kwargs['sort_order'] = sort_order
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('artifacts', 'artifacts', ctx)
    if all_pages:
        if page_size:
            kwargs['limit'] = page_size

        result = cli_util.list_call_get_all_results(
            client.list_container_repositories,
            compartment_id=compartment_id,
            **kwargs
        )
    elif limit is not None:
        result = cli_util.list_call_get_up_to_limit(
            client.list_container_repositories,
            limit,
            page_size,
            compartment_id=compartment_id,
            **kwargs
        )
    else:
        result = client.list_container_repositories(
            compartment_id=compartment_id,
            **kwargs
        )
    cli_util.render_response(result, ctx)


@container_image_group.command(name=cli_util.override('artifacts.remove_container_version.command_name', 'remove'), help=u"""Remove version from container image. \n[Command Reference](removeContainerVersion)""")
@cli_util.option('--image-id', required=True, help=u"""The [OCID] of the container image.

Example: `ocid1.containerimage.oc1..exampleuniqueID`""")
@cli_util.option('--version-parameterconflict', required=True, help=u"""The version to remove.""")
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `if-match` parameter to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["AVAILABLE", "DELETED", "DELETING"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'artifacts', 'class': 'ContainerImage'})
@cli_util.wrap_exceptions
def remove_container_version(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, image_id, version_parameterconflict, if_match):

    if isinstance(image_id, six.string_types) and len(image_id.strip()) == 0:
        raise click.UsageError('Parameter --image-id cannot be whitespace or empty string')

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    _details = {}
    _details['version'] = version_parameterconflict

    client = cli_util.build_client('artifacts', 'artifacts', ctx)
    result = client.remove_container_version(
        image_id=image_id,
        remove_container_version_details=_details,
        **kwargs
    )
    if wait_for_state:

        if hasattr(client, 'get_container_image') and callable(getattr(client, 'get_container_image')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_container_image(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@container_image_group.command(name=cli_util.override('artifacts.restore_container_image.command_name', 'restore'), help=u"""Restore a container image. \n[Command Reference](restoreContainerImage)""")
@cli_util.option('--image-id', required=True, help=u"""The [OCID] of the container image.

Example: `ocid1.containerimage.oc1..exampleuniqueID`""")
@cli_util.option('--version-parameterconflict', help=u"""Optional version to associate with image.""")
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `if-match` parameter to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["AVAILABLE", "DELETED", "DELETING"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'artifacts', 'class': 'ContainerImage'})
@cli_util.wrap_exceptions
def restore_container_image(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, image_id, version_parameterconflict, if_match):

    if isinstance(image_id, six.string_types) and len(image_id.strip()) == 0:
        raise click.UsageError('Parameter --image-id cannot be whitespace or empty string')

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    _details = {}

    if version_parameterconflict is not None:
        _details['version'] = version_parameterconflict

    client = cli_util.build_client('artifacts', 'artifacts', ctx)
    result = client.restore_container_image(
        image_id=image_id,
        restore_container_image_details=_details,
        **kwargs
    )
    if wait_for_state:

        if hasattr(client, 'get_container_image') and callable(getattr(client, 'get_container_image')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_container_image(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@container_configuration_group.command(name=cli_util.override('artifacts.update_container_configuration.command_name', 'update'), help=u"""Update container configuration. \n[Command Reference](updateContainerConfiguration)""")
@cli_util.option('--compartment-id', required=True, help=u"""The [OCID] of the compartment.""")
@cli_util.option('--is-repository-created-on-first-push', type=click.BOOL, help=u"""Whether to create a new container repository when a container is pushed to a new repository path. Repositories created in this way belong to the root compartment.""")
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `if-match` parameter to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'artifacts', 'class': 'ContainerConfiguration'})
@cli_util.wrap_exceptions
def update_container_configuration(ctx, from_json, compartment_id, is_repository_created_on_first_push, if_match):

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    _details = {}

    if is_repository_created_on_first_push is not None:
        _details['isRepositoryCreatedOnFirstPush'] = is_repository_created_on_first_push

    client = cli_util.build_client('artifacts', 'artifacts', ctx)
    result = client.update_container_configuration(
        compartment_id=compartment_id,
        update_container_configuration_details=_details,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@container_repository_group.command(name=cli_util.override('artifacts.update_container_repository.command_name', 'update'), help=u"""Modify the properties of a container repository. Avoid entering confidential information. \n[Command Reference](updateContainerRepository)""")
@cli_util.option('--repository-id', required=True, help=u"""The [OCID] of the container repository.

Example: `ocid1.containerrepo.oc1..exampleuniqueID`""")
@cli_util.option('--is-immutable', type=click.BOOL, help=u"""Whether the repository is immutable. Images cannot be overwritten in an immutable repository.""")
@cli_util.option('--is-public', type=click.BOOL, help=u"""Whether the repository is public. A public repository allows unauthenticated access.""")
@cli_util.option('--readme', type=custom_types.CLI_COMPLEX_TYPE, help=u"""""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `if-match` parameter to the value of the etag from a previous GET or POST response for that resource. The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@cli_util.option('--force', help="""Perform update without prompting for confirmation.""", is_flag=True)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["AVAILABLE", "DELETING", "DELETED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({'readme': {'module': 'artifacts', 'class': 'ContainerRepositoryReadme'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'readme': {'module': 'artifacts', 'class': 'ContainerRepositoryReadme'}}, output_type={'module': 'artifacts', 'class': 'ContainerRepository'})
@cli_util.wrap_exceptions
def update_container_repository(ctx, from_json, force, wait_for_state, max_wait_seconds, wait_interval_seconds, repository_id, is_immutable, is_public, readme, if_match):

    if isinstance(repository_id, six.string_types) and len(repository_id.strip()) == 0:
        raise click.UsageError('Parameter --repository-id cannot be whitespace or empty string')
    if not force:
        if readme:
            if not click.confirm("WARNING: Updates to readme will replace any existing values. Are you sure you want to continue?"):
                ctx.abort()

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    _details = {}

    if is_immutable is not None:
        _details['isImmutable'] = is_immutable

    if is_public is not None:
        _details['isPublic'] = is_public

    if readme is not None:
        _details['readme'] = cli_util.parse_json_parameter("readme", readme)

    client = cli_util.build_client('artifacts', 'artifacts', ctx)
    result = client.update_container_repository(
        repository_id=repository_id,
        update_container_repository_details=_details,
        **kwargs
    )
    if wait_for_state:

        if hasattr(client, 'get_container_repository') and callable(getattr(client, 'get_container_repository')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_container_repository(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)
