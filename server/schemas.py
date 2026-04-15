from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import date

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.OneOf(['Strength', 'Cardio', 'Flexibility', 'Balance', 'Other']))
    equipment_needed = fields.Bool(required=False, missing=False)
    
    @validates('name')
    def validate_name_not_empty(self, value):
        if not value.strip():
            raise ValidationError("Exercise name cannot be empty or whitespace")

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True)
    
    @validates('date')
    def validate_date_not_future(self, value):
        if value > date.today():
            raise ValidationError("Workout date cannot be in the future")


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=0))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=0))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=0))
    
    @validates('reps', 'sets', 'duration_seconds')
    def validate_at_least_one(self, data, **kwargs):
        # For deserialization, we need to check the whole object
        pass
    
    @validates('reps')
    def validate_reps_none_or_positive(self, value):
        if value is not None and value < 0:
            raise ValidationError("Reps cannot be negative")
    
    @validates('sets')
    def validate_sets_none_or_positive(self, value):
        if value is not None and value < 0:
            raise ValidationError("Sets cannot be negative")
    
    @validates('duration_seconds')
    def validate_duration_none_or_positive(self, value):
        if value is not None and value < 0:
            raise ValidationError("Duration seconds cannot be negative")
    
    # Cross-field validation: at least one metric provided and >0
    @validates('workout_id')
    def validate_has_metric(self, value, **kwargs):
        pass

# For POST requests to create a WorkoutExercise 
def validate_workout_exercise(data):
    reps = data.get('reps')
    sets = data.get('sets')
    duration = data.get('duration_seconds')
    if (reps is None or reps == 0) and (sets is None or sets == 0) and (duration is None or duration == 0):
        raise ValidationError("At least one of reps, sets, or duration_seconds must be greater than 0")
    return data

# For detailed GET responses
class WorkoutExerciseWithExerciseSchema(Schema):
    id = fields.Int()
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()
    exercise = fields.Nested(ExerciseBasicSchema)

class WorkoutWithExercisesSchema(WorkoutSchema):
    workout_exercises = fields.Nested(WorkoutExerciseWithExerciseSchema, many=True)

class WorkoutExerciseWithWorkoutSchema(Schema):
    id = fields.Int()
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()
    workout = fields.Nested(WorkoutBasicSchema)

class ExerciseWithWorkoutsSchema(ExerciseSchema):
    workout_exercises = fields.Nested(WorkoutExerciseWithWorkoutSchema, many=True)