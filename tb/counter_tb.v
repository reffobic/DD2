module counter_tb;
    reg clk = 0;
    reg rst, load, en;
    reg [7:0] load_value;
    wire [7:0] count;

    counter #(.WIDTH(8)) dut (
        .clk(clk), .rst(rst), .load(load), .load_value(load_value), .en(en), .count(count)
    );

    always #5 clk = ~clk;

    initial begin
        $dumpfile("counter.vcd");
        $dumpvars(0, counter_tb);

        rst = 1; load = 0; en = 0; load_value = 0;
        #20;
        rst = 0;
        #10;

        load = 1;
        load_value = 8'd42;
        #10;
        load = 0;
        #30;

        $finish;
    end
endmodule
