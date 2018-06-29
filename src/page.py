class Page:

    def __init__(self, title, content=None, attachments=[]):
        self.title = title
        self.content = content
        self.attachments = attachments

    def set_content(self, content):
        self.content = content

    def set_attachments(self, attachments):
        self.attachments = attachments

    def insert_attachments_src(self):
        pass

    def save(self, *, destination):
        self.save_attachemnts()
        content = self.insert_attachments()
        pass



