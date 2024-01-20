import struct
from solana.rpc.api import Client
from solders.pubkey import Pubkey
import datetime
from elftools.elf.elffile import ELFFile
from prettytable import PrettyTable
import io
import argparse

def get_program_data_key(program_id, owner=Pubkey.from_string("BPFLoaderUpgradeab1e11111111111111111111111")):
    if isinstance(program_id, str):
        program_id = Pubkey.from_string(program_id)

    assert(isinstance(program_id, Pubkey))
    return Pubkey.find_program_address(
        [bytes(program_id)], owner
    )[0]

def get_size_str(size):
    if size > 1024 * 1024:
        size_str = f"{round(size / 1024 / 1024, 2)} MB"
    else:
        size_str = f"{round(size / 1024, 2)} KB"
    return size_str

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="RPC Endpoint", default="m")
    parser.add_argument("program_id", help="Program ID of requested Solana Program, by default Phoenix V1 is requested", nargs="?", default="PhoeNiXZ8ByJGLkxNfZRnkUfjvmuYqLR89jjFHGqdXY")

    args = parser.parse_args()
    url = args.url
    if url.lower() == "m" or url.lower() == "mainnet" or url.lower() == "mainnet-beta":
        url = "https://api.mainnet-beta.solana.com/"
    elif url.lower() == "d" or url.lower() == "devnet":
        url = "https://api.devnet.solana.com/"

    c = Client(url)
    program_key = Pubkey.from_string(args.program_id)
    program_account = c.get_account_info(program_key, "confirmed")


    upgradeable = program_account.value.owner == Pubkey.from_string("BPFLoaderUpgradeab1e11111111111111111111111")
    if not upgradeable:
        account = program_account
        program_bytes = account.value.data
    else:
        key = get_program_data_key(program_key)
        account = c.get_account_info(key, "confirmed")
        program_bytes = account.value.data[45:]

    file = io.BytesIO(program_bytes)
    elf = ELFFile(file)

    dynsyms = elf.get_section_by_name(".dynsym")
    text = elf.get_section_by_name(".text")

    program_start = text.header["sh_offset"]

    regions = []
    syscalls = {}
    for s in elf.iter_sections():
        if s.header["sh_type"] == "SHT_NULL":
            continue
        offset = s.header["sh_offset"] - program_start + 0x100000000
        section_len = s.header["sh_size"]
        regions.append((hex(offset), hex(offset + section_len), s.name))

        if s.name == ".dynamic":
            relocs = s.get_relocation_tables()["REL"]
            for r in relocs.iter_relocations():
                if r.entry["r_info_type"] == 10:
                    syscall = dynsyms.get_symbol(r.entry["r_info_sym"]).name
                    syscalls[syscall] = syscalls.get(syscall, 0) + 1

    program_size = int(regions[-1][1], 16) - 0x100000000 + program_start

    program_meta = PrettyTable()
    program_meta.field_names = ["Property", "Value"]
    program_meta.add_row(["Program ID", program_key])
    if upgradeable:
        program_meta.add_row(["Program Data address", key])
    program_meta.add_row(["SOL Balance", f"◎{round(account.value.lamports / 1e9, 4)}"])

    if upgradeable:
        last_deployed_slot = struct.unpack("<Q", account.value.data[4:12])[0]
        program_meta.add_row(["Last deployed slot", last_deployed_slot])
        try:
            deploy_time = c.get_block_time(last_deployed_slot).value
            # add the time zone string
            time = datetime.datetime.fromtimestamp(deploy_time).strftime("%Y-%m-%d %H:%M:%S") + " UTC"
            program_meta.add_row(["Last deployed time", time])
        except:
            pass
        if account.value.data[12] == 1:
            auth = Pubkey.from_bytes(account.value.data[13:45])
            program_meta.add_row(["Upgrade Authority", auth])
            on_curve = auth.is_on_curve()
            program_meta.add_row(["Upgradeable by Keypair", "Yes 👎" if on_curve else "No 👌"])
        else:
            program_meta.add_row(["Upgrade Authority", f"None (frozen) 👍"])


    size = len(account.value.data)
    program_size = int(regions[-1][1], 16) - 0x100000000 + program_start

    program_meta.add_row(
        [
            "Program Data account size",
            f"{get_size_str(size)}",
        ]
    )

    program_meta.add_row(
        ["Actual Program Size", f"{get_size_str(program_size)}"]
    )
    program_meta.add_row(
        ["Total number of eBPF instructions", f"{len(text.data()) // 8}"]
    )
    program_meta.add_row(
        ["Program entrypoint virtual address", f"{hex(0x100000000 + elf.header['e_entry'])}"]
    )

    vm = PrettyTable()
    vm.field_names = ["Section", "Virtual Address Range", "Size (Bytes)"]
    for s, e, n in regions:
        vm.add_row([n, f"{s} - {e}", int(e, 16) - int(s, 16)])

    sc = PrettyTable()
    sc.field_names = ["System Call", "Frequency"]
    for k, v in syscalls.items():
        sc.add_row([k, v])

    print(program_meta)
    print()
    print("Virtual Memory Layout of Program Data:")
    print(vm)
    print()
    print("System Call Frequencies:")
    print(sc)

if __name__ == "__main__":
    main()
