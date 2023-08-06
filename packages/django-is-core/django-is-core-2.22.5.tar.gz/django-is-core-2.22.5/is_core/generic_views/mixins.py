from django.utils.functional import cached_property
from django.http import Http404

from chamber.shortcuts import get_object_or_404

from is_core.patterns import reverse_pattern

from .exceptions import GenericViewException


class ListParentMixin:

    def list_bread_crumbs_menu_item(self):
        from is_core.menu import LinkMenuItem

        list_pattern = self.core.ui_patterns.get('list')
        list_view = list_pattern.get_view(self.request)
        return LinkMenuItem(
            list_view.list_verbose_name % {
                'verbose_name': list_view.verbose_name,
                'verbose_name_plural': list_view.verbose_name_plural
            },
            list_pattern.get_url_string(self.request),
            active=not self.add_current_to_breadcrumbs
        )

    def parent_bread_crumbs_menu_items(self):
        menu_items = []
        if 'list' in self.core.ui_patterns and self.core.ui_patterns.get('list').has_permission('get', self.request):
            menu_items.append(self.list_bread_crumbs_menu_item())
        return menu_items

    def bread_crumbs_menu_items(self):
        return self.parent_bread_crumbs_menu_items() + super(ListParentMixin, self).bread_crumbs_menu_items()


class DetailParentMixin(ListParentMixin):

    def edit_bread_crumbs_menu_item(self):
        from is_core.menu import LinkMenuItem

        detail_pattern = self.core.ui_patterns.get('detail')
        detail_view = detail_pattern.get_view(self.request)
        parent_obj = self.get_parent_obj()
        if not isinstance(parent_obj, detail_view.model):
            raise GenericViewException('Parent obj must be instance of edit view model')

        return LinkMenuItem(detail_view.detail_verbose_name %
                            {'verbose_name': detail_view.verbose_name,
                             'verbose_name_plural': detail_view.verbose_name_plural,
                             'obj': parent_obj},
                            detail_pattern.get_url_string(self.request, view_kwargs={'pk': parent_obj.pk}),
                            active=not self.add_current_to_breadcrumbs)

    def parent_bread_crumbs_menu_items(self):
        menu_items = super().parent_bread_crumbs_menu_items()
        if ('detail' in self.core.ui_patterns and
                self.core.ui_patterns.get('detail').has_permission('get', self.request, obj=self.get_obj())):
            menu_items.append(self.edit_bread_crumbs_menu_item())
        return menu_items

    def get_parent_obj(self):
        return self.get_obj()


class TabItem:

    def __init__(self, pattern_name, label, can_show=None, is_active=None, pattern_kwargs=None,
                 is_active_starts_with=True):
        self._pattern_name = pattern_name
        self._label = label
        self._is_active = is_active
        self._pattern_kwargs = pattern_kwargs
        self._can_show = can_show
        self._is_active_starts_with = is_active_starts_with

    @cached_property
    def pattern(self):
        pattern = reverse_pattern(self._pattern_name)
        assert pattern is not None, 'Invalid pattern name {} in TabItem'.format(self._pattern_name)
        return pattern

    def get_pattern_kwargs(self, view):
        pattern_kwargs = self._pattern_kwargs or {}
        return pattern_kwargs(view) if hasattr(pattern_kwargs, '__call__') else pattern_kwargs

    def can_show(self, view):
        can_show = self._can_show
        if can_show is not None:
            return can_show(view) if hasattr(can_show, '__call__') else can_show
        else:
            return self.pattern.has_permission('get', view.request, view_kwargs=self.get_pattern_kwargs(view))

    def get_url(self, view):
        return self.pattern.get_url_string(view.request, view_kwargs=self.get_pattern_kwargs(view))

    def is_active(self, view):
        is_active = self._is_active
        if is_active is not None:
            return is_active(view) if hasattr(is_active, '__call__') else is_active
        else:
            return (
                (self._is_active_starts_with and view.request.path.startswith(self.get_url(view))) or
                (not self._is_active_starts_with and view.request.path == self.get_url(view))
            )

    def get_menu_link_item_or_none(self, view):
        from is_core.menu import LinkMenuItem

        return LinkMenuItem(
            self._label, self.get_url(view), active=self.is_active(view)) if self.can_show(view) else None


class TabsViewMixin:

    tabs = ()

    def get_tabs(self):
        return self.tabs

    def get_tab_menu_items(self):
        return [tab.get_menu_link_item_or_none(self) for tab in self.get_tabs() if tab.can_show(self)]

    def get_context_data(self, **kwargs):
        context_data = super(TabsViewMixin, self).get_context_data(**kwargs)
        context_data.update({
            'tabs': self.get_tab_menu_items(),
        })
        return context_data


class GetCoreObjViewMixin:

    pk_name = 'pk'

    def get_obj_filters(self):
        filters = {'pk': self.kwargs.get(self.pk_name)}
        return filters

    def _has_permission(self, name, obj=None):
        obj = obj or self.get_obj()
        return super()._has_permission(name, obj=obj)

    _obj = None
    def get_obj(self, cached=True):
        if cached and self._obj:
            return self._obj
        obj = get_object_or_404(self.core.get_queryset(self.request), **self.get_obj_filters())
        if cached and not self._obj:
            self._obj = obj
        return obj

    def get_obj_or_none(self, cached=True):
        try:
            return self.get_obj(cached=cached)
        except Http404:
            return None

    def _get_disallowed_fields_from_permissions(self, obj=None):
        return super()._get_disallowed_fields_from_permissions(obj=obj or self.get_obj())

    def _get_readonly_fields_from_permissions(self, obj=None):
        return super()._get_readonly_fields_from_permissions(obj=obj or self.get_obj())
