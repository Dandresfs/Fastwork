#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django_filters
from django_filters import MethodFilter
from accounts.models import User
from django.db.models import Q

class AspiranteFilter(django_filters.FilterSet):
    email = MethodFilter(action='email_filter')
    departamento = MethodFilter(action='departamento_filter')
    ciudad = MethodFilter(action='ciudad_filter')
    titulo = MethodFilter(action='titulo_filter')
    class Meta:
        model = User
        fields = ['email']

    def email_filter(self, qs, value):
        if value not in (None, ''):
            values = [v for v in value.split(',')]
            q = Q()
            for q_object in values:
                name = "%s__%s" % ('email', 'icontains')
                q.add(Q(**{name:q_object}),Q.OR)
            return qs.filter(q)
        return qs

    def departamento_filter(self, qs, value):
        if value not in (None, ''):
            values = [v for v in value.split(',')]
            q = Q()
            for q_object in values:
                name = "%s__%s" % ('departamento', 'icontains')
                q.add(Q(**{name:q_object}),Q.OR)
            return qs.filter(q)
        return qs

    def ciudad_filter(self, qs, value):
        if value not in (None, ''):
            values = [v for v in value.split(',')]
            q = Q()
            for q_object in values:
                name = "%s__%s" % ('ciudad', 'icontains')
                q.add(Q(**{name:q_object}),Q.OR)
            return qs.filter(q)
        return qs

    def titulo_filter(self, qs, value):
        if value not in (None, ''):
            values = [v for v in value.split(',')]
            q = Q()
            for q_object in values:
                name = "%s__%s" % ('titulo', 'icontains')
                q.add(Q(**{name:q_object}),Q.OR)
            return qs.filter(q)
        return qs