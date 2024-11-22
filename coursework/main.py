import tkinter as tk
from tkinter import messagebox, ttk
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# --- Настройки базы данных ---
Base = declarative_base()


class Driver(Base):
    __tablename__ = 'drivers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    license_category = Column(String)
    experience_years = Column(Integer)


class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    brand = Column(String)
    model = Column(String)
    year = Column(Integer)
    mileage = Column(Float)
    specialization = Column(String)
    status = Column(String, default="В наличии")


class Route(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True)
    start = Column(String)
    end = Column(String)
    distance = Column(Float)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    client_name = Column(String)
    route_id = Column(Integer)
    driver_id = Column(Integer)
    car_id = Column(Integer)
    price = Column(Float)
    status = Column(String, default="Ожидает")


# --- Создание базы данных ---
engine = create_engine('sqlite:///transport.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


# --- Функции для работы с базой данных ---
def add_driver():
    name = driver_name_entry.get()
    license_category = driver_license_category_entry.get()
    experience_years = driver_experience_years_entry.get()
    if name and license_category and experience_years:
        driver = Driver(
            name=name, license_category=license_category, experience_years=int(experience_years)
        )
        session.add(driver)
        session.commit()
        messagebox.showinfo("Успех", "Водитель добавлен!")
        clear_driver_entries()
        update_driver_combobox()
    else:
        messagebox.showerror("Ошибка", "Заполните все поля!")


def add_car():
    brand = car_brand_entry.get()
    model = car_model_entry.get()
    year = car_year_entry.get()
    specialization = car_specialization_combobox.get()
    mileage = car_mileage_entry.get()
    if brand and model and year and mileage:
        car = Car(
            brand=brand, model=model, year=int(year), mileage=float(mileage), specialization=specialization
        )
        session.add(car)
        session.commit()
        messagebox.showinfo("Успех", "Машина добавлена!")
        clear_car_entries()
        update_car_combobox()
    else:
        messagebox.showerror("Ошибка", "Заполните все поля!")


def add_route():
    start = route_start_entry.get()
    end = route_end_entry.get()
    distance = route_distance_entry.get()
    if start and end and distance:
        route = Route(
            start=start, end=end, distance=float(distance)
        )
        session.add(route)
        session.commit()
        messagebox.showinfo("Успех", "Маршрут добавлен!")
        clear_route_entries()
        update_route_combobox()
    else:
        messagebox.showerror("Ошибка", "Заполните все поля!")


def add_order():
    client_name = order_client_name_entry.get()
    route_id = order_route_id_combobox.get().split('.')[0]
    driver_id = order_driver_id_combobox.get().split('.')[0]
    car_id = order_car_id_combobox.get().split('.')[0]
    price = order_price_entry.get()
    if client_name and route_id and driver_id and car_id and price:
        order = Order(
            client_name=client_name, route_id=int(route_id), driver_id=int(driver_id), car_id=int(car_id),
            price=float(price)
        )
        session.add(order)
        session.commit()
        messagebox.showinfo("Успех", "Заказ добавлен!")
        clear_order_entries()
        ()
    else:
        messagebox.showerror("Ошибка", "Заполните все поля!")


# --- Обновление списка ---
def update_all_entities_list():
    # Очистить список
    all_entities_listbox.delete(0, tk.END)
    selected_category = entity_combobox.get()

    if selected_category == "Водители":
        drivers = session.query(Driver).all()
        for driver in drivers:
            all_entities_listbox.insert(tk.END,
                                        f"{driver.id}. {driver.name} - {driver.license_category}, {driver.experience_years} лет стажа")

    elif selected_category == "Машины":
        cars = session.query(Car).all()
        for car in cars:
            all_entities_listbox.insert(tk.END,
                                        f"{car.id}. {car.brand} {car.model} ({car.year}) - {car.specialization}, пробег: {car.mileage}")

    elif selected_category == "Маршруты":
        routes = session.query(Route).all()
        for route in routes:
            all_entities_listbox.insert(tk.END, f"{route.id}. {route.start} -> {route.end} - {route.distance} км")

    elif selected_category == "Заказы":
        orders = session.query(Order).all()
        for order in orders:
            all_entities_listbox.insert(
                tk.END,
                f"Заказ {order.id}. {order.client_name} - Маршрут {order.route_id}, Водитель {order.driver_id}, Машина {order.car_id}, Цена: {order.price}, Статус: {order.status}"
            )


# --- Очистка полей ---
def clear_driver_entries():
    driver_name_entry.delete(0, tk.END)
    driver_license_category_entry.delete(0, tk.END)
    driver_experience_years_entry.delete(0, tk.END)


def clear_car_entries():
    car_brand_entry.delete(0, tk.END)
    car_model_entry.delete(0, tk.END)
    car_year_entry.delete(0, tk.END)
    car_specialization_combobox.set("Грузовая")
    car_mileage_entry.delete(0, tk.END)


def clear_route_entries():
    route_start_entry.delete(0, tk.END)
    route_end_entry.delete(0, tk.END)
    route_distance_entry.delete(0, tk.END)


def clear_order_entries():
    order_client_name_entry.delete(0, tk.END)
    order_route_id_combobox.set('')
    order_driver_id_combobox.set('')
    order_car_id_combobox.set('')
    order_price_entry.delete(0, tk.END)


# --- Интерфейс пользователя ---
root = tk.Tk()
root.title("Автотранспортное предприятие")

# Адаптация окна под разрешение экрана пользователя
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 900
window_height = 700

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# --- Вкладки ---
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# --- Все записи ---
all_entities_frame = tk.Frame(notebook)
notebook.add(all_entities_frame, text="Все записи")

tk.Label(all_entities_frame, text="Просмотр всех записей", font=("Arial", 14)).pack(pady=10)

# Выпадающий список для выбора категории
entity_label = tk.Label(all_entities_frame, text="Выберите категорию: ")
entity_label.pack(pady=5)

entity_combobox = ttk.Combobox(all_entities_frame, values=["Водители", "Машины", "Маршруты", "Заказы"])
entity_combobox.set("Водители")
entity_combobox.pack(pady=5)

# Кнопка для обновления списка
update_button = tk.Button(all_entities_frame, text="Обновить список", command=update_all_entities_list)
update_button.pack(pady=10)

# Список всех сущностей
all_entities_listbox = tk.Listbox(all_entities_frame, height=15, width=100)
all_entities_listbox.pack(pady=10)

# --- Автопарк ---
car_frame = tk.Frame(notebook)
notebook.add(car_frame, text="Автопарк")

tk.Label(car_frame, text="Добавить машину", font=("Arial", 14)).pack(pady=10)

# Поля для добавления машины
car_brand_label = tk.Label(car_frame, text="Марка: ")
car_brand_label.pack()
car_brand_entry = tk.Entry(car_frame)
car_brand_entry.pack()

car_model_label = tk.Label(car_frame, text="Модель: ")
car_model_label.pack()
car_model_entry = tk.Entry(car_frame)
car_model_entry.pack()

car_year_label = tk.Label(car_frame, text="Год выпуска: ")
car_year_label.pack()
car_year_entry = tk.Entry(car_frame)
car_year_entry.pack()

car_specialization_label = tk.Label(car_frame, text="Специализация: ")
car_specialization_label.pack()
car_specialization_combobox = ttk.Combobox(car_frame, values=["Грузовая", "Легковая", "Спецтехника"])
car_specialization_combobox.set("Грузовая")
car_specialization_combobox.pack()

car_mileage_label = tk.Label(car_frame, text="Пробег: ")
car_mileage_label.pack()
car_mileage_entry = tk.Entry(car_frame)
car_mileage_entry.pack()

# Кнопка добавления машины
add_car_button = tk.Button(car_frame, text="Добавить машину", command=add_car)
add_car_button.pack(pady=10)

# --- Водители ---
driver_frame = tk.Frame(notebook)
notebook.add(driver_frame, text="Водители")

tk.Label(driver_frame, text="Добавить водителя", font=("Arial", 14)).pack(pady=10)

# Поля для добавления водителя
driver_name_label = tk.Label(driver_frame, text="Имя водителя: ")
driver_name_label.pack()
driver_name_entry = tk.Entry(driver_frame)
driver_name_entry.pack()

driver_license_category_label = tk.Label(driver_frame, text="Категория прав: ")
driver_license_category_label.pack()
driver_license_category_entry = tk.Entry(driver_frame)
driver_license_category_entry.pack()

driver_experience_years_label = tk.Label(driver_frame, text="Стаж: ")
driver_experience_years_label.pack()
driver_experience_years_entry = tk.Entry(driver_frame)
driver_experience_years_entry.pack()

# Кнопка добавления водителя
add_driver_button = tk.Button(driver_frame, text="Добавить водителя", command=add_driver)
add_driver_button.pack(pady=10)

# --- Маршруты ---
route_frame = tk.Frame(notebook)
notebook.add(route_frame, text="Маршруты")

tk.Label(route_frame, text="Добавить маршрут", font=("Arial", 14)).pack(pady=10)

# Поля для добавления маршрута
route_start_label = tk.Label(route_frame, text="Старт: ")
route_start_label.pack()
route_start_entry = tk.Entry(route_frame)
route_start_entry.pack()

route_end_label = tk.Label(route_frame, text="Конечный пункт: ")
route_end_label.pack()
route_end_entry = tk.Entry(route_frame)
route_end_entry.pack()

route_distance_label = tk.Label(route_frame, text="Расстояние: ")
route_distance_label.pack()
route_distance_entry = tk.Entry(route_frame)
route_distance_entry.pack()

# Кнопка добавления маршрута
add_route_button = tk.Button(route_frame, text="Добавить маршрут", command=add_route)
add_route_button.pack(pady=10)

# --- Заказы ---
order_frame = tk.Frame(notebook)
notebook.add(order_frame, text="Заказы")

tk.Label(order_frame, text="Добавить заказ", font=("Arial", 14)).pack(pady=10)

# Поля для добавления заказа
order_client_name_label = tk.Label(order_frame, text="Имя клиента: ")
order_client_name_label.pack()
order_client_name_entry = tk.Entry(order_frame)
order_client_name_entry.pack()

order_route_id_label = tk.Label(order_frame, text="Маршрут: ")
order_route_id_label.pack()
order_route_id_combobox = ttk.Combobox(order_frame)
order_route_id_combobox.pack()

order_driver_id_label = tk.Label(order_frame, text="Водитель: ")
order_driver_id_label.pack()
order_driver_id_combobox = ttk.Combobox(order_frame)
order_driver_id_combobox.pack()

order_car_id_label = tk.Label(order_frame, text="Машина: ")
order_car_id_label.pack()
order_car_id_combobox = ttk.Combobox(order_frame)
order_car_id_combobox.pack()

order_price_label = tk.Label(order_frame, text="Цена: ")
order_price_label.pack()
order_price_entry = tk.Entry(order_frame)
order_price_entry.pack()

# Кнопка добавления заказа
add_order_button = tk.Button(order_frame, text="Добавить заказ", command=add_order)
add_order_button.pack(pady=10)

# Инициализация списка
update_all_entities_list()

root.mainloop()
