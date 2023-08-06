import os

from pydantic import ValidationError

from ...repository import PackageVersion

try:
    import click
    from click_plugins import with_plugins
except ImportError:
    raise ImportError(
        'click modules not installed. Try `pip install queenbee[cli]` command.'
    )


@click.command('package')
@click.argument('path', type=click.Path(exists=True))
@click.option('-d', '--destination', help='location to write the package', show_default=True, default='.', type=click.Path(exists=False))
@click.option('-f', '--force', help='Boolean toggle to overwrite existing package with same name and version', default=False, type=bool, is_flag=True)
def package(path, destination, force):
    """package a plugin

    This command helps your package plugins and add them to repository folders. A
    packaged plugin is essentially a gzipped version of its folder.

    You can package a plugin in a specific folder or repository by using the
    ``--destination``

    flag::

        queenbee plugin package path/to/my/plugin --destination path/to/my/repository/plugins

    If you do not specify a ``--destination`` the command will package the plugin in the
    directory the command is invoked from (ie: ``.``)
    """
    path = os.path.abspath(path)
    destination = os.path.abspath(destination)
    os.chdir(path)

    try:
        plugin_version, file_object = PackageVersion.package_folder(
            resource_type='plugin',
            folder_path=path,
        )
    except ValidationError as error:
        raise click.ClickException(error)
    except FileNotFoundError as error:
        raise click.ClickException(error)
    except ValueError as error:
        raise click.ClickException(error)

    file_path = os.path.join(destination, plugin_version.url)

    if not force and os.path.isfile(file_path):
        raise click.ClickException(
            f'File already exists at path {file_path}. Use -f to overwrite it.')

    with open(file_path, 'wb') as f:
        file_object.seek(0)
        f.write(file_object.read())
