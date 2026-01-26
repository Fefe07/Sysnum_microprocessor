  addi x6, x0, 1
  addi x7, x0, 60
  addi x8, x0, 1800
  add x8, x8, x8
  addi x9, x0, 24
  mul x10, x8, x9
  lw x2, x0, 8
1:
  lw x3, x0, 8
  beq x3, x2, "1f"
  rem x4, x3, x10
  addi x2, x3, 0
  div x5, x4, x8
  sw x5, x0, 4
  sw x6, x0, 0
  rem x4, x4, x8
  div x5, x4, x7
  sw x5, x0, 4
  sw x6, x0, 0
  rem x5, x4, x7
  sw x5, x0, 4
  sw x6, x0, 0
  jal x12, "1f"
