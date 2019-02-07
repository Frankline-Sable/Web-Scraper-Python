import pyperclip
import time
from tkinter import *
from tkinter import messagebox
from web_scraper.scraper_CMD import ScraperCMD
import webbrowser, threading


class Scraper(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Primitive Website Copier")
        self.config(background='white', padx=10, pady=4, width=600, height=372, highlightthickness=0, bd=0)

        self.frame = Frame(self, background='black', width=600, height=372)
        self.frame.pack(fill=BOTH)

        self.cmd_line = None
        self.list_logs = None
        self.log_label = None
        self.scraper_exit = False

        self.img_logo = PhotoImage(file='logo.gif')
        self.img_guide = PhotoImage(file='guide.gif')
        self.img_logo2 = PhotoImage(file='side-logo.gif')
        self.img_prd = PhotoImage(file='proceed.gif')
        self.anim_files_1 = [
            PhotoImage(file='anim_one/scr1.gif'),
            PhotoImage(file='anim_one/scr2.gif'),
            PhotoImage(file='anim_one/scr3.gif'),
            PhotoImage(file='anim_one/scr4.gif'),
            PhotoImage(file='anim_one/scr5.gif'),
            PhotoImage(file='anim_one/scr6.gif'),
        ]
        self.anim_files_2 = [
            PhotoImage(file='anim_two/load00.gif'),
            PhotoImage(file='anim_two/load01.gif'),
            PhotoImage(file='anim_two/load02.gif'),
            PhotoImage(file='anim_two/load03.gif'),
            PhotoImage(file='anim_two/load04.gif'),
            PhotoImage(file='anim_two/load05.gif'),
            PhotoImage(file='anim_two/load06.gif'),
            PhotoImage(file='anim_two/load07.gif'),
            PhotoImage(file='anim_two/load08.gif'),
            PhotoImage(file='anim_two/load09.gif'),
            PhotoImage(file='anim_two/load10.gif'),
            PhotoImage(file='anim_two/load11.gif'),
            PhotoImage(file='anim_two/load12.gif'),
            PhotoImage(file='anim_two/load13.gif'),
            PhotoImage(file='anim_two/load14.gif'),
            PhotoImage(file='anim_two/load15.gif'),
            PhotoImage(file='anim_two/load16.gif'),
            PhotoImage(file='anim_two/load17.gif'),
            PhotoImage(file='anim_two/load18.gif'),
            PhotoImage(file='anim_two/load19.gif'),
            PhotoImage(file='anim_two/done1.gif')
        ]

        self.index = 1
        self.opt_index = IntVar()
        self.entry = None
        self.start_scraping = False
        self.anim_call = None
        self.anim_call2 = None
        self.scrape_data = 2
        self.scrape_web = None
        self.opt_dict = {1: "only images", 2: "only a single page", 3: "*.* everything! "}
        window_width = self.winfo_reqwidth()
        winfo_height = self.winfo_reqheight()

        position_right = int(self.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.winfo_screenheight() / 2 - winfo_height / 2)

        self.geometry("+{}+{}".format(position_right, position_down))
        self.view_1()

    def init_frame(self):
        self.frame = Frame(self, background='black', width=600, height=372)
        self.frame.pack(fill=BOTH)

    def view_1(self):
        canvas = Canvas(self.frame, width=600, height=300, background='white', highlightthickness=0, bd=0)
        canvas.pack(fill=BOTH, side=TOP)
        canvas.update()

        line = canvas.create_line(canvas.winfo_width() * 0.77, canvas.winfo_height() * 0.98,
                                  canvas.winfo_width(),
                                  canvas.winfo_height() * 0.98, tag='_screen1_obj')
        canvas.itemconfig(line, fill='#D0D0D0')

        self.img_logo.config(width=128, height=128)
        canvas.create_image(0, 0, anchor=NW, image=self.img_logo)

        canvas.create_text(350, 64, text="Prim.. Website Scraper",
                           font=("Times New Roman", 32, "bold"),
                           fill="#404040", tag='_screen1_obj')

        canvas.create_rectangle(128, 128, 600, 272, outline='lightgray')
        licence = 'Unless required by applicable law or agreed to in writing,\nsoftware distributed' \
                  ' under the License is distributed on an\n"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS ' \
                  'OF ANY\nKIND, either express or implied.  See the License for the\nspecific language ' \
                  'governing permissions and limitations\nunder the License; GNU Public license(Fully Freeware)' \
                  '\nProudly made by:\n\tFrankline Sable '
        canvas.create_text(353, 198, text=licence,
                           font=("serif", 10, "italic"),
                           fill="black", tag='_screen1_obj')
        bottom_frame = Frame(self.frame, bg='white')
        bottom_frame.pack(side=BOTTOM, fill=BOTH)

        label = Label(bottom_frame, text="Copy ",
                      font=('comic sans ms', 11, 'normal'),
                      background='white', foreground='#404040', image=self.img_prd)
        label.pack(side=LEFT)

        next_btn = Button(bottom_frame, text='Next>', command=self.go_forward, padx=12, pady=4, bd=2)
        next_btn.pack(side=RIGHT)

        prev_btn = Button(bottom_frame, text='< Back', command=self.go_back, padx=12, pady=4)
        prev_btn.pack(side=RIGHT)

    def view_2(self):
        lft_frame = Frame(self.frame)
        lft_frame.pack(side=LEFT, fill=BOTH)

        top_frame = Frame(self.frame)
        top_frame.pack(side=TOP, fill=BOTH)

        bottom_frame = Frame(self.frame, bg="white")
        bottom_frame.pack(side=BOTTOM, fill=BOTH)

        self.frame.config(bg='white')

        canvas = Canvas(lft_frame, width=128, height=328, background='white', highlightthickness=0, bd=0)
        canvas.pack(fill=BOTH)
        canvas.update()

        self.img_logo.config(width=128, height=128)
        canvas.create_image(0, 0, anchor=NW, image=self.img_logo2)

        label = Label(top_frame, text="Copy the link on the clipboard\nand paste it or enter down below:",
                      font=('comic sans ms', 16, 'normal'),
                      background='white', foreground='#404040 ', width=36, padx=4, pady=16)
        label.pack(fill=BOTH)

        sub_canvas = Canvas(top_frame, background='white', height=100, bd=0, highlightthickness=0)
        sub_canvas.pack(fill=BOTH)
        sub_canvas.update()

        sub_canvas.create_image(sub_canvas.winfo_width() / 3, 0, anchor=NW, image=self.img_guide)

        self.entry = Entry(top_frame, font=('normal', 11, 'normal'),
                           background='#594d45', foreground='white', borderwidth=2, cursor='plus',
                           insertwidth=3, insertbackground='red', selectbackground='blue',
                           textvariable="Paste Link Here")
        self.entry.insert(INSERT, 'http://')
        self.entry.pack(fill=BOTH)

        paste_btn = Button(top_frame, text='Paste Link *', command=self.paste_link,
                           activebackground='#02A4D3', highlightbackground='LIGHTGRAY',
                           relief=GROOVE)
        paste_btn.pack(fill=BOTH)

        lazy_frame = Frame(top_frame, height=16, bg="white")
        lazy_frame.pack(fill=BOTH)

        radio_frame = Frame(top_frame, background='white')
        radio_frame.pack(fill=BOTH)

        Radiobutton(radio_frame, text="Images Only", fg="#712617", bg='white', variable=self.opt_index,
                    command=self.rad_opt, value=1).pack(side=LEFT)
        _sing_rad = Radiobutton(radio_frame, text="Single Page", fg="brown", bg='white',
                                variable=self.opt_index,
                                command=self.rad_opt, value=2, )
        _sing_rad.select()
        _sing_rad.pack(side=LEFT)

        Radiobutton(radio_frame, text="Whole Website", fg="#bd1e24", bg='white', variable=self.opt_index,
                    command=self.rad_opt, value=3).pack(side=LEFT)

        next_btn = Button(bottom_frame, text='Next>', command=self.go_forward, padx=12, pady=4, bd=2)
        next_btn.pack(side=RIGHT)

        prev_btn = Button(bottom_frame, text='< Back', command=self.go_back, padx=12, pady=4)
        prev_btn.pack(side=RIGHT)

    def view_3(self):
        lft_frame = Frame(self.frame)
        lft_frame.pack(side=LEFT, fill=BOTH)

        top_frame = Frame(self.frame)
        top_frame.pack(side=TOP, fill=BOTH)

        bottom_frame = Frame(self.frame, bg="white")
        bottom_frame.pack(side=BOTTOM, fill=BOTH)

        canvas = Canvas(lft_frame, width=128, height=328, background='white', highlightthickness=0, bd=0)
        canvas.pack(fill=BOTH)
        canvas.update()

        self.anim_call = Animator(canvas, self.anim_files_1, 0, 0.2)

        disp = self.scrape_web[0:40] + ".."
        label = Label(top_frame,
                      text="Scraping " + self.opt_dict.get(self.scrape_data) + " from the link\n\"" + disp + "\"",
                      font=('comic sans ms', 14, 'normal'),
                      background='white', foreground='#404040 ', width=36, padx=4, pady=16)
        label.pack(fill=BOTH)

        scrollbar = Scrollbar(top_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.list_logs = Listbox(top_frame, yscrollcommand=scrollbar.set)
        self.list_logs.insert(END,
                              "NB: The process progress are displayed below, it can take sometimes depending on your internet speed")
        self.list_logs.insert(END, "NB: Scroll down to view the various progresses")

        self.list_logs.pack(fill=BOTH)
        scrollbar.config(command=self.list_logs.yview)

        self.log_label = Label(top_frame,
                               text="Please Wait...",
                               font=('comic sans ms', 10, 'normal'),
                               background='white', foreground='#404040 ')
        self.log_label.pack(fill=BOTH)

        loader_canvas = Canvas(top_frame, height=24, background='white', highlightthickness=0, bd=0)
        loader_canvas.pack(fill=BOTH)
        loader_canvas.update()

        self.anim_call2 = Animator(loader_canvas, self.anim_files_2, loader_canvas.winfo_width() / 2.3, 0.1)

        self.last_button = Button(bottom_frame, text='x < Quit', command=self.quit_load, padx=12, pady=4, bd=2)
        self.last_button.pack(side=RIGHT)

        self.initiate_scraping()

    def initiate_scraping(self):
        self.start_scraping = True
        self.cmd_line = ScraperCMD(self.scrape_web, self.scrape_data)

        threading.Thread(target=self.cmd_line._commence_scraping).start()


    def _speedy_cmd_analysis(self):
        self.start_scraping = self.cmd_line._process_running()
        for lg in self.cmd_line.get_quicklog():
            self.list_logs.insert(END, lg)

        if not self.start_scraping:
            self.log_label.config(text="It's done!", fg="blue")
            self.anim_call2._execution_done()
            self.anim_call._execution_done()
            self.last_button.config(text="Complete!(X)", command=self._exit_scraper, bg="brown", fg='white')

            self.list_logs.insert(END, "")
            self.list_logs.insert(END, "=" * 15, "Error logs are below:", "=" * 15, )
            for x in self.cmd_line.get_errorlogs():
                self.list_logs.insert(END, x)

    def _exit_scraper(self):
        self.scraper_exit = True
        sys.exit(0)

    def go_back(self):
        self.start_scraping = False
        self.frame.destroy()
        self.init_frame()
        self.index -= 1
        self.call_index()

    def go_forward(self):
        press_on = True
        url = None
        if self.index == 2:
            url = self.entry.get()
            if not self.link_verifier(url):
                press_on = False
                messagebox._show("Invalid Url",
                                 "The url you've entered, i.e: \n%s\nAppears to be invalid, please correct it" % (
                                     url), messagebox.ERROR, messagebox.OK)

        if press_on:
            self.scrape_web = url
            self.frame.destroy()
            self.init_frame()
            self.index += 1
            self.call_index()

    @staticmethod
    def link_verifier(link):
        valid = True
        pattern = re.compile(r'http(s)?://(\w)+')
        search = pattern.search(link)
        if search is None:
            valid = False
        elif link.count('http://') > 1:
            valid = False
        elif link.count('https://') > 1:
            valid = False
        elif len(link) > 50:
            valid = False
        return valid

    def call_index(self):
        if self.index < 1:
            self.index = 1

        elif self.index > 3:
            self.index = 3

        if self.index == 1:
            self.view_1()
        elif self.index == 2:
            self.view_2()
        elif self.index == 3:
            self.view_3()

    def paste_link(self):
        pst = pyperclip.paste()
        self.entry.insert(len(self.entry.get()), pst)

    def rad_opt(self):
        self.scrape_data = self.opt_index.get()

    def quit_load(self):
        if messagebox._show(title="Halting scraping process..", message="Are u sure you want to cancel the process?",
                            _icon=messagebox.QUESTION, _type=messagebox.YESNO) == 'yes':
            self.go_back()


class Animator:
    def __init__(self, canvas, anim_files, pos, speed):
        self.canvas = canvas

        self.anim_files_1 = anim_files
        self.speed = speed
        self.anim_1 = self.canvas.create_image(pos, 0, anchor=NW, image=self.anim_files_1[0])
        self.time_init = time.time()
        self.current_img = 0
        self.current_img_add = 0

    def execute_anim_1(self):
        if time.time() - self.time_init > self.speed:
            self.current_img += 1
            if self.current_img >= (len(self.anim_files_1) - 1):
                self.current_img = 0
            self.time_init = time.time()
        self.canvas.itemconfig(self.anim_1, image=self.anim_files_1[self.current_img])

    def _execution_done(self):
        self.canvas.itemconfig(self.anim_1, image=self.anim_files_1[len(self.anim_files_1) - 1])


def main():
    tk = Scraper()

    while True:
        if tk.start_scraping:
            tk.anim_call.execute_anim_1()
            tk.anim_call2.execute_anim_1()
            tk._speedy_cmd_analysis()
        if tk.scraper_exit:
            break

        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)


if __name__ == '__main__':
    main()
