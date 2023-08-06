## -*- coding: utf-8 -*-
<%doc>

camcops_server/templates/css/css_pdf_no_paged_media.mako

===============================================================================

    Copyright (C) 2012-2020 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of CamCOPS.

    CamCOPS is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CamCOPS is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CamCOPS. If not, see <http://www.gnu.org/licenses/>.

===============================================================================

</%doc>

## Genuinely static, so we can cache it:
<%page cached="True" cache_region="local" cache_key="css_pdf_no_paged_media.mako"/>

<%inherit file="css_base.mako"/>

<%namespace file="def_css_constants.mako" import="_get_css_varargs"/>
<%def name="get_css_varargs()"><%
    return _get_css_varargs("pdf_no_paged_media")
%></%def>
