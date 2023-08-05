#!/usr/bin/env python3

import sys, os, io, getopt, re, shutil
import importlib, subprocess
import email.utils
import pkg_resources
from datetime import date

# make sure that 'metadata' is taken from the current `dune-common` folder
# and not some installed version which might be different from the one I'm
# packaging (by mistake). The path to `packagemetadata.py` needs to be
# added to the python path (to work here) and to the environment so that a
# later call to `python setup.py` also works.
here = os.path.dirname(os.path.abspath(__file__))
mods = os.path.join(here, "..", "python", "dune")
sys.path.append(mods)
pythonpath  = mods + ":" + os.environ.get('PYTHONPATH','.')
os.environ['PYTHONPATH'] = pythonpath
from packagemetadata import metaData

def main(argv):

    repositories = ["gitlab", "testpypi", "pypi"]
    def usage():
        return 'usage: dunepackaging.py [--upload <'+"|".join(repositories)+'> | -c | --clean | --version <version> | --onlysdist | --bdist_conda]'

    try:
        opts, args = getopt.getopt(argv, "hc", ["upload=", "clean", "version=", "onlysdist", "bdist_conda"])
    except getopt.GetoptError:
        print(usage())
        sys.exit(2)

    upload = False
    repository = "gitlab"
    clean = False
    version = None
    onlysdist = False
    bdistconda = False
    for opt, arg in opts:
        if opt == '-h':
            print(usage())
            sys.exit(2)
        elif opt in ("--upload"):
            upload = True
            if arg != '':
                repository = arg
                if repository not in repositories:
                    print("Specified repository must be one of: " + " ".join(repositories))
                    sys.exit(2)
        elif opt in ("-c", "--clean"):
            clean = True
        elif opt in ("--version"):
            version = arg
        elif opt in ("--onlysdist"):
            onlysdist = True
        elif opt in ("--bdist_conda"):
            onlysdist  = True
            bdistconda = True

    # Remove generated files
    def removeFiles():
        import glob
        files = ['MANIFEST', 'dist', '_skbuild', '__pycache__']
        print("Remove generated files: " + ", ".join(files))
        remove = ['rm', '-rf'] + files
        subprocess.call(remove)
        # checkout setup.py and pyproject.toml
        checkout = ['git', 'checkout', 'setup.py', 'pyproject.toml']
        subprocess.call(checkout)

    if clean:
        removeFiles()
        sys.exit(0)

    data, cmake_flags = metaData(version, dependencyCheck=False)

    if version is None:
        version = data.version

    # Generate setup.py
    print("Generate setup.py")
    f = open("setup.py", "w")
    if data.name == 'dune-common':
        f.write("import os, sys\n")
        f.write("here = os.path.dirname(os.path.abspath(__file__))\n")
        f.write("mods = os.path.join(here, \"python\", \"dune\")\n")
        f.write("sys.path.append(mods)\n\n")
    f.write("try:\n")
    f.write("    from dune.packagemetadata import metaData\n")
    f.write("except ImportError:\n")
    f.write("    from packagemetadata import metaData\n")
    f.write("from skbuild import setup\n")
    f.write("setup(**metaData('"+version+"')[1])\n")
    f.close()

    # Generate pyproject.toml
    print("Generate pyproject.toml")
    f = open("pyproject.toml", "w")
    requires = ["setuptools", "wheel", "scikit-build", "cmake", "ninja", "requests"]
    requires += [r for r in data.asPythonRequirementString(data.depends + data.python_requires) if r not in requires]
    f.write("[build-system]\n")
    f.write("requires = "+requires.__str__()+"\n")
    f.write("build-backend = 'setuptools.build_meta'\n")
    f.close()

    # Create source distribution and upload to repository
    python = sys.executable
    if upload or onlysdist:
        print("Remove dist")
        remove = ['rm', '-rf', 'dist']
        subprocess.call(remove)

        # check if we have scikit-build
        import pkg_resources
        installed = {pkg.key for pkg in pkg_resources.working_set}
        if not 'scikit-build' in installed:
            print("Please install the pip package 'scikit-build' to build the source distribution.")
            sys.exit(2)

        # append hash of current git commit to README
        shutil.copy('README.md', 'tmp_README.md')
        githash = ['git', 'rev-parse', 'HEAD']
        hash = subprocess.check_output(githash, encoding='UTF-8')
        with open("README.md", "a") as f:
            f.write("\n\ngit-" + hash)

        print("Create source distribution")
        # make sure setup.py/pyproject.toml are tracked by git so that
        # they get added to the package by scikit
        gitadd = ['git', 'add', 'setup.py', 'pyproject.toml']
        subprocess.call(gitadd)
        # run sdist
        build = [python, 'setup.py', 'sdist']
        subprocess.call(build, stdout=subprocess.DEVNULL)
        # undo the above git add
        gitreset = ['git', 'reset', 'setup.py', 'pyproject.toml']
        subprocess.call(gitreset)

        # restore README.md
        shutil.move('tmp_README.md', 'README.md')

        if not onlysdist:
            # check if we have twine
            import pkg_resources
            installed = {pkg.key for pkg in pkg_resources.working_set}
            if not 'twine' in installed:
                print("Please install the pip package 'twine' to upload the source distribution.")
                sys.exit(2)

            twine = [python, '-m', 'twine', 'upload']
            twine += ['--repository', repository]
            twine += ['dist/*']
            subprocess.call(twine)

            removeFiles()

        # create conda package meta.yaml (experimental)
        if bdistconda:
            import hashlib
            remove = ['rm', '-rf', 'dist/'+data.name]
            subprocess.call(remove)
            mkdir  = ['mkdir', 'dist/'+data.name ]
            subprocess.call(mkdir)

            print("Create bdist_conda (experimental)")
            distfile = 'dist/'+data.name+'-'+version+'.tar.gz'
            datahash = ''
            with open(distfile, "rb") as include:
                source = include.read()
                datahash = hashlib.sha256( source ).hexdigest()

            print("Generate ",'dist/'+data.name+'/meta.yaml')
            f = open('dist/'+data.name+'/meta.yaml', "w")
            f.write('{% set name = "' + data.name + '" %}\n')
            f.write('{% set version = "' + version + '" %}\n')
            f.write('{% set hash = "' + datahash + '" %}\n\n')
            f.write('package:\n')
            f.write('  name: "{{ name|lower }}"\n')
            f.write('  version: "{{ version }}"\n\n')
            f.write('source:\n')
            f.write('  path: ../{{ name }}-{{ version }}/\n')
            f.write('  sha256: {{ hash }}\n\n')
            f.write('build:\n')
            f.write('  number: 1\n')
            if 'TMPDIR' in os.environ:
                f.write('  script_env:\n')
                f.write('    - TMPDIR=' + os.environ['TMPDIR'] +'\n')
            f.write('  script: "{{ PYTHON }} -m pip install . --no-deps --ignore-installed -vv "\n\n')
            f.write('requirements:\n')

            requirements = ['pip', 'python', 'mkl', 'tbb', 'intel-openmp',
                            'libgcc-ng', 'libstdcxx-ng', 'gmp', 'scikit-build',
                            'mpi4py', 'matplotlib', 'numpy', 'scipy', 'ufl']

            for dep in data.depends:
                requirements += [dep[0]]

            f.write('  host:\n')
            for dep in requirements:
                f.write('    - ' + dep + '\n')

            f.write('\n')
            f.write('  run:\n')
            for dep in requirements:
                f.write('    - ' + dep + '\n')

            f.write('\n')
            f.write('test:\n')
            f.write('  imports:\n')
            f.write('    - ' + data.name.replace('-','.') + '\n\n')
            f.write('about:\n')
            f.write('  home: '+data.url+'\n')
            f.write('  license: GPLv2 with linking exception.\n')
            f.write('  license_family: GPL\n')
            f.write('  summary: '+data.description+'\n')
            f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
