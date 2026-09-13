# Slovak Phone Number Generator

A simple Python command-line tool for generating possible Slovak mobile phone number combinations based on selected mobile network prefixes.

The program generates all six-digit combinations (`000000`–`999999`) for each selected area code and saves the results into a `.txt` file.

> **Note:** This project is intended for programming, learning and testing purposes. The generated numbers are combinations, not a list of confirmed active phone numbers.

## Features

* Generate numbers for specific Slovak mobile prefixes
* Generate numbers by mobile carrier
* Generate numbers for all supported prefixes
* Accept multiple carriers or prefixes at once
* Remove duplicate prefixes automatically
* Estimate required disk space before generation
* Check available disk space before starting
* Optional debug mode
* Uses only Python standard library modules

## Supported carriers

| Carrier          | Prefixes                                                                       |
| ---------------- | ------------------------------------------------------------------------------ |
| O2 Slovakia      | `0940`, `0944`, `0947`, `0948`, `0949`                                         |
| Orange Slovensko | `0905`, `0906`, `0907`, `0908`, `0915`, `0916`, `0917`, `0918`, `0919`, `0945` |
| Slovak Telekom   | `0901`, `0902`, `0903`, `0904`, `0909`, `0910`, `0911`, `0912`, `0914`         |
| 4ka              | `0950`, `0951`                                                                 |

The carrier groups also include prefixes associated with brands operating through the respective networks.

## Requirements

* Python 3.8 or newer
* No external Python packages are required

Check your Python version:

```bash
python3 --version
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Ricky-Real/slovak-phone-number-generator.git
```

Enter the project directory:

```bash
cd slovak-phone-number-generator
```

No additional dependencies need to be installed.

## Usage

The basic syntax is:

```bash
python3 slovak_phone_number_generator.py <area_codes>
```

### Generate numbers for a carrier

For example, generate numbers for 4ka:

```bash
python3 slovak_phone_number_generator.py 4ka
```

Generate numbers for Orange:

```bash
python3 slovak_phone_number_generator.py orange
```

### Generate numbers for multiple carriers

Multiple carriers can be separated with commas:

```bash
python3 slovak_phone_number_generator.py 4ka,telekom
```

The selected prefixes are combined automatically.

### Generate numbers for a specific prefix

You can also specify an exact four-digit prefix:

```bash
python3 slovak_phone_number_generator.py 0901
```

Multiple prefixes can be specified:

```bash
python3 slovak_phone_number_generator.py 0901,0915,0950
```

### Generate numbers for all supported prefixes

```bash
python3 slovak_phone_number_generator.py all
```

This generates combinations for every prefix in the `all_codes` list.

## Debug mode

Use `-d` or `--debug` to print every generated number to the terminal:

```bash
python3 slovak_phone_number_generator.py 4ka --debug
```

or:

```bash
python3 slovak_phone_number_generator.py 4ka -d
```

**Warning:** Debug mode is significantly slower because every generated number has to be printed to the terminal.

## Output

The generated numbers are saved to a `.txt` file.

For example:

```text
phone_numbers_4ka.txt
```

The output is grouped by prefix:

```text
0950

0950000000
0950000001
0950000002
...
0950999999

0951

0951000000
0951000001
0951000002
...
0951999999
```

Each prefix produces:

```text
1,000,000 numbers
```

because the last six digits range from:

```text
000000
```

to:

```text
999999
```

## Disk space estimation

Before generation starts, the program estimates the required disk space.

Each generated number consists of:

* 10 digits
* 1 newline character

Therefore, each number requires approximately:

```text
11 bytes
```

One prefix therefore requires approximately:

```text
1,000,000 × 11 bytes
≈ 11 MB
```

The program also adds a **10% safety margin** to the estimated size.

Before generating the numbers, it checks whether enough free disk space is available.

Example:

```text
Disk space check:
  Required:  11.54 MB
  Available:  120.35 GB
  OK: Enough disk space.
```

## How it works

The program follows these basic steps:

```text
1. Parse command-line arguments
        ↓
2. Determine selected carriers/prefixes
        ↓
3. Remove duplicate prefixes
        ↓
4. Estimate required disk space
        ↓
5. Check available disk space
        ↓
6. Generate six-digit combinations
        ↓
7. Save numbers to a TXT file
        ↓
8. Display generation statistics
```

For every selected prefix, the program generates:

```python
f"{area_code}{num:06d}"
```

For example:

```text
area_code = "0950"
num = 42
```

produces:

```text
0950000042
```

The `:06d` formatting ensures that the number always contains six digits.

## Performance

The generator processes numbers in chunks of 10,000 numbers instead of creating the entire output in memory at once.

This approach keeps memory usage relatively low while still allowing the program to write numbers efficiently using `writelines()`.

The program uses a single process and Python's standard libraries only.

## Limitations

* The program generates combinations; it does not determine whether a phone number is active.
* Generating all prefixes can produce a large output file.
* Debug mode can significantly reduce performance.
* The program currently uses a single CPU process.
* The list of prefixes is manually defined in the source code.

## License

The MIT License (MIT). Please see License File for more information.
