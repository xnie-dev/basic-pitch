import json
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

PITCH_CLASS_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

NoteEvent = Tuple[float, float, int, float, Optional[List[int]]]


def summarize_note_events(note_events: List[NoteEvent]) -> Dict[str, Any]:
    if not note_events:
        return {
            "num_notes": 0,
            "note_event_span_seconds": 0.0,
            "pitch_range": {
                "min_midi": None,
                "max_midi": None,
            },
            "average_note_duration_seconds": 0.0,
            "total_note_duration_seconds": 0.0,
            "mean_amplitude": 0.0,
            "pitch_class_histogram": {name: 0 for name in PITCH_CLASS_NAMES},
            "notes_with_pitch_bends": 0,
        }

    starts = []
    ends = []
    pitches = []
    amplitudes = []
    durations = []
    pitch_class_counter = Counter()
    notes_with_pitch_bends = 0

    for start_time, end_time, pitch_midi, amplitude, pitch_bends in note_events:
        duration = end_time - start_time

        starts.append(float(start_time))
        ends.append(float(end_time))
        pitches.append(int(pitch_midi))
        amplitudes.append(float(amplitude))
        durations.append(float(duration))

        pitch_class_name = PITCH_CLASS_NAMES[int(pitch_midi) % 12]
        pitch_class_counter[pitch_class_name] += 1

        if pitch_bends:
            notes_with_pitch_bends += 1

    summary = {
        "num_notes": int(len(note_events)),
        "note_event_span_seconds": round(max(ends) - min(starts), 3),
        "pitch_range": {
            "min_midi": min(pitches),
            "max_midi": max(pitches),
        },
        "average_note_duration_seconds": round(sum(durations) / len(durations), 3),
        "total_note_duration_seconds": round(sum(durations), 3),
        "mean_amplitude": round(sum(amplitudes) / len(amplitudes), 3),
        "pitch_class_histogram": {
            name: int(pitch_class_counter.get(name, 0)) for name in PITCH_CLASS_NAMES
        },
        "notes_with_pitch_bends": int(notes_with_pitch_bends),
    }

    return summary


def save_summary_json(summary: Dict[str, Any], save_path: str) -> None:
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)


def print_summary(summary: Dict[str, Any]) -> None:
    print("===== Note Event Summary =====")
    print(f"num_notes: {summary['num_notes']}")
    print(f"note_event_span_seconds: {summary['note_event_span_seconds']:.3f}")

    pitch_range = summary["pitch_range"]
    print(f"pitch_range: {pitch_range['min_midi']} - {pitch_range['max_midi']}")

    print(f"average_note_duration_seconds: {summary['average_note_duration_seconds']:.3f}")
    print(f"total_note_duration_seconds: {summary['total_note_duration_seconds']:.3f}")
    print(f"mean_amplitude: {summary['mean_amplitude']:.3f}")
    print(f"notes_with_pitch_bends: {summary['notes_with_pitch_bends']}")

    print("pitch_class_histogram:")
    for pitch_class, count in summary["pitch_class_histogram"].items():
        print(f"  {pitch_class}: {count}")