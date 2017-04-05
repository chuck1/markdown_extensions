import markdown
from markdown import util

class MyLinkPattern(markdown.inlinepatterns.Pattern):
    def __init__(self, pattern, md, absolute_prefix):
        super(MyLinkPattern, self).__init__(pattern, md)
        self.absolute_prefix = absolute_prefix

    """ Return a link element from the given match. """
    def handleMatch(self, m):
        el = util.etree.Element("a")
        el.text = m.group(2)
        title = m.group(13)
        href = m.group(9)

        if href:
            if href[0] == "<":
                href = href[1:-1]

            safe_href = self.sanitize_url(self.unescape(href.strip()))
        
            #print "safe_href={}".format(repr(safe_href))
            
            if safe_href[0] == '/':
                #print "is absolute"
                if safe_href[:len(self.absolute_prefix)] == self.absolute_prefix:
                    #print "already prefixed"
                    pass
                else:
                    safe_href = self.absolute_prefix + safe_href


            el.set("href", safe_href)
        else:
            el.set("href", "")

        if title:
            title = dequote(self.unescape(title))
            el.set("title", title)
        return el

    def sanitize_url(self, url):
        """
        Sanitize a url against xss attacks in "safe_mode".

        Rather than specifically blacklisting `javascript:alert("XSS")` and all
        its aliases (see <http://ha.ckers.org/xss.html>), we whitelist known
        safe url formats. Most urls contain a network location, however some
        are known not to (i.e.: mailto links). Script urls do not contain a
        location. Additionally, for `javascript:...`, the scheme would be
        "javascript" but some aliases will appear to `urlparse()` to have no
        scheme. On top of that relative links (i.e.: "foo/bar.html") have no
        scheme. Therefore we must check "path", "parameters", "query" and
        "fragment" for any literal colons. We don't check "scheme" for colons
        because it *should* never have any and "netloc" must allow the form:
        `username:password@host:port`.

        """
        if not self.markdown.safeMode:
            # Return immediately bipassing parsing.
            return url

        try:
            scheme, netloc, path, params, query, fragment = url = urlparse(url)
        except ValueError:  # pragma: no cover
            # Bad url - so bad it couldn't be parsed.
            return ''

        locless_schemes = ['', 'mailto', 'news']
        allowed_schemes = locless_schemes + ['http', 'https', 'ftp', 'ftps']
        if scheme not in allowed_schemes:
            # Not a known (allowed) scheme. Not safe.
            return ''

        if netloc == '' and scheme not in locless_schemes:  # pragma: no cover
            # This should not happen. Treat as suspect.
            return ''

        for part in url[2:]:
            if ":" in part:
                # A colon in "path", "parameters", "query"
                # or "fragment" is suspect.
                return ''

        # Url passes all tests. Return url as-is.
        return urlunparse(url)







from markdown.extensions import Extension

class MyExtension(Extension):
    def __init__(self, absolute_prefix):
        self.absolute_prefix = absolute_prefix
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['link'] = MyLinkPattern(markdown.inlinepatterns.LINK_RE, md, self.absolute_prefix)





