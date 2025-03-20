import tkinter as tk
from tkinter import messagebox, ttk

requests_list = []

def process_request():
    try:
        name = name_field.get()
        address = address_field.get()
        request_type = request_type_choice.get()

        if not name or not address or not request_type:
            raise ValueError("Заполните все поля!")

        report = f"Запрос от {name}\nАдрес: {address}\nТип запроса: {request_type}"

        requests_list.append(report)

        messagebox.showinfo("Запрос принят", report)

        name_field.delete(0, tk.END)
        address_field.delete(0, tk.END)
        request_type_choice.set("")
    except ValueError as ve:
        messagebox.showerror("Ошибка", str(ve))
    except Exception as e:
        messagebox.showerror("Критическая ошибка", f"Произошла ошибка: {str(e)}")

def add_equipment():
    try:
        identifier = id_field.get()
        equipment_type = equipment_type_choice.get()
        status = status_choice.get()
        date = date_field.get()

        if not (identifier and equipment_type and status and date):
            raise ValueError("Заполните все поля!")

        equipment_table.insert("", "end", values=(identifier, equipment_type, status, date))
        id_field.delete(0, tk.END)
        equipment_type_choice.set("")
        status_choice.set("")
        date_field.delete(0, tk.END)
    except ValueError as ve:
        messagebox.showerror("Ошибка", str(ve))
    except Exception as e:
        messagebox.showerror("Критическая ошибка", f"Произошла ошибка: {str(e)}")

def view_requests():
    try:
        request_window = tk.Toplevel(window)
        request_window.title("Просмотр запросов")
        request_window.geometry("600x600")

        tk.Label(request_window, text="Оставленные запросы", font=("Arial", 16, "bold")).pack(pady=10)

        canvas = tk.Canvas(request_window)
        scroll_y = tk.Scrollbar(request_window, orient="vertical", command=canvas.yview)

        frame = tk.Frame(canvas)

        for request in requests_list:
            request_frame = tk.Frame(frame, bd=2, relief=tk.GROOVE, padx=10, pady=5, bg='white')
            request_frame.pack(padx=10, pady=5, fill="x")
            tk.Label(request_frame, text=request, font=("Arial", 12), anchor="w", justify="left").pack(padx=5, pady=5, fill="x")

        frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
    except Exception as e:
        messagebox.showerror("Критическая ошибка", f"Произошла ошибка: {str(e)}")

def open_section_window(section_name):
    try:
        section_window = tk.Toplevel(window)
        section_window.title(section_name)
        section_window.geometry("600x400")

        tk.Label(section_window, text=f"{section_name}", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(section_window, text="Информация о разделе...", font=("Arial", 12)).pack(pady=10)
    except Exception as e:
        messagebox.showerror("Критическая ошибка", f"Произошла ошибка: {str(e)}")

window = tk.Tk()
window.title("ИС Росводоканал - Дашборд")
window.geometry("1000x700")

top_panel = tk.Frame(window, bg="#87CEEB", height=50)
top_panel.pack(fill="x")

logo = tk.Label(top_panel, text="Росводоканал", font=("Arial", 16, "bold"), bg="#87CEEB", fg="white")
logo.pack(side="left", padx=20)

user_name = tk.Label(top_panel, text="Пользователь: Менеджер", font=("Arial", 12), bg="#87CEEB", fg="white")
user_name.pack(side="right", padx=20)

side_panel = tk.Frame(window, bg="#E0E0E0", width=200)
side_panel.pack(side="left", fill="y")

sections = ["Стратегическое развитие", "Эксплуатация", "Потребители", "Администрирование"]
for section in sections:
    button = tk.Button(side_panel, text=section, font=("Arial", 12), bg="#E0E0E0", command=lambda s=section: open_section_window(s))
    button.pack(pady=10, fill="x")

view_requests_button = tk.Button(side_panel, text="Просмотр запросов", font=("Arial", 12), bg="#E0E0E0", command=view_requests)
view_requests_button.pack(pady=10, fill="x")

main_content = tk.Frame(window)
main_content.pack(side="right", expand=True, fill="both")

tk.Label(main_content, text="Форма подачи запроса", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(main_content, text="Имя клиента:", font=("Arial", 12)).pack(anchor="w", padx=20)
name_field = tk.Entry(main_content, font=("Arial", 12))
name_field.pack(padx=20, pady=5, fill="x")

tk.Label(main_content, text="Адрес клиента:", font=("Arial", 12)).pack(anchor="w", padx=20)
address_field = tk.Entry(main_content, font=("Arial", 12))
address_field.pack(padx=20, pady=5, fill="x")

tk.Label(main_content, text="Тип запроса:", font=("Arial", 12)).pack(anchor="w", padx=20)
request_type_choice = tk.StringVar(main_content)
request_type_choice.set("")
request_types = ["Качество воды", "Авария", "Консультация"]
request_dropdown = tk.OptionMenu(main_content, request_type_choice, *request_types)
request_dropdown.config(font=("Arial", 12))
request_dropdown.pack(padx=20, pady=5, fill="x")

submit_button = tk.Button(main_content, text="Отправить запрос", font=("Arial", 14, "bold"), bg="#87CEEB", fg="white", command=process_request)
submit_button.pack(pady=20)

tk.Label(main_content, text="Мониторинг оборудования", font=("Arial", 16, "bold")).pack(pady=10)

equipment_table = ttk.Treeview(main_content, columns=("Наименование", "Тип", "Состояние", "Дата"), show="headings")
for col in ("Наименование", "Тип", "Состояние", "Дата"):
    equipment_table.heading(col, text=col)
    equipment_table.column(col, width=150)
equipment_table.pack(padx=20, pady=5, fill="x")

id_field = tk.Entry(main_content, font=("Arial", 12))
id_field.pack(padx=20, pady=5, fill="x")

equipment_type_choice = tk.StringVar(main_content)
equipment_type_choice.set("")
equipment_types = ["Датчик", "Насос", "Фильтр"]
equipment_dropdown = tk.OptionMenu(main_content, equipment_type_choice, *equipment_types)
equipment_dropdown.pack(padx=20, pady=5, fill="x")

status_choice = tk.StringVar(main_content)
status_choice.set("")
status_options = ["Рабочее", "Неисправно", "Требует проверки"]
status_dropdown = tk.OptionMenu(main_content, status_choice, *status_options)
status_dropdown.pack(padx=20, pady=5, fill="x")

date_field = tk.Entry(main_content, font=("Arial", 12))
date_field.pack(padx=20, pady=5, fill="x")

add_button = tk.Button(main_content, text="Добавить оборудование", font=("Arial", 14, "bold"), bg="#87CEEB", fg="white", command=add_equipment)
add_button.pack(pady=20)

window.mainloop()