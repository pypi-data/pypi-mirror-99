from .exceptions import UserError

__all__ = ['check_package_version']

def check_package_version(PKG: str, min_version: str):
    pip_version = "?"
    try:
        # noinspection PyCompatibility
        from pip import __version__

        pip_version = __version__
        # noinspection PyCompatibility
        from pip._internal.utils.misc import get_installed_distributions
    except ImportError:
        msg = f"""
           You need a higher version of "pip".  You have {pip_version}

           You can install it with a command like:

               pip install -U pip

           (Note: your configuration might require a different command.)
           """
        raise UserError(msg)

    installed = get_installed_distributions()
    pkgs = {_.project_name: _ for _ in installed}
    if PKG not in pkgs:
        msg = f"""
        You need to have an extra package installed called `{PKG}`.

        You can install it with a command like:

            pip3 install -U "{PKG}>={min_version}"

        (Note: your configuration might require a different command.
         You might need to use "pip" instead of "pip3".)
        """
        raise UserError(msg)

    p = pkgs[PKG]

    installed_version = parse_version(p.version)
    required_version = parse_version(min_version)
    if installed_version < required_version:
        msg = f"""
       You need to have installed {PKG} of at least {min_version}.
       We have detected you have {p.version}.

       Please update {PKG} using pip.

           pip3 install -U  "{PKG}>={min_version}"

       (Note: your configuration might require a different command.
        You might need to use "pip" instead of "pip3".)
       """
        raise UserError(msg)


def parse_version(x):
    return tuple(int(_) for _ in x.split("."))
