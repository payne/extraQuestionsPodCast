#!/usr/bin/env python3
"""
Generate MP3 audio files from ham radio question pool JSON.

Groups questions by section (E0-E9, G1-G9, T1-T9) and creates one MP3 file
per section using Microsoft Edge Text-to-Speech.

Usage:
    python generate_mp3s.py <json_file> <output_dir>

Example:
    python generate_mp3s.py extra-2024-2028/extra-2024-2028.json mp3_output

Requirements:
    pip install edge-tts
"""

import argparse
import asyncio
import json
import os
import re
import sys
from collections import defaultdict

try:
    import edge_tts
except ImportError:
    print("Error: edge-tts not installed. Run: pip install edge-tts")
    sys.exit(1)


# Voice options - US English
VOICE = "en-US-GuyNeural"  # Clear male voice, good for technical content
# Alternatives:
# "en-US-JennyNeural" - female voice
# "en-US-AriaNeural" - female, natural
# "en-US-ChristopherNeural" - male, warm


def load_questions(json_path):
    """Load questions from a JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_section(question_id):
    """Extract section (E0-E9, G0-G9, T0-T9) from question ID like E1A01."""
    match = re.match(r'^([EGT]\d)', question_id)
    if match:
        return match.group(1)
    return None


def get_pool_name(question_id):
    """Get the pool name from question ID prefix."""
    if question_id.startswith('E'):
        return "Extra Class"
    elif question_id.startswith('G'):
        return "General Class"
    elif question_id.startswith('T'):
        return "Technician Class"
    return "Amateur Radio"


def group_by_section(questions):
    """Group questions by their section (E0-E9, G0-G9, T0-T9)."""
    sections = defaultdict(list)
    for q in questions:
        section = get_section(q['id'])
        if section:
            sections[section].append(q)
    return sections


def format_question_for_speech(question):
    """Format a question for text-to-speech output."""
    q_id = question['id']
    q_text = question['question']
    correct_letter = question.get('correct_letter', '')
    correct_idx = question['correct']
    correct_answer = question['answers'][correct_idx]

    # Build the speech text with clear pauses
    lines = [
        f"Question {q_id}.",
        q_text,
        f"Answer is ",
        correct_answer,
    ]
    return " ... ".join(lines)  # Ellipsis creates natural pauses


def generate_show_notes(section_name, questions, output_dir, pool_name):
    """Generate a text file with show notes (questions and answers)."""
    questions_sorted = sorted(questions, key=lambda q: q['id'])

    prefix = section_name[0].lower()
    notes_file = os.path.join(output_dir, f"{prefix}_{section_name.lower()}_notes.txt")

    with open(notes_file, 'w', encoding='utf-8') as f:
        f.write(f"Ham Radio {pool_name} Question Pool\n")
        f.write(f"Section {section_name} - {len(questions_sorted)} Questions\n")
        f.write("=" * 60 + "\n\n")

        for q in questions_sorted:
            q_id = q['id']
            q_text = q['question']
            correct_letter = q.get('correct_letter', '')
            correct_idx = q['correct']
            correct_answer = q['answers'][correct_idx]
            refs = q.get('refs', '')

            f.write(f"{q_id}\n")
            f.write(f"Q: {q_text}\n")
            f.write(f"A: ({correct_letter}) {correct_answer}\n")
            if refs:
                f.write(f"Ref: {refs}\n")
            f.write("\n")

    return notes_file


async def generate_section_mp3(section_name, questions, output_dir, pool_name, voice=VOICE):
    """Generate an MP3 file and show notes for a section of questions."""
    # Sort questions by ID within the section
    questions_sorted = sorted(questions, key=lambda q: q['id'])

    # Generate show notes text file
    notes_file = generate_show_notes(section_name, questions_sorted, output_dir, pool_name)

    # Build the full text for this section
    intro = f"Ham Radio {pool_name} Question Pool, Section {section_name}. "
    intro += f"This section contains {len(questions_sorted)} questions. "

    text_parts = [intro]
    for q in questions_sorted:
        text_parts.append(format_question_for_speech(q))

    full_text = " ... ".join(text_parts)

    # Generate the MP3
    prefix = section_name[0].lower()  # 'e', 'g', or 't'
    section_num = section_name[1]
    output_file = os.path.join(output_dir, f"{prefix}_{section_name.lower()}.mp3")

    print(f"  Generating {output_file} ({len(questions_sorted)} questions)...")

    communicate = edge_tts.Communicate(full_text, voice)
    await communicate.save(output_file)

    return output_file, notes_file


async def main_async(args):
    """Async main function."""
    # Load and group questions
    print(f"Loading questions from {args.json_file}...")
    questions = load_questions(args.json_file)
    print(f"Loaded {len(questions)} questions total")

    # Determine pool name from first question
    pool_name = get_pool_name(questions[0]['id']) if questions else "Amateur Radio"

    sections = group_by_section(questions)
    print(f"Found sections: {', '.join(sorted(sections.keys()))}")

    # Filter sections if specified
    if args.sections:
        selected = [s.strip().upper() for s in args.sections.split(',')]
        sections = {k: v for k, v in sections.items() if k in selected}
        if not sections:
            print(f"Error: No matching sections found for: {args.sections}")
            sys.exit(1)
        print(f"Generating only: {', '.join(sorted(sections.keys()))}")

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate MP3 for each section
    print(f"\nGenerating MP3 files using voice: {args.voice}")
    generated_files = []
    generated_notes = []
    for section_name in sorted(sections.keys()):
        output_file, notes_file = await generate_section_mp3(
            section_name,
            sections[section_name],
            args.output_dir,
            pool_name,
            args.voice
        )
        generated_files.append(output_file)
        generated_notes.append(notes_file)

    print(f"\nGenerated {len(generated_files)} MP3 files in {args.output_dir}/")
    for f in generated_files:
        size_mb = os.path.getsize(f) / (1024 * 1024)
        print(f"  {os.path.basename(f)}: {size_mb:.1f} MB")

    print(f"\nGenerated {len(generated_notes)} show notes files:")
    for f in generated_notes:
        print(f"  {os.path.basename(f)}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate MP3 files from ham radio question pool JSON'
    )
    parser.add_argument(
        'json_file',
        help='Path to the questions JSON file'
    )
    parser.add_argument(
        'output_dir',
        help='Directory to save MP3 files'
    )
    parser.add_argument(
        '--voice',
        default=VOICE,
        help=f'Voice to use (default: {VOICE}). Run "edge-tts --list-voices" for options'
    )
    parser.add_argument(
        '--sections',
        help='Comma-separated list of sections to generate (e.g., E1,E2,E3). Default: all'
    )

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.json_file):
        print(f"Error: JSON file not found: {args.json_file}")
        sys.exit(1)

    asyncio.run(main_async(args))


if __name__ == '__main__':
    main()
