	global	_start

	section	.text
_start:	mov	rdi, 1		; taint RDI here
	xor	rdi, rdi
	mov	rax, 60		; taint check RDI here
	syscall
