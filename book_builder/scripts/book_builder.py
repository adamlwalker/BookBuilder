# The driver script for the main program
import os
import click
import book_builder.config as config
import book_builder.util as util
import book_builder.examples as examples
import book_builder.packages as _packages
import book_builder.validate as _validate
import book_builder.fix as _fix
import book_builder.epub as _epub


@click.group()
@click.version_option()
def cli():
    """Book Builder

    Provides all book building and testing utilities under a single central command.
    """


##########################################################


@cli.group()
def code():
    """Code extraction and testing."""


@code.command('clean')
def code_clean():
    "Remove directory containing extracted example code"
    click.echo(examples.clean())


@code.command('extract')
def code_extract():
    "Extract examples from book's Markdown files"
    click.echo(examples.extractExamples())
    if config.language_name == "kotlin":
        click.echo(examples.create_test_files())
        click.echo(examples.create_tasks_for_gradle())


@code.command('testall')
def code_test_all_examples():
    "Compile and capture all results, to show percentage of rewritten examples"
    click.echo(examples.compile_all_examples())


@code.command('testfiles')
def code_test_files():
    "Create test.bat files for each package, to compile and run all files"
    click.echo(examples.create_test_files())


##########################################################


@cli.group()
def packages():
    """Discover and fix package issues"""


@packages.command('unpackaged')
def packages_unpackaged():
    "Show all examples that aren't in packages"
    click.echo(_packages.unpackaged())


# @packages.command('add')
# def packages_add_packages():
#     "Add package statements to all examples that don't have them"
#     click.echo(_packages.add_packages())

##########################################################


@cli.command()
def validate():
    "Validation tests"
    click.echo(_validate.all_checks())


##########################################################


@cli.command()
def fix():
    "Batch fixes"
    click.echo(_fix.all_fixes())


##########################################################

@cli.group()
def epub():
    "Creates epub"


@epub.command('clean')
def epub_clean():
    "Remove directory containing epub"
    click.echo(util.clean(config.ebook_build_dir))


@epub.command('combine')
def epub_combine():
    "Combine Markdown files into a single file"
    click.echo(_epub.combine_markdown_files())
    os.system("subl {}".format(config.combined_markdown))


@epub.command('disassemble')
@click.option('--test', is_flag=True, help='Unpack to "test" directory instead of overwriting Markdown.')
def epub_disassemble(test):
    "Split combined Markdown file into atom-numbered markdown files"
    if test:
        if config.test_dir.exists():
            click.echo(util.clean(config.test_dir))
        click.echo(_epub.disassemble_combined_markdown_file(config.test_dir))
    else:
        click.echo(_epub.disassemble_combined_markdown_file())


# @epub.command('newStatus')
def epub_create_new_status_file():
    "Create fresh STATUS.md if one doesn't exist"
    click.echo(util.create_new_status_file())
