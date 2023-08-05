import json

import click

from .cloudformation import CloudFormation
from pygments import highlight
from pygments.lexers import JsonLexer, BashLexer
from pygments.formatters import TerminalFormatter

@click.group()
@click.option("--debug/--no-debug", default=False)
@click.option("--region", default="eu-west-2")
@click.pass_context
def cli(ctx, debug, region):
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    ctx.obj['AWS_REGION'] = region


@click.option("--stack-prefix", required=True, help="The cloudformation stack prefix")
@click.option("--stack-name", required=False, help="Filter by stack name", default=None)
@click.option("--output-format", required=False, default="parameter_file", type=click.Choice(['parameter_file', 'cli_string']))
@click.argument('output_file', required=False, type=click.File('wb'), default=False)
@cli.command()
@click.pass_context
def exports_to_parameters(ctx, stack_prefix, stack_name, output_format, output_file):
    cf = CloudFormation(region = ctx.obj['AWS_REGION'])
    parameters = cf.exports_to_parameters(stack_prefix, stack_name)
    parameter_string = bytes(json.dumps(parameters, indent=2), "UTF-8")
    if output_format == "parameter_file":
        output_file.write(parameter_string)
    elif output_format == 'cli_string':
        cli_string = ",".join(["%s-%s" % (p['Name'],p['Value']) for p in parameters])
        click.echo(highlight(cli_string, BashLexer(), TerminalFormatter()))

if __name__ == "__main__":
    cli()
