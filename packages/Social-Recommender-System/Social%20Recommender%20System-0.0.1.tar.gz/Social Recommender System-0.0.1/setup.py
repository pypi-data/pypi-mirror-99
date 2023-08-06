from setuptools import setup

__project__ = "Social Recommender System"
__version__ = "0.0.1"
__description__ = "social recommender system to rated movies and tv shows"
__packages__ = ["main"]
__author__ = "Jadesola Bejide"
__author_email__= "jbejid14@st-pauls.leicester.sch.uk"
__url__ = "https://github.com/jade-bejide/Social-Recommender-System"
__classifiers__ = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python :: 3",
]
__keywords__ = ["Netflix", "IMDb", "recommender system", "streaming", "entertainment"]
__requires__ = ["guizero", "mysql.connector", "json", "urllib", "numpy", "math", "requests", "random", "PIL", "sys"]
setup (
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    url = __url__,
    classifiers = __classifiers__,
    keywords = __keywords__,
    requires = __requires__
    
)
