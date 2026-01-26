  addi x1, x0, 1
  addi x13, x0, 60
  addi x14, x0, 400
  addi x15, x0, 100
  addi x16, x0, 4
  addi x17, x0, 365
  addi x18, x0, 366
  mul x12, x13, x13
  addi x25, x0, 24
  mul x11, x12, x25
  mul x19, x17, x11
  mul x20, x18, x11
  addi x4, x0, 1970
  addi x5, x0, 1
  lw x2, x0, 28
1:
  rem x25, x4, x14
  beq x25, x0, "2f"
  rem x25, x4, x15
  beq x25, x0, "3f"
  rem x25, x4, x16
  beq x25, x0, "2f"
3:
  blt x2, x19, "4f"
  sub x2, x2, x19
  addi x4, x4, 1
  lw x4, x0, 8
  lw x2, x0, 4
  lw x1, x0, 0
  jal x0, "1b"
2:
  blt x2, x20, "5f"
  sub x2, x2, x20
  addi x4, x4, 1
  lw x4, x0, 8
  lw x2, x0, 4
  lw x1, x0, 0
  jal x0, "1b"
4:
  addi x29, x0, 31
  mul x30, x11, x29
  blt x2, x30, "6f"
  addi x5, x5, 1
  sub x2, x2, x30
  addi x29, x0, 28
  mul x30, x11, x29
  blt x2, x30, "6f"
  addi x5, x5, 1
  sub x2, x2, x30
  jal x0, "7f"
5:
  addi x29, x0, 31
  mul x30, x11, x29
  blt x2, x30, "6f"
  addi x5, x5, 1
  sub x2, x2, x30
  addi x29, x0, 29
  mul x30, x11, x29
  blt x2, x30, "6f"
  addi x5, x5, 1
  sub x2, x2, x30
7:
  addi x29, x0, 31
  mul x30, x11, x29
  blt x2, x30, "6f"
  addi x5, x5, 1
  sub x2, x2, x30
  addi x29, x0, 30
  mul x30, x11, x29
  blt x2, x30, "6f"
  addi x5, x5, 1
  sub x2, x2, x30
  addi x29, x0, 31
  mul x30, x11, x29
  blt x2, x30, "6f"
  addi x5, x5, 1
  sub x2, x2, x30
  addi x29, x0, 30
  mul x30, x11, x29
  blt x2, x30, "6f"
  addi x5, x5, 1
  sub x2, x2, x30
  addi x29, x0, 31
  mul x30, x11, x29
  blt x2, x30, "6f"
  addi x5, x5, 1
  sub x2, x2, x30
  addi x29, x0, 31
  mul x30, x11, x29
  blt x2, x30, "6f"
  addi x5, x5, 1
  sub x2, x2, x30
  addi x29, x0, 30
  mul x30, x11, x29
  blt x2, x30, "6f"
  addi x5, x5, 1
  sub x2, x2, x30
  addi x29, x0, 31
  mul x30, x11, x29
  blt x2, x30, "6f"
  addi x5, x5, 1
  sub x2, x2, x30
  addi x29, x0, 30
  mul x30, x11, x29
  blt x2, x30, "6f"
  addi x5, x5, 1
  sub x2, x2, x30
6:
  div x6, x2, x11
  rem x2, x2, x11
  div x7, x2, x12
  rem x2, x2, x12 
  div x8, x2, x13
  rem x9, x2, x13


  lw x6, x0, 4 
  lw x5, x0, 8
  lw x4, x0, 12
  lw x7, x0, 16
  lw x8, x0, 20
  lw x9, x0, 24
9:
  lw x1, x0, 0
  jal x0, "9b"
