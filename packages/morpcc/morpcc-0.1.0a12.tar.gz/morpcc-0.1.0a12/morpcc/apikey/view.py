import html
from dataclasses import dataclass, field

import colander
import deform
import morepath
from inverter import dc2colander
from morpfw.crud import permission as crudperms
from morpfw.crud.errors import AlreadyExistsError
from webob.exc import HTTPFound, HTTPNotFound

from ..app import App
from .model import APIKeyCollectionUI, APIKeyModelUI


@dataclass
class APIKeyDisplay(object):

    name: str = None
    api_identity: str = None
    api_secret: str = None


@App.html(
    model=APIKeyCollectionUI,
    name="create",
    template="master/simple-form.pt",
    permission=crudperms.Create,
    request_method="POST",
)
def process_create(context, request):
    if not context.create_view_enabled:
        raise HTTPNotFound()
    default_value_fields = list(request.GET.keys())
    formschema = dc2colander.convert(
        context.collection.schema,
        request=request,
        include_fields=context.create_include_fields,
        exclude_fields=context.create_exclude_fields,
        hidden_fields=default_value_fields,
        default_tzinfo=request.timezone(),
    )
    fs = formschema()
    fs = fs.bind(context=context, request=request)

    controls = list(request.POST.items())
    form = deform.Form(fs, buttons=("Submit",))

    failed = False
    data = {}
    try:
        data = form.validate(controls)
    except deform.ValidationFailure as e:
        form = e
        failed = True
    if not failed:
        try:
            obj = context.collection.create(data, deserialize=False)
        except AlreadyExistsError as e:
            failed = True
            form_error = colander.Invalid(
                form.widget, "Object with {} already exists".format(e.message)
            )
            form.widget.handle_error(form, form_error)

        if not failed:
            display_schema = dc2colander.convert(APIKeyDisplay, request=request)()
            display_schema.bind(context=context, request=request)
            display_form = deform.Form(display_schema)
            data = obj.base_json()
            data["api_secret"] = obj.generate_secret()

            return {
                "page_title": "API Key",
                "form_title": "Please save this API key",
                "form": display_form,
                "readonly": True,
                "form_data": data,
            }

    @request.after
    def set_header(response):
        response.headers.add("X-MORP-FORM-FAILED", "True")

    return {
        "page_title": "Create %s"
        % html.escape(
            str(context.collection.__class__.__name__.replace("Collection", ""))
        ),
        "form_title": "Create",
        "form": form,
        "form_data": data,
    }


@App.html(
    model=APIKeyCollectionUI,
    name="modal-create",
    template="master/crud/modal-form.pt",
    permission=crudperms.Create,
    request_method="POST",
)
def modal_process_create(context, request):
    result = process_create(context, request)
    return result
