/* Machine-generated using Migen */
module can_app_dek_ctrl(
	input rst,
	input tcp_link_status,
	input app_buf_wren,
	input [31:0] app_buf_datwr,
	input [31:0] qspim_readdata_i,
	input qspim_waitrequest,
	input qspim_readdatavalid,
	input gpio_int,
	output reg test_ro,
	input [15:0] app_empty_num,
	output reg [15:0] qspim_address,
	input qspim_read,
	output reg qspim_write,
	output [31:0] qspim_writedata_o,
	output [15:0] buffer_size,
	input sys_clk,
	input sys_rst
);

wire [31:0] qspim_readdata;
reg [31:0] qspim_writedata = 32'd0;
reg [12:0] counter = 13'd0;
reg app_buf_out_rden = 1'd0;
reg app_buf_empty = 1'd0;
reg [5:0] avalon_state = 6'd0;
reg [5:0] next_avalon_state = 6'd0;
reg [31:0] warten_counter = 32'd0;
reg [31:0] next_warten_counter = 32'd0;
reg [31:0] tst_counter = 32'd0;
reg [31:0] next_tst_counter = 32'd0;
reg [31:0] can_counter = 32'd0;
reg [31:0] next_can_counter = 32'd0;
reg [95:0] cannolo_ver = 96'd0;
reg [95:0] next_cannolo_ver = 96'd0;
reg test_r = 1'd0;
reg [2:0] fsm0 = 3'd0;
reg [2:0] fsm1;
reg [31:0] warten_counter_lowernext0;
reg warten_counter_lowernext1;
reg [31:0] tst_counter_lowernext2;
reg tst_counter_lowernext3;
reg [31:0] can_counter_lowernext4;
reg can_counter_lowernext5;
reg app_buf_out_rden_lowernext_lowernext0;
reg app_buf_out_rden_lowernext_lowernext1;
reg test_r_lowernext6;
reg test_r_lowernext7;
reg qspim_write_lowernext8;
reg qspim_write_lowernext9;
reg [31:0] qspim_writedata_lowernext10;
reg qspim_writedata_lowernext11;
reg [15:0] qspim_address_lowernext12;
reg qspim_address_lowernext13;

// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign buffer_size = {counter, 1'd0, 1'd0};
assign qspim_readdata = qspim_readdata_i;
assign qspim_writedata_o = qspim_writedata;

