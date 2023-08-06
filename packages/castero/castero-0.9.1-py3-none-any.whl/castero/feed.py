from lxml import etree

import requests
from typing import List

from castero import helpers
from castero.config import Config
from castero.episode import Episode
from castero.net import Net


class FeedError(Exception):
    """An ambiguous error while handling the feed.
    """


class FeedLoadError(FeedError):
    """A feed could not be found at the provided file, or an IO exception
    occurred when loading the file.
    """


class FeedDownloadError(FeedError):
    """A feed could not be found at the provided URL, or a request exception
    occurred when downloading the feed.
    """


class FeedParseError(FeedError):
    """The document at the provided URL could not be parsed as an XML document.
    """


class FeedStructureError(FeedError):
    """The feed at the provided URL is not a properly structured RSS document.
    """


class Feed:
    """A podcast feed.

    This class uses a provided url to retrieve all data and metadata for a
    podcast feed. It creates and is a parent to all episode objects which are
    available on the feed.

    The url for the feed should point to an RSS document.
    """

    def __init__(self, url=None, file=None, text=None, **kwargs) -> None:
        """
        A feed can be provided as either a url or a file, but exactly one must
        be given. Realistically, users will almost universally use a url to
        retrieve feeds from. However, having support for handling files makes
        testing easier.

        Args:
            url: (optional) the url where the feed is located
            file: (optional) the file where the feed is located
            text: (optional) pre-retrieved text for the feed. Can be useful if
                multiple feeds were downloaded previously; a URL or file is
                still required, providing this field will only skip the
                download step
        """
        # * Don't allow providing both a url and a file, but must provide one.
        # Check that one of them is None, and that they are not both the same.
        # The second conditional can be read as checking that both variables
        # are not None.
        assert (url is None or file is None) and (url is not file)

        self._url = url
        self._file = file
        self._tree = None
        self._validated = False

        self._title = kwargs.get('title', None)
        self._description = kwargs.get('description', None)
        self._link = kwargs.get('link', None)
        self._last_build_date = kwargs.get('last_build_date', None)
        self._copyright = kwargs.get('copyright', None)

        # assume that if we have been passed the title then we have also been
        # passed everything else and that the feed is valid
        if self._title is None:
            if text:
                # the content of a document was already provided, but we need
                # to ensure it is valid RSS
                try:
                    self._tree = etree.fromstring(text)
                except etree.ParseError:
                    raise FeedParseError(
                        "Unable to parse text as an XML document")
            else:
                # retrieve the feed and parse to XML document
                self._download_feed()
            # check that the XML document is a properly structured RSS feed
            self._validate_feed()
            # set this object's metadata using rss feed
            self._parse_metadata()
        else:
            self._validated = True

    def __str__(self) -> str:
        """Represent this object as a string.

        Returns:
            string: this feed's title
        """
        assert self._title is not None

        return self._title

    def _download_feed(self):
        """Parses the feed at the provided url or file into _tree.

        This method checks whether the url is valid and that there is a
        parse-able XML document at the url, but it does not check that the
        document is an RSS feed, nor whether the feed has all necessary tags.

        Raises:
            FeedParseError: unable to parse text as an XML document
            FeedDownloadError: (only when retrieving feed using url) did not
                receive an acceptable status code, or an exception occurred
                when attempting to download the page
            FeedLoadError: (only when retrieving feed using file) a feed could
                not be found at the file, or an exception occurred when
                attempting to load the file
        """
        if self._url is not None:
            # handle feed from url
            try:
                response = Net.Get(self._url)
                if response.status_code == 200:
                    try:
                        self._tree = etree.fromstring(response.content)
                    except etree.ParseError:
                        raise FeedParseError(
                            "Unable to parse text as an XML document")
                else:
                    raise FeedDownloadError(
                        "Did not receive an acceptable status code while"
                        " downloading the page. Expected 200, got: "
                        + str(response.status_code))
            except requests.exceptions.RequestException:
                raise FeedDownloadError(
                    "An exception occurred when attempting to download the"
                    " page")
        elif self._file is not None:
            # handle feed from file
            try:
                tree = etree.parse(self._file)
                self._tree = tree.getroot()
            except etree.ParseError:
                raise FeedParseError(
                    "Unable to parse text as an XML document")
            except IOError:
                raise FeedLoadError(
                    "An exception occurred when attempting to load the file")

    def _validate_feed(self):
        """Checks that the provided XML document is a valid RSS feed.

        This method is intended to be run only when this object is being
        created in order to raise any necessary exceptions at that time.

        The conditions checked are:
            - the root of the XML document is an 'rss' tag
            - the root has a 'version' attribute which equals '2.0'
            - the root has exactly one child, which is the channel tag
            - the channel tag has at least 3 children, which include a title,
              link, and description tag (in any order)
            - for each child of the channel tag which is an item tag, if any:
                - the item tag must have at least one child, which is a title
                  tag or a description tag
        See http://cyber.harvard.edu/rss/rss.html for more details.

        Exceptions to these conditions:
            - There are some feeds which have multiple children under the root,
              rather than a single channel tag as expected. These additional
              children tend to be warning or notices which don't otherwise
              affect the content. Therefore, we allow multiple children and
              simply use the first channel one.
            - Although the channel tag should have a "link" child, we also
              allow having an "atom:link" tag as a substitute. If multiple are
              present, the first is used.

        This method does not set this object's metadata. That is done in
        _process_feed().

        Raises:
            FeedStructureError: the XML document violates one of the conditions
        """
        assert self._tree is not None

        # root should be an rss tag
        if self._tree.tag != 'rss':
            raise FeedStructureError("XML document is not an RSS feed")

        # root should have version attribute which equals 2.0
        if 'version' in self._tree.attrib:
            if self._tree.attrib['version'] != '2.0':
                raise FeedStructureError("RSS version is not 2.0")
        else:
            raise FeedStructureError(
                "RSS feed does not have a version attribute")

        # root should a channel tag as its child
        # theoretically the root should have only one child, but see the
        # exception listed in the method description
        root_children = list(self._tree)
        if len(root_children) > 0:
            channel = None
            for root_child in root_children:
                if root_child.tag == 'channel':
                    channel = root_child
                    break
            if channel is None:
                raise FeedStructureError(
                    "RSS feed does not have a channel tag as its child")

            # Channel should have at least 3 children, including a
            # title and description tag. There should be a "link" tag, but we
            # allow an "atom:link" tag as a substitute
            channel_children = list(channel)
            if len(channel_children) >= 3:
                chan_title_tags = channel.findall('title')
                chan_link_tags = channel.findall('link')
                chan_atomlink_tags = channel.findall(
                    '{http://www.w3.org/2005/Atom}link')
                chan_description_tags = channel.findall('description')

                if len(chan_title_tags) != 1:
                    raise FeedStructureError(
                        "RSS feed's channel has too many or too few"
                        " title tags; expected 1, was: "
                        + str(len(chan_title_tags)))
                else:
                    if channel.find("title").text is None:
                        raise FeedStructureError(
                        "RSS feed's channel has no title text")
                if len(chan_link_tags) > 1:
                    raise FeedStructureError(
                        "RSS feed's channel has too many"
                        " link tags; expected 1, was: "
                        + str(len(chan_link_tags))
                        + ". The corresponding title is: "
                        + str(chan_title_tags[0].text))
                if len(chan_link_tags) == 0:
                    if len(chan_atomlink_tags) == 0:
                        raise FeedStructureError(
                            "RSS feed's channel had 0 link tags, expected 1."
                            + " There were also no atom:link tags available to"
                            + " use as a substitute"
                            + ". The corresponding title is: "
                            + str(chan_title_tags[0].text))
                if len(chan_description_tags) != 1:
                    raise FeedStructureError(
                        "RSS feed's channel has too many or too few"
                        " description tags; expected 1, was: "
                        + str(len(chan_description_tags))
                        + ". The corresponding title is: "
                        + str(chan_title_tags[0].text))

                # if the channel has any items, each item should have
                # at least a title or description tag
                channel_item_tags = channel.findall('item')
                for item in channel_item_tags:
                    if len(item.findall('title')
                            + item.findall('description')) < 1:
                        raise FeedStructureError(
                            "An item in the RSS feed's channel did not"
                            " have at least one of a title or a"
                            " description tag")
            else:
                raise FeedStructureError(
                    "RSS feed's channel does not have enough required"
                    " children; expected >=3, was: "
                    + str(len(channel_children)))
        else:
            raise FeedStructureError(
                "RSS feed does not have any children; expected 1 (a channel"
                " tag)")

        self._validated = True

    def _parse_metadata(self):
        """Process the RSS feed to set metadata fields.

        It is required that _validate_feed be run prior to running this method.
        """
        assert self._validated

        channel = None
        for root_child in list(self._tree):
            if root_child.tag == 'channel':
                channel = root_child
                break

        self._title = channel.find('title').text
        self._description = channel.find('description').text

        link_tags = channel.findall('link')
        if len(link_tags) > 0:
            self._link = link_tags[0].text
        else:
            atomlink_tags = channel.findall(
                '{http://www.w3.org/2005/Atom}link')
            self._link = atomlink_tags[0].attrib['href']

        last_build_date_tag = channel.find('lastBuildDate')
        copyright_tag = channel.find('copyright')

        if last_build_date_tag is not None:
            self._last_build_date = last_build_date_tag.text
        if copyright_tag is not None:
            self._copyright = copyright_tag.text

    def parse_episodes(self) -> List[Episode]:
        """Process the RSS feed to retrieve episodes.

        It is required that _validate_feed be run prior to running this method.

        Returns:
            List[Episode]: the episodes in this feed, which need to be added to
            the database
        """
        channel = None
        for root_child in list(self._tree):
            if root_child.tag == 'channel':
                channel = root_child
                break

        episodes = []
        for item in channel.findall('item'):
            item_title = item.find('title')
            item_description = item.find('description')
            item_link = item.find('link')
            item_pubdate = item.find('pubDate')
            item_copyright = item.find('copyright')
            item_enclosure = item.find('enclosure')

            item_title_str = None
            item_description_str = None
            item_link_str = None
            item_pubdate_str = None
            item_copyright_str = None
            item_enclosure_str = None

            if item_title is not None:
                item_title_str = item_title.text
            if item_description is not None:
                item_description_str = item_description.text
            if item_link is not None:
                item_link_str = item_link.text
            if item_pubdate is not None:
                item_pubdate_str = item_pubdate.text
            if item_copyright is not None:
                item_copyright_str = item_copyright.text
            if item_enclosure is not None:
                if 'url' in item_enclosure.attrib.keys():
                    item_enclosure_str = item_enclosure.attrib['url']

            # if we were unable to find an enclosure for this episode,
            # don't add it
            if not item_enclosure_str:
                continue

            episodes.append(
                Episode(self,
                        title=item_title_str,
                        description=item_description_str,
                        link=item_link_str,
                        pubdate=item_pubdate_str,
                        copyright=item_copyright_str,
                        enclosure=item_enclosure_str
                        )
            )
        return episodes

    @property
    def validated(self) -> bool:
        """bool: whether this feed has been validated"""
        return self._validated

    @property
    def key(self) -> str:
        """str: either the url or file of the feed, whichever is set"""
        return self._url if self._url is not None else self._file

    @property
    def title(self) -> str:
        """str: the title of the feed"""
        return self._title

    @property
    def description(self) -> str:
        """str: the description of the feed"""
        result = self._description
        if result is None:
            result = "Description not available."
        return result

    @property
    def link(self) -> str:
        """str: the link of/for the feed"""
        return self._link

    @property
    def last_build_date(self) -> str:
        """str: the last build date of the feed"""
        result = self._last_build_date
        if result is None:
            result = "Last build date not available."
        return result

    @property
    def copyright(self) -> str:
        """str: the copyright of the feed"""
        result = self._copyright
        if result is None:
            result = "No copyright specified."
        return result

    @property
    def metadata(self) -> str:
        """str: the user-displayed metadata of the feed"""
        description = helpers.html_to_plain(self.description) if \
            helpers.is_true(Config["clean_html_descriptions"]) else \
            self.description
        description = description.replace('\n', '')

        return \
            "!cb{title}\n" \
            "{last_build_date}\n\n" \
            "{link}\n\n" \
            "!cbCopyright:\n" \
            "{copyright}\n\n" \
            "!cbDescription:\n" \
            "{description}\n".format(
                title=self.title,
                last_build_date=self.last_build_date,
                link=self.link,
                copyright=self.copyright,
                description=description)
