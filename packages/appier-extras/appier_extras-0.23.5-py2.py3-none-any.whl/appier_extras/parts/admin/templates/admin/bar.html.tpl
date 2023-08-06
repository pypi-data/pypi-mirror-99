<div class="top-bar">
    <div class="container">
        <div class="logo">
            {% if owner.logo_url %}
                <a>
                    <img src="{{ owner.logo_url }}" />
                </a>
            {% else %}
                <a>{{ owner.description }}</a>
            {% endif %}
        </div>
        <div class="drop-field entities" placeholder="Search over some of the items"
             data-number_options="4">
            <li class="template">
                <div>
                    <p class="title">
                        <a href="%[url]">%[target_title]</a>
                    </p>
                    <p class="description">%[target_description]</p>
                </div>
            </li>
            <div class="data-source" data-url="{{ url_for('admin.search') }}" data-type="json"
                 data-timeout="0"></div>
        </div>
        <div class="right">
            <div class="menu system-menu">
                <div class="menu-button">
                    <a class="menu-link" data-no_left="1">{{ session.username }}</a>
                </div>
                <div class="menu-contents">
                    <div class="header-contents">
                        <img class="avatar-image" src="{{ url_for('admin.avatar_account', username = session.username) }}" />
                        <div class="avatar-contents">
                            <h2>
                                <a href="{{ url_for('admin.me_account') }}">{{ session.username }}</a>
                            </h2>
                            <h3>{{ session.email }}</h3>
                        </div>
                    </div>
                    <div class="footer-contents">
                        <a href="{{ url_for('admin.logout') }}">Logout</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
