import os
import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious



# Load hymns from separate text files
hymns_dir = 'hymns'
hymn_files = os.listdir(hymns_dir)
hymns = []
for hymn_file in hymn_files:
    with open(os.path.join(hymns_dir, hymn_file), 'r') as f:
        title = f.readline().strip()
        lyrics = f.read().strip()
        hymns.append({'title': title, 'lyrics': lyrics})




# Screen for displaying the list of all hymns
class AllHymnsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        action_bar = ActionBar(pos_hint={'top': 1})
        view = ActionView()
        previous = ActionPrevious(with_previous=False, title='All Hymns')
        view.add_widget(previous)
        action_bar.add_widget(view)
        layout.add_widget(action_bar)

        self.search_bar = TextInput(text='', multiline=False, size_hint_y=None, height=40)
        self.search_bar.bind(text=self.search)
        layout.add_widget(self.search_bar)

        self.hymns_scroll = ScrollView(size_hint=(1, 1))
        self.hymns_scroll.add_widget(self.create_hymns_grid())
        layout.add_widget(self.hymns_scroll)

        self.add_widget(layout)

    def create_hymns_grid(self):
        self.hymns_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.hymns_grid.bind(minimum_height=self.hymns_grid.setter('height'))
        for hymn_file in os.listdir(hymns_dir):
            # Load the contents of the hymn file
            with open(os.path.join(hymns_dir, hymn_file)) as f:
                hymn_title = f.readline().strip()
                hymn_lyrics = f.read().strip()

            button = Button(text=hymn_title, size_hint_y=None, height=40)
            button.bind(on_release=lambda x, y=hymn_lyrics: self.show_lyrics(y))
            self.hymns_grid.add_widget(button)
        return self.hymns_grid

    def search(self, instance, value):
        self.hymns_grid.clear_widgets()
        for hymn_file in os.listdir(hymns_dir):
            with open(os.path.join(hymns_dir, hymn_file)) as f:
                hymn_title = f.readline().strip()
                hymn_lyrics = f.read().strip()
            if value.lower() in hymn_title.lower():
                button = Button(text=hymn_title, size_hint_y=None, height=40)
                button.bind(on_release=lambda x, y=hymn_lyrics: self.show_lyrics(y))
                self.hymns_grid.add_widget(button)

    def show_lyrics(self, lyrics):
        screen_manager.current = 'lyrics'
        lyrics_screen.update_lyrics(lyrics)


# Screen for displaying the lyrics of a selected hymn
class LyricsScreen(Screen):
    def update_lyrics(self, lyrics):
        self.clear_widgets()

        scroll_view = ScrollView()
        text_input = TextInput(text=lyrics, font_size=20, size_hint_y=None, readonly=True)
        text_input.bind(minimum_height=text_input.setter('height'))
        scroll_view.add_widget(text_input)
        self.add_widget(scroll_view)

        # Add a Back button to return to the All Hymns screen
        self.add_widget(Button(text='Back', size_hint=(1, 0.1), on_release=lambda x: set_screen('all_hymns')))





def set_screen(screen_name):
    screen_manager.current = screen_name
    if screen_name == 'all_hymns':
        all_hymns_screen.search_bar.text = ''
        all_hymns_screen.hymns_scroll.scroll_y = 1
    elif screen_name == 'lyrics':
        pass


# Screen manager for switching between screens
screen_manager = ScreenManager()
all_hymns_screen = AllHymnsScreen(name='all_hymns')
lyrics_screen = LyricsScreen(name='lyrics')
screen_manager.add_widget(all_hymns_screen)
screen_manager.add_widget(lyrics_screen)


# Main App class
class CatholicHymnsApp(App):
    def build(self):
        return screen_manager


if __name__ == '__main__':
    CatholicHymnsApp().run()