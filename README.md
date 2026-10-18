# SHA-256 File Verifier

A command-line tool written in Python to generate and verify SHA-256 hashes of files.

## Features

- Generate SHA-256 hashes of files.
- Verify file integrity using a reference hash.
- Read files in chunks to avoid loading the entire file into memory.
- Validate file paths and hash input.
- Handle file access errors.
- Colored terminal output using Colorama.

## Requirements

- Python 3.10+
- cryptography
- colorama

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd YOUR_REPOSITORY_FOLDER
```

Install the dependencies:

```bash
pip install cryptography colorama
```

## Usage

### Generate a hash

```bash
python main.py create path/to/file
```

### Verify a hash

```bash
python main.py verify path/to/file YOUR_SHA256_HASH
```

## How it works

The program reads the target file in chunks, updates a SHA-256 hash using the `cryptography` library, and returns the resulting hexadecimal digest.

During verification, the calculated digest is compared against the provided reference hash.

## Limitations

SHA-256 verifies whether a file matches a known hash. It does not independently establish whether a file is authentic or trustworthy.

## Author

thiagosantosjrdev