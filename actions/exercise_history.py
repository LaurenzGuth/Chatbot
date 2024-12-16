class ExerciseHistory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExerciseHistory, cls).__new__(cls)
            cls._instance.last_exercises = []
        return cls._instance

    def add_exercise(self, exercise_id):
        self.last_exercises.append(exercise_id)
        if len(self.last_exercises) > 5:
            self.last_exercises.pop(0)

    def get_last_exercises(self):
        return self.last_exercises