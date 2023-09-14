def calculate_grade(score):
    if 80 <= score <= 100:
        return 'A'
    elif 75 <= score < 80:
        return 'B+'
    elif 70 <= score < 75:
        return 'B'
    elif 65 <= score < 70:
        return 'C+'
    elif 60 <= score < 65:
        return 'C'
    elif 55 <= score < 60:
        return 'D+'
    elif 50 <= score < 55:
        return 'D'
    else:
        return 'F'
def calculate_gpa(grades, credits):
    # Define grade point values for each grade
    grade_points = {
        'A': 4.0,
        'B+': 3.5,
        'B': 3.0,
        'C+': 2.5,
        'C': 2.0,
        'D+': 1.5,
        'D': 1.0,
        'F': 0.0,
    }

    total_grade_points = 0
    total_credits = 0

    for grade, credit in zip(grades, credits):
        # Ensure that the grade is valid
        if grade in grade_points:
            total_grade_points += grade_points[grade] * credit
            total_credits += credit

    if total_credits == 0:
        return 0.0  # Return 0.0 GPA if no credits or invalid grades

    gpa = total_grade_points / total_credits
    return round(gpa, 2)  # Round GPA to two decimal places