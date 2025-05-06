from app import db
from datetime import datetime

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_filed = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, processing, resolved, dismissed
    resolution = db.Column(db.Text)
    resolution_date = db.Column(db.DateTime)
    
    # Foreign Keys
    complainant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    complainant = db.relationship('User', foreign_keys=[complainant_id], backref='filed_complaints')
    handler = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_complaints')