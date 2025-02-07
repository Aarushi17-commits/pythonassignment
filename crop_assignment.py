import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("1000x700")

        # Variables
        self.image = None
        self.cropped_image = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect_id = None
        self.crop_rect = None
        self.undo_stack = []  # Stack for undo functionality
        self.redo_stack = []  # Stack for redo functionality

        # UI Elements
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        self.load_button = tk.Button(button_frame, text="Load Image (Ctrl+O)", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(button_frame, text="Save Image (Ctrl+S)", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.grayscale_button = tk.Button(button_frame, text="Grayscale", command=self.convert_to_grayscale, state=tk.DISABLED)
        self.grayscale_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edge_button = tk.Button(button_frame, text="Edge Detection", command=self.detect_edges, state=tk.DISABLED)
        self.edge_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.undo_button = tk.Button(button_frame, text="Undo (Ctrl+Z)", command=self.undo, state=tk.DISABLED)
        self.undo_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.redo_button = tk.Button(button_frame, text="Redo (Ctrl+Y)", command=self.redo, state=tk.DISABLED)
        self.redo_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Resize Slider
        self.resize_label = tk.Label(button_frame, text="Resize:")
        self.resize_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.resize_slider = tk.Scale(button_frame, from_=10, to=200, orient=tk.HORIZONTAL, command=self.resize_image)
        self.resize_slider.pack(side=tk.LEFT, padx=5, pady=5)
        self.resize_slider.set(100)

        # Mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Keyboard shortcuts
        self.root.bind("<Control-o>", lambda event: self.load_image())
        self.root.bind("<Control-s>", lambda event: self.save_image())
        self.root.bind("<Control-q>", lambda event: self.root.quit())
        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-y>", lambda event: self.redo())

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(self.image)
            self.save_button.config(state=tk.NORMAL)
            self.grayscale_button.config(state=tk.NORMAL)
            self.edge_button.config(state=tk.NORMAL)
            self.undo_stack = []  # Clear undo stack when a new image is loaded
            self.redo_stack = []  # Clear redo stack
            self.update_undo_redo_buttons()

    def display_image(self, image):
        self.canvas.delete("all")
        image = Image.fromarray(image)
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_button_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.crop_image()

    def crop_image(self):
        if self.image is not None:
            x1 = min(self.start_x, self.end_x)
            y1 = min(self.start_y, self.end_y)
            x2 = max(self.start_x, self.end_x)
            y2 = max(self.start_y, self.end_y)

            if x2 > x1 and y2 > y1:
                self.crop_rect = (x1, y1, x2, y2)
                self.cropped_image = self.image[y1:y2, x1:x2]
                self.undo_stack.append(self.image.copy())  # Save state for undo
                self.redo_stack = []  # Clear redo stack
                self.update_undo_redo_buttons()
                self.display_image(self.cropped_image)

    def resize_image(self, value):
        if self.cropped_image is not None:
            scale = int(value) / 100.0
            resized_image = cv2.resize(self.cropped_image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            self.display_image(resized_image)

    def save_image(self):
        if self.cropped_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                save_image = cv2.cvtColor(self.cropped_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite(file_path, save_image)
                messagebox.showinfo("Success", "Image saved successfully!")

    def convert_to_grayscale(self):
        if self.cropped_image is not None:
            gray_image = cv2.cvtColor(self.cropped_image, cv2.COLOR_RGB2GRAY)
            gray_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)  # Convert back to 3 channels for display
            self.undo_stack.append(self.cropped_image.copy())  # Save state for undo
            self.redo_stack = []  # Clear redo stack
            self.update_undo_redo_buttons()
            self.cropped_image = gray_image
            self.display_image(self.cropped_image)

    def detect_edges(self):
        if self.cropped_image is not None:
            edges = cv2.Canny(self.cropped_image, 100, 200)
            edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)  # Convert to 3 channels for display
            self.undo_stack.append(self.cropped_image.copy())  # Save state for undo
            self.redo_stack = []  # Clear redo stack
            self.update_undo_redo_buttons()
            self.cropped_image = edges
            self.display_image(self.cropped_image)

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.cropped_image.copy())  # Save current state for redo
            self.cropped_image = self.undo_stack.pop()  # Restore previous state
            self.display_image(self.cropped_image)
            self.update_undo_redo_buttons()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.cropped_image.copy())  # Save current state for undo
            self.cropped_image = self.redo_stack.pop()  # Restore next state
            self.display_image(self.cropped_image)
            self.update_undo_redo_buttons()

    def update_undo_redo_buttons(self):
        self.undo_button.config(state=tk.NORMAL if self.undo_stack else tk.DISABLED)
        self.redo_button.config(state=tk.NORMAL if self.redo_stack else tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()