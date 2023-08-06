#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
#
# This file is part of Hive Appier Framework.
#
# Hive Appier Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Appier Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Appier Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

from appier_extras.parts.admin.models import base

class Locale(base.Base):

    locale = appier.field(
        index = "all",
        default = True
    )

    context = appier.field(
        index = "all"
    )

    data_j = appier.field(
        type = dict,
        private = True,
        meta = "longmap",
        description = "JSON Data"
    )

    count_l = appier.field(
        type = int,
        initial = 0,
        description = "Count"
    )

    @classmethod
    def setup(cls):
        super(Locale, cls).setup()
        cls._flush()
        appier.get_bus().bind("locale/reload", cls._flush)

    @classmethod
    def validate(cls):
        return super(Locale, cls).validate() + [
            appier.not_null("locale"),
            appier.not_empty("locale"),
            appier.is_regex("locale", "^[a-z]{2}(?:_[a-z]{2}(?:_[a-z]+)?)?$"),

            appier.not_null("data_j"),
            appier.not_empty("data_j")
        ]

    @classmethod
    def list_names(cls):
        return ["locale", "context", "description", "count_l"]

    @classmethod
    def bundles_d(cls, locale = None):
        locales = cls.find_e(rules = False)
        return dict([((locale.locale, locale.context or None), locale.data_u) for locale in locales])

    @classmethod
    @appier.operation(
        name = "Import Bundle",
        parameters = (
            ("JSON File", "file", "file"),
            ("Locale", "locale", str),
            ("Context", "context", str)
        ),
        factory = True
    )
    def import_bundle_s(cls, file, locale, context = None, strict = False):
        context = context or None
        data_j = cls._json_read(file)
        conditions = cls._conditions(locale, context = context)
        locale_e = cls.get(rules = False, raise_e = False, **{"$and" : conditions})
        if locale_e: locale_e.data_j.update(data_j)
        else: locale_e = cls(locale = locale, context = context, data_j = data_j)
        locale_e.save()
        return locale_e

    @classmethod
    @appier.operation(
        name = "Import CSV",
        parameters = (("CSV File", "file", "file"),)
    )
    def import_csv_s(cls, file):
        csv_reader = cls._csv_read(file)
        header = next(csv_reader)

        result = dict()
        locales_n = header[1:]
        for line in csv_reader:
            name, locales_v = line[0], line[1:]
            for locale_n, locale_v in zip(locales_n, locales_v):
                if not locale_v: continue
                locale_m = result.get(locale_n, {})
                locale_m[name] = locale_v
                result[locale_n] = locale_m

        for locale, data_j in appier.legacy.iteritems(result):
            conditions = cls._conditions(locale)
            locale_e = cls.get(rules = False, raise_e = False, **{"$and" : conditions})
            if locale_e: locale_e.data_j.update(data_j)
            else: locale_e = cls(locale = locale, data_j = data_j)
            locale_e.save()

    @classmethod
    @appier.link(name = "Export CSV", context = True)
    def list_csv_url(cls, view = None, context = None, absolute = False):
        return appier.get_app().url_for(
            "admin.list_locales_csv",
            view = view,
            context = context,
            absolute = absolute
        )

    @classmethod
    @appier.view(
        name = "Explorer",
        parameters = (("Context", "context", str),)
    )
    def explorer_v(cls, context, *args, **kwargs):
        kwargs["sort"] = kwargs.get("sort", [("id", -1)])
        if context: kwargs.update(context = context)
        return appier.lazy_dict(
            model = cls,
            kwargs = kwargs,
            entities = appier.lazy(lambda: cls.find(*args, **kwargs)),
            page = appier.lazy(lambda: cls.paginate(*args, **kwargs))
        )

    @classmethod
    def _flush(cls):
        # retrieves the dictionary of bundles currently
        # enabled in the data source
        bundles_d = cls.bundles_d()

        # iterates over the complete set of locale data pairs
        # in the bundles dictionary to set these bundles (locales)
        for (locale, context), data_j in appier.legacy.iteritems(bundles_d):
            appier.get_app()._register_bundle(data_j, locale, context = context)

    @classmethod
    def _escape(cls, data_j, target = ".", sequence = "::"):
        data_j = dict(data_j)
        for key, value in appier.legacy.items(data_j):
            _key = key.replace(target, sequence)
            if _key == key: continue
            data_j[_key] = value
            del data_j[key]
        return data_j

    @classmethod
    def _unescape(cls, data_j, target = ".", sequence = "::"):
        return cls._escape(data_j, target = sequence, sequence = target)

    @classmethod
    def _conditions(cls, locale, context = None):
        conditions = []
        conditions.append(dict(locale = locale))
        if context: conditions.append(dict(context = context))
        else: conditions.append({"$or" : [dict(context = ""), dict(context = None)]})
        return conditions

    def pre_create(self):
        base.Base.pre_create(self)
        self.count_l = len(self.data_j)
        self.data_j = self.__class__._escape(self.data_j)

    def pre_update(self):
        appier.Model.pre_update(self)
        self.count_l = len(self.data_j)
        self.data_j = self.__class__._escape(self.data_j)

    def post_create(self):
        base.Base.post_create(self)
        self.owner.trigger_bus("locale/reload")

    def post_update(self):
        base.Base.post_update(self)
        self.owner.trigger_bus("locale/reload")

    def post_delete(self):
        base.Base.post_delete(self)
        self.owner.trigger_bus("locale/reload")

    @appier.operation(
        name = "Set Context",
        parameters = (("Context", "context", str),)
    )
    def set_context_s(self, context):
        locale = self.reload(rules = False)
        locale.context = context
        locale.save()

    @appier.link(name = "Export Bundle")
    def bundle_url(self, absolute = False):
        return appier.get_app().url_for(
            "admin.bundle_locale_json",
            id = self.id,
            absolute = absolute
        )

    @property
    def data_u(self):
        cls = self.__class__
        return cls._unescape(self.data_j)
