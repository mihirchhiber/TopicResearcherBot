class Article:
    def __init__(self, title, url, source, content, clean_content  = "", summary = ""):
        self.title = title
        self.url = url
        self.source = source
        self.content = content
        self.clean_content = clean_content
        self.summary = summary

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'source': self.source,
            'content': self.content,
            'clean_content': self.clean_content,
            'summary': self.summary
        }