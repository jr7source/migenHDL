# Random State Machine
# Migen 
# jra

from migen import *
from migen.fhdl import verilog

class MooreStateMachine(Module):            # Top Module
    def __init__(self):
        
        self.s = Signal(2, name = "s1")                   # 2-bit Singal [0:1]
        self.s2 = Signal(2, name = "s2")
        self.counter = Signal(4, name = "counter")            # 4-bit counter [0:15]
        self.o = Signal(3, name = "output")
        
        x = Array(Signal(name=f"a_{i}") for i in range(7))  # Array of signals

        fsm = FSM(reset_state="State_0")                         # Instantiating an FSM "fsm"
        self.submodules += fsm              # Adding submodule (fsm) to top module MooreStateMachine
        

        # self.sync += self.counter.eq(self.counter + 1)             # Updating value instruction

        # If(self.s, NextValue(self.counter,self.counter+1))

        # STATE_0
        fsm.act("State_0",
                If(self.counter == 24, NextValue(self.counter, 0)),
                If(self.s2, NextValue(self.counter,self.counter+1)),
                If(self.s, NextState("State_1"))
                .Else(NextState("State_2"))
                )
        
        fsm.act("State_1", 
                If(self.s2, NextValue(self.counter,self.counter+1)),
                If(~self.s, NextState("State_0"))
                .Else(NextState("State_2"))
        )

        fsm.act("State_2", 
                If(self.s2, NextValue(self.counter,self.counter+1)),
                If(self.counter == 20, NextValue(self.o, 2)),
                If(self.s, NextState("State_0"))
                .Else(NextState("State_10"))
        )
        
        fsm.act("State_10",
                If(self.s, NextValue(self.counter,self.counter+1)),
                If(~self.s, NextState("State_0"))
                .Else(
                   #NextValue(self.counter, self.counter + 1), 
                   If(self.counter == 23, NextState("State_0"))
                      )
                )


        self.be = fsm.before_entering("State_0")
        self.ae = fsm.after_entering("State_0")
        self.bl = fsm.before_leaving("State_0")
        self.al = fsm.after_leaving("State_0")
                    
# Define FHDL module MooreStateMachine here

if __name__ == "__main__":
  from migen.fhdl.verilog import convert
  msm = MooreStateMachine()
  verilog.convert(msm, ios = {msm.s, msm.counter, msm.o, msm.s2}).write("MSM.v")