## -*- coding: utf-8 -*-
<%doc>

camcops_server/templates/test/testpage.mako

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

<%inherit file="base_web.mako"/>
## <%page> DOES NOT PLAY NICELY WITH INHERITANCE ## <%page args="param1='<missing>'"/>

<%!
    import pprint
    from cardinal_pythonlib.debugging import get_caller_stack_info
%>

<div>
    Hello, I'm a Mako test template!<br>

    Parameter param1 is: ${param1 | h}<br>

    Request (in str format) is:<br>
    <pre>${request | h}</pre><br>

    request.environ (WSGI environment):<br>
    <pre>${pprint.pformat(request.environ) | h}</pre>

    pageargs:<br>
    <pre>${pprint.pformat(pageargs) | h}</pre>

    dir():<br>
    <pre>${pprint.pformat(dir()) | h}</pre>

    context.__dict__:<br>
    <pre>${pprint.pformat(context.__dict__) | h}</pre>

    request.__dict__:<br>
    <pre>${pprint.pformat(request.__dict__) | h}</pre>

    dir(request):<br>
    <pre>${pprint.pformat(dir(request)) | h}</pre>

    callers:<br>
    <pre>${show_call_stack()}</pre>

    ## See also:
    ## http://docs.makotemplates.org/en/latest/runtime.html#all-the-built-in-names
    ## https://stackoverflow.com/questions/10689162/output-all-variables-into-mako-template
</div>

<%def name="show_call_stack()">
    %for stack_info in get_caller_stack_info():
${stack_info | h}<br>
    %endfor
</%def>
