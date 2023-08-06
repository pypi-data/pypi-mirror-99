Installation:

* Install `django-mp-categories`

* Add `'categories.settings.default',` to settings factory.

* Migrate data

* Add special choice field:
```
from categories.fields import CategoryChoiceField
class Form(...):
    class Meta:
        field_classes = {
            'category': CategoryChoiceField
        }
```

* Rebuild data using shell, if initial records exist:
```
from categories.models import Category
Category.objects.rebuild()
```
