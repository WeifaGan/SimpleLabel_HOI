from tkinter.filedialog import askdirectory
import tkinter as tk
from tkinter import messagebox
from arg import * 

from tkinter import ttk

class GUI(object):
    def __init__(self):
        self.bbox_nums = 50 
        self.window = tk.Tk()
        self.sub_var = tk.IntVar()
        self.relation_var = tk.IntVar()
        self.relation_var_w  =tk.IntVar()  
        self.pair_sub_var = tk.IntVar() 
        self.pair_obj_var = tk.IntVar() 

    def start_gui(self,q_json,q_idx):
        self.window.title("Simple Label")
        # self.window.geometry('500x200')
        
        #每个bbox选择一个对象
        l = tk.Label(self.window,text="please select a subject for each bbox",bg='green', \
            font=('Arial', 12), width=40, height=1) 
        l.pack()
        for sub_key,sub_value in subject_cls.items():        
            r1 = tk.Radiobutton(self.window, text=str(sub_value)+":"+sub_key, variable=self.sub_var, \
                value=sub_value, command=None)
            r1.pack()
        b = tk.Button(self.window, text='certain', font=('Arial', 10), width=10, height=1, command=lambda:self.annotation(q_json,q_idx))
        b.pack()

        #选择为<人-物>
        # frm2_3 = tk.Frame(self.window)
        # frm2 = tk.Frame(frm2_3)
        # l = tk.Label(self.window,text="please select a <person,object> pair",bg='green', font=('Arial', 12), width=40, height=1) 
        # l.pack()
        
        # for i in range(self.bbox_nums):
        #     c2 = tk.Radiobutton(frm2, text = "bbox "+str(i), variable = self.pair_sub_var,value=i, command=None)
        #     c2.pack()
        # frm2.pack(side=tk.LEFT)

        # frm3 = tk.Frame(frm2_3)
        # for i in range(self.bbox_nums):
        #     c2 = tk.Radiobutton(frm3, text = "bbox "+str(i), variable = self.pair_obj_var,value=i, command=None)
        #     c2.pack()
        # frm3.pack(side=tk.LEFT)
        # frm2_3.pack()

        #——————————————————————————————————————————#
        #  下拉菜单
        #——————————————————————————————————————————#
        frm2_3 = tk.Frame(self.window)
        frm2 = tk.Frame(frm2_3)
        l = tk.Label(self.window,text="please select a <person,object> pair",bg='green', font=('Arial', 12), width=40, height=1) 
        l.pack()
    
        l = tk.Label(frm2,text="select a subject bbx num", font=('Arial', 12), width=40, height=1) 
        l.pack()
        num_choice = ttk.Combobox(frm2, width=12, textvariable=self.pair_sub_var)
        num_choice['values']= tuple(range(self.bbox_nums))
        num_choice.pack()
        frm2.pack()

        frm3 = tk.Frame(frm2_3)
    
        l = tk.Label(frm3,text="select a obj bbx num", font=('Arial', 12), width=40, height=1) 
        l.pack()
        num_choice = ttk.Combobox(frm3, width=12, textvariable=self.pair_obj_var)
        num_choice['values']= tuple(range(self.bbox_nums))
        num_choice.pack()
        frm3.pack()
        frm2_3.pack()



        #选择的<人-物>关系
        select_relation = False #不需要选择关系，根据bbx的类别来确定关系
        if select_relation: 
            frm4 = tk.Frame(self.window)
            l = tk.Label(self.window,text="please select a relation for the pair",\
                    bg='green', font=('Arial', 12), width=40, height=1) 
            l.pack()
            for hoi_key,hoi_value in Hoi_cls.items():     
                r1 = tk.Radiobutton(frm4, text=str(hoi_value)+":"+hoi_key, variable=self.relation_var, \
                    value=hoi_value, command=None)
                r1.pack()
            frm4.pack()

            if mode=="train":
                frm_t = tk.Frame(self.window)
                l_t = tk.Label(self.window,text="please select a object relation",\
                        bg='green', font=('Arial', 10), width=35, height=1) 
                l_t.pack()

                for hoi_key,hoi_value in Hoi_cls_What.items():     
                    r1 = tk.Radiobutton(frm_t, text=str(hoi_value)+":"+hoi_key, variable=self.relation_var_w, \
                        value=hoi_value, command=None)
                    r1.pack()
            
                frm_t.pack()



        b = tk.Button(self.window, text='certain', font=('Arial', 10), width=10, height=1, command=lambda:self.hoi_annotation(q_json,q_idx))
        b.pack()

        self.window.mainloop()

    def hoi_annotation(self,q_json,q_idx):
        pair_sub_var = self.pair_sub_var.get()
        pair_obj_var = self.pair_obj_var.get()
        relation_var = self.relation_var.get()
        if mode=="train":
            relation_var_w = self.relation_var_w.get()

        cur_dict = q_json.get()

        id_in_json= q_idx.get()
        q_idx.put(id_in_json)
        if mode=="test":
            hoi_dict = {"subject_id":pair_sub_var,"object_id":pair_obj_var,"category_id":relation_var}
        else:
            #如果不选择，默认为0
            if relation_var == 0 and relation_var_w ==0:
                sub = cur_dict[id_in_json]["annotations"][pair_sub_var]["category_id"]
                obj = cur_dict[id_in_json]["annotations"][pair_obj_var]["category_id"]
                if sub == 1:
                    if obj == 7:
                        relation_var,relation_var_w  = 2,7
                    else: 
                        relation_var,relation_var_w  = 1,obj 

                    hoi_dict = {"subject_id":pair_sub_var,"object_id":pair_obj_var,"category_id":relation_var,\
                         "hoi_category_id":relation_var_w}
                else:
                    bbx_subject_warning()
            else:
                hoi_dict = {"subject_id":pair_sub_var,"object_id":pair_obj_var,"category_id":relation_var,\
                        "hoi_category_id":relation_var_w}



        Err = [] 
        for idi,i in enumerate(cur_dict[id_in_json]["annotations"]):
            if i["category_id"]==-1:
                Err.append(idi)


        visited = []
        if not Err:
                    
            if hoi_dict not in cur_dict[id_in_json]["hoi_annotations"]: #避免重复添加hoi_annotation信息

                try: 
                    last_pair = list(cur_dict[id_in_json]["hoi_annotations"][-1].values())[:2]
                except:
                    last_pair = []
                
            
                if [pair_sub_var,pair_obj_var]==last_pair:
                    cur_dict[id_in_json]["hoi_annotations"][-1] = hoi_dict
                    print("after hoi modified:\n",cur_dict[id_in_json])#避免相同的pair会有不同relatioin
                else:
                    cur_dict[id_in_json]["hoi_annotations"].append(hoi_dict)
                    print("after hoi added:\n",cur_dict[id_in_json])

                
        else:
            self.bbx_category_warning(Err)

        q_json.put(cur_dict)

    def annotation(self,q_json,q_idx):
        category_id = self.sub_var.get()
        cur_dict = q_json.get()
        
        id_in_json = q_idx.get()
        q_idx.put(id_in_json)
        cur_dict[id_in_json]["annotations"][-1].update({"category_id":category_id})#更新最后那个的anno
        q_json.put(cur_dict)

        print("after bbx added:\n",cur_dict[id_in_json])

    def bbx_category_warning(self,Err):
        messagebox.showinfo(title='Warning', message="bbx catetory is empty!\n"+str(Err))   

    def bbx_subject_warning(self):
        messagebox.showinfo(title='Warning', message="subject catetory should be a person")   



