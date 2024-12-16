import csv
import os
from grades_comments import understanding_level, contribution_level, lab_completion, engagement, punctuality, further_learning_level

# Reading form the .CSV file
def read_student_names(filename):
    student_names = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            student_names.append(row['name'])
    return student_names

#henerate feedback
def generate_feedback(name, grades):
    feedback = f"""
    General Comments:
    {name} showed a {understanding_level[grades['understanding']]} understanding of Python.
    Contribution level was {contribution_level[grades['contribution']]}.
    Lab completion was {lab_completion[grades['lab']]}.
    Engagement level was {engagement[grades['engagement']]}.

    Learner Punctuality:
    Punctuality was {punctuality[grades['punctuality']]}.

    Recommendation on Further Learning:
    Further learning recommendation: {further_learning_level[grades['further_learning']]}.
    """
    return feedback

#save to a new .csv file
def save_grades_to_csv(students, directory='student_results', filename='student_grades.csv'):
    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)


    filepath = os.path.join(directory, filename)

    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['name', 'understanding', 'contribution', 'lab', 'engagement', 'punctuality', 'further_learning']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for student, grades in students:
            row = {'name': student, **grades}
            writer.writerow(row)


def create_feedback_files(students, directory='student_results'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for student, grades in students:
        feedback_text = generate_feedback(student, grades)
        with open(os.path.join(directory, f'{student}_feedback.txt'), 'w') as file:
            file.write(feedback_text)

# Main function
def main():
    # Read student names from CSV file
    student_names = read_student_names('students.csv')

    valid_grades = {'A', 'B', 'C', 'F'}
    students = []
    for name in student_names:
        print(f"\nEnter grades for {name}:")
        grades = {}
        for criterion in ['understanding', 'contribution', 'lab', 'engagement', 'punctuality', 'further_learning']:
            while True:
                grade = input(f"{criterion.capitalize().replace('_', ' ')} Level (A-F): ").upper()
                if grade in valid_grades:
                    grades[criterion] = grade
                    break
                else:
                    print("Invalid grade. Please enter a grade between A and F.")
        students.append((name, grades))

    save_grades_to_csv(students)
    print("Student grades saved to 'student_results/student_grades.csv'.")

    create_feedback_files(students)
    print("Feedback files generated successfully in the 'student_results' directory.")

if __name__ == '__main__':
    main()
