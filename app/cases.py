"""Define the main use case of this app"""


class ShowContent:
    def __init__(self, content_loader, renderer):
        self.content_loader = content_loader
        self.renderer = renderer

    def execute(self, identifier):
        content = self.content_loader.get_content(identifier)
        return self.renderer.render(content)
