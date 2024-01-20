# pyxie

Simple Python CLI tool for viewing Solana program metadata

Usage: pyxie [OPTIONS] COMMAND [ARGS]...

Example:

```
# By default, pyxie will use the mainnet-beta cluster and Phoenix V1
$ pyxie

+------------------------------------+----------------------------------------------+
|              Property              |                    Value                     |
+------------------------------------+----------------------------------------------+
|             Program ID             | PhoeNiXZ8ByJGLkxNfZRnkUfjvmuYqLR89jjFHGqdXY  |
|        Program Data address        | 2myyNegEA6pjAHmmEsJC6JdYhW51gwxQW7ZCTWvwaKTk |
|            SOL Balance             |                   ◎34.8012                   |
|         Last deployed slot         |                  231433470                   |
|         Last deployed time         |           2023-11-21 16:12:23 UTC            |
|         Upgrade Authority          | 8mv7G3fJq5a5ej7E14vgcSGeQKH79emjU9fVfuhyitEq |
|       Upgradeable by Keypair       |                    No 👌                     |
|     Program Data account size      |                   4.77 MB                    |
|        Actual Program Size         |                   1.28 MB                    |
| Total number of eBPF instructions  |                    148777                    |
| Program entrypoint virtual address |                 0x10010a988                  |
+------------------------------------+----------------------------------------------+

Virtual Memory Layout of Program Data:
+--------------+---------------------------+--------------+
|   Section    |   Virtual Address Range   | Size (Bytes) |
+--------------+---------------------------+--------------+
|    .text     | 0x100000000 - 0x100122948 |   1190216    |
|   .rodata    | 0x100122950 - 0x10012636f |    14879     |
| .data.rel.ro | 0x100126370 - 0x10012a728 |    17336     |
|   .dynamic   | 0x10012a728 - 0x10012a7d8 |     176      |
|   .dynsym    | 0x10012a7d8 - 0x10012a970 |     408      |
|   .dynstr    | 0x10012a970 - 0x10012aa6c |     252      |
|   .rel.dyn   | 0x10012aa70 - 0x100148030 |    120256    |
|  .shstrtab   | 0x100148030 - 0x100148078 |      72      |
+--------------+---------------------------+--------------+

System Call Frequencies:
+------------------------------+-----------+
|         System Call          | Frequency |
+------------------------------+-----------+
|            abort             |    1770   |
|           sol_log_           |    303    |
|    sol_log_compute_units_    |     14    |
|         custom_panic         |     1     |
|         sol_memcmp_          |     1     |
|         sol_memset_          |     2     |
| sol_try_find_program_address |     1     |
|        sol_keccak256         |     1     |
|    sol_invoke_signed_rust    |     1     |
|     sol_set_return_data      |     1     |
|     sol_get_clock_sysvar     |     1     |
|     sol_get_rent_sysvar      |     1     |
|         sol_memcpy_          |     1     |
|         sol_memmove_         |     1     |
+------------------------------+-----------+
```
