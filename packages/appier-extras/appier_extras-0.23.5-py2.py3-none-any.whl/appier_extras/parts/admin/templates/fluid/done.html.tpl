{% extends "admin/admin.simple.html.tpl" %}
{% block title %}Confirmation{% endblock %}
{% block body_style %}{{ super() }} {% if background %}background:url({{ background }});{% endif %}{% endblock %}
{% block content %}
    <div class="login-panel">
        <h1>Confirmation sent</h1>
        <h4>You'll receive an email for account recovery</h4>
        <p>
            Please check your spam folder if the email doesn’t appear within a few minutes.
        </p>
    </div>
{% endblock %}
