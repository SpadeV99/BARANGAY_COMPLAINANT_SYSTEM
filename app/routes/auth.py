from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms.user_forms import RoleForm, DeleteUserForm, AddUserForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
            
    return render_template('auth/login.html', title='Login')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        contact_number = request.form.get('contact_number')
        address = request.form.get('address')
        
        user_exists = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
        
        if user_exists:
            flash('Username or email already exists.', 'danger')
        else:
            new_user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                contact_number=contact_number,
                address=address
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/register.html', title='Register')

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.email = request.form.get('email')
        current_user.contact_number = request.form.get('contact_number')
        current_user.address = request.form.get('address')
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        
    return render_template('auth/profile.html', title='Profile')

@auth.route('/users')
@login_required
def manage_users():
    if current_user.role not in ['admin', 'staff']:
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('main.dashboard'))
        
    users = User.query.all()
    return render_template('auth/users.html', users=users, title='Manage Users')

@auth.route('/users/view/<int:user_id>')
@login_required
def view_user(user_id):
    if current_user.role not in ['admin', 'staff']:
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user = User.query.get_or_404(user_id)
    return render_template('auth/user_details.html', user=user, title=f'User Details - {user.username}')

@auth.route('/users/edit-role/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user_role(user_id):
    if current_user.role != 'admin':
        flash('You are not authorized to edit user roles.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user = User.query.get_or_404(user_id)
    form = RoleForm()
    
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.commit()
        flash(f'Role for {user.username} has been updated.', 'success')
        return redirect(url_for('auth.manage_users'))
    
    # Pre-populate the form with the user's current role
    if request.method == 'GET':
        form.role.data = user.role
    
    return render_template('auth/edit_user_role.html', form=form, user=user, title=f'Edit Role - {user.username}')

@auth.route('/users/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash('You are not authorized to delete users.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting your own account
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('auth.manage_users'))
    
    form = DeleteUserForm()
    
    if form.validate_on_submit():
        if form.confirmation.data == 'DELETE':
            # Delete user's complaints
            # complaints = Complaint.query.filter_by(user_id=user.id).all()
            # for complaint in complaints:
            #     db.session.delete(complaint)
            
            # Delete user
            db.session.delete(user)
            db.session.commit()
            flash(f'User {user.username} has been deleted.', 'success')
            return redirect(url_for('auth.manage_users'))
        else:
            flash('Incorrect confirmation. The user was not deleted.', 'danger')
    
    return render_template('auth/delete_user.html', form=form, user=user, title=f'Delete User - {user.username}')

@auth.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        flash('You are not authorized to add users.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = AddUserForm()
    if form.validate_on_submit():
        user_exists = User.query.filter_by(username=form.username.data).first() or User.query.filter_by(email=form.email.data).first()
        
        if user_exists:
            flash('Username or email already exists.', 'danger')
        else:
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                contact_number=form.contact_number.data,
                address=form.address.data,
                role=form.role.data
            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            
            flash(f'User {form.username.data} has been created successfully!', 'success')
            return redirect(url_for('auth.manage_users'))
            
    return render_template('auth/add_user.html', form=form, title='Add User')