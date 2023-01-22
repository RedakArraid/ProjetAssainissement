# -*- coding: utf-8 -*-
from tkinter import*
class Troncon(object):
	"""docstring for assainissement"""
	def __init__(self,nbcs=3):
		self.fen=Tk()
		self.h,self.l=self.fen.winfo_screenheight(),self.fen.winfo_screenwidth()
		self.fen.geometry(str(self.l//3)+"x"+str(int(self.h//1.5))+"+"+str(self.l//3)+"+"+str(int(self.h//7)))
		self.fond=Canvas(self.fen,width=int(self.l//3),height=int(self.h//1.5),bg="turquoise")
		self.fond.place(x=0,y=0)
		self.can=Canvas(self.fond,bg="skyblue",width=int(self.h//1.7),height=190)
		self.can.place(x=0,y=50)
		self.canpara=Canvas(self.fond,bg="skyblue",width=int(self.h//1.7),height=300)
		self.canpara.place(x=0,y=250)
		self.libpara=[["Horizon (ans) ","Taux d'accroissement "],["Nombre d'habitants actuelle (hbt) ","Consomation specifique (L/j/hbt)","Pente","Ks"]]
		self.parametres=[[],[],[],[],[]]
		self.pars=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[10.0,0.033]]
		self.parcal=[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
		self.debitsep=[0,0,0,0]
		self.debitreel=[0,0,0,0]
		self.d=[0,0,0,0]
		self.tabaffq=[]
		self.tabaffd=[]
		
		self.tzone=[]
		self.debit=[]
		for i in range(1,5):
			if i%2==0:
				z=self.can.create_line(100*i,190//2,100*i,30,fill="blue",width=5,activefill="white")
				self.tzone.append(z)
				
			else:
				z=self.can.create_line(100*i,190//2,100*i,170,fill="blue",width=5,activefill="white")
				self.tzone.append(z)
		self.can.create_line(10,190//2,450,190//2,fill="red",width=10,activefill="white")

		self.scroll0 = Scrollbar(self.can,command=self.can.yview)
		self.scroll0.place(x=495,y=0,relheight=1)
		for i in range(1,5):
			if i%2==0:
				self.can.create_text(100*i,30-10,text=["A","B","C","D"][i-1])
				q=self.can.create_text(100*i+35,30-10+90,text="Q = 0.0 m^3/s")
				d=self.can.create_text(100*i+35,30+10+90,text="D = 0.0 mm")
				self.tabaffq.append(q)
				self.tabaffd.append(d)
			else:
				self.can.create_text(100*i,170+10,text=["A","B","C","D"][i-1])
				q=self.can.create_text(100*i+35,170-30-90,text="Q = 0.0 m^3/s")
				d=self.can.create_text(100*i+35,30-50+90,text="D = 0.0 mm")
				self.tabaffq.append(q)
				self.tabaffd.append(d)
		self.qdbt=self.can.create_text(100,10,text="Horizon = "+str(self.pars[4][0])+" ans Taux = "+str(self.pars[4][1]))
		self.tabaffq.append(self.qdbt)

		self.can.bind("<Button-1>",self.action_clic_text)

		self.fond.mainloop()
		
	def parametrer(self,branche):
		self.creationentry(branche)

	def creationentry(self,branche):
		self.canpara.destroy()
		self.canpara=Canvas(self.fond,bg="skyblue",width=int(self.h//1.7),height=300)
		self.canpara.place(x=0,y=250)
		self.parametres[branche-1]=[]
		if branche==5:
			nb=0
		else:
			nb=1
		print("ici")
		for i in range(len(self.libpara[nb])):
			e=Entry(self.canpara,font="Calibri 20")
			self.canpara.create_text(100,80*i+10,text=self.libpara[nb][i])
			self.parametres[branche-1].append(e)
			self.parametres[branche-1][i].place(x=10,y=80*i+30)
	def calculer(self):
		for k in range(4):
			print(self.pars)
			self.parcal[k][0]=round((self.pars[k][0]*(1+self.pars[4][1])**(self.pars[4][0])))*self.pars[k][1]
			self.parcal[k][1]=self.parcal[k][0]*0.85
			try :
				self.parcal[k][2]=1.5+2.5/(self.parcal[k][1]/(24*3600))**0.5
			except:
				""
			self.parcal[k][3]=self.parcal[k][2]*(self.parcal[k][1]/(3600*24))*0.001
			self.parcal[k][4]=self.parcal[k][3]*0.03
			self.parcal[k][5]=self.parcal[k][4]+self.parcal[k][3]
			self.debitsep[k]=self.parcal[k][5]
		self.debitreel=self.caculdebitreel(self.debitsep)
		for k in range(4):
			try :
				self.parcal[k][6]=round(((10.08*self.debitreel[k]/(3.14*self.pars[k][3]*self.pars[k][2]**0.5))**(3/8)),3)
			except:
				if k==0:
					self.parcal[k][6]=0
				else:
					self.parcal[k][6]=round(((10.08*self.debitreel[k]/(3.14*self.pars[k-1][3]*self.pars[k-1][2]**0.5))**(3/8)),3)
			if self.parcal[k][6]<=0.160:
				self.d[k]=160
			elif self.parcal[k][6]<=0.2:
				self.d[k]=200
			elif self.parcal[k][6]<=0.26:
				self.d[k]=260
			elif self.parcal[k][6]<=0.300:
				self.d[k]=300
			elif self.parcal[k][6]<=0.4:
				self.d[k]=400
			elif self.parcal[k][6]<=0.5:
				self.d[k]=500
			elif self.parcal[k][6]<=0.6:
				self.d[k]=600
		self.actualiserdebit()

	def actualiserdebit(self):
		self.can.itemconfigure(self.tabaffq[-1],text="Horizon = "+str(self.pars[4][0])+" ans Taux = "+str(self.pars[4][1]))
		for i in range(len(self.tabaffq)-1):
			self.can.itemconfigure(self.tabaffq[i],text="Q = "+str(round(self.debitreel[i],4))+" m^3/s")
			self.can.itemconfigure(self.tabaffd[i],text="D = "+str(self.d[i])+" mm")

	def caculdebitreel(self,tabds):
		tabdr=[sum(tabds[:i]) for i in range(1,len(tabds)+1)]
		return tabdr
	def calculdiametre(self):
		d=""
		return d

	def validation(self,branche):
		self.pars[branche-1]=[float(self.parametres[branche-1][i].get()) for i in range(len(self.parametres[branche-1]))]
		self.calculer()


	def action_clic_text(self,event):
		items=self.can.find_withtag("current")
		self.creationentry(items[0])
		self.butvalider=Button(self.canpara,text="VALIDER",font="algerian 15",command= lambda x=items[0] : self.validation(x))
		self.butvalider.place(x=380,y=65)


if __name__=="__main__":
	# -*- coding: utf-8 -*-
	Troncon()