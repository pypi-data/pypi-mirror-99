
Overview
========

Flask-Authorize is a Flask extension designed to simplify the process of incorporating Access Control Lists (ACLs) and Role-Based Access Control (RBAC) into applications housing sensitive data, allowing developers to focus on the actual code for their application instead of logic for enforcing permissions. It uses a unix-like permissions scheme for enforcing access permissions on existing content, and also provides mechanisms for globally enforcing permissions throughout an application.

There are quite a few packages designed to simplify the process of adding ACLs and RBAC to a Flask application:

* `Flask-Principal <https://pythonhosted.org/Flask-Principal/>`_
* `Flask-ACL <https://mikeboers.github.io/Flask-ACL/>`_
* `Flask-RBAC <https://flask-rbac.readthedocs.io/en/latest/>`_
* `Flask-Security <https://pythonhosted.org/Flask-Security/>`_

And each provides a different developer experience and makes different assumptions in their design. This package is yet another take at solving the same problem, resulting in a slightly different development experience when working with Flask applications. The developers of this package recommend you check out these alternatives along with Flask-Authorize to see if they fit your needs better.


A Minimal Application
---------------------


Setting up the flask application with extensions:


.. code-block:: python

    from flask import Flask
    from flask_login import LoginManager
    from flask_sqlalchemy import SQLAlchemy
    from flask_authorize import Authorize

    app = Flask(__name__)
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    login = LoginManager(app)
    authorize = Authorize(app)


Defining database models:

.. code-block:: python

    from flask_authorize import RestrictionsMixin, AllowancesMixin
    from flask_authorize import PermissionsMixin


    # mapping tables
    UserGroup = db.Table(
        'user_group', db.Model.metadata,
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
    )


    UserRole = db.Table(
        'user_role', db.Model.metadata,
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
    )


    # models
    class User(db.Model):
        __tablename__ = 'users'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), nullable=False, unique=True)

        # `roles` and `groups` are reserved words that *must* be defined
        # on the `User` model to use group- or role-based authorization.
        roles = db.relationship('Role', secondary=UserRole)
        groups = db.relationship('Group', secondary=UserGroup)


    class Group(db.Model, RestrictionsMixin):
        __tablename__ = 'groups'
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), nullable=False, unique=True)


    class Role(db.Model, AllowancesMixin):
        __tablename__ = 'roles'
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), nullable=False, unique=True)


    class Article(db.Model, PermissionsMixin):
        __tablename__ = 'articles'
        __permissions__ = dict(
            owner=['read', 'update', 'delete', 'revoke'],
            group=['read', 'update'],
            other=['read']
        )

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), index=True, nullable=False)
        content = db.Column(db.Text)


Defining endpoint actions:

.. code-block:: python

    from flask import jsonify
    from werkzeug import NotFound, Unauthorized

    @app.route('/articles', methods=['POST'])
    @login.logged_in
    @authorize.create(Article)
    def article():
        article = Article(
          name=request.json.get('name'),
          content=request.json.get('content'),
        )
        db.session.add(article)
        db.session.commit()
        return jsonify(msg='Created Article'), 200

    @app.route('/articles/<int:ident>', methods=['GET', 'PUT', 'DELETE'])
    @login.logged_in
    def single_article(ident):
        article = db.session.query(Article).filter_by(id=ident).first()
        if not article:
            raise NotFound

        if request.method == 'GET':

            # check if the current user is authorized to read the article
            if not authorize.read(article):
                raise Unauthorized

            return jsonify(id=article.id, name=article.name), 200

        elif request.method == 'PUT':

            # check if the current user is authorized to update to the article
            if not authorize.update(article):
                raise Unauthorized

            # update values
            if 'name' in request.json:
                article.name = request.json['name']
            if 'content' in request.json:
                article.content = request.json['content']
            db.session.commit()

            return jsonify(id=article.id, name=article.name), 200

        elif request.method == 'DELETE':

            # check if the current user is associated with the 'admin' role
            if not authorize.delete(article) or \
               not authorize.has_role('admin'):
                raise Unauthorized

            db.session.delete(article)
            db.session.commit()

        return

    @app.route('/articles/<int:ident>/revoke', methods=['POST'])
    @login.logged_in
    def revoke_article(ident):
        article = db.session.query(Article).filter_by(id=ident).first()
        if not article:
            raise NotFound

        # check if the current user can revoke the article
        if not authorize.revoke(article):
            raise Unauthorized

        article.revoked = True
        db.session.commit()

        return


Additionally, if you've configured your application to dispatch request processing to API functions, you can use the ``authorize`` extension object as a decorator:

.. code-block:: python

    @authorize.create(Article)
    def create_article(name):
        article = Article(name=name)
        db.session.add(article)
        db.session.commit()
        return article

    @authorize.read
    def read_article(article):
        return article

    @authorize.update
    def update_article(article, **kwargs):
        for key, value in request.json.items():
            setattr(article, key, value)
        db.session.commit()
        return article

    @authorize.delete
    def delete_article(article):
        db.session.delete(article)
        return

    @authorize.revoke
    def revoke_article(article):
        article.revoke = True
        db.session.commit()
        return

    @authorize.has_role('admin')
    def get_admin_articles():
        pass


Using the extension as a decorator goes a long way in removing boilerplate associated with permissions checking. Additionally, using the ``authorize`` extension object as a decorator will implicitly check the current user's access to each argument or keyword argument to the function. For example, if your method takes two ``Article`` objects and merges them into one, you can add permissions for both operations like so:

.. code-block:: python

    @authorize.read
    @authorize.create(Article)
    def merge_articles(article1, article2):
        new_article = Article(name=article1.name + article.2.name)
        db.session.add(new_article)
        db.session.delete(article1, article2)
        db.session.commit()
        return new_article


This function will ensure that the current user has read access to both articles and also create permissions on the **Article** model itself. If the authorization criteria aren't satisfied, an ``Unauthorized`` error will be thrown.


Finally, the ``authorize`` operator is also available in Jinja templates:

.. code-block:: html

    <!-- button for creating new article -->
    {% if authorize.create('articles') %}
        <button>Create Article</button>
    {% endif %}

    <!-- display article feed -->
    {% for article in articles %}

        <!-- show article if user has read access -->
        {% if authorize.read(article) %}
            <h1>{{ article.name }}</h1>

            <!-- add edit button for users who can update-->
            {% if authorize.update(article) %}
                <button>Update Article</button>
            {% endif %}

            <!-- add delete button for administrators -->
            {% if authorize.in_group('admins') %}
                <button>Delete Article</button>
            {% endif %}

        {% endif %}
    {% endfor %}



Usage without Flask-Login
-------------------------

By default, this module uses the Flask-Login extension for determining the current user. If you aren't using that module, you simply need to provide a function to the plugin that will return the current user:

.. code-block:: python

    from flask import Flask, g
    from flask_authorize import Authorize

    def my_current_user():
        """
        Return current user to check authorization against.
        """
        return g.user

    # using the declarative method for setting up the extension
    app = Flask(__name__)
    authorize = Authorize(current_user=my_current_user)
    authorize.init_app(app)


For more in-depth discussion on design considerations and how to fully utilize the plugin, see the `User Guide <./usage.html>`_.
