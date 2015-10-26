section .bss
buffer: resb 2048 ; A 2 KB byte buffer used for read
section .data
entero: dd 5
hFile: dd 0
hFileName: dd 0
readed: dd 0
buflen: dd 2048
saludo: db 'Bienvenidos a el compilador Z, por favor llame con el nombre de archivo *.z a parsear',0
saludoLen: dd 89
	section .text ; ; code goes here
	global main ; ;entry point
_start:
main:
	 ; i had no time to set up a testcase so..
	nop
	inc ecx ;incdec ecx
	dec ecx ;incdec ecx
	 ; division (integer, signed, 32b)
mov ecx, 4
mov eax, [hFile] ;dividend
mov edx, 0 ;upper half of dividend
idiv dword ecx ;divide double register edx:eax by regc
	mov ecx, eax
	 ; simple math + asignment
mov edx, eax ;add op 1
add edx, 3 ;add op 2
	mov ecx, edx
mov eax, ebx ;sub op 1
sub eax, 2 ;sub op 2
	mov ecx, eax
	nop
	nop
	mov ecx, [esp+4]
	mov edx, [esp+8]
	mov eax, [edx+4]
	mov [hFileName], eax
mov rdi, [hFileName]
call open_r
	mov [hFile], rax
	cmp DWORD [hFile], 01
	jl _if_end_140062032041240 ;jump to false, below is 'true'
mov rdi, [buflen]
mov rsi, buffer
mov rdx, [hFile]
call read
		mov [readed], rax
			mov eax, 0
		_forstart_140062032043256:
			cmp DWORD [readed], 0
			jng _forend_140062032043256 ;jump to false, below is 'true'
			mov rdi, [readed]
			mov rsi, buffer
			call print
mov rdi, [buflen]
mov rsi, buffer
mov rdx, [hFile]
call read
			mov [readed], rax
			jmp _forstart_140062032043256
		_forend_140062032043256:
	_if_end_140062032041240:
	;exiting!
	mov eax, 1
	mov ebx, 0
	int 80h  ;byebyecruelworld
	

 ; now with 100% more comments
open_r:
	 ; open(char *path, int flags, mode_t mode) put filename in ebx. return is on eax
	mov ebx, [esp+4]
	mov eax, 5
	mov ecx, 0
	mov edx, 0
	syscall
	ret ;; end open_r

print:
	mov ecx, [esp+4]
	mov edx, [esp+8]
	mov eax, 4
	mov ebx, 1
	syscall
	ret ;; end print

read:
	 ; read(int fd, void *buf, size_t count);;fd=ebx, buf=ecx, len=edx; ret=eax
	mov ebx, [esp+4]
	mov ecx, [esp+8]
	mov edx, [esp+12]
	mov eax, 3
	syscall
	ret ;; end read

