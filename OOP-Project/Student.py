from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql
from pymysql import cursors

class Student:
    # --------------- انشاء نافذه البرنامج -------------
    def __init__(self, root):
        self.root = root
        self.root.geometry('1350x690+80+70')
        self.root.title('برنامج إداره المدارس')
        self.root.configure(background="silver")
        self.root.resizable(False, False)
        title = Label(self.root,
                      text='[نظام تسجيل الطلاب]',
                      bg='#3498DB',
                      font=('monospace', 14,),
                      fg='white'
                      )
        title.pack(fill=X)
        # ----------------   variable   ----------------------------
        self.id_var = StringVar()
        self.name_var = StringVar()
        self.email_var = StringVar()
        self.phone_var = StringVar()
        self.moahel_var = StringVar()
        self.gender_var = StringVar()
        self.address_var = StringVar()
        self.dell_var = StringVar()
        self.se_by = StringVar()
        self.se_var = StringVar()
        # ------------- ادوات التحكم بالبرنامج -------------------
        Manage_Frame = Frame(self.root, bg='white')
        Manage_Frame.place(x=1137, y=30, width=210, height=400)

        lbl_ID = Label(Manage_Frame, text='الرقم التسلسلي ', bg='white')
        lbl_ID.pack()
        ID_Enrty = Entry(Manage_Frame, textvariable=self.id_var, bd='2', justify='center')
        ID_Enrty.pack()

        lbl_Name = Label(Manage_Frame, bg='white', text='اسم الطالب')
        lbl_Name.pack()
        Name_Entry = Entry(Manage_Frame, textvariable=self.name_var, bd='2', justify='center')
        Name_Entry.pack()

        lbl_email = Label(Manage_Frame, bg='white', text='إيميل الطالب')
        lbl_email.pack()
        email_Entry = Entry(Manage_Frame, textvariable=self.email_var, bd='2', justify='center')
        email_Entry.pack()

        lbl_phone = Label(Manage_Frame, bg='white', text='هاتف الطالب')
        lbl_phone.pack()
        phone_Entry = Entry(Manage_Frame, textvariable=self.phone_var, bd='2', justify='center')
        phone_Entry.pack()

        lbl_crti = Label(Manage_Frame, bg='white', text='مؤهلات الطالب')
        lbl_crti.pack()
        crti_Entry = Entry(Manage_Frame, textvariable=self.moahel_var, bd='2', justify='center')
        crti_Entry.pack()

        lbl_gender = Label(Manage_Frame, bg='white', text='اختر جنس الطالب')
        lbl_gender.pack()
        combo_gender = ttk.Combobox(Manage_Frame, textvariable=self.gender_var)
        combo_gender['value'] = ('ذكر', 'انثي')
        combo_gender.pack()

        lbl_address = Label(Manage_Frame, text='عنوان الطالب ', bg='white')
        lbl_address.pack()
        address_Entry = Entry(Manage_Frame, textvariable=self.address_var, bd='2', justify='center')
        address_Entry.pack()

        lbl_delete = Label(Manage_Frame, fg='red', bg='white', text='حذف الطالب بالاسم ')
        lbl_delete.pack()
        delete_Entry = Entry(Manage_Frame, textvariable=self.dell_var, bd=2, justify='center')
        delete_Entry.pack()
        # ------------------- الازرار buttons ---------------------
        btn_Frame = Frame(self.root, bg='white')
        btn_Frame.place(x=1137, y=435, width=210, height=253)
        title1 = Label(btn_Frame, text='لوحة التحكم', font=('Deco', 14), fg='white', bg='#3498DB')
        title1.pack(fill=X)

        add_btn = Button(btn_Frame, text='اضافه طالب', bg='#85929E', fg='white',command=self.add_student)
        add_btn.place(x=33, y=35, width=150, height=30)
        del_btn = Button(btn_Frame, text='حذف طالب', bg='#85929E', fg='white',command=self.delete)
        del_btn.place(x=33, y=70, width=150, height=30)
        update_btn = Button(btn_Frame, text='تعديل بينات طالب', bg='#85929E', fg='white',command=self.update)
        update_btn.place(x=33, y=105, width=150, height=30)
        clear_btn = Button(btn_Frame, text='افراغ الحقول', bg='#85929E', fg='white',command=self.clear)
        clear_btn.place(x=33, y=140, width=150, height=30)
        about_btn = Button(btn_Frame, text='من نحن', bg='#85929E', fg='white',command=self.about)
        about_btn.place(x=33, y=175, width=150, height=30)
        exit_btn = Button(btn_Frame, text='اغلاق البرنامج', bg='#85929E', fg='white',command=root.quit)
        exit_btn.place(x=33, y=210, width=150, height=30)
        # ------------------- search frame ---------------------
        search_Frame = Frame(self.root, bg='white')
        search_Frame.place(x=1, y=30, width=1134, height=50)

        lbl_search = Label(search_Frame, text='البحث عن طالب', bg='white')
        lbl_search.place(x=1034, y=12)

        combo_search = ttk.Combobox(search_Frame,textvariable=self.se_by , justify='right')
        combo_search['value'] = ('id', 'name', 'email', 'phone')
        combo_search.place(x=880, y=12)

        search_Entry = Entry(search_Frame, textvariable=self.se_var, justify='right', bd=2)
        search_Entry.place(x=740, y=12)

        se_btn = Button(search_Frame, text='يحث ', bg='#3498DB',command=self.search)
        se_btn.place(x=630, y=12, width=100, height=25)
        # -----------details عرض النتائج والبيانات ----------------------
        Dietals_Frame = Frame(self.root, bg='#F2F4F4')
        Dietals_Frame.place(x=1, y=82, width=1134, height=605)
        # ------scroll-----
        scroll_x = Scrollbar(Dietals_Frame, orient=HORIZONTAL)  # راسي
        scroll_y = Scrollbar(Dietals_Frame, orient=VERTICAL)  # افقي
        # -----tree view ----
        self.student_table = ttk.Treeview(Dietals_Frame,
                                          columns=('id', 'name', 'email', 'phone', 'gender', 'certi', 'address'),
                                          xscrollcommand=scroll_x.set,
                                          yscrollcommand=scroll_y.set)
        self.student_table.place(x=18, y=1, width=1130, height=587)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=LEFT, fill=X)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table['show'] = 'headings'
        self.student_table.heading('id', text='الرقم التسلسلي')
        self.student_table.heading('name', text='اسم الطالب')
        self.student_table.heading('email', text='البريد الالكتروني')
        self.student_table.heading('phone', text='رقم الهاتف')
        self.student_table.heading('gender', text='جنس الطالب')
        self.student_table.heading('certi', text='مؤهلات الطالب')
        self.student_table.heading('address', text='عنوان الطالب')

        
        
        self.student_table.column('id', width=17)
        self.student_table.column('name', width=100)
        self.student_table.column('email', width=70)
        self.student_table.column('phone', width=65)
        self.student_table.column('gender', width=30)
        self.student_table.column('certi', width=65)
        self.student_table.column('address', width=125)
        self.student_table.bind("<ButtonRelease-1>",self.get_cursor)

