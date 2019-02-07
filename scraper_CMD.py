import requests
import pprint
import bs4
import re
import os
import threading


class ScraperCMD:
    def __init__(self, link, option):
        self.link = link
        self.option = option

        self.working_path = "C:/Users/%s/Documents/" % (os.environ["USERNAME"])
        if not os.path.isdir(self.working_path):
            self.working_path = os.getcwd()

        self.working_path = os.path.join(self.working_path, "Web Scraper")
        if not os.path.isdir(self.working_path):
            os.makedirs(self.working_path, exist_ok=True)
        os.chdir(self.working_path)

        self.arr_errorlogs = []
        self.quick_logs = []

        self.server_dir = None
        self.host = self.get_host(self.link)
        self._p_running=None

    def _commence_scraping(self):
        self._p_running=True
        scraping_opts = {1: self._grab_images,
                         2: self._grab_single_page,
                         3: self._grab_everything}

        self.set_quicklog(" ")
        self.set_quicklog("Working Path Set to: %s" % self.working_path)

        main_thread = threading.Thread(target=scraping_opts.get(self.option))
        main_thread.start()

        main_thread.join()

        self._p_running = False

        print("Scraping success!\n\n", '=' * 25, "Errors During Operation:", '=' * 25)
        msg = self.get_errorlogs()
        if not bool(msg):
            msg = "\tNo Errors, So far so good"
        pprint.pprint(msg)

    def _get_dirs(self, link):
        pattern = re.compile('http(s)?://((\w+\S)+/)+')
        search = pattern.search(link)

        if search is None:
            self.server_dir = self.link + "/"
        else:
            self.server_dir = search.group()

        folder_vw = self.server_dir.replace('https://', "")
        folder_vw = folder_vw.replace('http://', "")
        return folder_vw

    @staticmethod
    def get_host(url):
        url = url.replace('https://', "")
        url = url.replace('http://', "")
        url = url.split("/")[0]
        return url

    def _process_running(self):
        return self._p_running

    def set_quicklog(self, log):
        self.quick_logs.append(log)
        print(log)

    def get_quicklog(self):
        return self.quick_logs

    def _browse_styles(self, lnk, _cwd):

        pattern = re.compile('http(s)?://(\w*\S*)*')
        search = pattern.search(lnk)
        full_lnk = lnk

        if search is None:
            _cwd = self._pop_back(lnk, _cwd)
            lnk = lnk.replace("../", "")
            full_lnk = "http://" + _cwd + lnk
        file_dir = self._get_dirs(full_lnk)

        os.makedirs(file_dir, exist_ok=True)

        try:
            result = requests.get(full_lnk)
            result.raise_for_status()
            page = open(os.path.join(file_dir, os.path.basename(full_lnk)), 'wb')

            for chunk in result.iter_content(100000):
                page.write(chunk)
            page.close()

            if full_lnk.endswith(".css") or full_lnk.endswith(".script"):
                urls = self._css_url_fetcher(_result_set=result)
                for rls in urls:
                    file_dir = self._get_dirs(full_lnk)
                    self.set_quicklog("Fetching css url %s" % rls)
                    self.fetch_images_and_meta(rls, file_dir)

        except Exception as err:
            self.set_errorlogs(err)

    def _browse_images(self, lnk, _cwd):

        pattern = re.compile('http(s)?://(\w*\S*)*')
        search = pattern.search(lnk)
        full_lnk = lnk

        if search is None:
            _cwd = self._pop_back(lnk, _cwd)
            lnk = lnk.replace("../", "")
            full_lnk = "http://" + _cwd + lnk
        file_dir = self._get_dirs(full_lnk)

        os.makedirs(file_dir, exist_ok=True)

        try:
            result = requests.get(full_lnk)
            result.raise_for_status()
            if not full_lnk.endswith(".css") or not full_lnk.endswith(".script"):
                page = open(os.path.join(file_dir, os.path.basename(full_lnk)), 'wb')
                for chunk in result.iter_content(100000):
                    page.write(chunk)
                page.close()
            else:
                urls = self._css_url_fetcher(_result_set=result)
                for rls in urls:
                    file_dir = self._get_dirs(full_lnk)
                    self.set_quicklog("Fetching css url %s" % rls)
                    self.fetch_images_and_meta(rls, file_dir)

        except Exception as err:
            self.set_errorlogs(err)

    def fetch_images_and_meta(self, lnk, _cwd):
        pattern = re.compile('http(s)?://(\w*\S*)*')
        search = pattern.search(lnk)
        full_lnk = lnk
        if search is None:
            _cwd = self._pop_back(lnk, _cwd)
            lnk = lnk.replace("../", "")
            full_lnk = "http://" + _cwd + lnk
        file_dir = self._get_dirs(full_lnk)

        os.makedirs(file_dir, exist_ok=True)
        result = requests.get(full_lnk)

        try:
            result.raise_for_status()
            page = open(os.path.join(file_dir, os.path.basename(full_lnk)), 'wb')

            for chunk in result.iter_content(100000):
                page.write(chunk)
            page.close()
        except Exception as err:
            self.set_errorlogs(err)

        pass

    def _pop_back(self, local_dir, global_dir):
        count = local_dir.count("../")
        while count > 0:
            split_dir = global_dir.split('/')
            split_dir.pop()
            if global_dir.endswith("/") or global_dir.endswith("\\"):
                split_dir.pop()
            global_dir = ''
            for drs in split_dir:
                global_dir += "%s/" % drs

            count -= 1
        return global_dir

    def _css_url_fetcher(self, _result_set):
        urls = []
        for chunk in _result_set.iter_lines(100000):
            if len(chunk) < 20000:
                pattern = re.compile(r"url( )?\(((\w*\d*\S*\s*)*)\)")
                search = pattern.search(str(chunk))
                if search is not None:
                    grp = search.group(2)
                    grp = grp.replace("'", "")
                    grp = grp.replace('"', '')
                    grp = grp.split('format(')[0]
                    grp = grp.split('?')[0]
                    grp = grp.split(')')[0]
                    urls.append(grp)
                    urls = urls + self.greed_search(search)
            else:
                pass
        return urls

    def greed_search(self, search):
        holder = []
        grp = search.group()
        arr1 = grp.split('format(')
        for x in arr1:
            arr2 = x.split('url(')
            for y in arr2:
                tr = y.split("?")[0]
                tr = tr.replace("'", "")
                tr = tr.replace('"', '')
                tr = tr.split(')')[0]
                if len(tr) > 10:
                    holder.append(tr)
        return holder

    def set_errorlogs(self, error):
        self.arr_errorlogs.append(str(error))

    def get_errorlogs(self):
        return self.arr_errorlogs

    def _image_fetch(self):
        current_link = self.link

        self.set_quicklog("Fetching Images from: %s" % current_link)
        file_dir = self._get_dirs(current_link)

        os.makedirs(file_dir, exist_ok=True)
        try:
            result = requests.get(current_link)
            result.raise_for_status()

            soup = bs4.BeautifulSoup(result.text, features='lxml')

            images = soup.select('img')
            for lnk in images:
                style_url = str(lnk.get('src'))
                self.set_quicklog("Fetching images %s" % style_url)
                self._browse_images(style_url, file_dir)

            styles = soup.select('link')
            for lnk in styles:
                style_url = str(lnk.get('href'))
                self.set_quicklog("Fetching css images from %s" % style_url)
                self._browse_images(style_url, file_dir)

        except requests.ConnectionError as err1:
            self.set_errorlogs(err1)
        except Exception as err2:
            self.set_errorlogs(err2)

    def _single_page(self):
        self.set_quicklog("Fetching Page: %s" % self.link)

        file_dir = self._get_dirs(self.link)
        os.makedirs(file_dir, exist_ok=True)
        try:
            result = requests.get(self.link)
            result.raise_for_status()

            soup = bs4.BeautifulSoup(result.text, features='lxml')
            page = open(os.path.join(file_dir, os.path.basename(self.link)), 'wb')

            for chunk in result.iter_content(100000):
                page.write(chunk)
            page.close()
            self.set_quicklog("Page fetched successfully")

            styles = soup.select('link')
            for lnk in styles:
                self.set_quicklog("Fetching css %s" % lnk)
                style_url = str(lnk.get('href'))
                self._browse_styles(style_url, file_dir)

            scripts = soup.select('script')
            for lnk in scripts:
                self.set_quicklog("Fetching script %s" % lnk)
                style_url = str(lnk.get('src'))
                self._browse_styles(style_url, file_dir)

            images = soup.select('img')
            for lnk in images:
                style_url = str(lnk.get('src'))
                self.set_quicklog("Fetching images %s" % style_url)
                self._browse_styles(style_url, file_dir)

        except requests.ConnectionError as err1:
            self.set_errorlogs(err1)
        except Exception as err2:
            self.set_errorlogs(err2)

    def _grab_everything(self):
        stack_links = [self.link]
        page_threads = []
        for base_link in stack_links:

            try:
                result = requests.get(base_link)
                result.raise_for_status()
                if base_link.endswith(".zip") or base_link.endswith(".rar") or base_link.endswith(
                        ".mp3") or base_link.endswith(".exe"):
                    self.set_quicklog("Bounce back for %s" % base_link)
                    stack_links.remove(base_link)
                    continue
                elif stack_links.count(base_link) > 1:
                    self.set_quicklog("All ready in stack %s" % base_link)
                    continue

                self.link = base_link

                pg = threading.Thread(target=self._grab_single_page)
                page_threads.append(pg)
                pg.start()

                soup = bs4.BeautifulSoup(result.text, features='lxml')
                links = soup.select("a")

                file_dir = self._get_dirs(base_link)
                for link in links:
                    link = link.get('href')
                    if not link.startswith("#") and not link.startswith('javascript:') and bool(link.strip()):
                        pattern = re.compile('http(s)?://(\w*\S*)*')
                        search = pattern.search(link)
                        if search is None:
                            _cwd = self._pop_back(link, file_dir)
                            link = link.replace("../", "")
                            new_link = "http://" + _cwd + link
                            if stack_links.count(new_link) < 1:
                                self.set_quicklog("Link discovered %s" % new_link)
                                stack_links.append(new_link)

                        else:
                            if self.host == self.get_host(link):
                                self.set_quicklog("%s is outside the host!" % link)
                            else:
                                new_link = link
                                if stack_links.count(new_link) < 1:
                                    stack_links.append(new_link)
                                    self.set_quicklog("Link discovered %s" % new_link)

            except requests.ConnectionError as err1:
                self.set_errorlogs(err1)
            except Exception as err2:
                self.set_errorlogs(err2)

        for threads in page_threads:
            threads.join()

    def _grab_single_page(self):
        current_link = self.link

        self.set_quicklog("Fetching Page: %s" % current_link)
        file_dir = self._get_dirs(current_link)

        os.makedirs(file_dir, exist_ok=True)
        try:
            result = requests.get(current_link)
            result.raise_for_status()

            soup = bs4.BeautifulSoup(result.text, features='lxml')
            page = open(os.path.join(file_dir, os.path.basename(current_link)), 'wb')

            for chunk in result.iter_content(100000):
                page.write(chunk)
            page.close()
            self.set_quicklog("Page fetched successfully")

            styles = soup.select('link')
            for lnk in styles:
                style_url = str(lnk.get('href'))
                self.set_quicklog("Fetching css %s" % style_url)
                self._browse_styles(style_url, file_dir)

            scripts = soup.select('script')
            for lnk in scripts:
                style_url = str(lnk.get('src'))
                self.set_quicklog("Fetching script %s" % style_url)
                self._browse_styles(style_url, file_dir)

            images = soup.select('img')
            for lnk in images:
                style_url = str(lnk.get('src'))
                self.set_quicklog("Fetching images %s" % style_url)
                self._browse_styles(style_url, file_dir)

        except requests.ConnectionError as err1:
            self.set_errorlogs(err1)
        except Exception as err2:
            self.set_errorlogs(err2)

    def _grab_images(self):
        stack_links = [self.link]
        page_threads = []
        for base_link in stack_links:

            try:
                result = requests.get(base_link)
                result.raise_for_status()
                if base_link.endswith(".zip") or base_link.endswith(".rar") or base_link.endswith(
                        ".mp3") or base_link.endswith(".exe"):
                    self.set_quicklog("Bounce back for %s" % base_link)
                    stack_links.remove(base_link)
                    continue
                elif stack_links.count(base_link) > 1:
                    self.set_quicklog("All ready in stack %s" % base_link)
                    continue

                self.link = base_link

                pg = threading.Thread(target=self._image_fetch())
                page_threads.append(pg)
                pg.start()

                soup = bs4.BeautifulSoup(result.text, features='lxml')
                links = soup.select("a")

                file_dir = self._get_dirs(base_link)
                for link in links:
                    link = link.get('href')
                    if not link.startswith("#") and not link.startswith('javascript:') and bool(link.strip()):
                        pattern = re.compile('http(s)?://(\w*\S*)*')
                        search = pattern.search(link)
                        if search is None:
                            _cwd = self._pop_back(link, file_dir)
                            link = link.replace("../", "")
                            new_link = "http://" + _cwd + link
                            if stack_links.count(new_link) < 1:
                                self.set_quicklog("Link discovered %s" % new_link)
                                stack_links.append(new_link)

                        else:
                            if self.host == self.get_host(link):
                                self.set_quicklog("%s is outside the host!" % link)
                            else:
                                new_link = link
                                if stack_links.count(new_link) < 1:
                                    stack_links.append(new_link)
                                    self.set_quicklog("Link discovered %s" % new_link)

            except requests.ConnectionError as err1:
                self.set_errorlogs(err1)
            except Exception as err2:
                self.set_errorlogs(err2)

        for threads in page_threads:
            threads.join()


'''
listss = [
    "http://localhost/Scraper/index.html",
     "http://localhost/fsdev/index.html",
     "http://localhost/census/default.html",
     "http://localhost/Scraper/Pages/browse/page3.html",
     "http://localhost/Scraper/pages/page1.html",
     "https://www.google.com/"

]
for lks in listss:
    cmd_line = ScraperCMD(lks, 3)
    cmd_line._commence_scraping()

'''
