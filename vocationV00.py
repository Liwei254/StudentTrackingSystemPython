import tkinter as tk
from tkinter import messagebox, simpledialog


class Student:
    def __init__(self, name="", phone_number="", email_address="", feedback=""):
        self.name = name
        self.phone_number = phone_number
        self.email_address = email_address
        self.feedback = feedback


class Teacher:
    def __init__(self, name=""):
        self.name = name
        self.students = [Student() for _ in range(2)] 


class FeedbackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teacher-Student Feedback System")
        self.root.geometry("600x400")
        
        # Predefine 3 teachers with some students
        self.teachers = [
            Teacher("Teacher1"),
            Teacher("Teacher2"),
            Teacher("Teacher3")
        ]
        
        # Initialize some students
        self.teachers[0].students[0] = Student("Student1", "111-111-1111", "student1@gmail.com", "")
        self.teachers[0].students[1] = Student("Student2", "222-222-2222", "student2@gmail.com", "")
        self.teachers[1].students[0] = Student("Student3", "333-333-3333", "student3@gmail.com", "")
        self.teachers[1].students[1] = Student("Student4", "444-444-4444", "student4@gmail.com", "")
        self.teachers[2].students[0] = Student("Student5", "555-555-5555", "student5@gmail.com", "")
        self.teachers[2].students[1] = Student("Student6", "666-666-6666", "student6@gmail.com", "")

        # Create a simple main menu for manager and teacher actions
        self.create_main_menu()

    def create_main_menu(self):
        # Create a menu for Manager
        manager_frame = tk.Frame(self.root)
        manager_frame.pack(pady=10)
        
        tk.Label(manager_frame, text="Manager Actions", font=("Helvetica", 14)).pack(pady=5)

        tk.Button(manager_frame, text="Add Teacher", command=self.add_teacher).pack(pady=5)
        tk.Button(manager_frame, text="Delete Teacher", command=self.delete_teacher).pack(pady=5)
        tk.Button(manager_frame, text="View All Feedback", command=self.view_all_feedback).pack(pady=5)
        
        # Create a separate section for Teacher actions
        teacher_frame = tk.Frame(self.root)
        teacher_frame.pack(pady=20)

        tk.Label(teacher_frame, text="Teacher Actions", font=("Helvetica", 14)).pack(pady=5)

        tk.Button(teacher_frame, text="Manage Teacher", command=self.select_teacher).pack(pady=5)

    # Manager Functions
    def add_teacher(self):
        new_teacher_name = simpledialog.askstring("Input", "Enter new teacher's name:")
        if new_teacher_name:
            new_teacher = Teacher(new_teacher_name)
            self.teachers.append(new_teacher)
            messagebox.showinfo("Success", f"Teacher {new_teacher_name} added successfully.")

    def delete_teacher(self):
        teacher_names = [teacher.name for teacher in self.teachers]
        if not teacher_names:
            messagebox.showinfo("Error", "No teachers available.")
            return

        teacher_name = simpledialog.askstring("Input", f"Choose a teacher to delete: {teacher_names}")
        self.teachers = [t for t in self.teachers if t.name != teacher_name]
        messagebox.showinfo("Success", f"Teacher {teacher_name} deleted successfully.")

    def view_all_feedback(self):
        feedback_text = ""
        for teacher in self.teachers:
            feedback_text += f"\nFeedback for {teacher.name}'s students:\n"
            for student in teacher.students:
                if student.name:
                    feedback_text += f"Student: {student.name}, Feedback: {student.feedback}\n"
        if feedback_text:
            messagebox.showinfo("All Feedback", feedback_text)
        else:
            messagebox.showinfo("No Feedback", "No feedback available for any students.")

    # Teacher Functions
    def select_teacher(self):
        teacher_names = [teacher.name for teacher in self.teachers]
        if not teacher_names:
            messagebox.showinfo("Error", "No teachers available.")
            return

        selected_teacher = simpledialog.askstring("Input", f"Enter teacher name: {teacher_names}")
        teacher = next((t for t in self.teachers if t.name == selected_teacher), None)
        
        if teacher:
            self.manage_teacher(teacher)
        else:
            messagebox.showinfo("Error", "Teacher not found.")

    def manage_teacher(self, teacher):
        teacher_window = tk.Toplevel(self.root)
        teacher_window.title(f"Manage Teacher: {teacher.name}")
        teacher_window.geometry("400x300")

        tk.Label(teacher_window, text=f"Teacher: {teacher.name}", font=("Helvetica", 14)).pack(pady=5)

        # List students
        student_list = tk.Listbox(teacher_window)
        student_list.pack(pady=10)
        for idx, student in enumerate(teacher.students):
            student_list.insert(tk.END, f"{idx + 1}. {student.name}")

        # Add buttons to give feedback, add student, and delete student
        tk.Button(teacher_window, text="Give Feedback", command=lambda: self.give_feedback(teacher, student_list)).pack(pady=5)
        tk.Button(teacher_window, text="Add Student", command=lambda: self.add_student(teacher, student_list)).pack(pady=5)
        tk.Button(teacher_window, text="Delete Student", command=lambda: self.delete_student(teacher, student_list)).pack(pady=5)

    def give_feedback(self, teacher, student_list):
        selected_idx = student_list.curselection()
        if selected_idx:
            student = teacher.students[selected_idx[0]]
            if student.name:
                feedback = simpledialog.askstring("Input", f"Enter feedback for {student.name}:")
                if feedback:
                    student.feedback = feedback
                    messagebox.showinfo("Success", f"Feedback updated for {student.name}.")
        else:
            messagebox.showerror("Error", "No student selected.")

    def add_student(self, teacher, student_list):
        if len(teacher.students) >= 2:
            messagebox.showinfo("Limit", "Each teacher can only have 2 students.")
            return

        student_name = simpledialog.askstring("Input", "Enter student name:")
        phone = simpledialog.askstring("Input", "Enter student phone number:")
        email = simpledialog.askstring("Input", "Enter student email address:")

        new_student = Student(student_name, phone, email)
        teacher.students.append(new_student)
        student_list.insert(tk.END, student_name)
        messagebox.showinfo("Success", f"Student {student_name} added successfully.")

    def delete_student(self, teacher, student_list):
        selected_idx = student_list.curselection()
        if selected_idx:
            student = teacher.students[selected_idx[0]]
            if student.name:
                teacher.students[selected_idx[0]] = Student()  # Reset student
                student_list.delete(selected_idx)
                messagebox.showinfo("Success", f"Student {student.name} deleted.")
        else:
            messagebox.showerror("Error", "No student selected.")


# Run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = FeedbackApp(root)
    root.mainloop()
