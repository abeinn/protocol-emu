`default_nettype none

module tt_um_abeinn_protocol_emu_uart #(
    parameter integer CLOCKS_PER_BIT = 434
) (
    input wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input wire ena,
    input wire clk,
    input wire rst_n
);
    localparam integer COUNT_WIDTH = (CLOCKS_PER_BIT > 1) ? $clog2(CLOCKS_PER_BIT) : 1;

    reg [COUNT_WIDTH-1:0] count;
    reg [9:0] frame;
    reg [3:0] bit_index;
    reg busy;
    reg send_previous;

    assign uo_out = {6'b0, busy, busy ? frame[0] : 1'b1};
    assign uio_out = 8'b0;
    assign uio_oe = 8'b0;

    always @(posedge clk) begin
        if (!rst_n) begin
            count <= 0;
            frame <= 10'b1111111111;
            bit_index <= 0;
            busy <= 0;
            send_previous <= 0;
        end else begin
            send_previous <= uio_in[0];
            if (!busy) begin
                if (ena && uio_in[0] && !send_previous) begin
                    frame <= {1'b1, ui_in, 1'b0};
                    count <= 0;
                    bit_index <= 0;
                    busy <= 1;
                end
            end else if (count == CLOCKS_PER_BIT - 1) begin
                count <= 0;
                if (bit_index == 9) begin
                    busy <= 0;
                end else begin
                    frame <= {1'b1, frame[9:1]};
                    bit_index <= bit_index + 1'b1;
                end
            end else begin
                count <= count + 1'b1;
            end
        end
    end

    wire _unused = &{uio_in[7:1], 1'b0};
endmodule
