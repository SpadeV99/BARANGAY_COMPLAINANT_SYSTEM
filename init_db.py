from app import create_app, db
from app.models.user import User
from app.models.complaint import Complaint
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

app = create_app()

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin_exists = User.query.filter_by(username='admin').first()
        
        if not admin_exists:
            print("Creating admin user...")
            # Create admin user
            admin = User(
                username='admin',
                email='admin@barangay.gov',
                first_name='Admin',
                last_name='User',
                contact_number='09123456789',
                address='Barangay Hall',
                role='admin'
            )
            admin.set_password('admin123')  # Change this in production!
            db.session.add(admin)
            
            # Create staff user
            staff = User(
                username='staff',
                email='staff@barangay.gov',
                first_name='Staff',
                last_name='User',
                contact_number='09123456788',
                address='Barangay Hall',
                role='staff'
            )
            staff.set_password('staff123')  # Change this in production!
            db.session.add(staff)
            
            # Create some sample resident users
            for i in range(1, 6):
                resident = User(
                    username=f'resident{i}',
                    email=f'resident{i}@example.com',
                    first_name=f'Resident{i}',
                    last_name='Surname',
                    contact_number=f'091234567{i}0',
                    address=f'123 Street, Purok {i}',
                    role='resident',
                    date_registered=datetime.utcnow() - timedelta(days=random.randint(0, 60))
                )
                resident.set_password('password123')  # Change this in production!
                db.session.add(resident)
            
            db.session.commit()
            
            # Create some sample complaints
            status_options = ['pending', 'processing', 'resolved', 'dismissed']
            titles = [
                'Noise complaint from neighbor', 
                'Illegal parking in front of residence',
                'Water supply issue',
                'Garbage collection problem',
                'Public disturbance report',
                'Stray animals in the area',
                'Drainage system blocked',
                'Street light not working',
                'Vandalism in public park',
                'Business operating without permit'
            ]
            
            residents = User.query.filter_by(role='resident').all()
            staff_members = User.query.filter(User.role.in_(['admin', 'staff'])).all()
            
            print("Creating sample complaints...")
            for i in range(20):
                # Select random data
                random_resident = random.choice(residents)
                random_staff = random.choice(staff_members) if random.random() > 0.3 else None
                random_title = random.choice(titles)
                random_status = random.choice(status_options)
                random_days_ago = random.randint(1, 90)
                
                complaint = Complaint(
                    title=random_title,
                    description=f"This is a sample description for the complaint: {random_title}. The issue occurred on {datetime.utcnow() - timedelta(days=random_days_ago)} and needs attention.",
                    complainant_id=random_resident.id,
                    date_filed=datetime.utcnow() - timedelta(days=random_days_ago),
                    status=random_status
                )
                
                if random_status in ['processing', 'resolved', 'dismissed']:
                    complaint.assigned_to = random_staff.id
                
                if random_status == 'resolved':
                    complaint.resolution = "Issue has been addressed by barangay officials."
                    complaint.resolution_date = datetime.utcnow() - timedelta(days=random_days_ago - random.randint(1, 5))
                
                db.session.add(complaint)
            
            db.session.commit()
            print("Database initialization completed successfully!")
        else:
            print("Database already initialized.")

if __name__ == '__main__':
    init_db()