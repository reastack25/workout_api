# workout_api
# Workout API

A RESTful backend API for a workout tracking application, built with **Flask**, **SQLAlchemy**, and **Marshmallow**.  
This API allows personal trainers to manage workouts and exercises, with support for many-to-many relationships and detailed metrics (reps, sets, duration).

---

## Features

- **Full CRUD** for workouts and exercises
- Add exercises to workouts with reps, sets, or duration
- **Database constraints** (positive duration, non‑negative reps/sets, unique exercise names, etc.)
- **Model‑level validations** (e.g., category whitelist, no future workout dates)
- **Schema‑level validations** (e.g., name length, at least one metric per WorkoutExercise)
- **Cascade delete** – removing a workout or exercise also removes its join table entries
- **Detailed serialization** – GET `/workouts/<id>` returns all associated exercises with their metrics

---

## Tech Stack

- Python 3.8+
- Flask 2.2.2
- Flask‑SQLAlchemy 3.0.3
- Flask‑Migrate 3.1.0
- Marshmallow 3.20.1
- SQLite (development)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/reastack25/workout_api
cd workout-api