try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkinter import filedialog, colorchooser
from tkinter import ttk
from PIL import ImageTk, Image, ImageFont, ImageDraw
import numpy
import matplotlib.pyplot as plt
import time


# main window
root = tk.Tk()
root.title("Watermarker")
root.geometry("300x300")
root.resizable(width=True, height=True)


# watermark settings values to use------------------
color_to_use = (0, 0, 0, 255)
size_to_use = 30
font_to_use = "Gill Sans Medium.otf"
text_to_use = "Stadard Text"
position_to_use = (0, 0)

IMAGE = None

# watermarker settings in separated window
def watermarker(images):
    global color_to_use, size_to_use, font_to_use, text_to_use, position_to_use, IMAGE

    # opens settings in new window
    watermark_settings = tk.Toplevel(root)
    watermark_settings.title("watermarker")
    watermark_settings.resizable(width=True, height=True)

    # changes made on chosen 1st image
    image_to_use = images[0]

    image_to_use = Image.open(image_to_use)
    image_to_use.thumbnail((900, 900))

    # draw -------------------------
    def func_draw(iiimg):
        global font_to_use, size_to_use, color_to_use, text_to_use, position_to_use, IMAGE

        watermark_image = iiimg.convert("RGBA")
        watermark_image = watermark_image.copy()

        txt = Image.new('RGBA', watermark_image.size, (255, 255, 255, 0))

        image_font = ImageFont.truetype(font_to_use, size_to_use)

        draw = ImageDraw.Draw(txt)
        draw.text(position_to_use, text=text_to_use,
                  fill=color_to_use, font=image_font)

        combined = Image.alpha_composite(watermark_image, txt)

        img = ImageTk.PhotoImage(combined)
        IMAGE = numpy.asarray(combined)

        panel.configure(image=img)
        panel.image = img

    # hold and drag ----------------------------------------
    def function_function(x):
        global position_to_use
        position_to_use = (root.winfo_pointerx() - root.winfo_rootx(), root.winfo_pointery() - root.winfo_rooty())
        print(position_to_use)

    def drag_and_draw(x):
        function_function(x)
        func_draw(image_to_use)

    root.bind('<B1-Motion>', drag_and_draw)

    # text ------------------------------------------------
    text_label = tk.Label(watermark_settings, text="Text").grid(column=0, row=0)
    text = tk.Entry(watermark_settings)
    def return_text(x):
        global text_to_use
        text_to_use = text.get()
    def text_and_draw(x):
        return_text(1)
        func_draw(image_to_use)
    text.bind('<Return>', lambda x: text_and_draw(1))
    text.grid(column=1, row=0)

    # color ------------------------------------------------
    color_label = tk.Label(watermark_settings, text="color").grid(column=0, row=1)
    def choose_color():
        global color_to_use
        color_to_choose = colorchooser.askcolor(title="Choose color")[0]
        opacity_in_func = list(color_to_use)[-1]
        color_in_func = list(color_to_choose)
        color_in_func.append(opacity_in_func)
        color_to_use = tuple(color_in_func)
        return color_to_use
    def color_and_draw():
        choose_color()
        func_draw(image_to_use)

    color = tk.Button(watermark_settings, text="Select color", command=lambda: color_and_draw())
    color.grid(column=1, row=1)

    # opacity-transparency ------------------------------------------------
    opacity_label = tk.Label(watermark_settings, text="opacity").grid(column=0, row=3)
    def return_opacity(x):
        global color_to_use
        opacity_number = x * 255 / 100
        if len(color_to_use) == 3:
            color_to_use = list(color_to_use)
            color_to_use.append(int(opacity_number))
            color_to_use = tuple(color_to_use)
            print(color_to_use)
            return color_to_use
        else:
            color_to_use = list(color_to_use)
            color_to_use[-1] = int(opacity_number)
            color_to_use = tuple(color_to_use)
            print(color_to_use)
            return color_to_use

    def opacity_and_draw(x):
        return_opacity(x)
        func_draw(image_to_use)
        return return_opacity
    opacity = ttk.Scale(watermark_settings, from_=100, to=0, orient="horizontal",
                        command=lambda x: opacity_and_draw(opacity.get()))
    opacity.set(100)
    opacity.grid(column=1, row=3)

    # font ------------------------------------------------
    font_label = tk.Label(watermark_settings, text="font").grid(column=0, row=2)
    def return_font_label(x):
        global font_to_use
        font_dict = {" Gill Sans": "Gill Sans Medium.otf",
                     " Olympus": "Olympus-nD6Y.ttf",
                     " Paisley": "Paisleycaps-LPEZ.ttf",
                     " Tesla": "Tesla.otf",
                     }
        try:
            font_to_use = font_dict[x]
            return font_dict[x]
        except KeyError:
            print('error')
            print(KeyError)
            pass

    def font_family_and_draw(x):
        return_font_label(x)
        func_draw(image_to_use)
    font = ttk.Combobox(watermark_settings, width=27, postcommand=lambda: font_family_and_draw(font.get()))
    font['values'] = (
        " Gill Sans",
        " Olympus",
        " Paisley",
        " Tesla",
    )
    font.set(" Gill Sans")
    font.grid(column=1, row=2)

    # font_size ------------------------------------------------
    size_label = tk.Label(watermark_settings, text="size")
    size_label.grid(column=0, row=4)

    def return_font_size(x):
        global size_to_use
        size_to_use = int(x)

        return int(x)

    def font_size_and_draw(x):
        return_font_size(x)
        func_draw(image_to_use)

    font_size = ttk.Scale(watermark_settings, from_=10, to=200, orient="horizontal",
                          command=lambda x: font_size_and_draw(font_size.get()))
    font_size.grid(column=1, row=4)


    # SHOW BUTTON, sometimes you have to press enter (in text), or press arrow again to show; but you can press to this
    def show_func():
        text_and_draw(1)
        font_family_and_draw(font.get())
    tk.Button(watermark_settings, command=lambda: show_func(),
              width=30, text='show').grid(column=0, row=5, columnspan=2)

    # save_the_file
    def file_save():
        global IMAGE
        file = filedialog.askdirectory()
        print(file)
        watermark_settings.destroy()
        if file:
            for i in images:
                image_to_use = Image.open(i)
                image_to_use.thumbnail((900, 900))
                func_draw(image_to_use)
                i = file + '/' + i.split('/')[-1] + '_watermarked' + '.png'
                img = IMAGE
                plt.imsave(i, img)
                print(i)
        close_img()
        time.sleep(1)
        tk.messagebox.showinfo("Save", f"Watermarked images save to {file}")

    btn = ttk.Button(watermark_settings, text='Save', command=lambda: file_save())
    btn.grid(column=6)

# ------------------------------------------


def show_img():
    global panel
    names = filedialog.askopenfilenames()

    watermarker(names)


def close_img():
    global panel
    panel.configure(image="")
    panel.image = ""


# menu --------------------------------------
menu = tk.Menu(root)

item = tk.Menu(menu, tearoff=False)
item.add_command(label="open image to watermark", command=show_img)
item.add_command(label="close image", command=close_img)

menu.add_cascade(label="File", menu=item)
root.config(menu=menu)


panel = tk.Label(root)
panel.pack()


root.mainloop()