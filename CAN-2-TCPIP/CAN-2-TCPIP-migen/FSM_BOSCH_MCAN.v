/* Machine-generated using Migen */
module FSM_BOSCH_MCAN(
	input interrupt,
	output reg [11:0] mcan_adr,
	input [31:0] mcan_wrdat,
	input [31:0] mcan_rddat,
	input mcan_wrdat_en,
	output reg mcan_rddat_en,
	output reg [15:0] canappfdk_adr_i,
	output reg [31:0] canappfdk_dat_i,
	output reg canappfdk_wr_en_i,
	output reg [15:0] reg_0,
	output reg [31:0] reg_1,
	input sys_clk,
	input sys_rst
);

reg [15:0] dummy_reg = 16'd0;
reg [2:0] fsm0 = 3'd0;
reg [2:0] fsm1;

// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on


// synthesis translate_off
reg dummy_d;
// synthesis translate_on
always @(*) begin
	mcan_adr <= 12'd0;
	mcan_rddat_en <= 1'd0;
	canappfdk_adr_i <= 16'd0;
	canappfdk_dat_i <= 32'd0;
	canappfdk_wr_en_i <= 1'd0;
	reg_0 <= 16'd0;
	reg_1 <= 32'd0;
	fsm1 <= 3'd0;
	fsm1 <= fsm0;
	case (fsm0)
		1'd1: begin
			mcan_adr <= 7'd80;
			mcan_rddat_en <= 1'd1;
			reg_0 <= 7'd80;
			reg_1 <= mcan_rddat;
			fsm1 <= 2'd2;
		end
		2'd2: begin
			canappfdk_adr_i <= 16'd36864;
			canappfdk_dat_i <= {7'd80, mcan_rddat[31:16]};
			canappfdk_wr_en_i <= 1'd1;
			fsm1 <= 3'd4;
		end
		2'd3: begin
			canappfdk_adr_i <= 16'd36864;
			canappfdk_dat_i <= {mcan_rddat[15:0], dummy_reg};
			canappfdk_wr_en_i <= 1'd1;
			fsm1 <= 3'd4;
		end
		3'd4: begin
			canappfdk_adr_i <= 16'd36868;
			canappfdk_dat_i <= 3'd6;
			canappfdk_wr_en_i <= 1'd1;
			fsm1 <= 1'd0;
		end
		default: begin
			if (interrupt) begin
				fsm1 <= 1'd1;
			end
		end
	endcase
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end

always @(posedge sys_clk) begin
	fsm0 <= fsm1;
	if (sys_rst) begin
		fsm0 <= 3'd0;
	end
end

endmodule
