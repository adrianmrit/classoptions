class ClassOptionsMetaclass(type):
    """
    Implement namespaced and inheritable metadata at the class level.
    """

    meta_attr = "Meta"
    default_meta_attr = "DefaultMeta"

    def __new__(mcs, name, bases, attrs, **kwargs):
        cls = super().__new__(mcs, name, bases, attrs, **kwargs)

        new_cls_meta = attrs.get(mcs.meta_attr, None)
        new_cls_default_meta = attrs.get(mcs.default_meta_attr, None)

        # default_meta_attr should never be a subclass of another default_meta_attr class
        # default metas are inherited, non default ones are not

        default_meta_bases = (
            getattr(base, mcs.default_meta_attr)
            for base in bases
            if hasattr(base, mcs.default_meta_attr)
        )

        new_cls_default_meta = mcs._get_default_meta_subclass(
            new_cls_default_meta, default_meta_bases
        )
        meta_class = mcs._get_meta_subclass(new_cls_meta, new_cls_default_meta)

        setattr(cls, mcs.default_meta_attr, new_cls_default_meta)
        setattr(cls, mcs.meta_attr, meta_class)

        return cls

    @classmethod
    def _get_default_meta_subclass(mcs, new_cls_default_meta, default_meta_bases):
        """
        Constructs a default metadata class that inherits other default values.

        :param new_cls_default_meta: Default metadata class declared in the new class.
        :param default_meta_bases: Default metadata classes from direct bases.
        :return: Default metadata class with inherited default values.
        """
        if new_cls_default_meta is not None:
            bases = (new_cls_default_meta, *default_meta_bases)
        else:
            bases = tuple(default_meta_bases)

        return type(mcs.default_meta_attr, bases, {})

    @classmethod
    def _get_meta_subclass(mcs, new_cls_meta: type, default_meta_cls: type):
        """
        Returns a metadata class with the class specific values plus default values.

        :param new_cls_meta: Metadata class declared in the new class.
        :param default_meta_cls: Default metadata class to inherit defaults from.
        :return:
        """

        # Custom Meta should be at the beginning
        if new_cls_meta is not None:
            bases = (new_cls_meta, default_meta_cls)
        else:
            bases = (default_meta_cls,)

        return type(mcs.meta_attr, bases, {})

    @classmethod
    def factory(mcs, meta_attr, default_meta_attr):
        """
        Returns a ready to use metadata metaclass.

        :param meta_attr: Name of the attribute holding class specific metadata.
        :param default_meta_attr: Name of the attribute holding default metadata.
        :return: Metaclass ready to be used.
        """
        return type(
            mcs.__name__,
            (mcs, type),
            {"meta_attr": meta_attr, "default_meta_attr": default_meta_attr},
        )
