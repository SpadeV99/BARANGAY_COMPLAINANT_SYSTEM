from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.complaint import Complaint
from app.models.user import User
from datetime import datetime, timedelta
from sqlalchemy import func

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', title='Welcome')

@main.route('/dashboard')
@login_required
def dashboard():
    # Common data
    data = {}
    
    # Admin/Staff specific data
    if current_user.role in ['admin', 'staff']:
        # Complaint statistics
        data['total_complaints'] = Complaint.query.count()
        data['pending_complaints'] = Complaint.query.filter_by(status='pending').count()
        data['processing_complaints'] = Complaint.query.filter_by(status='processing').count()
        data['resolved_complaints'] = Complaint.query.filter_by(status='resolved').count()
        
        # Recent complaints
        data['recent_complaints'] = Complaint.query.order_by(Complaint.date_filed.desc()).limit(5).all()
        
        # Pending complaints that need action
        data['pending_complaints_list'] = Complaint.query.filter_by(status='pending').order_by(Complaint.date_filed).limit(5).all()
        
        # User statistics
        data['total_users'] = User.query.count()
        month_ago = datetime.utcnow() - timedelta(days=30)
        data['new_users_this_month'] = User.query.filter(User.date_registered >= month_ago).count()
    
    # Resident specific data
    else:
        data['user_complaints_count'] = Complaint.query.filter_by(complainant_id=current_user.id).count()
        data['user_pending_count'] = Complaint.query.filter_by(complainant_id=current_user.id, status='pending').count()
        data['user_resolved_count'] = Complaint.query.filter_by(complainant_id=current_user.id, status='resolved').count()
        data['user_complaints'] = Complaint.query.filter_by(complainant_id=current_user.id).order_by(Complaint.date_filed.desc()).limit(5).all()
    
    return render_template('dashboard.html', title='Dashboard', **data)

@main.route('/documentation')
def documentation():
    return render_template('documentation.html')