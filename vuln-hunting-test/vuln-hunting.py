from pintool import *
import struct
import triton

BLK_SIZE=8


ctx = getTritonContext()
ctx.setArchitecture(triton.ARCH.X86_64)
ctx.enableMode(triton.MODE.ALIGNED_MEMORY, True)
#ctx.enableMode(triton.MODE.TAINT_THROUGH_POINTERS, True)

def taint_check_strcpy(threadId):
    print("taint_check_strcpy()")
    print("@@: "+hex(ctx.getConcreteRegisterValue(ctx.getRegister(triton.REG.X86_64.RIP))))
    if ctx.isRegisterTainted(ctx.getRegister(triton.REG.X86_64.RSI)):
        print("[!]  ALERT: strcpy - src tainted")
    print

def taint_check_printf(threadId):
    #print("taint_check_printf()")
    #print("@@: "+hex(ctx.getConcreteRegisterValue(ctx.getRegister(triton.REG.X86_64.RIP))))
    if ctx.isRegisterTainted(ctx.getRegister(triton.REG.X86_64.RDI)):
        print("[!]  ALERT: printf - format string tainted")
    print
    
def taint_argv(threadId):
    argc = ctx.getConcreteRegisterValue(ctx.getRegister(triton.REG.X86_64.RDI))
    argv = ctx.getConcreteRegisterValue(ctx.getRegister(triton.REG.X86_64.RSI))

    if argc < 2:
        return;

    argv += 8; argc -= 1 # ignore argv[0]

    # Taint argv[:]
    argv_mem = triton.MemoryAccess(argv, argc*8)
    if ctx.taintMemory(argv_mem):
        print("[!]  TAINTED argv")

    # Taint argv[i][:]
    argv_bytes = ctx.getConcreteMemoryAreaValue(argv, argc*8)
    for i in xrange(argc):
        argv_i = struct.unpack("<Q", argv_bytes[i*8:(i+1)*8])[0]
        not_done = True
        offset = 0
        while not_done:
            argv_blk = str(ctx.getConcreteMemoryAreaValue(argv_i + offset, BLK_SIZE)).split(b'\x00')[0]
            argv_blk_len = len(argv_blk)
            if argv_blk_len != 0:
                offset += BLK_SIZE
            if argv_blk_len < BLK_SIZE:
               not_done = False
        argv_i_mem = triton.MemoryAccess(argv_i, offset)
        if ctx.taintMemory(argv_i_mem):
            print("[!]  TAINTED argv[" + str(i+1) +"]")
        print("")
	


if __name__ == '__main__':
    startAnalysisFromSymbol('main')

    print("Adding callbacks ...")
    insertCall(taint_argv, INSERT_POINT.ROUTINE_ENTRY, 'main')
    insertCall(taint_check_strcpy, INSERT_POINT.ROUTINE_ENTRY, 'strcpy_wrapper')
    insertCall(taint_check_printf, INSERT_POINT.ROUTINE_ENTRY, 'printf')
    
    print("Starting DTA ...")
    runProgram()
