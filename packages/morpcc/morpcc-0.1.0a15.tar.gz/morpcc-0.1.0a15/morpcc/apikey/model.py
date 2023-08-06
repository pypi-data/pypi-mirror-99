from ..crud.model import CollectionUI, ModelUI


class APIKeyModelUI(ModelUI):
    @property
    def view_exclude_fields(self):
        return super().view_exclude_fields + ["api_secret"]


class APIKeyCollectionUI(CollectionUI):

    modelui_class = APIKeyModelUI
    create_view_enabled = True

    columns = [
        {"title": "Name", "name": "name"},
        {"title": "Identity", "name": "api_identity"},
        {"title": "Actions", "name": "structure:buttons"},
    ]
