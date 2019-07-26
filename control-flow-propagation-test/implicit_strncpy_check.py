from pintool import *
import struct
import triton

TAINTED_STR_ADDR = 0x4006c4 # This might have to be adjusted


ctx = getTritonContext()
ctx.setArchitecture(triton.ARCH.X86_64)
ctx.enableMode(triton.MODE.ALIGNED_MEMORY, True)

def taint_check_strncpy(threadId):
    print("taint_check_strncpy()")
    if ctx.isRegisterTainted(ctx.getRegister(triton.REG.X86_64.RDX)):
        print("[!] ALERT: strncpy - src tainted")
    else:
        print("[!] All _seems_ fine!")
    print
    


if __name__ == '__main__':
    startAnalysisFromSymbol('main')
    #startAnalysisFromEntry()
    ctx.taintMemory(TAINTED_STR_ADDR)

    #Add callbacks
    print("")
    print("Adding callbacks for strncpy")
    insertCall(taint_check_strncpy, INSERT_POINT.ROUTINE_ENTRY, 'strncpy_wrapper') # wrapper coz of pin bug

    print("runProgram()")
    runProgram()
