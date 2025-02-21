# Converting canappdek_ctrl from Python to Verilog using Migen
# Jatin 

from migen import *
from migen.genlib.fsm import FSM, NextState, NextValue
from migen.fhdl.structure import ResetSignal


class canappdek_ctrl(Module):
    def __init__(self):
        
        # Inputs (9)
        # Override default clock domain
        self.clk = Signal(name="clk")
        self.rst = Signal(name="rst")
        

        self.tcp_link_status = Signal(name="tcp_link_status")
        self.app_buf_wren = Signal(name="app_buf_wren")
        self.app_buf_datwr = Signal(32, name="app_buf_datwr")

        self.qspim_readdata_i = Signal(32, name="qspim_readdata_i")
        self.qspim_waitrequest = Signal(name="qspim_waitrequest")
        self.qspim_readdatavalid = Signal(name="qspim_readdatavalid")
        self.gpio_int = Signal(name="gpio_int")

        # Outputs (7)
        self.test_ro = Signal(name="test_ro")
        self.app_empty_num = Signal(16, name="app_empty_num")
        self.qspim_address = Signal(16, name="qspim_address")
        self.qspim_read = Signal(name="qspim_read")
        self.qspim_write = Signal(name="qspim_write")
        self.qspim_writedata_o = Signal(32, name="qspim_writedata_o")
        self.buffer_size = Signal(16, name="buffer_size")

        # Internal signals/Wires (15)
        self.qspim_readdata = Signal(32, name="qspim_readdata")  # wire "assign qspim_readdata = qspim_readdata_i;"
        self.qspim_writedata = Signal(32, name="qspim_writedata")  # wire "assign qspim_writedata_o = qspim_writedata;"

        self.counter = Signal(13, name="counter")  # wire "wire [12:0] counter;"

        self.app_buf_out_rden = Signal(name="app_buf_out_rden")
        self.app_buf_empty = Signal(name="app_buf_empty")
        self.app_buf_out = Signal(32, name="app_buf_out")

        self.avalon_state = Signal(6, name="avalon_state")
        self.next_avalon_state = Signal(6, name="next_avalon_state")

        self.warten_counter = Signal(32, name="warten_counter")
        self.next_warten_counter = Signal(32, name="next_warten_counter")

        self.tst_counter = Signal(32, name="tst_counter")
        self.next_tst_counter = Signal(32, name="next_tst_counter")

        self.can_counter = Signal(32, name="can_counter")
        self.next_can_counter = Signal(32, name="next_can_counter")

        self.cannolo_ver = Signal(96, name="cannolo_ver")
        self.next_cannolo_ver = Signal(96, name="next_cannolo_ver")

        self.test_r = Signal(1, name="test_r")

        # Assign buffer size
        self.comb += self.buffer_size.eq(Cat(0b0, 0b0 ,self.counter))       # "assign buffer_size = {counter, 2'b0};"
        self.comb += self.qspim_readdata.eq(self.qspim_readdata_i)
        self.comb += self.qspim_writedata_o.eq(self.qspim_writedata)

        # Parameters
        # 16-bit parameters for adr
        ADR_INIT_CCCR = 0x0 & 0xFFFF # 16 bits ## Enforcing 16 bits with AND gate
        ADR_INIT_DBTP = 0x0     # 16 bits
        ADR_INIT_DTCR = 0x0     # 16 bits
        ADR_INIT_NBTP = 0x0     # 16 bits
        ADR_INIT_IR = 0x0       # 16 bits
        ADR_INIT_IE = 0x0       # 16 bits
        ADR_INIT_TXBTIE = 0x0   # 16 bits
        ADR_INIT_TXBCIE = 0x0   # 16 bits
        ADR_INIT_DONE = 0x0     # 16 bits

        ADR_RX_POINT_A = 0x0  # 16 bits
        ADR_RX_POINT_B = 0x0  # 16 bits
        ADR_RX_POINT_C = 0x0  # 16 bits
        ADR_RX_POINT_D = 0x0  # 16 bits

        ADR_RX_POINT_E = 0x0  # 16 bits
        ADR_RX_POINT_F = 0x0  # 16 bits
        ADR_RX_POINT_G = 0x0  # 16 bits
        ADR_RX_POINT_H = 0x0  # 16 bits

        ADR_RX_POINT_I = 0x0  # 16 bits
        ADR_RX_POINT_J = 0x0  # 16 bits
        ADR_RX_POINT_K = 0x0  # 16 bits
        ADR_RX_POINT_L = 0x0  # 16 bits

        ADR_RX_POINT_M = 0x0  # 16 bits
        ADR_RX_POINT_N = 0x0  # 16 bits
        ADR_RX_POINT_O = 0x0  # 16 bits
        ADR_RX_POINT_P = 0x0  # 16 bits

        ADR_TX_POINT_A = 0x0  # 16 bits
        ADR_TX_POINT_B = 0x0  # 16 bits
        ADR_TX_POINT_C = 0x0  # 16 bits
        ADR_TX_POINT_D = 0x0  # 16 bits

        ADR_TX_POINT_E = 0x0  # 16 bits
        ADR_TX_POINT_F = 0x0  # 16 bits
        ADR_TX_POINT_G = 0x0  # 16 bits
        ADR_TX_POINT_H = 0x0  # 16 bits

        # 32-bit parameters for write data
        DAT_INIT_CCCR = 0x0 & 0xFFFFFFFF  # 32 bits ## Enforcing 32 bits with AND gate
        DAT_INIT_DBTP = 0x0  # 32 bits
        DAT_INIT_DTCR = 0x0  # 32 bits
        DAT_INIT_NBTP = 0x0  # 32 bits
        DAT_INIT_IR = 0x0    # 32 bits
        DAT_INIT_IE = 0x0    # 32 bits
        DAT_INIT_TXBTIE = 0x0  # 32 bits
        DAT_INIT_TXBCIE = 0x0  # 32 bits
        DAT_INIT_DONE = 0x0  # 32 bits

        """ Sync logic
        always @(posedge clk or negedge rst) begin
	        if (rst == 1'b0) begin
		        avalon_state <= STATE_INIT_START;
                warten_counter <= 32'h0;
                tst_counter <= 32'h0;
                can_counter <= 32'h0;
                cannolo_ver <= 96'h0;

                test_ro <= 1'b0;
		     end
		     else begin
			     avalon_state <= next_avalon_state;
                 warten_counter <= next_warten_counter;
                 tst_counter <= next_tst_counter;
                 can_counter <= next_can_counter;
                 cannolo_ver <= next_cannolo_ver;

                 test_ro <= test_r;
		     end
	    end
        """
        
        self.sync += [
            If(self.rst == 0,
                # self.avalon_state.eq(STATE_INIT_START) already done below
                self.warten_counter.eq(0),
                self.tst_counter.eq(0),
                self.can_counter.eq(0),
                self.cannolo_ver.eq(0),
                self.test_ro.eq(0)
            ).Else(
                self.avalon_state.eq(self.next_avalon_state),
                self.warten_counter.eq(self.next_warten_counter),
                self.tst_counter.eq(self.next_tst_counter),
                self.can_counter.eq(self.next_can_counter),
                self.cannolo_ver.eq(self.next_cannolo_ver),
                self.test_ro.eq(self.test_r)
            )
        ]
        
        # FSM transitions # Default logic for all states
        # self.comb += [
        #     self.next_avalon_state.eq(self.avalon_state),  # Default state
        #     self.next_warten_counter.eq(self.warten_counter),  # Default counter values
        #     self.next_tst_counter.eq(self.tst_counter),
        #     self.next_can_counter.eq(self.can_counter),
        #     self.next_cannolo_ver.eq(self.cannolo_ver),

        #     # self.app_buf_out_rden.eq(0),  # No reading from buffer by default
        #     # self.qspim_writedata.eq(0),  # No data for QSPI
        #     # self.qspim_write.eq(0),  # No write to QSPI
        #     # self.qspim_address.eq(0),  # No QSPI address
        #     # self.qspim_read.eq(0),  # No read from QSPI
        #     # self.test_r.eq(0)  # Test read-out is inactive by default
        # ]
        
        # State Machine
        fsm = FSM(reset_state="STATE_INIT_START")
        self.submodules += fsm

        fsm.act("STATE_INIT_START",
            NextValue(self.warten_counter, 0),
            NextValue(self.tst_counter, 0),
            NextValue(self.can_counter, 0),
            If(self.tcp_link_status, NextState("STATE_TST_GO"))
        )

        fsm.act("STATE_TST_GO",
            If(~self.app_buf_empty,
                NextValue(self.app_buf_out_rden, 1),
                NextState("STATE_TMP")
            )
        )

        fsm.act("STATE_TMP",
            NextValue(self.warten_counter, self.warten_counter + 1),
            NextValue(self.tst_counter, self.tst_counter + 1),
            If(~self.tcp_link_status,
                NextState("STATE_INIT_START")
            ).Elif(self.warten_counter == 0x400,
                NextValue(self.warten_counter, 0),
                NextState("STATE_TMP")
            ),
            If(~self.app_buf_empty,
                NextValue(self.app_buf_out_rden, 1)
            )
        )

        fsm.act("STATE_TMP1",
            NextValue(self.test_r, 1),
            NextValue(self.qspim_write, 1),
            NextValue(self.qspim_writedata, 0x2),
            NextValue(self.qspim_address, 0x7000),
            If(~self.qspim_waitrequest, NextState("STATE_TMP2"))
        )

        fsm.act("STATE_TMP2",
            NextValue(self.qspim_write, 1),
            NextValue(self.qspim_writedata, Cat(C(0x4, 8), self.tst_counter[:24])),
            NextValue(self.qspim_address, 0x7000),
            If(~self.qspim_waitrequest, NextState("STATE_TMP5"))
        )

        fsm.act("STATE_TMP5",
            NextValue(self.qspim_write, 1),
            NextValue(self.qspim_writedata, Cat(self.tst_counter[:8], C(0, 24))),
            NextValue(self.qspim_address, 0x7000),
            If(~self.qspim_waitrequest, NextState("STATE_TMP3"))
        )

        fsm.act("STATE_TMP3",
            NextValue(self.qspim_write, 1),
            NextValue(self.qspim_writedata, 0x9),
            NextValue(self.qspim_address, 0x7004),
            If(~self.qspim_waitrequest,
                NextState("STATE_TMP"),
                NextValue(self.can_counter, self.can_counter + 1)
            )
        )

        # The missing states
        # fsm.act("STATE_INIT_START_WART",
        #     NextValue(self.avalon_state, "STATE_INIT_START_WART"),
        #     If(self.app_buf_empty == 0,
        #         NextState("STATE_INIT_START_WART_TWO"),
        #         NextValue(self.app_buf_out_rden, 1)
        #     )
        # )

        # self.fsm.act("STATE_INIT_START_WART_TWO", NextValue(self.avalon_state, 0),
        #     NextValue(self.cannolo_ver, Cat(self.cannolo_ver[63:0], self.app_buf_out)),
        #     If(self.cannolo_ver == 96'h43414e4e454c4c4f4e497631,
        #         NextState("STATE_INIT_START_CANNACK_ONE")
        #     )
        # )

        # fsm.act("STATE_INIT_START_CANNACK_ONE",
        #     NextValue(self.avalon_state, "STATE_INIT_START_CANNACK_ONE"),
        #     NextValue(self.qspim_write, 1),
        #     NextValue(self.qspim_writedata, 0x43414e4e),
        #     NextValue(self.qspim_address, 0x7000),
        #     If(~self.qspim_waitrequest, NextState("STATE_INIT_START_CANNACK_TWO"))
        # )

        # fsm.act("STATE_INIT_START_CANNACK_TWO",
        #     NextValue(self.avalon_state, "STATE_INIT_START_CANNACK_TWO"),
        #     NextValue(self.qspim_write, 1),
        #     NextValue(self.qspim_writedata, 0x454c4c4f),
        #     NextValue(self.qspim_address, 0x7000),
        #     If(~self.qspim_waitrequest, NextState("STATE_INIT_START_CANNACK_THREE"))
        # )

        # fsm.act("STATE_INIT_START_CANNACK_THREE",
        #     NextValue(self.avalon_state, "STATE_INIT_START_CANNACK_THREE"),
        #     NextValue(self.qspim_write, 1),
        #     NextValue(self.qspim_writedata, 0x4e497631),
        #     NextValue(self.qspim_address, 0x7000),
        #     If(~self.qspim_waitrequest, NextState("STATE_INIT_START_CANNACK_FOUR"))
        # )

        # fsm.act("STATE_INIT_START_CANNACK_FOUR",
        #     NextValue(self.avalon_state, "STATE_INIT_START_CANNACK_FOUR"),
        #     NextValue(self.qspim_write, 1),
        #     NextValue(self.qspim_writedata, 0xc),
        #     NextValue(self.qspim_address, 0x7004),
        #     If(~self.qspim_waitrequest, NextState("STATE_TST_GO"))
        # )
        

