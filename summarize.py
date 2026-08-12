#!/usr/bin/env python3
"""Summarize a text file using Groq's fast inference API."""

import argparse
import os
import sys

from dotenv import load_dotenv
from groq import Groq


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a text file with Groq.")
    parser.add_argument("file", help="Path to a .txt file to summarize")
    parser.add_argument(
        "--model",
        default="llama-3.1-8b-instant",
        help="Groq model name (default: llama-3.1-8b-instant)",
    )
    parser.add_argument(
        "--bullets", type=int, default=3, help="Number of summary bullet points"
    )
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not set. Copy .env.example to .env and fill it in.", file=sys.stderr)
        return 1

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"Error reading {args.file}: {e}", file=sys.stderr)
        return 1

    if not text.strip():
        print("Error: input file is empty.", file=sys.stderr)
        return 1

    client = Groq(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=[
                {
                    "role": "system",
                    "content": "You summarize text into concise, plain-language bullet points.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text in {args.bullets} bullet points:\n\n{text}",
                },
            ],
            max_tokens=500,
            temperature=0.3,
        )
    except Exception as e:
        print(f"Error calling Groq API: {e}", file=sys.stderr)
        return 1

    summary = response.choices[0].message.content
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
