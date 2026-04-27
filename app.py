from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["grades_db"]

def list_courses():
    print("\n=== ALL COURSES ===")
    courses = db.courses.find()
    for c in courses:
        print(f"ID: {c['_id']} | {c['name']} | {c['teacher_name']}")

def add_course():
    print("\n=== ADD COURSE ===")
    name = input("Course name: ")
    teacher = input("Teacher name: ")
    credits = int(input("Credits: "))
    year = int(input("Year: "))
    semester = input("Semester (Spring/Fall): ")
    topics = input("Topics (comma separated): ").split(",")
    topics = [t.strip() for t in topics]
    course = {
        "name": name,
        "teacher_name": teacher,
        "credits": credits,
        "year": year,
        "semester": semester,
        "topics": topics
    }
    result = db.courses.insert_one(course)
    print(f"Course added! ID: {result.inserted_id}")

def update_course():
    list_courses()
    course_id = input("Enter course ID to update: ")
    new_name = input("New course name: ")
    db.courses.update_one({"_id": ObjectId(course_id)}, {"$set": {"name": new_name}})
    print("Course updated!")

def delete_course():
    list_courses()
    course_id = input("Enter course ID to delete: ")
    db.courses.delete_one({"_id": ObjectId(course_id)})
    print("Course deleted!")

def list_grades():
    print("\n=== ALL GRADES ===")
    grades = db.grades.find()
    for g in grades:
        print(f"ID: {g['_id']} | {g['student_name']} | Grade: {g['grade']}")

def add_grade():
    list_courses()
    course_id = input("Course ID: ")
    student_name = input("Student name: ")
    student_number = input("Student number: ")
    grade = int(input("Grade (0-5): "))
    comment = input("Comment: ")
    grade_doc = {
        "course_id": ObjectId(course_id),
        "student_name": student_name,
        "student_number": student_number,
        "grade": grade,
        "comment": comment
    }
    result = db.grades.insert_one(grade_doc)
    print(f"Grade added! ID: {result.inserted_id}")

def update_grade():
    list_grades()
    grade_id = input("Enter grade ID to update: ")
    new_grade = int(input("New grade (0-5): "))
    new_comment = input("New comment: ")
    db.grades.update_one({"_id": ObjectId(grade_id)}, {"$set": {"grade": new_grade, "comment": new_comment}})
    print("Grade updated!")

def delete_grade():
    list_grades()
    grade_id = input("Enter grade ID to delete: ")
    db.grades.delete_one({"_id": ObjectId(grade_id)})
    print("Grade deleted!")

def insert_sample_data():
    if db.courses.count_documents({}) == 0:
        db.courses.insert_many([
            {
                "name": "Introduction to NoSQL",
                "teacher_name": "John Smith",
                "credits": 5,
                "year": 2024,
                "semester": "Spring",
                "topics": ["MongoDB", "NoSQL", "Database"]
            },
            {
                "name": "Business Intelligence",
                "teacher_name": "Mary Johnson",
                "credits": 3,
                "year": 2024,
                "semester": "Fall",
                "topics": ["Power BI", "Data Analysis"]
            }
        ])
        print("Sample courses added!")

    if db.grades.count_documents({}) == 0:
        course = db.courses.find_one()
        db.grades.insert_many([
            {
                "course_id": course["_id"],
                "student_name": "Alice Brown",
                "student_number": "HH-2024-001",
                "grade": 5,
                "comment": "Excellent work"
            },
            {
                "course_id": course["_id"],
                "student_name": "Bob Wilson",
                "student_number": "HH-2024-002",
                "grade": 3,
                "comment": "Good effort"
            }
        ])
        print("Sample grades added!")

def main():
    insert_sample_data()

    while True:
        print("\n========== GRADE DATABASE ==========")
        print("COURSES:")
        print("  1. List all courses")
        print("  2. Add a course")
        print("  3. Update a course")
        print("  4. Delete a course")
        print("GRADES:")
        print("  5. List all grades")
        print("  6. Add a grade")
        print("  7. Update a grade")
        print("  8. Delete a grade")
        print("  0. Exit")
        print("=====================================")
        choice = input("Choose an option: ")
        if choice == "1":
            list_courses()
        elif choice == "2":
            add_course()
        elif choice == "3":
            update_course()
        elif choice == "4":
            delete_course()
        elif choice == "5":
            list_grades()
        elif choice == "6":
            add_grade()
        elif choice == "7":
            update_grade()
        elif choice == "8":
            delete_grade()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
