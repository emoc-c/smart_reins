from load_cell import *
from ap import *
from mode import *

freq(160000000)
            
ssid = "SmartReins"
password = "jntpslgdp"


#init
load_cell_1 = mesure(d_out=15,pd_sck=14,nb_mesure=5,gap=0,save_rate=1,save_mode="value")
ap = access_point(ssid,password)
actual_mode = mode(led_pin="LED",button_pin=2)
checker = weight_checker(pin=13,duration=0.1,states=[[0,10],[1,1000],[2,2000],[5,3000]])

f = open(load_cell.save_path, "w")
f.write("")
f.close()

checker.buzzer.start_buzz()
while True :
    
    if actual_mode.check_status():
        #if the status changed
        print("switch to mode",actual_mode.status)
        checker.buzzer.transfert_buzz()
        if actual_mode.status=="transfert":
            load_cell.save_in_file()
            ap.new_instance()
            ap.run(data_path=load_cell.save_path,data_size=load_cell.nb_save)
            ap.stop()
            actual_mode.switch_status("mesurement")
            load_cell.nb_save=0
            load_cell.saves=[]
            f = open(load_cell.save_path, "w")
            f.write("")
            f.close()
            
            
            
            checker.buzzer.transfert_buzz()
    else :
        #if the status is the same
        if actual_mode.status=="mesurement":
            v=load_cell.safe_read(kg=True,r=2)
            print("-----")
            checker.check(v)
            print(v)
            
    
    


