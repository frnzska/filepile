import requests
from src.page import Page
import src.utils as utils
from collections import namedtuple


class confluence:

    def __init__(self, *, page_id):
        cred = utils.get_credentials('confluence')
        self.auth = (cred['user'], cred['password'])
        self.page_id = page_id
        self.base_url = f'https://{cred["domain"]}/wiki/rest/api/content/{page_id}'
        self.domain = cred["domain"]
        self.title = None
        self.page = None

    def __str__(self):
        return f'title: {self.title} \n' \
               f'page_id: {self.page_id}\n' \
               f'at {self.base_url} with no of attachments: ' \
               f'{len(self.page.attachments)}'

    def save(self, *, dest_folder):
        self.__set_page_title()
        self.page.title = self.format_title(self.title)
        self.download_attachments() \
            .download_page_content()
        self.page.save(dest_folder=dest_folder)
        return self

    def __set_page_title(self):
        self.title = requests.get(self.base_url, auth=self.auth).json()['title']
        self.page = Page(title=self.title)
        return self

    @staticmethod
    def format_title(title, delimiter='_'):
        return title.replace(' ', delimiter)

    def download_attachments(self):
        """
        Download all page attachments (list(namedtuple))
        :return: self
        """
        Attachment = namedtuple('Attachment', ['title', 'content'], verbose=False)
        attachements = []
        download_info = requests.get(f'{self.base_url}/child/attachment', auth=self.auth).json()['results']
        for elem in download_info:
            title = elem['title']
            download_url = f'https://{self.domain}/wiki{elem["_links"]["download"]}'
            download_content = requests.get(download_url, auth=self.auth, stream=True).content
            attachements.append(Attachment(title=title, content=download_content))
        self.page.set_attachments(attachements)
        return self

    def download_page_content(self):
        """
        Download raw page source.
        :return: self
        """
        url = f'{self.base_url}/?expand=body.view'
        self.page.set_content(content=requests.get(url, auth=self.auth).json()['body']['view']['value'])
        return self


