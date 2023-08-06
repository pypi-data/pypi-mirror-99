import os, sys
import click
import json
from services import ConfluenceService

verifyssl = False


@click.group()
@click.pass_context
def releaseNote(ctx):

    context_parent = click.get_current_context(silent=True)
    ctx.ensure_object(dict)
    ctx.obj['bitbucket_url'] = context_parent.obj["bitbucket_url"]
    ctx.obj['jira_url'] = context_parent.obj["jira_url"]
    ctx.obj['confluence_url'] = context_parent.obj["confluence_url"]
    ctx.obj['username'] = context_parent.obj["username"]
    ctx.obj['password'] = context_parent.obj["password"]
    verifyssl = context_parent.obj["verifyssl"]
    pass


@releaseNote.command()
@click.pass_context
@click.option('-v', '--version', required=True, default="", help="Release/Product version")
@click.option('-s', '--space-key', required=True, default="", help="Space key for the Confluence space")
@click.option('-j', '--project-key', required=True, default="", help="Project key used in your Jira project")
@click.option('-i', '--parent-page-id', required=True, default="", help="Id of the page under which you will create your changelogs")
@click.option('-t', '--template-file', required=True, default="", help="Path to the template file for your changelog")
@click.option('--dry-run/--no-dry-run', required=False, default=False, help="Dry run for testing")
def generate(ctx, version, space_key, project_key, parent_page_id, template_file, dry_run):
    """Creates a release note one on Confluence"""
    version = version.strip()
    project_key = project_key.strip()
    space_key = space_key.strip()
    parent_page_id = parent_page_id.strip()
    template_file = template_file.strip()

    confluence_service = ConfluenceService(
        ctx.obj['confluence_url'], ctx.obj['jira_url'], ctx.obj['bitbucket_url'], ctx.obj['username'], ctx.obj['password'], ctx.obj['verifyssl'])
    tupleResult = confluence_service.generate_releasenote(
        project_key, version, template_file)

    releasenote = tupleResult[0]
    start_date = tupleResult[1]
    release_date = tupleResult[2]

    if releasenote is not None:
        if not dry_run:
            if space_key is not None or parent_page_id is not None:
                confluence_service.push_releasenote(
                    space_key, version, start_date, release_date,parent_page_id, releasenote)

            else:                
                sys.exit("ERROR: Page already exist or missing argument.")
        else:
            print("This was a dry-run test")
    else:        
        sys.exit("ERROR: Provided version not found. Please check the arguments passed.")