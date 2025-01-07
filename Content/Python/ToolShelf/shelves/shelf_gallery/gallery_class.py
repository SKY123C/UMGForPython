import unreal


class GallaryWidgetFactory:

    export = True

    def create(self) -> unreal.Widget:
        ...
    