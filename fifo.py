from collections import deque

# 1. FIFO Inventory Management
# This class manages inventory using the First-In-First-Out (FIFO) method.
class FIFOInventory:
    def __init__(self, stock_batches):
        # Use deque for efficient FIFO operations
        self.stock = deque(stock_batches)

    def get_next_batch(self, quantity):
        """
        Fetches the next available stock in FIFO order based on the required quantity.
        Ensures stock is not overdrawn.
        """
        used_batches = []
        remaining_qty = quantity

        while remaining_qty > 0 and self.stock:
            qty, price = self.stock.popleft()  # Take the oldest stock batch
            if qty <= remaining_qty:
                used_batches.append((qty, price))
                remaining_qty -= qty
            else:
                used_batches.append((remaining_qty, price))
                self.stock.appendleft((qty - remaining_qty, price))  # Return the unused portion
                remaining_qty = 0

        if remaining_qty > 0:
            raise ValueError("Insufficient stock available.")

        return used_batches


# 2. Sales Order Processing
# This class handles the creation and management of sales orders.
class SalesOrder:
    def __init__(self):
        self.orders = []  # Stores all orders

    def add_order(self, order):
        """
        Adds a new order to the orders list.
        Each order contains multiple items with price and quantity.
        """
        self.orders.append(order)

    def total_revenue(self):
        """
        Calculates the total revenue by summing the price * quantity for all items in all orders.
        """
        return sum(
            item["price"] * item["qty"]  # Multiply price by quantity for each item
            for order in self.orders
            for item in order["items"]
        )


# 3. Data Relationships (Many-to-Many)
# This class manages student enrollments into courses.
class University:
    def __init__(self):
        self.student_courses = {}  # Dictionary mapping students to enrolled courses
        self.course_students = {}  # Dictionary mapping courses to enrolled students

    def enroll(self, student, course):
        """
        Enrolls a student in a course while preventing duplicate enrollments.
        """
        if student not in self.student_courses:
            self.student_courses[student] = set()
        if course not in self.course_students:
            self.course_students[course] = set()

        if course in self.student_courses[student]:
            return  # Prevent duplicate enrollments

        self.student_courses[student].add(course)
        self.course_students[course].add(student)

    def get_student_courses(self, student):
        """
        Retrieves a list of courses a student is enrolled in.
        """
        return list(self.student_courses.get(student, []))

    def get_course_students(self, course):
        """
        Retrieves a list of students enrolled in a specific course.
        """
        return list(self.course_students.get(course, []))


# Example Usage
# if __name__ == "__main__":
# FIFO Inventory Management Test
stock = [(10, 5), (20, 6), (15, 7)]  # Stock format: (quantity, price per unit)
inventory = FIFOInventory(stock)
print(inventory.get_next_batch(25))  # Expected: [(10, 5), (15, 6)]
print(inventory.get_next_batch(20))  # Expected: [(10, 5), (15, 6)]

# Sales Order Processing Test
orders = [
    {"id": 1, "items": [{"name": "A", "price": 10, "qty": 2},
                            {"name": "B", "price": 15, "qty": 1}]},
    {"id": 2, "items": [{"name": "A", "price": 10, "qty": 1},
                            {"name": "C", "price": 20, "qty": 2}]}
]
sales = SalesOrder()
for order in orders:
    sales.add_order(order)
print("Total Revenue:", sales.total_revenue())  # Expected: $85

# University Enrollment Test
uni = University()
uni.enroll("Alice", "Math")
uni.enroll("Alice", "Physics")
uni.enroll("Bob", "Math")
print(uni.get_student_courses("Alice"))  # Expected: ['Math', 'Physics']
print(uni.get_course_students("Math"))  # Expected: ['Alice', 'Bob']
