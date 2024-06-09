## Exercise 1

From the `gdb` output, it seems that the program received a `SIGABRT` signal, indicating that the program called the `abort` function due to a critical error detected by the program itself. Specifically, the program aborts when two consecutive numeric characters are found in the input string where the second character is exactly one greater than the first.

## Exercise 2

The crash might be related to how the `interact()` method of the `Airplane` class processes the input. The crash in the `interact` method is caused by the explicit call to `abort()` when `crew.num` is 0 and the 'l' (land) command is issued. The `abort()` function is a standard library function that terminates the program and generates a core dump.
