section .bss
buffer: resb 2048 ; A 2 KB byte buffer used for read
section .data
entero: dd 5
hFile: dd 0
hFileName: dd 0
readed: dd 0
buflen: dd 2048
saludo: db 'Bienvenidos a el compilador Z, por favor llame con el nombre de archivo *.z a parsear',0
saludoLen: dd 85
	section .text ; ; code goes here
	global main ; ;entry point
_start:
main:
	mov ecx, [esp+4]
	mov edx, [esp+8]
	mov eax, [edx+4]
	mov [hFileName], eax
		push DWORD [hFileName] ;open_r param 0
	call open_r
	add esp, 4 ;end open_r
	cmp eax, 0
	jge _false_140098311378592 ;jump to true, below must be jmp to false
			push DWORD [buflen] ;read param 0
			push DWORD buffer ;read param 1
			push DWORD [hFile] ;read param 2
		call read
		add esp, 12 ;end read
			nop
		_forstart_140098311377416:
			cmp eax, 0
			jne _forend_140098311377416 ;jump to true, below must be jmp to false
			mov [readed], eax
				push DWORD [readed] ;print param 0
				push DWORD buffer ;print param 1
			call print
			add esp, 8 ;end print
				push DWORD [buflen] ;read param 0
				push DWORD buffer ;read param 1
				push DWORD [hFile] ;read param 2
			call read
			add esp, 12 ;end read
			jmp _forstart_140098311377416
		_forend_140098311377416:
	jmp _end_140098311378592
	_false_140098311378592:
	_end_140098311378592:
	;exiting!
	mov eax, 1
	mov ebx, 0
	int 80h  ;byebyecruelworld
	

 ; pass
	 ; pass
	 ; eax != 0
