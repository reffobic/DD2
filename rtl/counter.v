module counter #(
    parameter WIDTH = 8
)(
    input wire clk,
    input wire rst,       
    input wire load,     
    input wire [WIDTH-1:0] load_value, 
    input wire en,
    output reg [WIDTH-1:0] count
);

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            count <= {WIDTH{1'b0}}; 
        end else if (load) begin
            count <= load_value;    
        end else if (en) begin
            count <= count + 1'b1;   
        end
    end
endmodule
