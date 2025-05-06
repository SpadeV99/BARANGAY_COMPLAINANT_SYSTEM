from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app.models.complaint import Complaint
from app.models.user import User
from app import db
from datetime import datetime

complaints = Blueprint('complaints', __name__)

@complaints.route('/complaints')
@login_required
def list_complaints():
    if current_user.role == 'admin' or current_user.role == 'staff':
        all_complaints = Complaint.query.all()
    else:
        all_complaints = Complaint.query.filter_by(complainant_id=current_user.id).all()
        
    return render_template('complaints/list.html', complaints=all_complaints, title='Complaints')

@complaints.route('/complaints/new', methods=['GET', 'POST'])
@login_required
def new_complaint():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        new_complaint = Complaint(
            title=title,
            description=description,
            complainant_id=current_user.id
        )
        
        db.session.add(new_complaint)
        db.session.commit()
        flash('Your complaint has been submitted successfully!', 'success')
        return redirect(url_for('complaints.list_complaints'))
        
    return render_template('complaints/new.html', title='New Complaint')

@complaints.route('/complaints/<int:complaint_id>')
@login_required
def view_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    
    if complaint.complainant_id != current_user.id and current_user.role not in ['admin', 'staff']:
        flash('You are not authorized to view this complaint.', 'danger')
        return redirect(url_for('complaints.list_complaints'))
        
    return render_template('complaints/view.html', complaint=complaint, title='View Complaint')

@complaints.route('/complaints/<int:complaint_id>/update', methods=['GET', 'POST'])
@login_required
def update_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    
    if current_user.role not in ['admin', 'staff']:
        flash('You are not authorized to update complaint status.', 'danger')
        return redirect(url_for('complaints.list_complaints'))
        
    if request.method == 'POST':
        complaint.status = request.form.get('status')
        complaint.assigned_to = request.form.get('assigned_to')
        
        if complaint.status == 'resolved':
            complaint.resolution = request.form.get('resolution')
            complaint.resolution_date = datetime.utcnow()
            
        db.session.commit()
        flash('Complaint has been updated!', 'success')
        return redirect(url_for('complaints.view_complaint', complaint_id=complaint.id))
    
    staff_members = User.query.filter(User.role.in_(['admin', 'staff'])).all()
    return render_template('complaints/update.html', complaint=complaint, staff_members=staff_members, title='Update Complaint')