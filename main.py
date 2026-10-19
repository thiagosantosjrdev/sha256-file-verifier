from cryptography.hazmat.primitives.hashes import Hash, SHA256
from colorama import Fore, init
from hmac import compare_digest
from pathlib import Path
import argparse
import logging
import sys


logging.basicConfig(
    format="[%(levelname)s]:%(lineno)s > %(message)s"
)


def validate_file(file_path: Path) -> bool:
    """Check whether the path points to an existing file."""
    if not file_path.exists():
        logging.error("The specified path does not exist.")
        return False

    if not file_path.is_file():
        logging.error("The specified path is not a file.")
        return False

    return True


def hash_file(file_path: Path, chunk_size: int = 4096) -> str | None:
    """
    Calculate the SHA-256 hash of a file and return its
    hexadecimal digest.
    """
    if not validate_file(file_path):
        return None

    try:
        with open(file_path, "rb") as file:
            sha256: Hash = Hash(SHA256())

            while chunk := file.read(chunk_size):
                sha256.update(chunk)

        return sha256.finalize().hex()

    except PermissionError:
        logging.error("Permission denied while reading the file.")
        return None

    except OSError as error:
        logging.error("Error accessing the file: %s", error)
        return None


def verify(file_path: Path, expected_hash: str, chunk_size: int) -> int:
    """Verify a file against an expected SHA-256 hash."""
    if (
        len(expected_hash) != 64
        or any(c not in "0123456789abcdefABCDEF" for c in expected_hash)
    ):
        logging.error("Invalid SHA-256 hexadecimal hash.")
        return 1

    file_hash = hash_file(file_path, chunk_size)

    if file_hash is None:
        logging.error("Could not complete hash verification.")
        return 1

    if compare_digest(file_hash, expected_hash.lower()):
        print(f"{Fore.GREEN}File hash matches!{Fore.RESET}")
        return 0

    print(f"{Fore.RED}File hash does not match!{Fore.RESET}")
    return 2


def create(file_path: Path, chunk_size: int) -> int:
    """Generate and print a file's SHA-256 hash."""
    file_hash = hash_file(file_path, chunk_size)

    if file_hash is None:
        logging.error("Could not generate the file hash.")
        return 1

    print(file_hash)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="SHA-256 File Verifier",
        description="Generate and verify SHA-256 file hashes.",
        epilog="Created by thiagosantosjrdev",
    )

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "-cs", "--chunk-size",
        type=int,
        default=4096,
        help="Chunk size for reading the file in bytes (default: 4096)"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="Available commands",
        required=True,
    )

    parser_create = subparsers.add_parser(
        "create",
        parents=[parent_parser],
        help="Generate a file's SHA-256 hash",
    )
    parser_create.add_argument(
        "file",
        type=Path,
        help="Path to the file to hash",
    )

    parser_verify = subparsers.add_parser(
        "verify",
        parents=[parent_parser],
        help="Verify a file's SHA-256 hash",
    )
    parser_verify.add_argument(
        "file",
        type=Path,
        help="Path to the file to verify",
    )
    parser_verify.add_argument(
        "hash",
        type=str,
        help="Expected SHA-256 hexadecimal hash",
    )

    args = parser.parse_args()
    init()

    if args.command == "create":
        sys.exit(create(args.file, args.chunk_size))

    elif args.command == "verify":
        sys.exit(verify(args.file, args.hash, args.chunk_size))
