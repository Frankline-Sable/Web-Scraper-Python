from tkinter import *
import time, pyperclip


class Scrape(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Primitive Website Copier")
        self.config(background='white', padx=10, pady=4)
        self.resizable(0, 0)
        self.canvas = Canvas(self, width=600, height=300, background='white', highlightthickness=0, bd=0)
        self.logoImg = PhotoImage(file='logo.gif')
        self.sideImg1 = PhotoImage(file='guide.gif')
        self.sideImg2 = PhotoImage(file='side-logo.gif')
        self.sideImg3 = PhotoImage(file='side-logo.gif')

        self.alreadyExist = False
        self.entry = None
        self.opt_index=IntVar()
        self.screen_one()

    def screen_one(self):
        self.canvas = Canvas(self, width=600, height=300, background='white', highlightthickness=0, bd=0)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.canvas.update()

        line = self.canvas.create_line(self.canvas.winfo_width() * 0.77, self.canvas.winfo_height() * 0.98,
                                       self.canvas.winfo_width(),
                                       self.canvas.winfo_height() * 0.98, tag='_screen1_obj')
        self.canvas.itemconfig(line, fill='#D0D0D0')

        self.logoImg.config(width=128, height=128)
        self.logo_bg = self.canvas.create_image(0, 0, anchor=NW, image=self.logoImg)

        self.canvas.create_text(350, 64, text="Prim.. Website Scraper",
                                font=("Times New Roman", 32, "bold"),
                                fill="#404040", tag='_screen1_obj')

        r = self.canvas.create_rectangle(128, 128, 600, 272, outline='lightgray', tag='_screen1_obj')
        licence = 'Unless required by applicable law or agreed to in writing,\nsoftware distributed under the License is distributed on an\n"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\nKIND, either express or implied.  See the License for the\nspecific language governing permissions and limitations\nunder the License.'
        self.canvas.create_text(356, 192, text=licence,
                                font=("serif", 10, "italic"),
                                fill="black", tag='_screen1_obj')

        if not self.alreadyExist:
            self.nextButton = Button(self, text='Next>', command=self.next_page, padx=12, pady=4, bd=2)
            self.nextButton.pack(side=RIGHT)

            self.prevButton = Button(self, text='< Back', command=self.prev_page, padx=12, pady=4)
            self.prevButton.pack(side=RIGHT)

        self.alreadyExist = True

    def screen_two(self):
        self.canvas.delete('_screen1_obj')
        self.canvas.itemconfigure(self.logo_bg, image=self.sideImg2)
        self.canvas.pack(side=LEFT)
        self.canvas.config(width=self.logoImg.width(), height=328)
        self.resizable(False, False)

        label = Label(self, text="Copy the link on the clipboard\nand paste it or enter down below:",
                      font=('comic sans ms', 16, 'normal'),
                      background='white', foreground='#404040 ', width=36, padx=4, pady=16)
        label.pack(fill=BOTH, side=TOP)

        sub_canvas = Canvas(self, background='white', height=100, bd=0, highlightthickness=0)
        sub_canvas.pack(fill=BOTH, side=TOP)
        sub_canvas.update()

        self.sideImg1.config(width=128, height=128)
        im = sub_canvas.create_image(sub_canvas.winfo_width() / 3, 0, anchor=NW, image=self.sideImg1)

        self.entry = Entry(self, font=('normal', 11, 'normal'),
                           background='#594d45', foreground='white', borderwidth=2, cursor='plus',
                           insertwidth=3, insertbackground='red', selectbackground='blue',
                           textvariable="Paste Link Here")
        self.entry.insert(0, 'http://')
        self.entry.pack(fill=BOTH, side=TOP)
        self.pasteButton = Button(self, text='Paste Link *', command=self.paste_link,
                                  activebackground='#02A4D3', highlightbackground='LIGHTGRAY',
                                  relief=GROOVE)
        self.pasteButton.pack(fill=BOTH, side=TOP)

        sub_canvas2 = Canvas(self, background='white', height=16, bd=0, highlightthickness=0)
        sub_canvas2.pack(fill=BOTH, side=TOP)
        sub_canvas2.update()

        frame = Frame(self, background='white')
        frame.pack(fill=BOTH)

        redbutton = Radiobutton(frame, text="Images Only", fg="#712617", bg='white', variable=self.opt_index,
                                command=self.rad_opt, value=1)
        redbutton.pack(side=LEFT)

        greenbutton = Radiobutton(frame, text="Single Page", fg="brown", bg='white', variable=self.opt_index,
                                  command=self.rad_opt, value=2,)
        greenbutton.select()
        greenbutton.pack(side=LEFT)

        bluebutton = Radiobutton(frame, text="Whole Website", fg="#bd1e24", bg='white', variable=self.opt_index,
                                 command=self.rad_opt, value=3)
        bluebutton.pack(side=LEFT)

        self.nextButto = Button(self, text='Finish>', command=self.screen_three(), padx=12, pady=4, bd=2)
        self.nextButto.pack(side=RIGHT, anchor=SE)

        self.prevButto = Button(self, text='< Back', command=self.prev_page, padx=12, pady=4)
        self.prevButto.pack(side=RIGHT, anchor=SW)

    def rad_opt(self):
        print(str(self.opt_index.get()))

    def paste_link(self):
        pst = pyperclip.paste()

        self.entry.insert(len(self.entry.get()), pst)

    def prev_page(self):
        self.canvas.destroy()
        self.nextButton.destroy()
        self.prevButton.destroy()
        self.alreadyExist = False

        self.screen_one()

    def next_page(self):
        self.nextButton.destroy()
        self.prevButton.destroy()

        self.screen_two()

    def screen_three(self):
        self.canvas.itemconfigure(self.logo_bg, image=self.sideImg2)


class animations:
    def __init__(self,canvas):
        self.canvas=canvas

        self.anim_files_1=[
            PhotoImage(file='anim_one/scr1.gif'),
            PhotoImage(file='anim_one/scr2.gif'),
            PhotoImage(file='anim_one/scr3.gif'),
            PhotoImage(file='anim_one/scr4.gif'),
            PhotoImage(file='anim_one/scr5.gif'),
            PhotoImage(file='anim_one/scr6.gif'),
        ]
        self.anim_1=self.canvas.create_image(0,0,anchor=NW, image=self.anim_files_1[0])
        self.time_init=time.time()
        self.current_img=0
        self.current_img_add = 0

    def execute_anim_1(self):
        self.img_array=[]
        if time.time()-self.time_init>0.1:
            self.current_img+=1
            if self.current_img>=1:
                self.current_img=0
            self.time_init=time.time()
        self.canvas.itemconfig(self.anim_1, image=self.img_array[self.current_img])


def main():
    tk = Scrape()
    #anim=animations(tk.canvas)

    while (1):
        #anim.execute_anim_1()
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)



if __name__ == '__main__':
    main()
