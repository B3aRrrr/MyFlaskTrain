from flask import render_template,abort
from ..decorators import admin_required,permission_required
from . import main
from .forms import *
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..models import *
from flask_login import current_user



@main.route('/')
def index():
    return render_template('index.html')

@main.route('/edit-profile',methods=['GET','POST'])
def edit_profile():
    # Вызываем форму
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user',username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form=form)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user=user)


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return 'For administrators!'

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return 'For comment moderators!'
