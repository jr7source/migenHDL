/* Machine-generated using Migen */
module top(
	input [1:0] s1,
	input [1:0] s2,
	output reg [3:0] counter,
	output reg [2:0] output_1,
	input sys_clk,
	input sys_rst
);

wire fsm_fsm0;
reg fsm_fsm1 = 1'd1;
wire fsm_fsm2;
reg fsm_fsm3 = 1'd0;
reg [1:0] moorestatemachine_fsm0 = 2'd0;
reg [1:0] moorestatemachine_fsm1;
reg [3:0] counter_lowernext0;
reg counter_lowernext1;
reg [2:0] output_lowernext2;
reg output_lowernext3;

// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign fsm_fsm2 = ((moorestatemachine_fsm0 == 1'd0) & (~(moorestatemachine_fsm1 == 1'd0)));
assign fsm_fsm0 = ((~(moorestatemachine_fsm0 == 1'd0)) & (moorestatemachine_fsm1 == 1'd0));

// synthesis translate_off
reg dummy_d;
// synthesis translate_on
always @(*) begin
	moorestatemachine_fsm1 <= 2'd0;
	counter_lowernext0 <= 4'd0;
	counter_lowernext1 <= 1'd0;
	output_lowernext2 <= 3'd0;
	output_lowernext3 <= 1'd0;
	moorestatemachine_fsm1 <= moorestatemachine_fsm0;
	case (moorestatemachine_fsm0)
		1'd1: begin
			if (s2) begin
				counter_lowernext0 <= (counter + 1'd1);
				counter_lowernext1 <= 1'd1;
			end
			if ((~s1)) begin
				moorestatemachine_fsm1 <= 1'd0;
			end else begin
				moorestatemachine_fsm1 <= 2'd2;
			end
		end
		2'd2: begin
			if (s2) begin
				counter_lowernext0 <= (counter + 1'd1);
				counter_lowernext1 <= 1'd1;
			end
			if ((counter == 5'd20)) begin
				output_lowernext2 <= 2'd2;
				output_lowernext3 <= 1'd1;
			end
			if (s1) begin
				moorestatemachine_fsm1 <= 1'd0;
			end else begin
				moorestatemachine_fsm1 <= 2'd3;
			end
		end
		2'd3: begin
			if (s1) begin
				counter_lowernext0 <= (counter + 1'd1);
				counter_lowernext1 <= 1'd1;
			end
			if ((~s1)) begin
				moorestatemachine_fsm1 <= 1'd0;
			end else begin
				if ((counter == 5'd23)) begin
					moorestatemachine_fsm1 <= 1'd0;
				end
			end
		end
		default: begin
			if ((counter == 5'd24)) begin
				counter_lowernext0 <= 1'd0;
				counter_lowernext1 <= 1'd1;
			end
			if (s2) begin
				counter_lowernext0 <= (counter + 1'd1);
				counter_lowernext1 <= 1'd1;
			end
			if (s1) begin
				moorestatemachine_fsm1 <= 1'd1;
			end else begin
				moorestatemachine_fsm1 <= 2'd2;
			end
		end
	endcase
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end

always @(posedge sys_clk) begin
	fsm_fsm1 <= fsm_fsm0;
	fsm_fsm3 <= fsm_fsm2;
	moorestatemachine_fsm0 <= moorestatemachine_fsm1;
	if (counter_lowernext1) begin
		counter <= counter_lowernext0;
	end
	if (output_lowernext3) begin
		output_1 <= output_lowernext2;
	end
	if (sys_rst) begin
		counter <= 4'd0;
		output_1 <= 3'd0;
		fsm_fsm1 <= 1'd1;
		fsm_fsm3 <= 1'd0;
		moorestatemachine_fsm0 <= 2'd0;
	end
end

endmodule
