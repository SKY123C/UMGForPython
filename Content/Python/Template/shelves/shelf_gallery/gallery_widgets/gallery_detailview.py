import unreal
from .. import gallery_class


class GalleryDetailView(gallery_class.GallaryWidgetFactory):

    def create(self):   

        widget = unreal.DetailsView()
        widget.set_object(unreal.StaticMesh.static_class())
        return widget
    
    def with_content(self):
        return "DetailView"
