from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from .models import db, Exercise, Workout, WorkoutExercise
from .schemas import (
    ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema,
    WorkoutWithExercisesSchema, ExerciseWithWorkoutsSchema,
    validate_workout_exercise
)
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Initialize schemas
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
workout_with_exercises_schema = WorkoutWithExercisesSchema()
exercise_with_workouts_schema = ExerciseWithWorkoutsSchema()

# ---------- Workout Endpoints ----------
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.jsonify(workouts)

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return workout_with_exercises_schema.jsonify(workout)

@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.json)
        new_workout = Workout(
            date=data['date'],
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
        return workout_schema.jsonify(new_workout), 201
    except ValidationError as err:
        return make_response(jsonify(err.messages), 400)
    except ValueError as err:
        return make_response(jsonify({"error": str(err)}), 400)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return make_response('', 204)

# ---------- Exercise Endpoints ----------
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.jsonify(exercises)

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return exercise_with_workouts_schema.jsonify(exercise)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.json)
        new_exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data.get('equipment_needed', False)
        )
        db.session.add(new_exercise)
        db.session.commit()
        return exercise_schema.jsonify(new_exercise), 201
    except ValidationError as err:
        return make_response(jsonify(err.messages), 400)
    except ValueError as err:
        return make_response(jsonify({"error": str(err)}), 400)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return make_response('', 204)

# ---------- WorkoutExercise Endpoint (add exercise to workout) ----------
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    # Verify that both workout and exercise exist
    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(exercise_id)
    
    try:
        data = workout_exercise_schema.load(request.json)
        # Override ids from URL to prevent mismatch
        data['workout_id'] = workout_id
        data['exercise_id'] = exercise_id
        
        # Cross-field validation for at least one metric > 0
        validate_workout_exercise(data)
        
        new_we = WorkoutExercise(
            workout_id=data['workout_id'],
            exercise_id=data['exercise_id'],
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(new_we)
        db.session.commit()
        return workout_exercise_schema.jsonify(new_we), 201
    except ValidationError as err:
        return make_response(jsonify(err.messages), 400)
    except ValueError as err:
        return make_response(jsonify({"error": str(err)}), 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)