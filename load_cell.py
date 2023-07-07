from machine import freq
from hx711 import HX711
import time
from machine import PWM,Pin

freq(160000000)



class mesure(HX711): 
    def __init__(self,d_out,pd_sck,nb_mesure=5,gap=0.1,save_rate=60,save_mode="value",save_path="data.txt",Buffer=100):
        HX711.__init__(self,d_out=d_out,pd_sck=pd_sck)
        self.channel=HX711.CHANNEL_A_64
        self.nb_mesure=nb_mesure
        self.gap=gap
        self.save_rate=save_rate
        self.save_mode=save_mode
        self.save_path=save_path
        self.nb_save=0
        self.Buffer=Buffer
        self.clock=1
        
        
        #tmp_saves : data we will use in the next save
        #saves : saved data
        self.tmp_saves=[]
        self.saves=[]
        
        #init val
        #v0 initial value for 0kg
        #ikg the weight for the second mesurement
        #valikg the value of the second mesurement
        
        #v0=2142373
        v0=-6671758.0
        
        ikg=3
        
        #valikg=2266122
        valikg=-6600512.0
        
        
        #we have kg=a*mesure+b
        
        self.a=ikg/(valikg-v0)
        self.b=-self.a*v0
        
        # calculation of the offset when we switch on the device
        self.init=0
        tmp_init=self.safe_read(kg=True)
        self.init=tmp_init
        
        
        
    def safe_read(self,kg=True,r=2):
        '''
        safe_read: read HX711 value
        inupts:
        kg :  convert the value to kg
        r : the round
        ouputs
        the value or the weigth
        '''
        val=0
        try:
            for i in range(self.nb_mesure):
                read=self.read()
                val+=read
                time.sleep(self.gap)
            val=val/self.nb_mesure
        except:
            self.power_off()
            f = open(self.save_path, "w")
            f.write("")
            f.close()
            raise Exception("error during mesurement")
        if kg:
            weight=round(self.kg(val),2)
            self.tmp_saves.append(weight)
            if self.clock == self.save_rate:
                self.save()
                self.clock=1
            else :
                self.clock+=1
            
            return weight
        else :
            return val
    def kg(self,val):
        """
        kg : convert mesurement to kg
        inputs :
        val : the mesurement
        outputs :
        the weight
        """
        return self.a*val+self.b-self.init
    
    def save(self):
        """
        save : add key values (min,max,mean) to saved values using the save_rate
        
        """
        if self.save_mode=="key":
            max_val = max(self.tmp_saves)
            min_val = min(self.tmp_saves)
            mean_val = sum(self.tmp_saves)/self.save_rate
            
            self.saves.append({"max":max_val,"min":min_val,"mean":mean_val})
        elif self.save_mode=="value":
            mean_val = sum(self.tmp_saves)/self.save_rate
            self.saves.append(mean_val)
        
        self.tmp_saves=[]
        if len(self.saves)>self.Buffer:
            self.save_in_file()
    def save_in_file(self):
        """
        save_in_file: save the data buffer inside a file with the path chosen during the initialisation
        inputs:
        /
        outputs:
        /
        """
        f = open(self.save_path, "a")
        for s in self.saves:
            string="{:0.2f}".format(abs(s))
            
            f.write(string+"\n")
            self.nb_save+=1
        f.close()
        self.saves=[]
        
        
        
class Buzzer():
    def __init__(self,pin,power=1000,duration=1):
        self.pwm=PWM(Pin(pin))
        self.power=power
        self.duration=duration
    def bip(self,freq,power=None,duration=None):
        """
        bip : bip to a freq with an intencity of power and during duration by default it will use the buzzer parameters
        inputs:
        freq : the frequence of vibration
        power ;  the intencity
        duration : number of seconds
        outputs:
        /
        """
        if power==None:
            power=self.power
        if duration==None:
            duration=self.duration
        try :
            self.pwm.freq(freq)
            self.pwm.duty_u16(power)
            time.sleep(duration)
            self.pwm.duty_u16(0)
        except :
            self.pwm.duty_u16(0)
    def start_buzz(self):
        """
        start_buzz :  the sequence to play when we switch the device on
        inputs :
        /
        outputs :
        /
        """
        self.bip(1000,1000,0.2)
        self.bip(2000,1000,0.2)
        self.bip(1000,1000,0.2)
    def transfert_buzz(self):
        """
        transfert_buzz : the sequence to play when we swith the divice's mode
        inputs:
        /
        outputs:
        /
        """
        self.bip(2000,1000,0.1)
        time.sleep(0.1)
        self.bip(2000,1000,0.1)
        
            
class weight_checker():
    def __init__(self,states,pin,power=None,duration=None):
        #all the value we can bip
        self.all_states=states
        self.state=0
        self.buzzer=Buzzer(pin)
        self.power=power
        self.duration=duration
    def check(self,value):
        """
        check : check if we have to produce a sound and and update the state if needed
        inputs:
        value :  the value we want to check
        outputs:
        /
        """
        print(self.state)
        it=list(reversed(self.all_states))
        for i,state_val in enumerate(it):
            if value>state_val[0]:
                if len(it)-1-i>self.state :
                    self.buzzer.bip(state_val[1],self.power,self.duration)
                self.state=len(it)-1-i
                return
        self.state=0
        return
                
            
        
        
    
    

        


