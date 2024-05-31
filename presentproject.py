import sqlite3
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
import random
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from datetime import datetime
from tkinter import messagebox
import tkinter as toplevel
import hashlib
conn = sqlite3.connect(r"E:\project\databeta.db")
cursor = conn.cursor()
now = datetime.today()
    
def checkint(P):
    if P.isdigit() or P == "":
        return True
    else:
        return False  
def shop(): 
    def display_show_product():       
        cursor.execute("SELECT * FROM mystore")
        pictures = cursor.fetchall() 
        def addtocart(item):
            def add():
                c = conn.cursor()
                c.execute("INSERT INTO myorder (name, price, quantity, picture) VALUES (?, ?, ?, ?)", (item[1], item[2], 1, item[4]))
                conn.commit()
            return add
        for i, x in enumerate(pictures):
            image = Image.open(BytesIO(x[4]))
            target_width, target_height = 197, 197
            image = image.resize((target_width, target_height))
            image = ImageTk.PhotoImage(image)

            label1 = Button(product, font=("Times", 14), image=image, text=" {}  ฿ {} ".format(x[1], x[2]), compound="top", command=addtocart(x), bg= "#cecece", fg="#000000")
            label1.image = image
            label1.grid(row=i // 4, column=i % 4, padx=15, pady=10)
    def backstore():
        bgorder.destroy()  
        cart.destroy() 
        end_order.destroy() 
        gg.destroy()  
        product.destroy() 
        productdisplay.destroy() 
    def on_mousewheel(event):
        productdisplay.yview_scroll(int(-1*(event.delta/120)), "units")
    #-----------------------------------------------------------------------------------------------------
    def opencart(): 

        tempidproduct=[]   
        def edit():
            selected_product = products_listbox.curselection()
            if selected_product:
                a = selected_product[0]
                idedit = tempidproduct[a]
                orderquantity = int(quantity.get())
                c = conn.cursor()
                c.execute('''SELECT * FROM myorder''')
                result = c.fetchall()
                stoploop = False
                for x in result:
                    c = conn.cursor()
                    c.execute("SELECT id,name,quantity  FROM mystore  WHERE name=?",(x[1],))
                    resultstock = c.fetchall()
                    for y in resultstock:
                        if stoploop==False:
                            if orderquantity>y[2] :
                                messagebox.showinfo(title="Not enough product", message="Enter the quantity of new products.") 
                                quantity.delete(0, tk.END)   
                                stoploop=True                    
                                break     
                            else:
                                cursor.execute('''UPDATE myorder SET quantity=? WHERE id =? ''',(orderquantity,idedit))
                                quantity.delete(0, tk.END)
                                conn.commit()
                                show()
                        elif stoploop==True:
                            break
        def delete():
            selected_product = products_listbox.curselection()
            if selected_product:
                a = selected_product[0]
                product_id = tempidproduct[a]
                cursor.execute("DELETE FROM myorder WHERE id=?", (product_id,))
                conn.commit()
                show()       
        def show():
            totalprice=0  
            tempidproduct.clear()
            products_listbox.delete(0, tk.END)
            price_listbox.delete(0, tk.END)
            q_listbox.delete(0, tk.END)
            c = conn.cursor()
            c.execute('''SELECT * FROM myorder''')
            result = c.fetchall()
            for x in result:
                c = conn.cursor()
                c.execute("SELECT id,name,quantity  FROM mystore  WHERE name=?",(x[1],))
                resultstock = c.fetchall()
                for y in resultstock:
                    products_listbox.insert(x[0]," ▶    {}   ".format(x[1]))
                    tempidproduct.append(x[0])
                    totalprice+= x[2]*x[3]
                    totalpricelabel.config(text=f"Total Price: ฿{totalprice:.2f}")
                    q_listbox.insert(x[0]," {} * {} = {}  THB".format(x[2],x[3],x[2]*x[3]))   
                    price_listbox.insert(x[0]," ▶In Stock  {}  ▶In Cart  {} ".format(y[2]-x[3],x[3]))
        def backcart():      
            quantity.destroy()
            delete_button.destroy()
            edit_button.destroy()
            products_listbox.destroy()
            price_listbox.destroy()
            q_listbox.destroy()
            pay.destroy()
            end.destroy()
            bgcart.destroy()
            totalpricelabel.destroy()
#----------------------------------------bill--------------------------------------------------------------
        def membercheck():
            choice = messagebox.askquestion("Member", "คุณเป็นสมาชิกมั้ย?")   
            print(choice) 
            if choice == 'yes':
                loginmember()
            if choice== 'no':
                bill() 
        def loginmember():
            def hash_password(passwordmem):
                return hashlib.sha256(passwordmem.encode()).hexdigest()

            def add_user(usernamemem, passwordmem):
                hashed_password = hash_password(passwordmem)
                cursor.execute('INSERT INTO member (username, password, level, passwordnothast) VALUES (?,?,?,?)', (usernamemem, hashed_password,0, passwordmem))
                conn.commit()

            def add_user1():
                usernamemem = username_entrymember.get()
                passwordmem = password_entrymember.get()

                if usernamemem and passwordmem:
                    add_user(usernamemem, passwordmem)
                    messagebox.showinfo('เพิ่มผู้ใช้', 'เพิ่มผู้ใช้เรียบร้อยแล้ว!')
                else:
                    messagebox.showerror('ข้อผิดพลาด', 'โปรดป้อนชื่อผู้ใช้และรหัสผ่านทั้งคู่.')
                username_entrymember.delete(0, tk.END)
                password_entrymember.delete(0, tk.END)

            def login():
                usernamemem = username_entrymember.get()
                passwordmem = password_entrymember.get()
                hashed_password = hash_password(passwordmem)
                cursor.execute('SELECT password FROM member WHERE username = ?', (usernamemem,))
                result = cursor.fetchone()
                if result and result[0] == hashed_password:
                    messagebox.showinfo('Login', '🔓Login successful!🔓')
                    billmem()
                    closing()
                else:
                    messagebox.showerror('Login', '🔒nvalid credentials.🔒')
                    username_entrymember.delete(0,tk.END)
                    password_entrymember.delete(0,tk.END)

            def closing():
                bgloginmember.destroy()
                username_entrymember.destroy()
                password_entrymember.destroy()
                add_user_buttonmember.destroy()
                login_buttonmember.destroy()
                exit_buttonmember.destroy()
            bgloginmember = Label(guimain, bg="#ff99cc",image=loginadminpic)
            bgloginmember.place(x=0, y=0, width=1017, height=730)

            username_entrymember = Entry(guimain, bg="#ffffff", borderwidth="1px", cursor="heart", font=("Times", 22), fg="#000000", justify="center", relief="sunken")
            username_entrymember.place(x=355,y=150,width=400,height=55)

            password_entrymember = Entry(guimain, bg="#ffffff", borderwidth="1px", cursor="heart", font=("Times", 22),show='🔒', fg="#000000", justify="center", relief="sunken")
            password_entrymember.place(x=355,y=268,width=400,height=55)

            add_user_buttonmember = Button(guimain, bg="#d8d8d8",image=buttonlogin ,cursor="heart",command=login)
            add_user_buttonmember.place(x=400, y=400, width=256, height=67)

            login_buttonmember = Button(guimain, bg="#d8d8d8",image=buttonsignin,cursor="heart",command=add_user1)
            login_buttonmember.place(x=400, y=500, width=256, height=67)

            exit_buttonmember = tk.Button(guimain, bg="#d8d8d8",image=bgclose,cursor="heart",command=closing)
            exit_buttonmember.place(x=400, y=600, width=256, height=67)

        def billmem():    
            def payment():
                c = conn.cursor()
                c.execute('''SELECT * FROM myorder''')
                result = c.fetchall()
                date=now
                category="sales,transfer payment"
                for x in result:
                    c.execute("SELECT id,name,quantity  FROM mystore  WHERE name=?",(x[1],))
                    resultstock = c.fetchall()
                    for   x in result:
                        for y in resultstock:
                            cursor.execute('''UPDATE mystore SET quantity=? WHERE id =? ''',(y[2]-x[3],y[0]))
                            conn.commit() 
                    namehistory,pricehistory,quantity=x[1],x[2],x[3]
                    print(category,"  /  ",namehistory,"  /  ",pricehistory,"  /  ",quantity,"  /  ",date)
                    if category and namehistory and pricehistory and quantity and date :
                        cursor.execute("INSERT INTO history (category,name,price,quantity,date) VALUES (?, ?, ?, ?, ?)", (category,namehistory,pricehistory,quantity,date))
                        conn.commit()
                    cursor.execute("DELETE FROM myorder")
                    conn.commit()
                    backbill()
                    backcart()
                    backstore()
            def cash():
                c = conn.cursor()
                c.execute('''SELECT * FROM myorder''')
                result = c.fetchall()
                date=now
                category="sales,cash"
                for x in result:
                    c.execute("SELECT id,name,quantity  FROM mystore  WHERE name=?",(x[1],))
                    resultstock = c.fetchall()
                    for   x in result:
                        for y in resultstock:
                            cursor.execute('''UPDATE mystore SET quantity=? WHERE id =? ''',(y[2]-x[3],y[0]))
                            conn.commit()
                    namehistory,pricehistory,quantity=x[1],x[2],x[3]
                    if category and namehistory and pricehistory and quantity and date :
                        cursor.execute("INSERT INTO history (category,name,price,quantity,date) VALUES (?, ?, ?, ?, ?)", (category,namehistory,pricehistory,quantity,date))
                        conn.commit()
                    cursor.execute("DELETE FROM myorder")
                    conn.commit()
                    backbill()
                    backcart()
                    backstore()
            def transferpayment():
                    payment()
            def show():
                        totalprice=0  
                        products_listbox5.delete(0, tk.END)
                        products_listbox5.insert(0,(now))
                        c = conn.cursor()
                        c.execute('''SELECT * FROM myorder''')
                        result = c.fetchall()
                        for x in result:
                            products_listbox5.insert(x[0]," ▶   {}    {} * {} = {}  THB  ".format(x[1],x[2],x[3],x[2]*x[3]))
                            totalprice+= x[2]*x[3]
                        products_listbox5.insert(tk.END,"     ")
                        products_listbox5.insert(tk.END,"       Voucher  Voucher  Voucher  Voucher    ")
                        products_listbox5.insert(tk.END," ▶ Voucher for member 5%   {}  -5 % = {}  THB  ".format(totalprice,totalprice/100*95))
                        totalprice-=totalprice/100*5
                        totalbill.config(text=f"Total Price: ฿{totalprice:.2f}")   
            def backbill():
                bg_bill.destroy()
                delete_button.destroy()
                edit_button.destroy()
                totalbill.destroy()
                products_listbox5.destroy()
                nn.destroy()
                end.destroy()    
            bg_bill=tk.Label(guimain,image=bghomepage)
            bg_bill.place(x=0,y=0,width=1019,height=725)
            delete_button = tk.Button(guimain, bg="#F9DEC9", cursor="heart", font=("Times", 17), fg="#000000", justify="center", text="cash", borderwidth="3px",command=cash)
            delete_button.place(x=620, y=670, width=80, height=40)

            edit_button = tk.Button(guimain, bg="#F9DEC9", cursor="heart",font=("Times", 17), fg="#000000", justify="center", text="Transfer payment", borderwidth="3px",command=transferpayment)
            edit_button.place(x=720, y=670, width=200, height=40)

            totalbill = Label(guimain, text="Total Price: $0.00", bg="#ffffff",cursor="heart", font=("Times", 12), fg="#000000", justify="center",borderwidth="3px")
            totalbill.place(x=717, y=610, width=200, height=40)

            products_listbox5 = tk.Listbox(guimain, bg="#ffffff", borderwidth="4px", cursor="heart", font=("Times", 14), fg="#333333", relief="sunken")
            products_listbox5.place(x=570, y=80, width=400, height=530)

            nn=tk.Label(guimain,bg="#DCDCDC", cursor="heart", font=("Times", 17), fg="#000000", justify="center", text="BILL", borderwidth="3px", relief="groove")
            nn.place(x=667, y=20, width=200, height=40)

            end = tk.Button(guimain,borderwidth="1px",image=iconbackadmin, command=backbill)
            end.place(x=940, y=17, width=49, height=43)
            show()

        def bill():    
            def payment():
                c = conn.cursor()
                c.execute('''SELECT * FROM myorder''')
                result = c.fetchall()
                date=now
                category="sales,transfer payment"
                for x in result:
                    c.execute("SELECT id,name,quantity  FROM mystore  WHERE name=?",(x[1],))
                    resultstock = c.fetchall()
                    for   x in result:
                        for y in resultstock:
                            cursor.execute('''UPDATE mystore SET quantity=? WHERE id =? ''',(y[2]-x[3],y[0]))
                            conn.commit()
                    namehistory,pricehistory,quantity=x[1],x[2],x[3]
                    print(category,"  /  ",namehistory,"  /  ",pricehistory,"  /  ",quantity,"  /  ",date)
                    if category and namehistory and pricehistory and quantity and date :
                        cursor.execute("INSERT INTO history (category,name,price,quantity,date) VALUES (?, ?, ?, ?, ?)", (category,namehistory,pricehistory,quantity,date))
                        conn.commit()
                    cursor.execute("DELETE FROM myorder")
                    conn.commit()
                    backbill()
                    backcart()
                    backstore()
            def cash():
                c = conn.cursor()
                c.execute('''SELECT * FROM myorder''')
                result = c.fetchall()
                date=now
                category="sales,cash"
                for x in result:
                    c.execute("SELECT id,name,quantity  FROM mystore  WHERE name=?",(x[1],))
                    resultstock = c.fetchall()
                    for   x in result:
                        for y in resultstock:
                            cursor.execute('''UPDATE mystore SET quantity=? WHERE id =? ''',(y[2]-x[3],y[0]))
                            conn.commit()
                    namehistory,pricehistory,quantity=x[1],x[2],x[3]
                    if category and namehistory and pricehistory and quantity and date :
                        cursor.execute("INSERT INTO history (category,name,price,quantity,date) VALUES (?, ?, ?, ?, ?)", (category,namehistory,pricehistory,quantity,date))
                        conn.commit()
                    cursor.execute("DELETE FROM myorder")
                    conn.commit()
                    backbill()
                    backcart()
                    backstore()
            def transferpayment():
                    payment()
            def show():
                        totalprice=0  
                        products_listbox5.delete(0, tk.END)
                        products_listbox5.insert(0,(now))
                        c = conn.cursor()
                        c.execute('''SELECT * FROM myorder''')
                        result = c.fetchall()
                        for x in result:
                            products_listbox5.insert(x[0]," ▶   {}    {} * {} = {}  THB  ".format(x[1],x[2],x[3],x[2]*x[3]))
                            totalprice+= x[2]*x[3]
                        totalbill.config(text=f"Total Price: ฿{totalprice:.2f}")   
            def backbill():
                bg_bill.destroy()
                delete_button.destroy()
                edit_button.destroy()
                totalbill.destroy()
                products_listbox5.destroy()
                nn.destroy()
                end.destroy()    
            bg_bill=tk.Label(guimain,image=bghomepage)
            bg_bill.place(x=0,y=0,width=1019,height=725)
            delete_button = tk.Button(guimain, bg="#F9DEC9", cursor="heart", font=("Times", 17), fg="#000000", justify="center", text="cash", borderwidth="3px",command=cash)
            delete_button.place(x=620, y=670, width=80, height=40)

            edit_button = tk.Button(guimain, bg="#F9DEC9", cursor="heart",font=("Times", 17), fg="#000000", justify="center", text="Transfer payment", borderwidth="3px",command=transferpayment)
            edit_button.place(x=720, y=670, width=200, height=40)

            totalbill = Label(guimain, text="Total Price: $0.00", bg="#ffffff",cursor="heart", font=("Times", 12), fg="#000000", justify="center",borderwidth="3px")
            totalbill.place(x=717, y=610, width=200, height=40)

            products_listbox5 = tk.Listbox(guimain, bg="#ffffff", borderwidth="4px", cursor="heart", font=("Times", 14), fg="#333333", relief="sunken")
            products_listbox5.place(x=620, y=80, width=300, height=530)

            nn=tk.Label(guimain,bg="#DCDCDC", cursor="heart", font=("Times", 17), fg="#000000", justify="center", text="BILL", borderwidth="3px", relief="groove")
            nn.place(x=667, y=20, width=200, height=40)

            end = tk.Button(guimain,borderwidth="1px",image=iconbackadmin, command=backbill)
            end.place(x=940, y=17, width=49, height=43)
            show()

#----------------------------------------billmem--------------------------------------------------------------

        bgcart = Label(guimain, bg="#c71585",image=blackgcart,cursor="heart")
        bgcart.place(x=0, y=0, width=1019, height=730)

        validate_func = guimain.register(checkint)
        quantity=tk.Entry(guimain,validate='key',validatecommand=(validate_func, "%P"), bg="#ffffff", borderwidth="3px", cursor="heart", font=("Times", 10), fg="#000000", justify="center", relief="sunken")
        quantity.place(x=720, y=100, width=201, height=40)

        delete_button = tk.Button(guimain, cursor="heart", image=bgicondelete, command=delete)
        delete_button.place(x=870, y=20, width=49, height=43)

        edit_button = tk.Button(guimain,bg="#ffffff", cursor="heart", image=bgiconedit, font=("Times", 14), fg="#000000", command=edit)
        edit_button.place(x=940, y=100, width=49, height=43)

        products_listbox = tk.Listbox(guimain, bg="#7a7a7a", borderwidth="1px", cursor="heart", font=("Times", 20), fg="#333333", relief="sunken")
        products_listbox.place(x=30, y=200, width=350, height=420)
        
        price_listbox= tk.Listbox(guimain, bg="#7a7a7a", borderwidth="1px", cursor="heart", font=("Times", 20), fg="#333333", relief="sunken")
        price_listbox.place(x=380, y=200, width=340, height=420)
        
        q_listbox = tk.Listbox(guimain, bg="#7a7a7a", borderwidth="1px", cursor="heart", font=("Times", 20), fg="#333333", relief="sunken")
        q_listbox.place(x=720, y=200, width=270, height=420)

        pay = tk.Button(guimain, fg="#000000", justify="center",image=bgiconpay,command=membercheck)
        pay.place(x=940, y=680, width=49, height=43)

        totalpricelabel = Label(guimain, text="Total Price: $0.00", bg="#ffffff",cursor="heart", font=("Times", 15), fg="#000000", justify="center",borderwidth="3px")
        totalpricelabel.place(x=800, y=630, width=191, height=43)

        end = tk.Button(guimain,image=bgiconcartback, command=backcart)
        end.place(x=937, y=20, width=49, height=43)
        show()
    #-----------------------------------------------------------------------------------------------------
    bgorder = Label(guimain,image=bgbuynow,cursor="heart")
    bgorder.place(x=0, y=0, width=1019, height=730)
    cart = Button(guimain, cursor="heart",image=bgiconcart,command=opencart)
    cart.place(x=350,y=55, width=49, height=43)
    end_order = Button(guimain,  cursor="heart",image=bgiconback,command=backstore)
    end_order.place(x=930, y=55, width=49, height=43)
    gg = Label(guimain)
    gg.place(x=40, y=155, width=938, height=530)
    productdisplay = Canvas(guimain, bg="#7a7a7a")
    productdisplay.place(x=40, y=155, width=938, height=530)
    product = Frame(productdisplay, bg="#7a7a7a")
    productdisplay.create_window((0, 0), window=product, anchor='nw')
    bgorder.bind("<MouseWheel>", on_mousewheel)
    display_show_product()
def admin():
    tempidproduct=[]       
    def edit():
        selected_product = products_listbox.curselection()
        if selected_product:
            a = selected_product[0]
            idedit = tempidproduct[a]
            name = name_entry.get()
            price = price_entry.get()
            quantity= quantity_entry.get()
            file_pic = filedialog.askopenfilename()
            if file_pic:
                with open(file_pic, 'rb') as file:
                    picture = file.read()
            cursor.execute('''UPDATE mystore SET name =?,price =?,quantity=?,picture=? WHERE id =? ''',(name, price, quantity, picture,idedit))
            category="admin,editproduct"
            namehistory=name
            pricehistory=price
            quantityhistory=quantity
            date=now
            cursor.execute("INSERT INTO history (category,name,price,quantity,date) VALUES (?, ?, ?, ?, ?)", (category,namehistory,pricehistory,quantityhistory,date))
            conn.commit()
            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            conn.commit()
            show()
    def add():
        name = name_entry.get()
        price =price_entry.get()
        quantity= quantity_entry.get()
        file_pic = filedialog.askopenfilename()
        if file_pic:
            with open(file_pic, 'rb') as file:
                picture = file.read()
        if name and price and quantity and picture:
            cursor.execute("INSERT INTO mystore (name, price,quantity,picture) VALUES (?, ?, ?, ?)", (name, price, quantity, picture))
            category="admin,addproduct"
            namehistory=name
            pricehistory=price
            quantityhistory=quantity
            date=now
            cursor.execute("INSERT INTO history (category,name,price,quantity,date) VALUES (?, ?, ?, ?, ?)", (category,namehistory,pricehistory,quantityhistory,date))
            conn.commit()
            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            show()
    def delete():
        selected_product = products_listbox.curselection()
        if selected_product:
            a = selected_product[0]
            c = conn.cursor()
            c.execute("SELECT name,price,quantity FROM mystore WHERE id=?", (tempidproduct[a],))
            result=c.fetchall()
            for x in result:
                namehistory=x[0]
                pricehistory=x[1]
                quantityhistory=x[2]
            date=now
            category="admin,deleteproduct"
            cursor.execute("INSERT INTO history (category,name,price,quantity,date) VALUES (?, ?, ?, ?, ?)", (category,namehistory,pricehistory,quantityhistory,date))
            conn.commit()                
        if selected_product:
            a = selected_product[0]
            product_id = tempidproduct[a]
            cursor.execute("DELETE FROM mystore WHERE id=?", (product_id,))
            conn.commit()  
            show()       
    def show():
        products_listbox.delete(0, tk.END)
        c = conn.cursor()
        c.execute('''SELECT * FROM mystore''')
        result = c.fetchall()
        i = 1
        tempidproduct.clear()
        for x in result:
            products_listbox.delete(0, tk.END)
            adminprice_listbox.delete(0, tk.END)
            adminquantity_listbox.delete(0, tk.END)
            picture_listbox.delete(0, tk.END)
            c=conn.cursor()   
            c.execute('''SELECT * FROM mystore''')
            result=c.fetchall()
            tempidproduct.clear()
            for x in result:
                products_listbox.insert(x[0],"  {}    ".format(x[1]))
                adminprice_listbox.insert(x[0],"  {}  THB   ".format(x[2])) 
                adminquantity_listbox.insert(x[0],"  {}    ".format(x[3]))  
                picture_listbox.insert(x[0]," {}    ".format(x[4]))   
                tempidproduct.append(x[0])         
    def back():
        bg_color.destroy() 
        name_entry.destroy() 
        price_entry.destroy() 
        quantity_entry.destroy() 
        add_button.destroy() 
        delete_button.destroy() 
        edit_button.destroy() 
        products_listbox.destroy()
        adminprice_listbox.destroy()
        adminquantity_listbox.destroy()
        picture_listbox.destroy()
        endadmin.destroy() 
    bg_color=tk.Label(guimain,image=bgadmin)
    bg_color.place(x=0,y=0,width=1017,height=725)
    name_entry = tk.Entry(guimain, bg="#ffffff", borderwidth="1px", cursor="heart", font=("Times", 10), fg="#000000", justify="center", relief="sunken")
    name_entry.place(x=527,y=63,width=303,height=31)
    validate_func = guimain.register(checkint)
    price_entry=tk.Entry(guimain,validate='key',validatecommand=(validate_func, "%P"),bg="#ffffff", borderwidth="1px", cursor="heart", font=("Times", 10), fg="#000000", justify="center", relief="sunken")
    price_entry.place(x=527,y=125,width=303,height=31)
    quantity_entry=tk.Entry(guimain,validate='key',validatecommand=(validate_func, "%P"),bg="#ffffff", borderwidth="1px", cursor="heart", font=("Times", 10), fg="#000000", justify="center", relief="sunken")
    quantity_entry.place(x=527,y=190,width=303,height=31)

    add_button = tk.Button(guimain, cursor="heart", image=iconaddadmin, font=("Times", 17), fg="#000000", justify="center", text="ADD",  borderwidth="3px", command=add)
    add_button.place(x=840, y=56, width=49, height=43)

    delete_button = tk.Button(guimain, cursor="heart", image=icondeleteadmin, font=("Times", 17), fg="#000000", justify="center", text="DELETE", borderwidth="3px", command=delete)
    delete_button.place(x=840, y=120, width=49, height=43)

    edit_button = tk.Button(guimain, cursor="heart", image=iconeditadmin,font=("Times", 17), fg="#000000", justify="center", text="EDIT", borderwidth="3px", command=edit)
    edit_button.place(x=840, y=185, width=49, height=43)

    products_listbox = tk.Listbox(guimain, bg="#ffffff", borderwidth="1px", cursor="heart", font=("Times", 20), fg="#333333", relief="sunken")
    products_listbox.place(x=43, y=325, width=350, height=360)

    adminprice_listbox = tk.Listbox(guimain, bg="#ffffff", borderwidth="1px", cursor="heart", font=("Times", 20), fg="#333333", relief="sunken")
    adminprice_listbox.place(x=393, y=325, width=185, height=360)

    adminquantity_listbox = tk.Listbox(guimain, bg="#ffffff", borderwidth="1px", cursor="heart", font=("Times", 20), fg="#333333", relief="sunken")
    adminquantity_listbox.place(x=578, y=325, width=350, height=360)

    picture_listbox = tk.Listbox(guimain, bg="#ffffff", borderwidth="1px", cursor="heart", font=("Times", 20), fg="#333333", relief="sunken")
    picture_listbox.place(x=763, y=325, width=210, height=360)

    endadmin = tk.Button(guimain,image=iconbackadmin, bg="#ff0000", font=("Times", 20), justify="center", borderwidth="0px", command=back)
    endadmin.place(x=940, y=17, width=49, height=43)
    show()
    
def pujudtum():
    def back():
        bg_pujudtum.destroy()
        endpujudtum.destroy()
    bg_pujudtum=tk.Label(guimain,image=pjt)
    bg_pujudtum.place(x=0,y=0,width=1017,height=725)
    endpujudtum = tk.Button(guimain,image=iconbackadmin, bg="#ff0000", font=("Times", 20), justify="center", borderwidth="0px", command=back)
    endpujudtum.place(x=940, y=17, width=49, height=43)

def loginadmin():
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(username, password):
        hashed_password = hash_password(password)
        cursor.execute('INSERT INTO admin (username, password, level, passwordnothast) VALUES (?,?,?,?)', (username, hashed_password,0, password))
        conn.commit()

    def add_user1():
        username = username_entry.get()
        password = password_entry.get()

        if username and password:
            add_user(username, password)
            messagebox.showinfo('เพิ่มผู้ใช้', 'เพิ่มผู้ใช้เรียบร้อยแล้ว!')

        else:
            messagebox.showerror('ข้อผิดพลาด', 'โปรดป้อนชื่อผู้ใช้และรหัสผ่านทั้งคู่.')
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

    def login():
        username = username_entry.get()
        password = password_entry.get()

        hashed_password = hash_password(password)
        cursor.execute('SELECT password FROM admin WHERE username = ?', (username,))
        result = cursor.fetchone()
        if result and result[0] == hashed_password:
            messagebox.showinfo('Login', '🔓Login successful!🔓')
            admin()
            closing()
        else:
            messagebox.showerror('Login', '🔒nvalid credentials.🔒')
            username_entry.delete(0,tk.END)
            password_entry.delete(0,tk.END)


    def closing():
        bglogin.destroy()
        username_entry.destroy()
        password_entry.destroy()
        add_user_button.destroy()
        login_button.destroy()
        exit_button.destroy()
    bglogin = Label(guimain, bg="#ff99cc",image=loginadminpic)
    bglogin.place(x=0, y=0, width=1017, height=730)

    username_entry = Entry(guimain, bg="#ffffff", borderwidth="1px", cursor="heart", font=("Times", 22), fg="#000000", justify="center", relief="sunken")
    username_entry.place(x=355,y=150,width=400,height=55)

    password_entry = Entry(guimain, bg="#ffffff", borderwidth="1px", cursor="heart", font=("Times", 22),show='🔒', fg="#000000", justify="center", relief="sunken")
    password_entry.place(x=355,y=268,width=400,height=55)

    add_user_button = Button(guimain, bg="#d8d8d8",image=buttonlogin ,cursor="heart",command=login)
    add_user_button.place(x=400, y=400,width=256, height=67)

    login_button = Button(guimain, bg="#d8d8d8",image=buttonsignin,cursor="heart",command=add_user1)
    login_button.place(x=400, y=500, width=256, height=67)

    exit_button = tk.Button(guimain, bg="#d8d8d8",image=bgclose,cursor="heart",command=closing)
    exit_button.place(x=400, y=600, width=256, height=67)

def closeprogram():
    guimain.withdraw()

guimain = tk.Tk()
guimain.title("CLASSY STORE")
width=1019
height=730
screenwidth = guimain.winfo_screenwidth()
screenheight = guimain.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
guimain.geometry(alignstr)
guimain.resizable(width=False, height=False)

bghomepage = PhotoImage(file="E:\project\GFGUI\homepage\homepage.png")
bgshop = PhotoImage(file="E:/project/GFGUI/homepage/buynow01.png")
bgbuttonadmin = PhotoImage(file="E:/project/GFGUI/homepage/admin01.png")
bgclose = PhotoImage(file="E:\project\GFGUI\homepage\close01.png")
bgiconcredit = PhotoImage(file="E:\project\GFGUI\homepage\Cr.png")

bgbuynow = PhotoImage(file="E:/project/GFGUI/buynow/buynowbg.png")
bgiconback = PhotoImage(file="E:/project/GFGUI/buynow/back.png")
bgiconcart = PhotoImage(file="E:/project/GFGUI/buynow/cart.png")

blackgcart = PhotoImage(file="E:\project\GFGUI\Cart\BG.png")
bgiconcartback = PhotoImage(file="E:/project/GFGUI/Cart/back.png")
bgicondelete = PhotoImage(file="E:\project\GFGUI\Cart\delete.png")
bgiconedit = PhotoImage(file="E:\project\GFGUI\Cart\edit.png")
bgiconpay = PhotoImage(file="E:\project\GFGUI\Cart\pay.png")
bgicontotalprice = PhotoImage(file="E:\project\GFGUI\Cart\price1.png")
bgiconeditnumber = PhotoImage(file="E:\project\GFGUI\Cart\editNumber.png")

bgadmin = PhotoImage(file="E:\project\GFGUI\Admin\BG.png")
iconaddadmin = PhotoImage(file="E:\\project\\GFGUI\\Admin\\add.png")
icondeleteadmin = PhotoImage(file="E:\project\GFGUI\Admin\delete.png")
iconeditadmin = PhotoImage(file="E:\project\GFGUI\Admin\edit.png")
iconbackadmin = PhotoImage(file="E:\\project\\GFGUI\\Admin\\back.png")

pjt = PhotoImage(file="E:\project\GFGUI\pjt.png")
loginadminpic = PhotoImage(file="E:\project\GFGUI\\n.png")
buttonlogin = PhotoImage(file="E:\project\GFGUI\login.png")
buttonsignin = PhotoImage(file="E:\project\GFGUI\singin.png")

bgmain = tk.Label(guimain, bg="#ff99cc",image=bghomepage).place(x=0, y=0, width=1017, height=730)
buttonshop = tk.Button(guimain, bg="#d8d8d8",image=bgshop,cursor="heart", command=shop).place(x=620, y=170, width=256, height=67)
buttonadmin = tk.Button(guimain, bg="#d8d8d8",image=bgbuttonadmin,cursor="heart",command=loginadmin).place(x=620, y=310, width=256, height=67)
buttonclose = tk.Button(guimain, bg="#d8d8d8",image=bgclose,cursor="heart",command=closeprogram).place(x=620, y=450, width=256, height=67)
buttoncredit = tk.Button(guimain, bg="#d8d8d8",image=bgiconcredit,cursor="heart",command=pujudtum).place(x=950, y=23, width=41, height=36)
guimain.mainloop()
