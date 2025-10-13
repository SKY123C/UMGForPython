import unreal


class GallaryWidgetFactory:

    export = True

    def create(self) -> unreal.Widget:
        ...
    def with_content(self):
        return "Example"