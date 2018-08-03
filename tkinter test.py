from tkinter import *
import time
from Ticket_GLPI import New_Ticket
from Centreon import Centreon_Status

class Application:

  def __init__(self,master):
    global frame, Centreon, GLPI, Centreon_Host, Centreon_Service, GLPI_New_Ticket
    self.master = master
    frame = Frame(master, width =1080, height =720)
    frame['bg'] = 'white'
    frame.pack()

    self.TimeInterval = 600000

# Interface principal Centreon & GLPI

    GLPI = Frame(frame, borderwidth=2, relief=GROOVE)
    GLPI.pack(side=LEFT, padx=30, pady=30)

    GLPI_label = Label(GLPI, text="Information GLPI")
    GLPI_label.pack(padx=10, pady=10)

    GLPI_New_Ticket = Frame(GLPI)
    GLPI_New_Ticket.pack(side=TOP)

    Centreon = Frame(frame, borderwidth=2, relief=GROOVE)
    Centreon.pack(side=RIGHT, padx=30, pady=30)


    Centreon_label = Label(Centreon, text="Information Centreon ")
    Centreon_label.pack(padx=10, pady=10)

    Centreon_Host = Frame(Centreon)
    Centreon_Host.pack(side=RIGHT)
    Centreon__Host_label = Label(Centreon_Host, text="Information Centreon Hosts")
    Centreon__Host_label.pack()


    Centreon_Service = Frame(Centreon)
    Centreon_Service.pack(side=LEFT)
    Centreon__Service_label = Label(Centreon_Service, text="Information Centreon Services")
    Centreon__Service_label.pack()

    self.Refresh()

  def ticket(self):
# Recuperation des nouveaux tickets

    new_ticket = New_Ticket()
    self.Delete_frame(GLPI_New_Ticket)

# Interface GLPI
    Label(GLPI_New_Ticket, text="Nouveau TICKET", background='cyan', anchor=CENTER).pack()
    if len(new_ticket) == 0:
        Label(GLPI_New_Ticket, text="Aucun Nouveau Ticket", background='white', anchor=CENTER).pack()
    else:
      for i in new_ticket:
        Label(GLPI_New_Ticket, text=i['name'], background='white', anchor=CENTER).pack()

  def centreon(self):
# Recuperation Info Centreon
    problem_centreon = Centreon_Status()
    hosts_problems = problem_centreon[0]
    services_problems = problem_centreon[1]

# Interface Centreon

    # Interface Host
    self.Delete_frame(Centreon_Host)
    Label(Centreon_Host, text="Hosts Probleme", background='cyan', anchor=CENTER).pack()
    if len(hosts_problems) == 0:
        Label(Centreon_Host, text="Host : Aucun  Probleme", background='white', anchor=CENTER).pack()
    else:
      for p in range(len(hosts_problems)):
          Label(Centreon_Host, text=hosts_problems[p], background='white', anchor=CENTER).pack()

    # Interface Service
    self.Delete_frame(Centreon_Service)
    Label(Centreon_Service, text="Services Probleme", background='cyan', anchor=CENTER).pack()
    if len(services_problems) == 0:
        Label(Centreon_Service, text="Service : Aucun Probleme", background='white', anchor=CENTER).pack()
    else:
      for q in range(len(services_problems)):
          Label(Centreon_Service, text=services_problems[q], background='white', anchor=CENTER).pack()

  def Refresh(self):
    self.ticket()
    self.centreon()
    self.master.after(self.TimeInterval, self.Refresh )



  def Delete_frame(self,frame):
    for widget in frame.winfo_children():
      widget.pack_forget()


root = Tk()
app = Application(root)
root.title('Nikita')
root['bg'] = 'white'
root.mainloop()