# **Main function to generate Verilog**
if __name__ == "__main__":
    from migen.fhdl import verilog
    from migen.fhdl.verilog import convert
    
    # Instantiate the module
    can_app_dek_ctrl = canappdek_ctrl()

    # verilog_code = verilog.convert(can_app_dek_ctrl, {
    #     can_app_dek_ctrl.rst,
    #     can_app_dek_ctrl.clk,
    #     can_app_dek_ctrl.tcp_link_status,
    #     can_app_dek_ctrl.app_buf_wren,
    #     can_app_dek_ctrl.app_buf_datwr,
    #     can_app_dek_ctrl.qspim_readdata_i,
    #     can_app_dek_ctrl.qspim_waitrequest,
    #     can_app_dek_ctrl.qspim_readdatavalid,
    #     can_app_dek_ctrl.gpio_int,
    #     can_app_dek_ctrl.app_empty_num,
    #     can_app_dek_ctrl.qspim_address,
    #     can_app_dek_ctrl.qspim_read,
    #     can_app_dek_ctrl.qspim_write,
    #     can_app_dek_ctrl.qspim_writedata_o,
    #     can_app_dek_ctrl.buffer_size,
    #     can_app_dek_ctrl.test_ro
    # })
    
    # print(verilog_code)

    convert(can_app_dek_ctrl, ios={can_app_dek_ctrl.rst,
        #can_app_dek_ctrl.clk,
        can_app_dek_ctrl.tcp_link_status,
        can_app_dek_ctrl.app_buf_wren,
        can_app_dek_ctrl.app_buf_datwr,
        can_app_dek_ctrl.qspim_readdata_i,
        can_app_dek_ctrl.qspim_waitrequest,
        can_app_dek_ctrl.qspim_readdatavalid,
        can_app_dek_ctrl.gpio_int,
        can_app_dek_ctrl.app_empty_num,
        can_app_dek_ctrl.qspim_address,
        can_app_dek_ctrl.qspim_read,
        can_app_dek_ctrl.qspim_write,
        can_app_dek_ctrl.qspim_writedata_o,
        can_app_dek_ctrl.buffer_size,
        can_app_dek_ctrl.test_ro}, name='can_app_dek_ctrl').write('can_app_dek_ctrl.v')

   