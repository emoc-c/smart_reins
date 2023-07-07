from machine import Pin

class mode():
    def __init__(self,led_pin,button_pin):
        self.led=Pin(led_pin,Pin.OUT)
        #init led
        self.led.value(0)
        self.button=Pin(button_pin, Pin.IN)
        self.status="mesurement"
        self.all_status=["mesurement","transfert"]
    def check_status(self):
        """
        check_status : looks for changes (activation of the button)
        inputs:
        /
        outputs:
        0: same status
        1 : the status changed
        """
        val=self.status=="transfert"
        if self.button.value():
            self.status=self.all_status[abs(val-1)]
            self.led.value(abs(val-1))
            while self.button.value():
                pass
            return 1
        return 0
    def switch_status(self,new_status):
        """
        switch_status : manually change the status
        inputs:
        new_status : the new status
        outputs:
        / 
        """
        if new_status=="mesurement":
            self.led.value(0)
        self.status=new_status
