from tkinter import *
import time
from Ticket_GLPI import New_Ticket
from Centreon import Centreon_Status

test = 0

class Application:

  def __init__(self,master):
    global frame, Centreon, GLPI, Centreon_Host, Centreon_Service, GLPI_New_ticket
    self.master = master
    frame = Frame(master)
    frame['bg'] = 'white'
    frame.pack()

    self.TimeInterval = 2000

# Interface principal Centreon & GLPI

    Centreon = Frame(frame, borderwidth=2, relief=GROOVE)
    Centreon.pack(side=RIGHT, padx=30, pady=30)

    GLPI = Frame(frame, borderwidth=2, relief=GROOVE)
    GLPI.pack(side=LEFT, padx=30, pady=30)

    Centreon_label = Label(Centreon, text="Information Centreon %d" %test)
    Centreon_label.pack(padx=10, pady=10)

    Centreon_Host = PanedWindow(Centreon, orient=VERTICAL)
    Centreon_Host.pack(side=LEFT, expand=Y, fill=BOTH, pady=5, padx=5)
    Centreon_Host.add(Label(Centreon_Host, text="Host Probleme", background='cyan', anchor=CENTER))

    Centreon_Service = PanedWindow(Centreon, orient=VERTICAL)
    Centreon_Service.pack(side=RIGHT, expand=Y, fill=BOTH, pady=5, padx=5)
    Centreon_Service.add(Label(Centreon_Service, text="Service Probleme", background='cyan', anchor=CENTER))

    GLPI_label = Label(GLPI, text="Information GLPI")
    GLPI_label.pack(padx=10, pady=10)

    GLPI_New_ticket = PanedWindow(GLPI, orient=VERTICAL)
    GLPI_New_ticket.pack(side=TOP, expand=Y, fill=BOTH, pady=5, padx=5)
    GLPI_New_ticket.add(Label(GLPI_New_ticket, text="Nouveau TICKET", background='cyan', anchor=CENTER))

    self.Refresh()

  def ticket(self):
# Recuperation des nouveaux tickets

    new_ticket = New_Ticket()

# Interface GLPI
    if len(new_ticket) == 0:
      GLPI_New_ticket.add(Label(GLPI_New_ticket, text="Aucun Nouveau Ticket", background='white', anchor=CENTER))
    else:
      for i in new_ticket:
        GLPI_New_ticket.add(Label(GLPI_New_ticket, text=i['name'], background='white', anchor=CENTER))

  def centreon(self):
# Recuperation Info Centreon

    problem_centreon = Centreon_Status()

# Interface Centreon

    # Interface Host
    if len(problem_centreon[0]) == 0:
      Centreon_Host.add(Label(Centreon_Host, text="Host : Aucun  Probleme", background='white', anchor=CENTER))
    else:
      for problem_host in problem_centreon[0]:
        Centreon_Host.add(Label(Centreon_Host, text=problem_host['name'], background='white', anchor=CENTER))

    # Interface Service
    if len(problem_centreon[1]) == 0:
      Centreon_Service.add(Label(Centreon_Service, text="Service : Aucun Probleme", background='white', anchor=CENTER))
    else:
      for problem_service in problem_centreon[1]:
        Centreon_Service.add(Label(Centreon_Service, text=problem_service['name'], background='white', anchor=CENTER))



  def Refresh(self):
    self.ticket()
    self.centreon()
    self.master.after(self.TimeInterval, self.Refresh )

root = Tk()
app = Application(root)
root.title('Nikita')
root['bg'] = 'white'
root.mainloop()
