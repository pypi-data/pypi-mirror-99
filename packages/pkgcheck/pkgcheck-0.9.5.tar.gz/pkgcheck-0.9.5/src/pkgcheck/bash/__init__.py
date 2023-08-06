"""bash parsing support"""

from functools import partial
import os

from snakeoil.osutils import pjoin
from tree_sitter import Language, Parser

from .. import const

# path to bash parsing library
lib = pjoin(os.path.dirname(__file__), 'lang.so')


# copied from tree-sitter with the following changes:
# - prefer stdc++ over c++ when linking
# - perform platform-specific compiler customizations
def build_library(output_path, repo_paths):  # pragma: no cover
    """
    Build a dynamic library at the given path, based on the parser
    repositories at the given paths.

    Returns `True` if the dynamic library was compiled and `False` if
    the library already existed and was modified more recently than
    any of the source files.
    """
    from ctypes.util import find_library
    from distutils.ccompiler import new_compiler
    from distutils.sysconfig import customize_compiler
    from os import path
    from platform import system
    from tempfile import TemporaryDirectory

    output_mtime = path.getmtime(output_path) if path.exists(output_path) else 0

    if not repo_paths:
        raise ValueError("Must provide at least one language folder")

    cpp = False
    source_paths = []
    for repo_path in repo_paths:
        src_path = path.join(repo_path, "src")
        source_paths.append(path.join(src_path, "parser.c"))
        if path.exists(path.join(src_path, "scanner.cc")):
            cpp = True
            source_paths.append(path.join(src_path, "scanner.cc"))
        elif path.exists(path.join(src_path, "scanner.c")):
            source_paths.append(path.join(src_path, "scanner.c"))
    source_mtimes = [path.getmtime(__file__)] + [
        path.getmtime(path_) for path_ in source_paths
    ]

    compiler = new_compiler()
    if cpp:
        if find_library("stdc++"):
            compiler.add_library("stdc++")
        elif find_library("c++"):
            compiler.add_library("c++")
        else:
            # fallback to assuming libstdc++ exists (#299)
            compiler.add_library("stdc++")

    if max(source_mtimes) <= output_mtime:
        return False

    # perform platform-specific compiler customizations
    customize_compiler(compiler)

    with TemporaryDirectory(suffix="tree_sitter_language") as out_dir:
        object_paths = []
        for source_path in source_paths:
            flags = []
            if system() != "Windows" and source_path.endswith(".c"):
                flags.append("-std=c99")
            object_paths.append(
                compiler.compile(
                    [source_path],
                    output_dir=out_dir,
                    include_dirs=[path.dirname(source_path)],
                    extra_preargs=flags,
                )[0]
            )
        compiler.link_shared_object(object_paths, output_path)
    return True


try:
    from .. import _const
except ImportError:  # pragma: no cover
    # build library when running from git repo or tarball
    if not os.path.exists(lib) and 'tree-sitter-bash' in os.listdir(const.REPO_PATH):
        bash_src = pjoin(const.REPO_PATH, 'tree-sitter-bash')
        build_library(lib, [bash_src])


if os.path.exists(lib):
    lang = Language(lib, 'bash')
    query = partial(lang.query)
    parser = Parser()
    parser.set_language(lang)

    # various parse tree queries
    cmd_query = query('(command) @call')
    func_query = query('(function_definition) @func')
    var_assign_query = query('(variable_assignment) @assign')
    var_query = query('(variable_name) @var')
