from datetime import date

AUTHOR = "Matt Woodward"
SITENAME = "Irondale Brewing"
SITEURL = "https://irondalebrewing.com" # Set for local development with pelican --listen

THEME = "themes/irondale-brewing"

PATH = "content"

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
    ("Homebrewing", "/pages/homebrewing.html"),
    ("Craft Beer", "/pages/craft-beer.html"),
    ("About", "/pages/about.html"),
    ("Contact", "/pages/contact.html"),
)

# Make the current year available to templates
JINJA_GLOBALS = {"CURRENT_YEAR": date.today().year}

# Pagination
DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
