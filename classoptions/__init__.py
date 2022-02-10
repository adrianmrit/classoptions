from typing import Tuple


class ClassOptionsMetaclass(type):
    """
    Implement namespaced and inheritable metadata at the class level.
    """

    _meta_attr = "Meta"
    _default_meta_attr = "DefaultMeta"
    _access_attr = "_meta"

    def __new__(mcs, name: str, bases: Tuple[type], attrs: dict) -> type:
        new_cls_meta = attrs.get(mcs._meta_attr, None)
        new_cls_default_meta = attrs.get(mcs._default_meta_attr, None)

        # We override the default meta to inherit other defaults
        new_cls_default_meta = mcs._get_default_meta_subclass(
            new_cls_default_meta, bases
        )
        new_cls_final_meta = mcs._get_meta_subclass(new_cls_meta, new_cls_default_meta)

        # We update the default metadata class attribute to use the one we constructed
        # before. This way we implement an implicit inheritance.
        attrs[mcs._default_meta_attr] = new_cls_default_meta
        attrs[mcs._access_attr] = new_cls_final_meta

        return super().__new__(mcs, name, bases, attrs)

    @classmethod
    def _get_default_meta_subclass(
        mcs, new_cls_default_meta: type, new_cls_bases: Tuple[type]
    ) -> type:
        """
        Constructs a default metadata class that inherits from default metadata classes
        in the direct bases of the new class.

        :param new_cls_default_meta: Default metadata class declared in the new class.
        :param new_cls_bases: Direct bases of the new class.
        :return: Default metadata class with inherited default values.
        """
        default_meta_bases = (
            getattr(base, mcs._default_meta_attr)
            for base in new_cls_bases
            if hasattr(base, mcs._default_meta_attr)
        )

        if new_cls_default_meta is not None:
            bases = (new_cls_default_meta, *default_meta_bases)
        else:
            bases = tuple(default_meta_bases)

        return type(mcs._default_meta_attr, bases, {})

    @classmethod
    def _get_meta_subclass(mcs, new_cls_meta: type, new_cls_default_meta: type) -> type:
        """
        Returns a metadata class with the class specific values plus default values.

        :param new_cls_meta: Metadata class declared in the new class.
        :param new_cls_default_meta: Default metadata class to inherit defaults from.
        :return:
        """

        # Custom Meta should be at the beginning
        if new_cls_meta is not None:
            bases = (new_cls_meta, new_cls_default_meta)
        else:
            bases = (new_cls_default_meta,)

        return type(mcs._meta_attr, bases, {})

    @classmethod
    def factory(
        mcs,
        meta_attr: str,
        default_meta_attr: str,
        access_attr: str,
        cls_name: str = None,
    ) -> type:
        """
        Returns a ready to use metadata metaclass.

        :param meta_attr: Name of the attribute holding class specific metadata.
        :param default_meta_attr: Name of the attribute holding default metadata.
        :param access_attr: Attribute to access the final result from.
        :param cls_name: Name for the new class. If not given, defaults to the
         name of the metaclass.
        :return: Metaclass ready to be used.
        """
        properties = {
            "_meta_attr": meta_attr,
            "_default_meta_attr": default_meta_attr,
            "_access_attr": access_attr,
        }

        return type(
            cls_name or mcs.__name__,
            (mcs, type),
            properties,
        )
