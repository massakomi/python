from setuptools import setup
import re

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = ''
with open('neocord/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

if version.endswith(('a', 'b', 'rc')):
    try:
        import subprocess
        p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += out.decode('utf-8').strip()
        p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += '+g' + out.decode('utf-8').strip()
    except Exception:
        pass

readme = ''
with open('README.MD') as f:
    readme = f.read()

packages = [
    'neocord',
    'neocord.api',
    'neocord.api.routes',
    'neocord.dataclasses',
    'neocord.dataclasses.flags',
    'neocord.errors',
    'neocord.internal',
    'neocord.models',
    'neocord.typings',
    'neocord.utils',
]

setup(name='neocord',
      author='NerdGuyAhmad',
      url='https://github.com/nerdguyahmad/neocord',
      project_urls={
        "Documentation": "https://neocord.readthedocs.io/en/latest/",
        "Issue tracker": "https://github.com/nerdguyahmad/neocord/issues",
      },
      version=version,
      packages=packages,
      license='MIT',
      description='An API wrapper around Discord API.',
      long_description=readme,
      long_description_content_type="text/markdown",
      include_package_data=True,
      install_requires=requirements,
      python_requires='>=3.8.0',
      classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
      ]
)









with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycord-btns-menus",
    version="0.1.6",
    author="P. Sai Keerthan Reddy",
    author_email="saikeerthan.keerthan.9@gmail.com",
    description="A responsive package for Buttons, DropMenus and Combinations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skrphenix/pycord_btns_menus",
    project_urls={
        "Documentation": "https://skrphenix.github.io/pycord_btns_menus/",
        "Bug Tracker": "https://github.com/skrphenix/pycord_btns_menus/issues",
        "Examples": "https://github.com/skrphenix/pycord_btns_menus/tree/main/Examples",
        "Source": "https://github.com/skrphenix/pycord_btns_menus/tree/main/package/btns_menus",
        "Support Server": "https://discord.gg/GVMWx5EaAN",
    },
    keywords=["pycord", "py-cord", "btns", "pycord buttons",
              "pycord btns", "pycord btns menus", "py-cord btns menus"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    package_dir={"": "package"},
    packages=["btns_menus", "btns_menus.builds", "btns_menus.builds.base"],
    include_package_data=True,
    python_requires=">=3.6",
    dependency_links=[
        "https://github.com/Pycord-Development/pycord"
    ],
    install_requires=[
        "requests",
        "tabulate"
    ]
)