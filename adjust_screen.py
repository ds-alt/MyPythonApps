import customtkinter as ctk
import screen_brightness_control as sbc

class MonitorControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor Control")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Brightness Control
        self.brightness_label = ctk.CTkLabel(root, text="Brightness")
        self.brightness_label.pack(pady=10)

        self.brightness_scale = ctk.CTkSlider(root, from_=0, to=100, command=self.set_brightness)
        current_brightness = sbc.get_brightness()[0]  # Get the brightness of the first monitor
        self.brightness_scale.set(current_brightness)
        self.brightness_scale.pack(pady=10)

        # Contrast Control (Placeholder)
        self.contrast_label = ctk.CTkLabel(root, text="Contrast (Not functional)")
        self.contrast_label.pack(pady=10)

        self.contrast_scale = ctk.CTkSlider(root, from_=0.5, to=1.5, command=self.set_contrast)
        self.contrast_scale.set(1)
        self.contrast_scale.pack(pady=10)

    def set_brightness(self, value):
        sbc.set_brightness(int(value))

    def set_contrast(self, value):
        # Placeholder for contrast adjustment functionality
        # Actual implementation depends on the capabilities of your monitor and available libraries
        print(f"Contrast set to {value}")  # Replace this with actual contrast adjustment code

if __name__ == "__main__":
    root = ctk.CTk()
    app = MonitorControlApp(root)
    root.mainloop()
