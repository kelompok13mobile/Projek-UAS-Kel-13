from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

class ToDoApp(App):
    def build(self):
        self.tasks = []

        # Layout utama
        self.layout = BoxLayout(orientation='vertical')

        # Input untuk menambahkan tugas baru
        self.task_input = TextInput(hint_text='Masukkan tugas baru...', size_hint_y=None, height=40)
        self.layout.add_widget(self.task_input)

        # Tombol untuk menambah tugas
        self.add_button = Button(text='Tambah Tugas', size_hint_y=None, height=40)
        self.add_button.bind(on_press=self.add_task)
        self.layout.add_widget(self.add_button)

        # ScrollView untuk menampilkan daftar tugas
        self.task_list = GridLayout(cols=1, size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 300))
        self.scroll_view.add_widget(self.task_list)
        self.layout.add_widget(self.scroll_view)

        return self.layout

    def add_task(self, instance):
        task_text = self.task_input.text.strip()
        if task_text:  # Pastikan input tidak kosong
            task_button = Button(text=task_text, size_hint_y=None, height=40)
            task_button.bind(on_press=self.edit_task)
            remove_button = Button(text="Hapus", size_hint_y=None, height=40)
            remove_button.bind(on_press=lambda btn: self.remove_task(task_button.text))

            task_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            task_box.add_widget(task_button)
            task_box.add_widget(remove_button)
            self.task_list.add_widget(task_box)

            self.tasks.append(task_text)
            self.task_input.text = ''  # Bersihkan input setelah menambahkan tugas

    def edit_task(self, instance):
        current_text = instance.text
        edit_popup = Popup(title='Edit Tugas',
                           size_hint=(0.7, 0.4))

        content = self.create_edit_task_content(current_text, edit_popup)
        edit_popup.content = content
        edit_popup.open()

    def create_edit_task_content(self, current_text, popup):
        box = BoxLayout(orientation='vertical')

        self.edit_task_input = TextInput(text=current_text, size_hint_y=None, height=40)
        box.add_widget(self.edit_task_input)

        save_button = Button(text='Simpan', size_hint_y=None, height=40)
        save_button.bind(on_press=lambda btn: self.save_edited_task(current_text, popup))
        box.add_widget(save_button)

        return box

    def save_edited_task(self, old_text, popup):
        new_text = self.edit_task_input.text.strip()
        if new_text:
            for task_box in self.task_list.children:
                for button in task_box.children:
                    if button.text == old_text:
                        button.text = new_text
                        break
            self.tasks[self.tasks.index(old_text)] = new_text
            popup.dismiss()  # Tutup popup setelah menyimpan

    def remove_task(self, task_text):
        for task_box in list(self.task_list.children):  # Salin daftar karena akan dimodifikasi
            for button in task_box.children:
                if button.text == task_text:
                    self.task_list.remove_widget(task_box)
                    if task_text in self.tasks:
                        self.tasks.remove(task_text)
                    return


if __name__ == '__main__':
    ToDoApp().run()
