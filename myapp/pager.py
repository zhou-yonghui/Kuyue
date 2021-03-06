class Pagination(object):
    def __init__(self, totalCount, currentPage, perPageItemNum=15, maxPageNum=7):
        # 数据总个数
        self.total_count = totalCount
        # 当前页
        try:
            v = int(currentPage)
            if v <= 0:
                v = 1
            self.current_page = v
        except Exception as e:
            self.current_page = 1
        # 每页显示的行数
        self.per_page_item_num = perPageItemNum
        # 最多显示页面
        self.max_page_num = maxPageNum

    def start(self):
        return (self.current_page - 1) * self.per_page_item_num

    def end(self):
        return self.current_page * self.per_page_item_num

    @property
    def num_pages(self):
        """
        总页数
        :return:
        """
        # 666
        # 10
        a, b = divmod(self.total_count, self.per_page_item_num)
        if b == 0:
            return a
        return a + 1

    def pager_num_range(self):
        # self.num_pages()
        # self.num_pages
        # 当前页
        # self.current_page
        # 最多显示的页码数量 11
        # self.per_pager_num
        # 总页数
        # self.num_pages
        if self.num_pages < self.max_page_num:
            return range(1, self.num_pages + 1)
        # 总页数特别多 5
        part = int(self.max_page_num / 2)
        if self.current_page <= part:
            return range(1, self.max_page_num + 1)
        if (self.current_page + part) > self.num_pages:
            return range(self.num_pages - self.max_page_num + 1, self.num_pages + 1)
        return range(self.current_page - part, self.current_page + part + 1)

    def page_str_author(self):
        page_list = []

        first = "<li><a href='/author_list?p=1'>首页</a></li>"
        page_list.append(first)

        if self.current_page == 1:
            prev = "<li><a href='#'>上一页</a></li>"
        else:
            prev = "<li><a href='/author_list?p=%s'>上一页</a></li>" % (self.current_page - 1,)
        page_list.append(prev)
        for i in self.pager_num_range():
            if i == self.current_page:
                temp = "<li class='active'><a href='/author_list?p=%s'>%s</a></li>" % (i, i)
            else:
                temp = "<li><a href='/author_list?p=%s'>%s</a></li>" % (i, i)
            page_list.append(temp)

        if self.current_page == self.num_pages:
            nex = "<li><a href='#'>下一页</a></li>"
        else:
            nex = "<li><a href='/author_list?p=%s'>下一页</a></li>" % (self.current_page + 1,)
        page_list.append(nex)

        last = "<li><a href='/author_list?p=%s'>尾页</a></li>" % (self.num_pages,)
        page_list.append(last)

        return ''.join(page_list)

    def page_str_bookinfo(self):
        page_list = []

        first = "<li><a href='/bookinfo_list?p=1'>首页</a></li>"
        page_list.append(first)

        if self.current_page == 1:
            prev = "<li><a href='#'>上一页</a></li>"
        else:
            prev = "<li><a href='/bookinfo_list?p=%s'>上一页</a></li>" % (self.current_page - 1,)
        page_list.append(prev)
        for i in self.pager_num_range():
            if i == self.current_page:
                temp = "<li class='active'><a href='/bookinfo_list?p=%s'>%s</a></li>" % (i, i)
            else:
                temp = "<li><a href='/bookinfo_list?p=%s'>%s</a></li>" % (i, i)
            page_list.append(temp)

        if self.current_page == self.num_pages:
            nex = "<li><a href='#'>下一页</a></li>"
        else:
            nex = "<li><a href='/bookinfo_list?p=%s'>下一页</a></li>" % (self.current_page + 1,)
        page_list.append(nex)

        last = "<li><a href='/bookinfo_list?p=%s'>尾页</a></li>" % (self.num_pages,)
        page_list.append(last)

        return ''.join(page_list)

    def page_str_chapter(self):
        page_list = []

        first = "<li><a href='/chapter_list?p=1'>首页</a></li>"
        page_list.append(first)

        if self.current_page == 1:
            prev = "<li><a href='#'>上一页</a></li>"
        else:
            prev = "<li><a href='/chapter_list?p=%s'>上一页</a></li>" % (self.current_page - 1,)
        page_list.append(prev)
        for i in self.pager_num_range():
            if i == self.current_page:
                temp = "<li class='active'><a href='/chapter_list?p=%s'>%s</a></li>" % (i, i)
            else:
                temp = "<li><a href='/chapter_list?p=%s'>%s</a></li>" % (i, i)
            page_list.append(temp)

        if self.current_page == self.num_pages:
            nex = "<li><a href='#'>下一页</a></li>"
        else:
            nex = "<li><a href='/chapter_list?p=%s'>下一页</a></li>" % (self.current_page + 1,)
        page_list.append(nex)

        last = "<li><a href='/chapter_list?p=%s'>尾页</a></li>" % (self.num_pages,)
        page_list.append(last)

        return ''.join(page_list)

    def page_str_house(self):
        page_list = []

        first = "<li><a href='/house_list?p=1'>首页</a></li>"
        page_list.append(first)

        if self.current_page == 1:
            prev = "<li><a href='#'>上一页</a></li>"
        else:
            prev = "<li><a href='/house_list?p=%s'>上一页</a></li>" % (self.current_page - 1,)
        page_list.append(prev)
        for i in self.pager_num_range():
            if i == self.current_page:
                temp = "<li class='active'><a href='/house_list?p=%s'>%s</a></li>" % (i, i)
            else:
                temp = "<li><a href='/house_list?p=%s'>%s</a></li>" % (i, i)
            page_list.append(temp)

        if self.current_page == self.num_pages:
            nex = "<li><a href='#'>下一页</a></li>"
        else:
            nex = "<li><a href='/house_list?p=%s'>下一页</a></li>" % (self.current_page + 1,)
        page_list.append(nex)

        last = "<li><a href='/house_list?p=%s'>尾页</a></li>" % (self.num_pages,)
        page_list.append(last)

        return ''.join(page_list)

    def page_str_book(self):
        page_list = []

        first = "<li><a href='/book_list?p=1'>首页</a></li>"
        page_list.append(first)

        if self.current_page == 1:
            prev = "<li><a href='#'>上一页</a></li>"
        else:
            prev = "<li><a href='/book_list?p=%s'>上一页</a></li>" % (self.current_page - 1,)
        page_list.append(prev)
        for i in self.pager_num_range():
            if i == self.current_page:
                temp = "<li class='active'><a href='/book_list?p=%s'>%s</a></li>" % (i, i)
            else:
                temp = "<li><a href='/book_list?p=%s'>%s</a></li>" % (i, i)
            page_list.append(temp)

        if self.current_page == self.num_pages:
            nex = "<li><a href='#'>下一页</a></li>"
        else:
            nex = "<li><a href='/book_list?p=%s'>下一页</a></li>" % (self.current_page + 1,)
        page_list.append(nex)

        last = "<li><a href='/book_list?p=%s'>尾页</a></li>" % (self.num_pages,)
        page_list.append(last)

        return ''.join(page_list)

    def page_str_find(self):
        page_list = []

        first = "<li><a href='/find?p=1'>首页</a></li>"
        page_list.append(first)

        if self.current_page == 1:
            prev = "<li><a href='#'>上一页</a></li>"
        else:
            prev = "<li><a href='/find?p=%s'>上一页</a></li>" % (self.current_page - 1,)
        page_list.append(prev)
        for i in self.pager_num_range():
            if i == self.current_page:
                temp = "<li class='active'><a href='/find?p=%s'>%s</a></li>" % (i, i)
            else:
                temp = "<li><a href='/find?p=%s'>%s</a></li>" % (i, i)
            page_list.append(temp)

        if self.current_page == self.num_pages:
            nex = "<li><a href='#'>下一页</a></li>"
        else:
            nex = "<li><a href='/find?p=%s'>下一页</a></li>" % (self.current_page + 1,)
        page_list.append(nex)

        last = "<li><a href='/find?p=%s'>尾页</a></li>" % (self.num_pages,)
        page_list.append(last)

        return ''.join(page_list)

    def page_str_authormain(self):
        page_list = []

        first = "<li><a href='/author?p=1'>首页</a></li>"
        page_list.append(first)

        if self.current_page == 1:
            prev = "<li><a href='#'>上一页</a></li>"
        else:
            prev = "<li><a href='/author?p=%s'>上一页</a></li>" % (self.current_page - 1,)
        page_list.append(prev)
        for i in self.pager_num_range():
            if i == self.current_page:
                temp = "<li class='active'><a href='/author?p=%s'>%s</a></li>" % (i, i)
            else:
                temp = "<li><a href='/author?p=%s'>%s</a></li>" % (i, i)
            page_list.append(temp)

        if self.current_page == self.num_pages:
            nex = "<li><a href='#'>下一页</a></li>"
        else:
            nex = "<li><a href='/author?p=%s'>下一页</a></li>" % (self.current_page + 1,)
        page_list.append(nex)

        last = "<li><a href='/author?p=%s'>尾页</a></li>" % (self.num_pages,)
        page_list.append(last)

        return ''.join(page_list)