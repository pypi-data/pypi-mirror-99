## -*- coding: utf-8 -*-
<%doc>

camcops_server/templates/menu/report_offer.mako

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

<%inherit file="base_web_form.mako"/>

<%!
from camcops_server.cc_modules.cc_pyramid import Routes
%>

<%include file="db_user_info.mako"/>

<h1>${_("Configure report:")} ${ report.title(request) | h }</h1>

${ form }

<div>
    <a href="${request.route_url(Routes.REPORTS_MENU)}">${_("Return to reports menu")}</a>
</div>
<%include file="to_main_menu.mako"/>
