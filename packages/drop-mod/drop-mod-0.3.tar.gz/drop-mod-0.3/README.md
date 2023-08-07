# Drop
###### *also known as drop-mod*
Drop is a Python module focused on providing moderation commands for chat-bots (i.e. Discord, Matrix.org, etc.)
## How do I install/use it?
Unfortunately I have not yet made this package a terminal app, so you'll have to use it in scripts (for example, [drop-discord](https://github.com/AtlasC0R3/drop-discord/))

There are 2 ways: either cloning the GitHub repository, or using `pip`
### Cloning from GitHub
1. Clone this repository, [by downloading this repository as a \*.zip file](https://github.com/AtlasC0R3/drop-mod/archive/main.zip), [by cloning this repository using Git](https://github.com/AtlasC0R3/drop-mod.git) or [by going into this repository's releases](https://github.com/AtlasC0R3/drop-mod/releases) and downloading the latest release. If you download from this repository's release, you have the stable release. If you cloned this repository directly, you have a more "canary" release.
2. Run `setup.py` using your preferred Python installation
### Using `pip`
1. Run `pip install drop-mod`

Drop should be installed *unless `setup.py` threw an error*!

To use it, import `drop` into your Python scripts (or specific commands using `from drop.basic import owofy`) and, well, use them!

Example:
```python
from drop.basic import owofy
owofy("The quick brown fox jumps over the lazy dog.")
# This is just a simple command to work with, hence why I use it as a prime example.
# no im not a furry shhHHHHHH.
```

## F.A.Q.
### Q: Are there any open images for this project?
**A:** Yes, [they are updated in a Gitdab repository](https://gitdab.com/atlas_core/drop-misc/src/branch/master/images). *[License link](https://gitdab.com/atlas_core/drop-misc/src/branch/master/images/license.txt)*
### Q: Can I use this for my own projects?
**A:** Of course, it's a Python module! Just install it, set it up in your projects/scripts, and off you go! *note: this Python module still has a license, please make sure your project respects the license.*
### ~~Q: who are you?~~
~~**A:** a person why are you asking~~

### Dependencies
**None of these packages listed below are included directly into this software!** They are only installed from [PyPI](https://pypi.org/) when running `setup.py`!

[duckduckpy](https://github.com/ivankliuk/duckduckpy/), licensed under [MIT License](https://github.com/ivankliuk/duckduckpy/blob/master/LICENSE)

[LyricsGenius](https://github.com/johnwmillr/LyricsGenius/), licensed under [MIT License](https://github.com/johnwmillr/LyricsGenius/blob/master/LICENSE.txt)

[Parsedatetime](https://github.com/bear/parsedatetime/), licensed under [Apache 2.0](https://github.com/bear/parsedatetime/blob/master/LICENSE.txt)
