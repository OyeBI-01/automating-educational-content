# Educational Content Visualizer

A tool that automatically analyzes educational scripts and generates relevant visual assets to enhance learning comprehension.

## Overview

This system processes educational content through four key steps:

1. **Script Analysis**: Extracts key concepts, examples, and sections that would benefit from visualization
2. **Visual Prompt Generation**: Creates detailed prompts for image generation based on the analysis
3. **Visual Generation**: Uses OpenAI's DALL-E to generate appropriate visual assets
4. **Quality Control**: Validates the generated visuals and provides refinement suggestions

## Requirements

- Python 3.7 or higher
- OpenAI API key with access to GPT-4 and DALL-E API

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/educational-visualizer.git
   cd educational-visualizer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:

   **Option 1:** Create a `.env` file (recommended)
   ```
   # Copy the example .env file
   cp .env.example .env
   
   # Edit the .env file and replace 'your_openai_api_key_here' with your actual API key
   ```

   **Option 2:** Set environment variable
   ```
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   For Windows:
   ```
   set OPENAI_API_KEY=your-api-key-here
   ```

   **Option 3:** Pass it directly when running the script
   ```
   python educational_visualizer.py --script path/to/script.txt --output output.json --api-key your-api-key-here
   ```

## Usage

### Basic Usage

```
python educational_visualizer.py --script path/to/script.txt --output output.json --images images/
```

### Arguments

- `--script`: Path to the educational script file (required)
- `--output`: Path to save the output JSON (required)
- `--images`: Directory to save generated images to (optional)
- `--api-key`: OpenAI API key (optional, uses .env file or environment variable if not provided)

### Example

1. Create a sample educational script `sample_script.txt`:
   ```
   Understanding Binary Search
   
   Binary search is an efficient algorithm for finding a target value within a sorted array.
   
   How it works:
   1. Compare the target value to the middle element of the array.
   2. If the target value is equal to the middle element, return the middle element's index.
   3. If the target value is less than the middle element, repeat the search on the sub-array to the left.
   4. If the target value is greater than the middle element, repeat the search on the sub-array to the right.
   
   Binary search has a worst-case time complexity of O(log n), which makes it much faster than linear search for large datasets.
   ```

2. Run the visualizer:
   ```
   python educational_visualizer.py --script sample_script.txt --output visualized_script.json --images generated_images/
   ```

3. Examine the `visualized_script.json` output and the images in the `generated_images/` directory.

## Output Format

The system produces a JSON file with the following structure:

```json
{
  "original_script": "The original script content",
  "visualized_script": "Script with visual placeholders inserted",
  "generated_visuals": [
    {
      "id": "visual_1",
      "concept": "Binary Search Algorithm",
      "prompt": "A step-by-step visualization of binary search...",
      "type": "static",
      "url": "https://example.com/image_url.png",
      "local_path": "generated_images/visual_1.png",
      "position": "How it works:",
      "success": true
    }
  ],
  "quality_assessment": {
    "assessment": "The visuals effectively illustrate the key concepts...",
    "refinement_suggestions": [
      "Consider adding an animation for the binary search steps",
      "The comparison visualization could be more detailed"
    ]
  }
}
```

## Customization

You can modify the system behavior by editing the following:

- `educational_visualizer.py`: Main script with the visualization workflow
- `image_generator.py`: Handles image generation using OpenAI's API

## License

MIT 