from typing import List, Optional, Tuple
import matplotlib.pyplot as plt

NoteEvent = Tuple[float, float, int, float, Optional[List[int]]]

def save_piano_roll(note_events: List[NoteEvent], output_path: str) -> None:
    """Save a simple piano roll visualization as a png file."""
    if not note_events:
        raise ValueError("node_events is empty, cannot draw piano roll.")
    
    plt.figure(figsize=(12, 6))

    for start_time, end_time, pitch_midi, amplitude, pitch_bend in note_events:
        plt.hlines(
            y=pitch_midi,
            xmin=start_time,
            xmax=end_time,
            linewidth=2,
        )


    plt.xlabel("Time(s)")
    plt.ylabel("MIDI Pitch")
    plt.title("Piano Roll")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.savefig(output_path, dpi=200)
    plt.close()