// synthesis translate_off
reg dummy_d;
// synthesis translate_on
always @(*) begin
	fsm1 <= 3'd0;
	warten_counter_lowernext0 <= 32'd0;
	warten_counter_lowernext1 <= 1'd0;
	tst_counter_lowernext2 <= 32'd0;
	tst_counter_lowernext3 <= 1'd0;
	can_counter_lowernext4 <= 32'd0;
	can_counter_lowernext5 <= 1'd0;
	app_buf_out_rden_lowernext_lowernext0 <= 1'd0;
	app_buf_out_rden_lowernext_lowernext1 <= 1'd0;
	test_r_lowernext6 <= 1'd0;
	test_r_lowernext7 <= 1'd0;
	qspim_write_lowernext8 <= 1'd0;
	qspim_write_lowernext9 <= 1'd0;
	qspim_writedata_lowernext10 <= 32'd0;
	qspim_writedata_lowernext11 <= 1'd0;
	qspim_address_lowernext12 <= 16'd0;
	qspim_address_lowernext13 <= 1'd0;
	fsm1 <= fsm0;
	case (fsm0)
		1'd1: begin
			if ((~app_buf_empty)) begin
				app_buf_out_rden_lowernext_lowernext0 <= 1'd1;
				app_buf_out_rden_lowernext_lowernext1 <= 1'd1;
				fsm1 <= 2'd2;
			end
		end
		2'd2: begin
			warten_counter_lowernext0 <= (warten_counter + 1'd1);
			warten_counter_lowernext1 <= 1'd1;
			tst_counter_lowernext2 <= (tst_counter + 1'd1);
			tst_counter_lowernext3 <= 1'd1;
			if ((~tcp_link_status)) begin
				fsm1 <= 1'd0;
			end else begin
				if ((warten_counter == 11'd1024)) begin
					warten_counter_lowernext0 <= 1'd0;
					warten_counter_lowernext1 <= 1'd1;
					fsm1 <= 2'd2;
				end
			end
			if ((~app_buf_empty)) begin
				app_buf_out_rden_lowernext_lowernext0 <= 1'd1;
				app_buf_out_rden_lowernext_lowernext1 <= 1'd1;
			end
		end
		2'd3: begin
			test_r_lowernext6 <= 1'd1;
			test_r_lowernext7 <= 1'd1;
			qspim_write_lowernext8 <= 1'd1;
			qspim_write_lowernext9 <= 1'd1;
			qspim_writedata_lowernext10 <= 2'd2;
			qspim_writedata_lowernext11 <= 1'd1;
			qspim_address_lowernext12 <= 15'd28672;
			qspim_address_lowernext13 <= 1'd1;
			if ((~qspim_waitrequest)) begin
				fsm1 <= 3'd4;
			end
		end
		3'd4: begin
			qspim_write_lowernext8 <= 1'd1;
			qspim_write_lowernext9 <= 1'd1;
			qspim_writedata_lowernext10 <= {tst_counter[23:0], 8'd4};
			qspim_writedata_lowernext11 <= 1'd1;
			qspim_address_lowernext12 <= 15'd28672;
			qspim_address_lowernext13 <= 1'd1;
			if ((~qspim_waitrequest)) begin
				fsm1 <= 3'd5;
			end
		end
		3'd5: begin
			qspim_write_lowernext8 <= 1'd1;
			qspim_write_lowernext9 <= 1'd1;
			qspim_writedata_lowernext10 <= {24'd0, tst_counter[7:0]};
			qspim_writedata_lowernext11 <= 1'd1;
			qspim_address_lowernext12 <= 15'd28672;
			qspim_address_lowernext13 <= 1'd1;
			if ((~qspim_waitrequest)) begin
				fsm1 <= 3'd6;
			end
		end
		3'd6: begin
			qspim_write_lowernext8 <= 1'd1;
			qspim_write_lowernext9 <= 1'd1;
			qspim_writedata_lowernext10 <= 4'd9;
			qspim_writedata_lowernext11 <= 1'd1;
			qspim_address_lowernext12 <= 15'd28676;
			qspim_address_lowernext13 <= 1'd1;
			if ((~qspim_waitrequest)) begin
				fsm1 <= 2'd2;
				can_counter_lowernext4 <= (can_counter + 1'd1);
				can_counter_lowernext5 <= 1'd1;
			end
		end
		default: begin
			warten_counter_lowernext0 <= 1'd0;
			warten_counter_lowernext1 <= 1'd1;
			tst_counter_lowernext2 <= 1'd0;
			tst_counter_lowernext3 <= 1'd1;
			can_counter_lowernext4 <= 1'd0;
			can_counter_lowernext5 <= 1'd1;
			if (tcp_link_status) begin
				fsm1 <= 1'd1;
			end
		end
	endcase
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end

always @(posedge sys_clk) begin
	if ((rst == 1'd0)) begin
		warten_counter <= 1'd0;
		tst_counter <= 1'd0;
		can_counter <= 1'd0;
		cannolo_ver <= 1'd0;
		test_ro <= 1'd0;
	end else begin
		avalon_state <= next_avalon_state;
		warten_counter <= next_warten_counter;
		tst_counter <= next_tst_counter;
		can_counter <= next_can_counter;
		cannolo_ver <= next_cannolo_ver;
		test_ro <= test_r;
	end
	fsm0 <= fsm1;
	if (warten_counter_lowernext1) begin
		warten_counter <= warten_counter_lowernext0;
	end
	if (tst_counter_lowernext3) begin
		tst_counter <= tst_counter_lowernext2;
	end
	if (can_counter_lowernext5) begin
		can_counter <= can_counter_lowernext4;
	end
	if (app_buf_out_rden_lowernext_lowernext1) begin
		app_buf_out_rden <= app_buf_out_rden_lowernext_lowernext0;
	end
	if (test_r_lowernext7) begin
		test_r <= test_r_lowernext6;
	end
	if (qspim_write_lowernext9) begin
		qspim_write <= qspim_write_lowernext8;
	end
	if (qspim_writedata_lowernext11) begin
		qspim_writedata <= qspim_writedata_lowernext10;
	end
	if (qspim_address_lowernext13) begin
		qspim_address <= qspim_address_lowernext12;
	end
	if (sys_rst) begin
		test_ro <= 1'd0;
		qspim_address <= 16'd0;
		qspim_write <= 1'd0;
		qspim_writedata <= 32'd0;
		app_buf_out_rden <= 1'd0;
		avalon_state <= 6'd0;
		warten_counter <= 32'd0;
		tst_counter <= 32'd0;
		can_counter <= 32'd0;
		cannolo_ver <= 96'd0;
		test_r <= 1'd0;
		fsm0 <= 3'd0;
	end
end

endmodule
