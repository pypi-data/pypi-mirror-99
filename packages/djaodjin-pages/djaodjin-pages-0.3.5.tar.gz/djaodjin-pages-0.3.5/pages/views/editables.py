# Copyright (c) 2021, Djaodjin Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import logging

from django.http import Http404
from django.views.generic import TemplateView

from .. import settings
from ..compat import NoReverseMatch, reverse
from ..models import RelationShip
from ..mixins import AccountMixin, TrailMixin
from ..utils import update_context_urls


LOGGER = logging.getLogger(__name__)


class PageElementEditableView(AccountMixin, TrailMixin, TemplateView):

    template_name = 'pages/element.html'

    @property
    def is_prefix(self):
        if not hasattr(self, '_is_prefix'):
            try:
                self._is_prefix = RelationShip.objects.filter(
                    orig_element=self.element).exists()
            except Http404:
                self._is_prefix = True
        return self._is_prefix

    def get_template_names(self):
        if self.is_prefix:
            # It is not a leaf, let's return the list view
            return ['pages/index.html']
        return super(PageElementEditableView, self).get_template_names()

    def get_context_data(self, **kwargs):
        context = super(PageElementEditableView, self).get_context_data(
            **kwargs)
        url_kwargs = {'path': self.path.strip('/')}
        for url_kwarg in [settings.ACCOUNT_URL_KWARG]:
            if url_kwarg in kwargs:
                url_kwargs.update({url_kwarg: kwargs[url_kwarg]})

        context = update_context_urls(context, {
            'edit': {
                'api_page_element_base': reverse('pages_api_edit_element',
                    kwargs={'path':''}),
                'api_medias': reverse('uploaded_media_elements',
                    kwargs={'path':''}),
            }
        })
        if self.is_prefix:
            context = update_context_urls(context, {
                'pages': {
                    'api_content': reverse('pages_api_edit', kwargs=url_kwargs),
                }
            })
        else:
            context = update_context_urls(context, {
                'pages': {
                    'api_content': reverse(
                        'pages_api_edit_element', kwargs=url_kwargs),
                    'api_follow': reverse('pages_api_follow',
                        args=(self.element,)),
                    'api_unfollow': reverse('pages_api_unfollow',
                        args=(self.element,)),
                    'api_downvote': reverse('pages_api_downvote',
                        args=(self.element,)),
                    'api_upvote': reverse('pages_api_upvote',
                        args=(self.element,)),
                    'api_comments': reverse('pages_api_comments',
                        args=(self.element,)),
                }
            })

        return context
