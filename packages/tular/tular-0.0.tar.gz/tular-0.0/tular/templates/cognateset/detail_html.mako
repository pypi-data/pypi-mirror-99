<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "cognatesets" %>

<%block name="head">
    <script src="${request.static_url('tular:static/alignment.js')}"></script>
    <link rel="stylesheet" href="${request.static_url('tular:static/alignment.css')}" type="text/css"/>
    <script>
        $( document ).ready(function() {
            var alignments = document.getElementsByClassName("alignment");
            for (var i=0,alignment; alignment=alignments[i]; i++) {
                alignment.innerHTML = plotWord(alignment.innerHTML, 'span');
            }
        });
    </script>
</%block>

<h2>${_('Cognate set')} ${ctx.id}</h2>

From dataset ${h.link(request, ctx.contribution)}
<small>cite as</small>
<blockquote>
    ${ctx.contribution.description}
</blockquote>

<h3>${len(ctx.cognates)} Counterparts</h3>
<%util:table items="${ctx.cognates}" args="item" options="${dict(bInfo=True)}">
    <%def name="head()">
        <th>Counterpart</th>
        <th>Language</th>
        <th>Concept</th>
        <th>certain</th>
        <th>alignment</th>
    </%def>
    <td>${h.link(request, item.counterpart)}</td>
    <td>${h.link(request, item.counterpart.valueset.language)}</td>
    <td>${h.link(request, item.counterpart.valueset.parameter)}</td>
    <td>${'no' if item.doubt else 'yes'}</td>
    <td>
        <span class="alignment">${item.alignment}</span>
    </td>
</%util:table>