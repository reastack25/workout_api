from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates
from datetime import date

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    
    # Table constraint
    __table_args__ = (
        CheckConstraint('length(name) > 0', name='check_exercise_name_length'),
    )
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Exercise name cannot be empty")
        return name.strip()
    
    @validates('category')
    def validate_category(self, key, category):
        allowed = ['Strength', 'Cardio', 'Flexibility', 'Balance', 'Other']
        if category not in allowed:
            raise ValueError(f"Category must be one of {allowed}")
        return category

class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    
    # Table constraints
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
        CheckConstraint('date <= CURRENT_DATE', name='check_date_not_future'),  # SQLite requires CURRENT_DATE, works
    )
    
    @validates('duration_minutes')
    def validate_duration(self, key, minutes):
        if minutes <= 0:
            raise ValueError("Duration must be positive")
        return minutes
    
    @validates('date')
    def validate_date(self, key, value):
        if value > date.today():
            raise ValueError("Workout date cannot be in the future")
        return value

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id', ondelete='CASCADE'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id', ondelete='CASCADE'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    
    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')
    
    # Table constraints
    __table_args__ = (
        CheckConstraint('reps >= 0', name='check_reps_non_negative'),
        CheckConstraint('sets >= 0', name='check_sets_non_negative'),
        CheckConstraint('duration_seconds >= 0', name='check_duration_seconds_non_negative'),
    )
    
    @validates('reps', 'sets', 'duration_seconds')
    def validate_non_negative(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key} must be non-negative")
        return value
    
    @validates('reps', 'sets', 'duration_seconds')
    def validate_at_least_one_positive(self, key, value):
        # This runs after each field is set; we need to check all three together.
        return value
    
    # Model-level validation that at least one of reps, sets, duration_seconds is >0
    @validates('workout_id')  # after all fields are set, we can validate in one place
    def validate_has_metric(self, key, workout_id):
        # Only run when all three fields are present 
        if hasattr(self, 'reps') and hasattr(self, 'sets') and hasattr(self, 'duration_seconds'):
            if (self.reps is None or self.reps == 0) and (self.sets is None or self.sets == 0) and (self.duration_seconds is None or self.duration_seconds == 0):
                raise ValueError("At least one of reps, sets, or duration_seconds must be > 0")
        return workout_id