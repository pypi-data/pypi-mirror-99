#!/usr/bin/env python
import distutils.core
import jinja2 as jj

__version__ = "0.1.1"

def template(tstr, docstr, setup, add=dict()):
    """
    Read a template from the file and replace the variables.
    docstr is the docstring consisting of:
      0th line: ignored
      1st line: a brief explanation.
      2nd..   : Usage of the module.
    setup is the content of setup.py, given by
      setup = distutils.core.run_setup("setup.py")

    Returns a jinja2 object.
    """
    genice_link="[GenIce2](https://github.com/vitroid/GenIce)"

    lines = docstr.splitlines()

    d = {
        "usage"   : "\n".join(lines[2:]),
        "summary" : lines[1].replace("GenIce2", genice_link),
        "version" : setup.get_version(),
        "package" : setup.get_name(),
        "base"    : setup.get_name().replace("-", "_"),
        "url"     : setup.get_url(),
        "genice"  : genice_link,
        "requires": setup.install_requires,
    }
    d = {**d, **add}

    return jj.Template(tstr).render(d)
