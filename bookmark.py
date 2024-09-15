import urwid
import json
from pathlib import Path

BOOKMARKS_FILE = Path("bookmarks.json")

class BookmarkManager:
    def __init__(self):
        self.bookmarks = self.load_bookmarks()

    def load_bookmarks(self):
        if BOOKMARKS_FILE.exists():
            with open(BOOKMARKS_FILE, "r") as f:
                return json.load(f)
        return []

    def save_bookmarks(self):
        with open(BOOKMARKS_FILE, "w") as f:
            json.dump(self.bookmarks, f, indent=2)

    def add_bookmark(self, url, tags):
        if not any(b['url'] == url for b in self.bookmarks):
            self.bookmarks.append({"url": url, "tags": tags or []})
            self.save_bookmarks()

    def list_bookmarks(self):
        return self.bookmarks


class BookmarkTUI:
    def __init__(self):
        self.bookmark_manager = BookmarkManager()
        self.main()

    def main(self):
        self.url_edit = urwid.Edit("Enter Bookmark URL: ")
        self.tags_edit = urwid.Edit("Enter Tags (comma-separated): ")
        self.feedback_text = urwid.Text("")
        self.bookmarks_list = urwid.Text("")
        
        add_button = urwid.Button("Add Bookmark", on_press=self.add_bookmark)
        list_button = urwid.Button("List Bookmarks", on_press=self.list_bookmarks)

        layout = urwid.Pile([
            self.url_edit,
            self.tags_edit,
            urwid.Columns([add_button, list_button], dividechars=2),
            urwid.Divider(),
            self.feedback_text,
            urwid.Divider(),
            urwid.Text("Bookmarks:"),
            self.bookmarks_list,
        ])

        urwid.MainLoop(urwid.Filler(layout, valign='top')).run()

    def add_bookmark(self, button):
        url = self.url_edit.get_edit_text()
        tags = [tag.strip() for tag in self.tags_edit.get_edit_text().split(",")]
        if url:
            self.bookmark_manager.add_bookmark(url, tags)
            self.feedback_text.set_text(f"Bookmark added: {url}")
        else:
            self.feedback_text.set_text("URL cannot be empty")

    def list_bookmarks(self, button):
        bookmarks = self.bookmark_manager.list_bookmarks()
        if bookmarks:
            bookmark_str = "\n\n".join([f"URL: {bookmark['url']}\nTags: {', '.join(bookmark['tags'])}" for bookmark in bookmarks])
            self.bookmarks_list.set_text(bookmark_str)
        else:
            self.bookmarks_list.set_text("No bookmarks found.")


if __name__ == "__main__":
    BookmarkTUI()
