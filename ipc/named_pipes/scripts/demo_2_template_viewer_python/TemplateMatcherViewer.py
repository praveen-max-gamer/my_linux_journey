import tkinter as tk
from PIL import Image, ImageTk
import threading
import io
import os

PIPE_NAME = "/tmp/demo_named_pipe"

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Demo 2 - Named pipe : {PIPE_NAME}")
        self.root.geometry("800x400")
        
        self.canvas = tk.Canvas(root, bg="lightblue")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.photo = None
        self.current_image = None  # Store original PIL image for rescaling
        
        self.canvas.bind("<Configure>", self.on_resize)
        
        self.running = True
        self.thread = threading.Thread(target=self.read_pipe, daemon=True)
        self.thread.start()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def read_pipe(self):
        if not os.path.exists(PIPE_NAME):
            os.mkfifo(PIPE_NAME)
        
        print(f"Waiting for images on pipe: {PIPE_NAME}")
        print(f"Send image data with: cat image.png > {PIPE_NAME}")
        
        while self.running:
            try:
                with open(PIPE_NAME, "rb") as pipe:
                    data = pipe.read()
                    if data:
                        img = Image.open(io.BytesIO(data))
                        self.current_image = img
                        self.root.after(0, self.render_image)
            except Exception as e:
                if self.running:
                    print(f"Error reading pipe: {e}")
    
    def render_image(self):
        if self.current_image is None:
            return
        try:
            w = self.canvas.winfo_width() or 200
            h = self.canvas.winfo_height() or 200
            img = self.current_image.copy()
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(w // 2, h // 2, anchor=tk.CENTER, image=self.photo)
        except Exception as e:
            print(f"Error displaying image: {e}")
    
    def on_resize(self, event):
        self.render_image()
    
    def on_close(self):
        self.running = False
        self.root.destroy()
        if os.path.exists(PIPE_NAME):
            os.remove(PIPE_NAME)

def main():
    root = tk.Tk()
    root.attributes("-topmost", True)
    ImageViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()