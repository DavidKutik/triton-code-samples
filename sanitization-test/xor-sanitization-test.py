#!/usr/bin/python2

import triton

BPATH="xor.elf"

ENTRYPOINT  = 0x0000000000401000
SOURCE      = 0x0000000000401005
SINK        = 0x0000000000401008


# Init Triton
ctx = triton.TritonContext()
ctx.setArchitecture(triton.ARCH.X86_64)
ctx.enableMode(triton.MODE.ALIGNED_MEMORY, True) # Symbolic optimization
ctx.setAstRepresentationMode(triton.AST_REPRESENTATION.PYTHON)

# Load segments into triton.
def loadBinary(path):
  import lief
  binary = lief.parse(path)
  phdrs  = binary.segments
  for phdr in phdrs:
    ctx.setConcreteMemoryAreaValue(phdr.virtual_address, phdr.content)
  return


loadBinary(BPATH)


pc = ENTRYPOINT
while(pc):
  oc = ctx.getConcreteMemoryAreaValue(pc, 16)

  inst = triton.Instruction()
  inst.setOpcode(oc)
  inst.setAddress(pc)

  ctx.processing(inst)


  if inst.getAddress() == SOURCE:
    ctx.taintRegister(ctx.getRegister(triton.REG.X86_64.RDI))
    print("[!] Tainting register rdi")



  if inst.getAddress() == SINK:
    print("[!] After instruction xor rdi, rdi")
    if ctx.isRegisterTainted(ctx.getRegister(triton.REG.X86_64.RDI)):
      print("[!]  Register rdi is still tainted")
    else:
      print("[!]  Register rdi was sanitized")

  pc = ctx.getConcreteRegisterValue(ctx.getRegister(triton.REG.X86_64.RIP))
