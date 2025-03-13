# Brief: FSM Interrupt Handler for BOSCH MCAN
# Version: 2
# Author: Jatin

from migen import *
from migen import Module, Signal, FSM

class MCAN(Module):
    def __init__(self):
    
        # Bosch MCAN core Signals
        
        self.interrupt = Signal(name = "interrupt")
        self.mcan_adr = Signal(12, name = "mcan_adr")
        self.mcan_wrdat = Signal(32, name = "mcan_wrdat")
        self.mcan_rddat = Signal(32, name = "mcan_rddat")
        self.mcan_wrdat_en = Signal(name = "mcan_wrdat_en")
        self.mcan_rddat_en = Signal(name = "mcan_rddat_en")
        self.txefs = Signal(32, name = "TXEFS") # Tx Event FIFO Status
        self.txefa = Signal(5, name = "TXEFA") # Tx Event FIFO Acknowledge


class TCPIP_Phy(Module):
    def __init__ (self):
        
        # TCP IP Phy Signals
        
        self.canappfdk_adr_i = Signal(16, name = "canappfdk_adr_i")
        self.canappfdk_dat_i = Signal(32, name = "canappfdk_dat_i")
        self.canappfdk_wr_en_i = Signal(name = "canappfdk_wr_en_i")
        

class Machine(Module):
    def __init__ (self):
        
        self.mcan = MCAN()
        self.tcpip = TCPIP_Phy()
        
        # Internal registers v1
        
        self.ro = Signal(16, name = "reg_0")
        self.r1 = Signal(32, name = "reg_1")
        self.r2 = Signal(16, name = "dummy_reg")
        
        # Internal registers v2
        self.readback_TXEFS = Signal(32, name = "Tx_Event_FIFO_Status")
        self.time_stamp_1 = Signal(32, name = "Timestamp_1")
        self.time_stamp_2 = Signal(32, name = "Timestamp_2")
        self.base_addr = Signal(16, reset=0x0020)

        # v1
        
        self.submodules += self.mcan, self.tcpip

        fsm = FSM(reset_state="Interrupt_line")
        self.submodules += fsm
        
        # State Default
        fsm.act("Interrupt_line", 
                If(self.mcan.interrupt,
                NextState("Read_Status_Register")
            )
        )
        
        # State 1'd1
        fsm.act("Read_Status_Register",
            self.mcan.mcan_adr.eq(0x050),
            self.mcan.mcan_rddat_en.eq(1),
            self.ro.eq(0x0050),
            self.r1.eq(self.mcan.mcan_rddat),
            NextState("Write_to_TCPIP")
        )
        
        # State 1'd2
        fsm.act("Write_to_TCPIP",
            self.tcpip.canappfdk_adr_i.eq(0x9000),
            self.tcpip.canappfdk_dat_i.eq(Cat(self.mcan.mcan_rddat[16:32], 0x0050)),
            self.tcpip.canappfdk_wr_en_i.eq(1),
            NextState("Write_Length")
        )
        
        # State 1'd3
        fsm.act("Write_to_TCPIP_2",
            self.tcpip.canappfdk_adr_i.eq(0x9000),
            self.tcpip.canappfdk_dat_i.eq(Cat(self.r2, self.mcan.mcan_rddat[0:16])),
            self.tcpip.canappfdk_wr_en_i.eq(1),
            NextState("Write_Length")
        )
        
        # State 1'd4
        fsm.act("Write_Length",
            self.tcpip.canappfdk_adr_i.eq(0x9004),
            self.tcpip.canappfdk_dat_i.eq(6),
            self.tcpip.canappfdk_wr_en_i.eq(1),
            NextState("Readback")
                    )
        
        # State 1'd5 [v2]
        fsm.act("Readback",
                self.readback_TXEFS.eq(self.mcan.txefs),
                self.time_stamp_1.eq((0x0020)+2*(self.mcan.txefs[8:12])),
                self.time_stamp_2.eq((0x0020)+2*(self.mcan.txefs[8:12])+1),
                self.mcan.txefa.eq(self.mcan.txefs[8:12]),
                NextState("Interrupt_line")
            )


if __name__ ==  "__main__":
    
    from migen.fhdl import verilog
    from migen.fhdl.verilog import convert
    
    machine = Machine()
    convert(machine, ios = {machine.ro,
        machine.r1, 
                
        machine.mcan.interrupt, 
        machine.mcan.mcan_adr,
        machine.mcan.mcan_wrdat,
        machine.mcan.mcan_rddat,
        machine.mcan.mcan_wrdat_en,
        machine.mcan.mcan_rddat_en,
        machine.mcan.txefa,
        machine.mcan.txefs,

        machine.tcpip.canappfdk_adr_i,
        machine.tcpip.canappfdk_dat_i,
        machine.tcpip.canappfdk_wr_en_i
        }, name='FSM_BOSCH_MCAN_v2').write('FSM_BOSCH_MCAN_v2.v')         