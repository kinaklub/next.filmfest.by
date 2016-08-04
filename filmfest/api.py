from wagtail.api.v2.endpoints import PagesAPIEndpoint
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.wagtailimages.api.v2.endpoints import ImagesAPIEndpoint


v2 = WagtailAPIRouter('wagtailapi_v2')
v2.register_endpoint('pages', PagesAPIEndpoint)
v2.register_endpoint('images', ImagesAPIEndpoint)
