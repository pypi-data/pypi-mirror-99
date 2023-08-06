collective.soupstrainer
=======================


Quite often there is a need to clean up HTML from some source, be it user
input or data gathered by scraping, which needs to be cleaned up. With the
SoupStrainer class in collective.soupstrainer this is made easy. It uses
beautifulsoup4 to parse and clean up HTML. The constructor of the class takes
four arguments.

exclusions
    This is a list of tuples with two items each. The first item is a list of
    tag names, the second item is a list of attributes. If the list of
    attributes is empty, then each tag in the first list is completely
    removed from the passed in HTML. If the list of tags is empty, then each
    attribute listed is completely removed. If there are both tags and
    attributes listed, then the attributes are only removed from matching
    tags.

style_whitelist
    This is a white list of CSS styles allowed in 'style' attributes. All
    other styles are removed.

class_blacklist
    This is a black list for CSS classes. Each matching class is removed from
    'class' attributes.

parser
    This is the parser used by beautifulsoup4, when the strainer is called with
    a string. It must be an installed parser for beautifulsoup4, defaults to
    ``html.parser``

An instance of the SoupStrainer class can be called directly with one
argument. The argument can either be a string, in which case it will
internally be parsed by beautifulsoup4 and the result will be unicode (or 
string in python 3), or it can be a parsed HTML tree created by beautifulsoup4,
in which case it will be modified in place and be returned again.
