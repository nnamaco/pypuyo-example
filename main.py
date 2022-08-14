import pypuyo as ppy
import tkinter as tk


class MainFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        master.title('pyyo_beta')
        master.geometry("500x500")
        master.resizable(width=False, height=False)
        master.bind("<KeyPress>", lambda e: self.key_pressed(e.keysym))
        self.pack(expand=1, fill=tk.BOTH)

        self.game = ppy.Game(frames_to_fall=10)
        if max(self.game.get_height(), self.game.get_width()) == self.game.get_height():
            self.canvas = self.GameCanvas(self, 500 * (self.game.get_width() / self.game.get_height()), 500)
        elif max(self.game.get_height(), self.game.get_width()) == self.game.get_width():
            self.canvas = self.GameCanvas(self, 500, 500 * (self.game.get_height() / self.game.get_width()))
        else:
            self.canvas = self.GameCanvas(self, 500, 500)
        
        self.after(500, self.update)

    def update(self):
        self.game.update()
        self.canvas.draw_color(self.game.get())
        self.after(50, self.update)
    
    def key_pressed(self, key):
        if not self.game.is_over():
            if key == "a":
                self.game.move_left()
            elif key == "n":
                self.game.spin_left()
            elif key == "m":
                self.game.spin_right()
            elif key == "d":
                self.game.move_right()

    class GameCanvas(tk.Canvas):
        def __init__(self, master=None, width=100, height=100, x=0, y=0):
            self.width = width
            self.height = height
            super().__init__(master,
                             width=width,
                             height=height,
                             highlightthickness=0,
                             background="#FFFFFF"
                            )
            self.place(x=x, y=y)
        
        def draw_color(self, list):
            self.delete("all")
            block_width = max(self.height, self.width) / len(list)
            for yi in range(len(list)):
                for xi, color in enumerate(list[yi]):
                    if color is not None:
                        self.create_rectangle(block_width * xi,
                                            block_width * yi,
                                            block_width * (xi + 1),
                                            block_width * (yi + 1),
                                            fill=color,
                                            outline=color
                                            )


if __name__ == '__main__':
    root = tk.Tk()
    app = MainFrame(root)
    app.mainloop()