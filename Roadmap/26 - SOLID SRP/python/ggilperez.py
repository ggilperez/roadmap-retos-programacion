# 26 SOLID Single responsibility principle
from dataclasses import dataclass, field


# Without SOLID
class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, name, description):
        self.tasks.append({
            "name": name,
            "description": description
        })

    def remove_task(self, name):
        for task in self.tasks:
            if name == task["name"]:
                self.tasks.remove(task)

    def list_tasks(self):
        for task in self.tasks:
            print(f"# {task['name']} ({task['description']})")


task_manager = TaskManager()
task_manager.add_task("SW Acolyte", "New episode wednesday")
task_manager.add_task("Do house", "Clean")
task_manager.list_tasks()
task_manager.remove_task("SW Acolyte")
task_manager.list_tasks()
task_manager.add_task("Acolyte", "Create review")
task_manager.remove_task("Do house")


# With SOLID
class Task:
    def __init__(self, name: str, description: str) -> None:
        self.name: str = name
        self.description: str = description

    def __repr__(self):
        return f">>> {self.name} - {self.description}."


class TaskManager:
    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_task(self, task: Task):
        for my_task in self.tasks:
            if task.name == my_task.name:
                self.tasks.remove(task)

    def list_tasks(self):
        for task in self.tasks:
            print(task)


task_manager = TaskManager()
sw_task = Task("SW Acolyte", "New episode wednesday")
task_manager.add_task(sw_task)
house_task = Task("Do house", "Clean")
task_manager.add_task(house_task)
task_manager.list_tasks()
task_manager.remove_task(sw_task)
task_manager.list_tasks()
task_manager.add_task(sw_task)
task_manager.remove_task(house_task)

# EXTRA
@dataclass
class Book:
    title: str
    author: str
    stock: int

@dataclass
class User:
    name: str
    id: int
    email: str

@dataclass
class LoanService:
    loans: list = field(default_factory=list)

    def loan_book(self, book: Book, user: User):
        if book.stock > 0:
            book.stock -= 1
            self.loans.append((book, user))

    def return_book(self, returned_book: Book, return_user: User):
        for loan in self.loans:
            book, user = loan
            if book.title == returned_book.title and user.id == return_user.id:
                self.loans.remove(loan)
                returned_book.stock += 1

@dataclass
class Library:
    books: list[Book] = field(default_factory=list)
    users: list[User] = field(default_factory=list)
    loan_service: LoanService = field(default_factory=LoanService)

    def register_book(self, book: Book):
        self.books.append(book)

    def register_user(self, user: User):
        self.users.append(user)

    def loan_book(self, book: Book, user: User):
        self.loan_service.loan_book(book, user)

    def return_book(self, book: Book, user: User):
        self.loan_service.return_book(book, user)

the_hobbit = Book("The Hobbit", "J.R.R Tolkien", 1)
stuart_little = Book("Stuart Little", "E.B. White", 5)

user_1 = User("Guillermo", 1, "ggilperezalcazar@gmail.com")
user_2 = User("Brais", 2, "mouredev@gmail.com")

library = Library()
library.register_book(the_hobbit)
library.register_book(stuart_little)
library.register_user(user_1)
library.register_user(user_2)

library.loan_book(the_hobbit, user_1)
library.loan_book(the_hobbit, user_2)
library.loan_book(stuart_little, user_2)