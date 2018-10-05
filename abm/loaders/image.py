from types import ModuleType
try:
    import PIL
except ImportError:
    print('PIL not found, install a PIL compatible package such as '
          'pillow to support loading images as modules.')
    raise
from PIL import Image, ExifTags

from abm.loaders import AbmLoader


# noinspection PyAbstractClass
class ImageLoader(AbmLoader):

    extensions = ('.jpg', '.jpeg', '.bmp', '.tiff')

    def create_module(self, spec):
        module = ImageModule(spec.name)
        self.init_module_attrs(spec, module)
        return module

    def exec_module(self, module):
        image = Image.open(self.path)
        module._image = image


class ImageModule(ModuleType):

    def __init__(self, spec_name):
        super().__init__(spec_name)
        self._image = None
        self._available_exif = []

    @property
    def image(self):
        return self._image

    @property
    def data(self):
        return self._image.getdata()

    # noinspection PyProtectedMember
    def __dir__(self):
        if not self._available_exif:
            for name in ExifTags.TAGS.values():
                method = getattr(type(self), name)
                tag = getattr(method.fget, 'exif_tag', None)
                if tag in self._image._getexif():
                    self._available_exif.append(name)

        return sorted(super().__dir__() + self._available_exif)


def _get_exif(exif_tag, exif_tag_name):

    def _wrapper(self):
        try:
            # noinspection PyProtectedMember
            return self._image._getexif()[exif_tag]
        except KeyError:
            return None

    _wrapper.__name__ = exif_tag_name
    _wrapper.exif_tag = exif_tag
    return _wrapper


def _add_exif_attributes():
    for tag, name in ExifTags.TAGS.items():
        setattr(ImageModule, name, property(_get_exif(tag, name)))


_add_exif_attributes()
