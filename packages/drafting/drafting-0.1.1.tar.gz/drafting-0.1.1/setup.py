import setuptools

long_description = """
# Drafting

Color and geometric primitives
"""

setuptools.setup(
    name="drafting",
    version="0.1.1",
    author="Rob Stenson / Goodhertz",
    author_email="rob@goodhertz.com",
    description="Color and geometric primitives",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/goodhertz/drafting",
    packages=[
        "drafting",
        "drafting.sh",
        "drafting.grid",
        "drafting.pens",
        "drafting.text",
        "drafting.color",
        #"drafting.drawbot",
        #"drafting.beziers",
        "drafting.geometry",
        "drafting.fontgoggles",
        "drafting.interpolation",
        "drafting.fontgoggles.font",
        "drafting.fontgoggles.misc",
        "drafting.fontgoggles.compile",
    ],
    install_requires=[
        "fontPens",
        "fonttools[ufo,lxml,unicode,woff,type1]==4.21.1",
        "more-itertools",
        "skia-pathops",
        "freetype-py",
        "uharfbuzz==0.14.0",
        "python-bidi",
        "ufo2ft",
        "unicodedata2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
