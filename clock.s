  addi x1, x0, 0
  addi x2, x0, 0
  addi x3, x0, 0
  addi x4, x0, 60
  addi x5, x0, 1
boucle:
  sw x3, x0, 4
  sw x5, x0, 0
  sw x2, x0, 4
  sw x5, x0, 0
  sw x1, x0, 4
  sw x5, x0, 0
  addi x1, x1, 1
  bne x1, x4, -28
  addi x1, x0, 0
  addi x2, x2, 1
  bne x2, x4, -40
  addi x2, x0, 0
  addi x3, x3, 1
  j -52
