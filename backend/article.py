class Article:
    def __init__(self, id, topics, sites, title, url, source, content, clean_content  = "", summary = ""):
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