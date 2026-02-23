module mul_tb;
    reg [7:0] mc, mp;
    wire [15:0] p;

    // Instantiate the DUV 
    mul dut (.mc(mc), .mp(mp), .p(p));

    task check_mul(input [7:0] a, input [7:0] b);
        begin
            #1; // Wait for logic to settle [cite: 163]
            if (p !== a * b) begin
                $display("FAIL: %d * %d = %d (Expected %d)", a, b, p, a*b);
                $fatal(1); // Stop on error [cite: 153]
            end else begin
                $display("PASS: %d * %d = %d", a, b, p);
            end
        end
    endtask

    initial begin
        // Setup waveform dumping [cite: 74, 75]
        $dumpfile("mul.vcd");
        $dumpvars(0, mul_tb);

        // Self-checking stimulus [cite: Step 5.5]
        mc = 8'd14; mp = 8'd10;
        check_mul(8'd14, 8'd10);
        mc = 8'h0A; mp = 8'hF6;
        check_mul(8'h0A, 8'hF6);

        $finish;
    end
endmodule
