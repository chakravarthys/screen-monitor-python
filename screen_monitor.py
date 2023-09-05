import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab
import pyautogui
import numpy as np
import cv2
import winsound

class ScreenMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Monitor")

        self.label = ttk.Label(self.root, text="Press 'Select Area' to choose the section to monitor.")
        self.label.pack(pady=20)

        self.button1 = ttk.Button(self.root, text="Select Area", command=self.select_area)
        self.button1.pack(pady=10)

        self.button2 = ttk.Button(self.root, text="Start Monitoring", command=self.start_monitoring, state=tk.DISABLED)
        self.button2.pack(pady=10)

        self.button3 = ttk.Button(self.root, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.button3.pack(pady=10)

        self.area = None
        self.prev_screenshot = None
        self.monitoring = False

    def select_area(self):
        self.root.withdraw()
        self.root.after(1000, self.capture_screen)

    def capture_screen(self):
        screenshot = ImageGrab.grab()
        select_root = tk.Toplevel(self.root)
        select_root.title("Select Area")

        tk_screenshot = ImageTk.PhotoImage(screenshot)

        canvas = tk.Canvas(select_root, width=screenshot.width, height=screenshot.height)
        canvas.pack()

        canvas.create_image(0, 0, anchor=tk.NW, image=tk_screenshot)
        canvas.bind("<ButtonPress-1>", self.start_draw_rect)
        canvas.bind("<B1-Motion>", self.drawing_rect)
        canvas.bind("<ButtonRelease-1>", self.end_draw_rect)

        self.canvas = canvas
        self.select_root = select_root
        self.tk_screenshot = tk_screenshot

    def start_draw_rect(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def drawing_rect(self, event):
        self.canvas.delete("rect")
        self.end_x, self.end_y = event.x, event.y
        self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="red", tags="rect")

    def end_draw_rect(self, event):
        self.canvas.delete("rect")
        self.area = (self.start_x, self.start_y, self.end_x, self.end_y)
        self.select_root.destroy()
        self.root.deiconify()
        self.label.config(text=f"Area Selected: {self.area}")
        self.button2.config(state=tk.NORMAL)

    def start_monitoring(self):
        if self.area:
            self.monitoring = True
            self.button2.config(state=tk.DISABLED)
            self.button3.config(state=tk.NORMAL)
            self.monitor()

    def stop_monitoring(self):
        self.monitoring = False
        self.button2.config(state=tk.NORMAL)
        self.button3.config(state=tk.DISABLED)

    def monitor(self):
        if not self.monitoring:
            return

        x1, y1, x2, y2 = self.area
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        screenshot_np = np.array(screenshot)
        gray_screenshot = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        if self.prev_screenshot is not None:
            # Ensure the dimensions are the same before the comparison
            if gray_screenshot.shape == self.prev_screenshot.shape:
                diff = cv2.absdiff(self.prev_screenshot, gray_screenshot)
                if np.sum(diff) > 0:
                    for _ in range(3):  # loop for 3 beeps
                        winsound.Beep(2000, 500)
                        self.root.after(300)  # wait for 300 milliseconds between each beep
                    self.stop_monitoring()
            else:
                print("Dimensions changed, restarting monitoring")
                self.stop_monitoring()
                self.start_monitoring()

        self.prev_screenshot = gray_screenshot
        self.root.after(200, self.monitor)



if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenMonitorApp(root)
    root.mainloop()
