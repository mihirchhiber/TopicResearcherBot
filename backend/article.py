class Article:
    def __init__(self, id, topics, sites, title, url, source, content, clean_content="", summary=""):
        """
        Initialize an Article object.

        Args:
            id (int): Unique ID for the article.
            topics (list): List of topics the article relates to.
            sites (list): List of sites where the article was found.
            title (str): Title of the article.
            url (str): URL link to the article.
            source (str): Source website.
            content (str): Raw content of the article.
            clean_content (str, optional): Cleaned main content.
            summary (str, optional): Summarized content.
        """
        self.id = id
        self.topics = topics
        self.sites = sites
        self.title = title
        self.url = url
        self.source = source
        self.content = content
        self.clean_content = clean_content
        self.summary = summary

    def to_dict(self):
        """
        Convert the Article object to a dictionary.
        """
        return {
            'id': self.id,
            'topics': self.topics,
            'sites': self.sites,
            'title': self.title,
            'url': self.url,
            'source': self.source,
            'content': self.content,
            'clean_content': self.clean_content,
            'summary': self.summary
        }
