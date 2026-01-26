    j "main"
test: 
    addi sp,sp,-16
    sw ra, 0(sp)
    addi a0, zero, 42
    lw ra, 0(sp)
    addi sp,sp,16
    ret
main:
    sw a0, 0(zero)
    call "test"
    sw a0, 0(zero)
    mov x21, 42
    mov x20, 0
1:
    addi x20, x20, 7
    bne x20, x21, "1b"
    lui s4, 5
    auipc x20, 0

    addi x20, x0, 42
    sw x20, 0(x0)
    lw x22, 0(x0)
    add x21, x22, x22
    addi x24, x0, 3
    sll x23, x20, x24
    slli x23, x20, 2
    sra x23, x20, x24