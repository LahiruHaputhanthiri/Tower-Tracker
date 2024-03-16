import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

class FivePageApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x550')
        self.current_page = 0
        self.project_data_list = LinkedList()
        self.item_data_list = LinkedList()

        self.root.configure(bg='light blue')

        self.pages = [
            self.create_login_page,
            self.create_add_project_page,
            self.create_add_item_page,
            self.create_search_page
        ]

        self.show_page(self.current_page)

    def show_page(self, page_num):
        self.current_page = page_num
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg='light blue')

        self.pages[page_num]()

    def go_back(self):
        if self.current_page > 0:
            self.show_page(self.current_page - 1)

    def go_next(self):
        if self.current_page < len(self.pages) - 1:
            self.show_page(self.current_page + 1)

    def create_login_page(self):
        title_label = tk.Label(self.root, text='CELLULAR TOWER PROJECT MANAGEMENT', font=('Helvetica', 16, 'bold'), bg='light blue')
        title_label.pack(pady=20)

        login_frame = tk.Frame(self.root, bg='light blue')
        login_frame.pack(pady=10)

        tk.Label(login_frame, text='Username:', bg='light blue').grid(row=0, column=0, padx=10)
        self.user_entry = tk.Entry(login_frame)
        self.user_entry.grid(row=0, column=1, padx=10)

        tk.Label(login_frame, text='Password:', bg='light blue').grid(row=1, column=0, padx=10)
        self.password_entry = tk.Entry(login_frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=10)

        tk.Button(self.root, text='Login', command=self.check_credentials).pack(pady=10)

    def check_credentials(self):
        user_name = self.user_entry.get()
        password = self.password_entry.get()
        if user_name == 'admin' and password == 'password':
            messagebox.showinfo('Login successful', 'Welcome, ' + user_name + '!')
            self.go_next()  # Go to the next page after successful login
        else:
            messagebox.showerror('Login failed', 'Invalid credentials')

    def create_add_project_page(self):
        title_label = tk.Label(self.root, text='ADD NEW PROJECT', font=('Helvetica', 16, 'bold'), bg='light blue')
        title_label.pack(pady=20)

        project_frame = tk.Frame(self.root, bg='light blue')
        project_frame.pack(pady=10)

        tk.Label(project_frame, text='Project Name:', bg='light blue').grid(row=0, column=0, padx=10)
        self.project_name_entry = tk.Entry(project_frame)
        self.project_name_entry.grid(row=0, column=1, padx=10)

        tk.Label(project_frame, text='Project Type:', bg='light blue').grid(row=1, column=0, padx=10)
        self.project_type_entry = tk.Entry(project_frame)
        self.project_type_entry.grid(row=1, column=1, padx=10)

        tk.Label(project_frame, text='Date:', bg='light blue').grid(row=2, column=0, padx=10)
        self.date_entry = tk.Entry(project_frame)
        self.date_entry.grid(row=2, column=1, padx=10)

        tk.Button(self.root, text='Submit', command=self.submit_project).pack(pady=10)

        self.project_tree = ttk.Treeview(self.root, columns=('Project Data',))
        self.project_tree.heading('#0', text='Index')
        self.project_tree.heading('Project Data', text='Project Data')
        self.project_tree.pack(expand=True, fill='both', padx=20, pady=10)

        tk.Button(self.root, text='Delete Project', command=self.delete_project).pack(pady=10)
        tk.Button(self.root, text='Back', command=self.go_back).pack(side='left', padx=10)
        tk.Button(self.root, text='Next', command=self.go_next).pack(side='right', padx=10)

    def submit_project(self):
        project_name = self.project_name_entry.get()
        project_type = self.project_type_entry.get()
        date = self.date_entry.get()
        project_data = f"Project Name: {project_name}, Project Type: {project_type}, Date: {date}"
        self.project_data_list.add_node(project_data)
        self.show_project_data()
        messagebox.showinfo('Success', 'Project data submitted successfully!')

    def delete_project(self):
        selected_item = self.project_tree.selection()
        if selected_item:
            selected_item = selected_item[0]
            self.project_data_list.delete_node(self.project_tree.item(selected_item, "values")[0])
            self.show_project_data()
            messagebox.showinfo('Success', 'Project data deleted successfully!')
        else:
            messagebox.showerror('Error', 'Please select a project to delete.')

    def show_project_data(self):
        self.project_tree.delete(*self.project_tree.get_children())
        current = self.project_data_list.head
        index = 1
        while current is not None:
            self.project_tree.insert('', 'end', text=index, values=(current.data,))
            current = current.next_node
            index += 1

    def create_add_item_page(self):
        title_label = tk.Label(self.root, text='ADD NEW ITEM', font=('Helvetica', 16, 'bold'), bg='light blue')
        title_label.pack(pady=20)

        item_frame = tk.Frame(self.root, bg='light blue')
        item_frame.pack(pady=10)

        tk.Label(item_frame, text='Item Name:', bg='light blue').grid(row=0, column=0, padx=10)
        self.item_name_entry = tk.Entry(item_frame)
        self.item_name_entry.grid(row=0, column=1, padx=10)

        tk.Label(item_frame, text='Item Qty:', bg='light blue').grid(row=1, column=0, padx=10)
        self.item_qty_entry = tk.Entry(item_frame)
        self.item_qty_entry.grid(row=1, column=1, padx=10)

        tk.Button(self.root, text='Submit', command=self.submit_item).pack(pady=10)

        self.item_tree = ttk.Treeview(self.root, columns=('Item Data',))
        self.item_tree.heading('#0', text='Index')
        self.item_tree.heading('Item Data', text='Item Data')
        self.item_tree.pack(expand=True, fill='both', padx=20, pady=10)

        tk.Button(self.root, text='Delete Item', command=self.delete_item).pack(pady=10)
        tk.Button(self.root, text='Back', command=self.go_back).pack(side='left', padx=10)
        tk.Button(self.root, text='Next', command=self.go_next).pack(side='right', padx=10)

    def submit_item(self):
        item_name = self.item_name_entry.get()
        item_qty = self.item_qty_entry.get()
        item_data = f"Item Name: {item_name}, Item Quantity: {item_qty}"
        self.item_data_list.add_node(item_data)
        self.show_item_data()
        messagebox.showinfo('Success', 'Item data submitted successfully!')

    def delete_item(self):
        selected_item = self.item_tree.selection()
        if selected_item:
            selected_item = selected_item[0]
            self.item_data_list.delete_node(self.item_tree.item(selected_item, "values")[0])
            self.show_item_data()
            messagebox.showinfo('Success', 'Item data deleted successfully!')
        else:
            messagebox.showerror('Error', 'Please select an item to delete.')

    def show_item_data(self):
        self.item_tree.delete(*self.item_tree.get_children())
        current = self.item_data_list.head
        index = 1
        while current is not None:
            self.item_tree.insert('', 'end', text=index, values=(current.data,))
            current = current.next_node
            index += 1

    def create_search_page(self):
        title_label = tk.Label(self.root, text='SEARCH DATA', font=('Helvetica', 16, 'bold'), bg='light blue')
        title_label.pack(pady=20)

        search_frame = tk.Frame(self.root, bg='light blue')
        search_frame.pack(pady=10)

        tk.Label(search_frame, text='Search:', bg='light blue').grid(row=0, column=0, padx=10)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=10)

        self.tree = ttk.Treeview(self.root)
        self.tree['columns'] = ('Data',)
        self.tree.heading('#0', text='Index')
        self.tree.heading('Data', text='Data')

        scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(expand=True, fill='both', padx=20, pady=10)

        tk.Button(self.root, text='Search', command=self.search_data_action).pack(pady=10)
        tk.Button(self.root, text='Back', command=self.go_back).pack()

    def search_data_action(self):
        search_query = self.search_entry.get()
        search_results = []
        current = self.project_data_list.head
        index = 1
        while current is not None:
            if search_query in current.data:
                search_results.append(current.data)
                self.tree.insert('', 'end', text=index, values=(current.data,))
                index += 1
            current = current.next_node

        current = self.item_data_list.head
        while current is not None:
            if search_query in current.data:
                search_results.append(current.data)
                self.tree.insert('', 'end', text=index, values=(current.data,))
                index += 1
            current = current.next_node

        if not search_results:
            messagebox.showinfo('Search Results', 'No matching data found.')

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next_node = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next_node:
                current = current.next_node
            current.next_node = new_node

    def delete_node(self, target_data):
        if not self.head:
            return
        if self.head.data == target_data:
            self.head = self.head.next_node
            return
        current = self.head
        while current.next_node:
            if current.next_node.data == target_data:
                current.next_node = current.next_node.next_node
                return
            current = current.next_node

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Cellular Tower Project Management")
    app = FivePageApp(root)
    root.mainloop()
