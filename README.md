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

1. Create a sample educational script `sample.txt`:
   ```
   Bernoulli's Principle
   
   Bernoulli’s principle formulated by Daniel Bernoulli states that as the speed of a moving fluid increases (liquid or gas), the pressure within the fluid decreases. Although Bernoulli deduced the law, it was Leonhard Euler who derived Bernoulli’s equation in its usual form in the year 1752.
   What is Bernoulli’s Principle?
   Bernoulli’s principle states that
   The total mechanical energy of the moving fluid comprising the gravitational potential energy of elevation, the energy associated with the fluid pressure and the kinetic energy of the fluid motion, remains constant.
   Bernoulli’s principle can be derived from the principle of conservation of energy.
   Bernoulli’s Principle Formula
   Bernoulli’s equation formula is a relation between pressure, kinetic energy, and gravitational potential energy of a fluid in a container.
   The formula for Bernoulli’s principle is given as follows:
   p+12ρv2+ρgh=constant
   Where p is the pressure exerted by the fluid, v is the velocity of the fluid, ρ is the density of the fluid and h is the height of the container.
   Bernoulli’s equation gives great insight into the balance between pressure, velocity and elevation.
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
  "original_script": "Bernoulli\u2019s principle formulated by Daniel Bernoulli states that as the speed of a moving fluid increases (liquid or gas), the pressure within the fluid decreases. Although Bernoulli deduced the law, it was Leonhard Euler who derived Bernoulli\u2019s equation in its usual form in the year 1752.\nWhat is Bernoulli\u2019s Principle?\nBernoulli\u2019s principle states that\nThe total mechanical energy of the moving fluid comprising the gravitational potential energy of elevation, the energy associated with the fluid pressure and the kinetic energy of the fluid motion, remains constant.\nBernoulli\u2019s principle can be derived from the principle of conservation of energy.\nBernoulli\u2019s Principle Formula\nBernoulli\u2019s equation formula is a relation between pressure, kinetic energy, and gravitational potential energy of a fluid in a container.\nThe formula for Bernoulli\u2019s principle is given as follows:\np+12\u03c1v2+\u03c1gh=constant\nWhere p is the pressure exerted by the fluid, v is the velocity of the fluid, \u03c1 is the density of the fluid and h is the height of the container.\nBernoulli\u2019s equation gives great insight into the balance between pressure, velocity and elevation.\n",
  "visualized_script": "Bernoulli\u2019s principle formulated by Daniel Bernoulli states that as the speed of a moving fluid increases (liquid or gas), the pressure within the fluid decreases. Although Bernoulli deduced the law, it was Leonhard Euler who derived Bernoulli\u2019s equation in its usual form in the year 1752.\nWhat is Bernoulli\u2019s Principle?\nBernoulli\u2019s principle states that\nThe total mechanical energy of the moving fluid comprising the gravitational potential energy of elevation, the energy associated with the fluid pressure and the kinetic energy of the fluid motion, remains constant.\nBernoulli\u2019s principle can be derived from the principle of conservation of energy.\nBernoulli\u2019s Principle Formula\nBernoulli\u2019s equation formula is a relation between pressure, kinetic energy, and gravitational potential energy of a fluid in a container.\nThe formula for Bernoulli\u2019s principle is given as follows:\np+12\u03c1v2+\u03c1gh=constant\nWhere p is the pressure exerted by the fluid, v is the velocity of the fluid, \u03c1 is the density of the fluid and h is the height of the container.\nBernoulli\u2019s equation gives great insight into the balance between pressure, velocity and elevation.\n",
  "generated_visuals": [
    {
      "id": "visual_1",
      "concept": "Bernoulli's principle",
      "prompt": "Visualize a fluid flowing through a pipe where the velocity of the fluid increases, resulting in a decrease in pressure. Show how the total energy of the fluid (kinetic energy + potential energy + pressure energy) remains constant along the flow path.",
      "type": "static",
      "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-G6sAjMzO3wKwSinNzshEZ1gT/user-cPFTIO93uGfP24FTEZneTur7/img-wyB57CIiahWbZj8no6NWJv3O.png?st=2025-03-17T10%3A14%3A07Z&se=2025-03-17T12%3A14%3A07Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-03-16T15%3A51%3A36Z&ske=2025-03-17T15%3A51%3A36Z&sks=b&skv=2024-08-04&sig=DM9qMdMBYx5PqrM9O/U8IfG4sYiD4NCyrdB5yEG7pY0%3D",
      "local_path": "generated_images/visual_1.png",
      "position": "Bernoulli's principle explanation",
      "success": true
    },
    {
      "id": "visual_2",
      "concept": "total mechanical energy of a moving fluid",
      "prompt": "Create an illustration showing a moving fluid within a container. Highlight the different components of the fluid's total mechanical energy including kinetic energy, pressure energy, and gravitational potential energy. Emphasize the conservation of energy in the system.",
      "type": "static",
      "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-G6sAjMzO3wKwSinNzshEZ1gT/user-cPFTIO93uGfP24FTEZneTur7/img-MDSmoA8tSo0gQGNIy31WNZez.png?st=2025-03-17T10%3A14%3A24Z&se=2025-03-17T12%3A14%3A24Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-03-16T15%3A58%3A19Z&ske=2025-03-17T15%3A58%3A19Z&sks=b&skv=2024-08-04&sig=m8thRDqHdHmhjkd3PRvwQ5EOcUUKEgJL6J4lIA1jucQ%3D",
      "local_path": "generated_images/visual_2.png",
      "position": "Bernoulli's principle explanation",
      "success": true
    },
    {
      "id": "visual_3",
      "concept": "Bernoulli's equation",
      "prompt": "Visualize the derivation of Bernoulli's equation by considering a streamline flow of a fluid. Show how the sum of the dynamic pressure, pressure potential, and gravitational potential per unit mass along the streamline remains constant.",
      "type": "static",
      "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-G6sAjMzO3wKwSinNzshEZ1gT/user-cPFTIO93uGfP24FTEZneTur7/img-sfqEqlCQOc6LIOpmmanaa0oZ.png?st=2025-03-17T10%3A14%3A40Z&se=2025-03-17T12%3A14%3A40Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-03-16T17%3A46%3A30Z&ske=2025-03-17T17%3A46%3A30Z&sks=b&skv=2024-08-04&sig=bSVZ/PXm/3OrfFXdDe8rKM9hrW2RlDHI8HFqOxQ0j6I%3D",
      "local_path": "generated_images/visual_3.png",
      "position": "Derivation of Bernoulli's equation",
      "success": true
    },
    {
      "id": "visual_4",
      "concept": "pressure",
      "prompt": "Create an image showing how pressure changes in a fluid flow system. Illustrate high and low pressure areas within a pipe or around an object immersed in a fluid.",
      "type": "static",
      "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-G6sAjMzO3wKwSinNzshEZ1gT/user-cPFTIO93uGfP24FTEZneTur7/img-BZ9pxrLoDMkRoJVwKyLKzQm1.png?st=2025-03-17T10%3A14%3A53Z&se=2025-03-17T12%3A14%3A53Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-03-16T20%3A57%3A08Z&ske=2025-03-17T20%3A57%3A08Z&sks=b&skv=2024-08-04&sig=wEjyI2ma44CyuHGUyPcovvtQIVdCn5qc2zdoWTdppb0%3D",
      "local_path": "generated_images/visual_4.png",
      "position": "Interplay between pressure, velocity, and elevation",
      "success": true
    },
  "quality_assessment": {
    "assessment": "The visuals provided support the learning objectives well by illustrating key concepts related to Bernoulli's principle, total mechanical energy of a moving fluid, Bernoulli's equation, pressure, kinetic energy, and gravitational potential energy.",
    "refinement_suggestions": [],
    "missing_concepts": [
      "Visualization showing the application of Bernoulli's principle in different scenarios such as aerodynamics or hydraulics to enhance practical understanding."
    ]
  },
  "refinement_suggestions": []
}
```

## Customization

You can modify the system behavior by editing the following:

- `educational_visualizer.py`: Main script with the visualization workflow
- `image_generator.py`: Handles image generation using OpenAI's API

## License

MIT 
