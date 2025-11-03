from datetime import date
from slugify import slugify

AUTHOR = "Matt Woodward"
SITENAME = "Irondale Brewing"
# SITEURL is set in publishconf.py for production.
# For local development, it's best to leave it empty.
# When you run `pelican --listen`, it will default to http://localhost:8000
SITEURL = ""

THEME = "themes/irondale-brewing"

PATH = "content"

# Tell Pelican to look for articles in the 'articles' directory
ARTICLE_PATHS = ["articles"]

# Tell Pelican to look for pages in the 'pages' directory
PAGE_PATHS = ["pages"]

# Directories that contain static files (like images) that should be copied
# directly to the output without being processed as content.
STATIC_PATHS = ["images"]

TIMEZONE = "America/Los_Angeles"
DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

# Menu items for the theme
MENUITEMS = (
    ("Homebrewing", "/category/homebrewing.html"),
    ("Craft Beer", "/category/craft-beer.html"),
    ("About", "/pages/about.html"),
    ("Contact", "/pages/contact.html"),
)

# Plugins
PLUGINS = [
    "liquid_tags",
    "photos",
    "more_categories",
    "search",
]

# Pelican Liquid Tags configuration
LIQUID_TAGS = [
    "youtube",
]

# Jinja filters
JINJA_FILTERS = {
    "slugify": slugify,
}

# pelican-photos configuration
PHOTO_LIBRARY = "content/images"
PHOTO_GALLERY = (1024, 768, 80) # (width, height, quality)
PHOTO_THUMBNAIL = (280, 210, 80) # (width, height, quality)
PHOTO_RESIZE_JOBS = 5 # Number of parallel jobs to resize images
PHOTO_LIGHTBOX_GALLERY_ATTR = "data-lightgallery" # To integrate with lightgallery.js

# Make the current year available to templates
JINJA_GLOBALS = {"CURRENT_YEAR": date.today().year}

# Markdown settings
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}

# Pagination
DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# This is recommended for local development. It is set to False in publishconf.py
RELATIVE_URLS = True
