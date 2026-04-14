#!/usr/bin/env python3

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date, timedelta

with app.app_context():
    # Clear existing data
    db.session.query(WorkoutExercise).delete()
    db.session.query(Workout).delete()
    db.session.query(Exercise).delete()
    
    # Create exercises
    pushups = Exercise(name="Push-ups", category="Strength", equipment_needed=False)
    squats = Exercise(name="Squats", category="Strength", equipment_needed=False)
    running = Exercise(name="Running", category="Cardio", equipment_needed=False)
    plank = Exercise(name="Plank", category="Flexibility", equipment_needed=False)
    
    db.session.add_all([pushups, squats, running, plank])
    db.session.commit()
    
    # Create workouts
    workout1 = Workout(date=date.today() - timedelta(days=2), duration_minutes=30, notes="Morning full body")
    workout2 = Workout(date=date.today(), duration_minutes=45, notes="Evening cardio focus")
    
    db.session.add_all([workout1, workout2])
    db.session.commit()
    
    # Link exercises to workouts via WorkoutExercise
    we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=pushups.id, reps=15, sets=3, duration_seconds=None)
    we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=squats.id, reps=20, sets=4, duration_seconds=None)
    we3 = WorkoutExercise(workout_id=workout2.id, exercise_id=running.id, reps=None, sets=None, duration_seconds=1800)
    we4 = WorkoutExercise(workout_id=workout2.id, exercise_id=plank.id, reps=None, sets=2, duration_seconds=60)
    
    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()
    
    print("Database seeded successfully!")