#============== con + add ===========================
        self.fetch_all() 
        
    def add_student(self):
        con = pymysql.connect(host = 'localhost',user='root',password='',database='scho')
        cur = con.cursor()
        cur.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s)",(                                                        
                                                       self.id_var.get(),
                                                       self.name_var.get(),
                                                       self.email_var.get(),
                                                       self.phone_var.get(),  
                                                       self.gender_var.get(),
                                                       self.moahel_var.get(),  
                                                       self.address_var.get()
                                                        ))
        con.commit()
        self.fetch_all()
        self.clear()
        con.close()   
        
    def fetch_all(self):
        con = pymysql.connect(host='localhost' , user='root',password='',database='scho')
        cur =con.cursor()
        cur.execute('select * from student ')
        rows = cur.fetchall()
        if len(rows) !=0:
                self.student_table.delete(*self.student_table.get_children())
                for row in rows:
                    self.student_table.insert("",END,value=row)
                con.commit()
        con.close()   

    def delete(self):
        con = pymysql.connect(host='localhost' , user='root',password='',database='scho')
        cur =con.cursor()
        cur.execute('delete from student where name=%s',self.dell_var.get())

        con.commit()
        self.fetch_all()
        con.close()
#-----------------------------------------clear function -----
    def clear (self) :
        self.id_var.set('')
        self.name_var.set('')
        self.email_var.set('')
        self.phone_var.set('')
        self.moahel_var.set('')
        self.gender_var.set('')
        self.address_var.set('')

    def get_cursor(self,ev):
        cursor_row= self.student_table.focus()
        contents   = self.student_table.item(cursor_row)
        row = contents['values']
        self.id_var.set(row[0])
        self.name_var.set(row[1])
        self.email_var.set(row[2])
        self.phone_var.set(row[3])
        self.gender_var.set(row[4])
        self.moahel_var.set(row[5])
        self.address_var.set(row[6])

    def update(self):
        con = pymysql.connect(host = 'localhost',user='root',password='',database='scho')
        cur = con.cursor()
        cur.execute("update student set address=%s, gender=%s , moahel=%s ,email=%s , phone=%s , name=%s where id=%s",(                                                        
                                                       self.address_var.get(),
                                                       self.gender_var.get(),
                                                       self.moahel_var.get(),
                                                       self.email_var.get(),
                                                       self.phone_var.get(),
                                                       self.name_var.get(),                                                        
                                                       self.id_var.get()
                                                        ))
        con.commit()
        self.fetch_all()
        self.clear()
        con.close()

    def search(self):
        con = pymysql.connect(host='localhost' , user='root',password='',database='scho')
        cur =con.cursor()
        cur.execute("select * from student where " +
        str(self.se_by.get() )+" LIKE '%"+str(self.se_var.get())+"%'")

        rows = cur.fetchall()
        if len(rows) !=0:
                self.student_table.delete(*self.student_table.get_children())
                for row in rows:
                    self.student_table.insert("",END,value=row)
                con.commit()
        con.close()

    def about(self):
        messagebox.showinfo("Devloper Youssef Shahien","welcome to our first project")



        
root = Tk()
ob = Student(root)
root.mainloop()
