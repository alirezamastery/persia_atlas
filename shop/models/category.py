from django.db import models
from django.core import serializers
from treebeard.mp_tree import MP_Node
from treebeard.mp_tree import get_result_class


__all__ = [
    'ProductCategory',
    'ProductCategoryAttribute',
]


class ProductCategory(MP_Node):
    title = models.CharField(max_length=255)

    selector_type = models.ForeignKey(
        'shop.VariantSelectorType',
        on_delete=models.PROTECT
    )
    attributes = models.ManyToManyField(
        'shop.ProductAttribute',
        through='shop.ProductCategoryAttribute',
        related_name='product_categories'
    )

    node_order_by = ['title']

    def __str__(self):
        return self.title

    @classmethod
    def dump_bulk_custom(cls, parent=None, keep_ids=True):
        """
        Dumps a tree branch to a python data structure.
        original code is from MP_Node.dump_bulk()
        """

        klass = get_result_class(cls)

        # Because of fix_tree, this method assumes that the depth
        # and numchild properties in the nodes can be incorrect,
        # so no helper methods are used
        qs = klass._get_serializable_model().objects.all()
        if parent:
            qs = qs.filter(path__startswith=parent.path)
        ret, lnk = [], {}
        pk_field = klass._meta.pk.attname
        for pyobj in serializers.serialize('python', qs):
            # django's serializer stores the attributes in 'fields'
            fields = pyobj['fields']
            path = fields['path']
            depth = int(len(path) / klass.steplen)
            # this will be useless in load_bulk
            del fields['depth']
            del fields['path']
            del fields['numchild']
            if pk_field in fields:
                # this happens immediately after a load_bulk
                del fields[pk_field]

            newobj = {'data': fields, 'title': fields['title']}
            if keep_ids:
                newobj[pk_field] = pyobj['pk']

            if (not parent and depth == 1) or \
                    (parent and len(path) == len(parent.path)):
                ret.append(newobj)
            else:
                parentpath = klass._get_basepath(path, depth - 1)
                parentobj = lnk[parentpath]
                if 'children' not in parentobj:
                    parentobj['children'] = []
                parentobj['children'].append(newobj)
            lnk[path] = newobj
        return ret


class ProductCategoryAttribute(models.Model):
    category = models.ForeignKey('shop.ProductCategory', on_delete=models.CASCADE)
    attribute = models.ForeignKey('shop.ProductAttribute', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'attribute'],
                name='unique_category_attribute'
            )
        ]
