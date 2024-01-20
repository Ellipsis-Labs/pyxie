# Pyxie

Pyxie (pronounced "pixie") is a simple CLI tool for viewing Solana program metadata.

By default, pyxie will use the mainnet-beta cluster and Phoenix V1

```
usage: pyxie [-h] [-u URL] [program_id]

positional arguments:
  program_id         Program ID of requested Solana Program, by default Phoenix V1 is requested

options:
  -h, --help         show this help message and exit
  -u URL, --url URL  RPC Endpoint
```

### Example:

```
$ pyxie TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA
+------------------------------------+---------------------------------------------+
|              Property              |                    Value                    |
+------------------------------------+---------------------------------------------+
|             Program ID             | TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA |
|            SOL Balance             |                   ◎0.9341                   |
|     Program Data account size      |                  130.94 KB                  |
|        Actual Program Size         |                  130.38 KB                  |
| Total number of eBPF instructions  |                    14124                    |
| Program entrypoint virtual address |                 0x10000f9d8                 |
+------------------------------------+---------------------------------------------+

Virtual Memory Layout of Program Data:
+--------------+---------------------------+--------------+
|   Section    |   Virtual Address Range   | Size (Bytes) |
+--------------+---------------------------+--------------+
|    .text     | 0x100000000 - 0x10001b960 |    112992    |
|   .rodata    | 0x10001b960 - 0x10001d227 |     6343     |
| .data.rel.ro | 0x10001d228 - 0x10001ddf8 |     3024     |
|   .dynamic   | 0x10001ddf8 - 0x10001dea8 |     176      |
|   .dynsym    | 0x10001dea8 - 0x10001dfb0 |     264      |
|   .dynstr    | 0x10001dfb0 - 0x10001e031 |     129      |
|   .rel.dyn   | 0x10001e038 - 0x100020818 |    10208     |
|  .shstrtab   | 0x100020818 - 0x100020860 |      72      |
+--------------+---------------------------+--------------+

System Call Frequencies:
+---------------------+-----------+
|     System Call     | Frequency |
+---------------------+-----------+
|        abort        |    113    |
|     sol_memcmp_     |     11    |
|       sol_log_      |     29    |
|     custom_panic    |     1     |
|     sol_memset_     |     1     |
| sol_set_return_data |     1     |
| sol_get_rent_sysvar |     1     |
|     sol_memcpy_     |     1     |
|     sol_memmove_    |     1     |
+---------------------+-----------+
```
