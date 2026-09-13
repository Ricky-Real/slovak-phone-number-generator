import argparse
import shutil
from time import time

#area_codes 
#"0940","0944","0947","0948","0949", # O2 Slovakia (includes Radosť a Tesco Mobile)
# "0905", "0906","0907","0908","0915","0916","0917","0918","0919","0945", #Orange Slovensko (includes Funfón)
# "0901", "0902","0903","0904","0909","0910","0911","0912","0914", #Slovak Telekom (includes Juro)
# "0950","0951") #4ka (includes SWAN)

o2_slovakia = [
    "0940", "0944", "0947", "0948", "0949"
]

orange = [
    "0905", "0906", "0907", "0908", "0915",
    "0916", "0917", "0918", "0919", "0945"
]

telekom = [
    "0901", "0902", "0903", "0904", "0909",
    "0910", "0911", "0912", "0914"
]

swan = [
    "0950", "0951"
]

all_codes = [
    "0901","0902","0903","0904","0905","0906","0907","0908","0909","0910","0911",
    "0912","0913","0914","0915","0916","0917","0918","0919","0920","0921","0922",
    "0923","0924","0925","0926","0927","0928","0929","0930","0931","0932","0933",
    "0934","0935","0936","0937","0938","0939","0940","0941","0942","0943","0944",
    "0945","0946","0947","0948","0949","0950","0951","0952","0953","0954","0955",
    "0956","0957","0958","0970","0971","0972","0973","0974","0975","0976","0977",
    "0978","0979","0980","0981","0982","0983","0984","0985","0986","0987","0988","0989"
]

CARRIERS = {
    "o2": o2_slovakia,
    "02": o2_slovakia,
    "orange": orange,
    "telekom": telekom,
    "4ka": swan,
}

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate Slovak phone number combinations."
    )

    parser.add_argument(
        "area_codes",
        help="Comma-separated carriers or area codes. Examples: 4ka,telekom | orange | 0901,0915 | all"
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Print every generated number. Warning: It is very slow"
    )

    return parser.parse_args()

def get_area_codes(user_input):
    selected_codes = []
    filename = "phone_numbers"

    inputs = user_input.split(",")

    for code in inputs:
        code = code.strip().lower()

        if code == "all":
            selected_codes = all_codes.copy()
            filename += "_all"
            break

        elif code in CARRIERS:
            selected_codes.extend(CARRIERS[code])
            filename += f"_{code}"

        elif len(code) == 4 and code.isdigit():
            selected_codes.append(code)
            filename += f"_{code}"

        else:
            raise ValueError(
                f"Unknown area code or carrier: '{code}'"
            )

    selected_codes = list(dict.fromkeys(selected_codes))

    return selected_codes, filename

def estimate_required_space(area_codes):
    """
    Estimate required disk space.

    Each area code generates: 1,000,000 numbers

    Each number is 10 digits + newline = 11 bytes.

    We add some extra space for safety.
    """

    numbers_per_code = 1_000_000
    bytes_per_number = 11

    base_size = (len(area_codes) * numbers_per_code * bytes_per_number)

    required = int(base_size * 1.10)

    return required

def format_bytes(size):
    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} PB"

def check_disk_space(required_space):
    """
    Check available disk space in the directory
    where the output file will be created.
    """

    directory = "."

    total, used, free = shutil.disk_usage(directory)

    print("\nDisk space check:")
    print(f"  Required:  {format_bytes(required_space)}")
    print(f"  Available: {format_bytes(free)}")

    if free < required_space:
        print("\nERROR: Not enough disk space.")
        print(f"Need approximately {format_bytes(required_space - free)} more free space.")
        return False

    print("  OK: Enough disk space.")
    return True

def generate_numbers(area_codes, filename, debug=False):
    start_time = time()

    print("\nStarting generation...")
    print(f"Output: {filename}.txt")
    print(f"Area codes: {', '.join(area_codes)}")
    print(f"Total area codes: {len(area_codes)}")
    print()

    numbers_per_code = 1_000_000
    nums_generated = 0

    with open(f"{filename}.txt", "w") as file:

        for area_code in area_codes:
            print(f"Generating numbers with area code: {area_code}")

            file.write(f"{area_code}\n\n")

            for start in range(0, numbers_per_code, 10_000):
                numbers = []

                for num in range(start, min(start + 10_000, numbers_per_code)):
                    number = f"{area_code}{num:06d}"
                    
                    numbers.append(f"{number}\n")
                    
                    if debug:
                        print(f"Current number: {number}")    

                file.writelines(numbers)
            file.write("\n")
                
            nums_generated += numbers_per_code

    elapsed = round(time() - start_time, 2)

    print("\nEverything done.")
    print(f"Saved to: {filename}.txt")
    print(f"Generated: {nums_generated:,} phone numbers")
    print(f"Took: {elapsed} seconds")

def main():
    args = parse_arguments()

    try:
        area_codes, filename = get_area_codes(args.area_codes)

    except ValueError as error:
        print(f"ERROR: {error}")
        return 1

    if not area_codes:
        print("ERROR: No area codes selected.")
        return 1

    required_space = estimate_required_space(area_codes)

    if not check_disk_space(required_space):
        return 1

    generate_numbers(area_codes, filename, debug=args.debug)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())