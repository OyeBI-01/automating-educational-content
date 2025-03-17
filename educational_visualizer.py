import os
import json
import argparse
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import OpenAI for LLM functionality
from openai import OpenAI

# Import our image generator
from image_generator import ImageGenerator

# Configuration
MODEL_NAME = "gpt-3.5-turbo"  # Changed to a more widely available model

class EducationalVisualizer:
    def __init__(self, api_key: str = None):
        """
        Initialize the Educational Visualizer.
        
        Args:
            api_key: OpenAI API key for LLM and image generation
        """
        self.api_key = api_key or os.environ.get("OPEN_AI_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set it as an environment variable or pass it as a parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.image_generator = ImageGenerator(api_key=self.api_key)
    
    def process_script(self, script_content: str, output_dir: str = None) -> Dict[str, Any]:
        """
        Process an educational script and generate visual prompts.
        
        Args:
            script_content: The content of the educational script
            output_dir: Directory to save generated images to (optional)
            
        Returns:
            A dictionary containing the processed script, key concepts, and visual prompts
        """
        print("Step 1: Analyzing the script...")
        # Step 1: Understanding the Script
        analysis_result = self._analyze_script(script_content)
        
        print("Step 2: Generating visual prompts...")
        # Step 2: Generating Visual Prompts
        visual_prompts = self._generate_visual_prompts(analysis_result)
        
        print("Step 3: Generating visuals...")
        # Step 3: Generate visuals
        visualized_script = self._generate_visuals(script_content, visual_prompts, output_dir)
        
        print("Step 4: Quality control...")
        # Step 4: Quality Control
        final_output = self._quality_control(visualized_script)
        
        return final_output
    
    def _analyze_script(self, script_content: str) -> Dict[str, Any]:
        """
        Analyze the script to identify key concepts, examples, and sections for visualization.
        
        Args:
            script_content: The educational script content
            
        Returns:
            Dictionary containing key concepts, examples, keywords, and sections for visualization
        """
        # Use LLM to extract key concepts and identify visualization opportunities
        system_message = """
        You are an AI assistant specialized in educational content analysis.
        Your task is to analyze the educational script and extract:
        1. Key concepts that need visualization
        2. Examples and scenarios that can benefit from visual representation
        3. Keywords related to objects, actions, or relationships that can be illustrated
        4. Sections that would benefit from visual aids like diagrams, flowcharts, or animations
        
        Return your response as a JSON object with these keys:
        - key_concepts: array of strings
        - examples: array of strings
        - keywords: array of strings
        - visualization_sections: array of strings
        
        Make sure your response can be parsed as valid JSON.
        """
        
        try:
            # Remove response_format parameter as it's not supported by all models
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": script_content}
                ]
            )
            
            # Parse the JSON from the text response
            try:
                analysis = json.loads(response.choices[0].message.content)
                return analysis
            except json.JSONDecodeError:
                # If not valid JSON, try to extract structured data with basic parsing
                print("Warning: Response was not valid JSON. Attempting to extract data.")
                content = response.choices[0].message.content
                return {
                    "key_concepts": self._extract_list_items(content, "Key concepts"),
                    "examples": self._extract_list_items(content, "Examples"),
                    "keywords": self._extract_list_items(content, "Keywords"),
                    "visualization_sections": self._extract_list_items(content, "Sections")
                }
        except Exception as e:
            print(f"Error during script analysis: {e}")
            return {
                "key_concepts": [],
                "examples": [],
                "keywords": [],
                "visualization_sections": []
            }
    
    def _extract_list_items(self, text, section_name):
        """Extract list items from a text section."""
        try:
            # Very basic extraction - this could be improved
            lines = text.split('\n')
            items = []
            in_section = False
            
            for line in lines:
                if section_name in line:
                    in_section = True
                    continue
                elif in_section and line.strip() and any(section in line for section in ["Key concepts", "Examples", "Keywords", "Sections"]) and not section_name in line:
                    in_section = False
                elif in_section and line.strip().startswith("- "):
                    items.append(line.strip()[2:])
                
            return items
        except:
            return []
    
    def _generate_visual_prompts(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate structured prompts for image generation based on the script analysis.
        
        Args:
            analysis: The script analysis containing key concepts, examples, etc.
            
        Returns:
            List of visual prompts with metadata
        """
        system_message = """
        You are an AI assistant specialized in creating image generation prompts.
        Your task is to convert educational concepts into detailed prompts for image generation.
        
        IMPORTANT: Do NOT include any text or labels in the image prompts. The AI image generator struggles with rendering readable text.
        Instead, focus on clear visuals that can be labeled separately after generation.
        
        For each concept, create a prompt that includes:
        1. A detailed description of what should be visualized (WITHOUT text labels or equations)
        2. Style preferences (e.g., "Minimalist vector graphic", "Realistic 3D model")
        3. For animated concepts, describe the sequence of actions
        
        Return your response as a JSON array with objects containing:
        - "concept": The original concept
        - "prompt": The image generation prompt (Remember: NO text in the images)
        - "type": Either "static" or "animated"
        - "position": Where this should appear in the script (description)
        - "style": The visual style to use
        
        Make sure your response can be parsed as valid JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": json.dumps(analysis)}
                ]
            )
            
            try:
                content = response.choices[0].message.content
                # Try to parse as JSON
                prompts_data = json.loads(content)
                # Check if the response is directly an array
                if isinstance(prompts_data, list):
                    return prompts_data
                # Otherwise look for a "prompts" key
                return prompts_data.get("prompts", [])
            except json.JSONDecodeError:
                print("Warning: Response was not valid JSON. Extracting data from text.")
                # Simple fallback extraction logic
                content = response.choices[0].message.content
                # Try to extract JSON array from the content (may be surrounded by text)
                import re
                json_match = re.search(r'\[\s*{.*}\s*\]', content, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group(0))
                    except:
                        pass
                
                # If all else fails, return empty list
                return []
        except Exception as e:
            print(f"Error during prompt generation: {e}")
            return []
    
    def _generate_visuals(self, script_content: str, prompts: List[Dict[str, Any]], output_dir: str = None) -> Dict[str, Any]:
        """
        Generate visuals using the prompts and integrate them with the script.
        
        Args:
            script_content: The original script content
            prompts: List of visual prompts
            output_dir: Directory to save generated images to (optional)
            
        Returns:
            Dictionary containing the script with visual placeholders and metadata
        """
        results = {
            "original_script": script_content,
            "visualized_script": script_content,
            "generated_visuals": []
        }
        
        # Prepare prompts for image generation
        image_prompts = []
        for i, prompt_data in enumerate(prompts):
            # Create a unique ID for the visual
            visual_id = f"visual_{i+1}"
            
            # Create a formatted prompt for DALL-E
            image_prompt = {
                "id": visual_id,
                "prompt": prompt_data["prompt"],
                "size": "1024x1024",  # Default size
                "quality": "standard"  # Default quality
            }
            
            image_prompts.append(image_prompt)
        
        # Generate images if there are any prompts
        if image_prompts:
            print(f"Generating {len(image_prompts)} images...")
            image_results = self.image_generator.generate_multiple(image_prompts, output_dir)
            
            # Process the results and update the script
            for i, (prompt_data, image_result) in enumerate(zip(prompts, image_results)):
                visual_id = image_result["id"]
                
                # Add metadata to the results
                visual_metadata = {
                    "id": visual_id,
                    "concept": prompt_data["concept"],
                    "prompt": prompt_data["prompt"],
                    "type": prompt_data["type"],
                    "url": image_result.get("url"),
                    "local_path": image_result.get("local_path"),
                    "position": prompt_data["position"],
                    "success": image_result.get("success", False)
                }
                
                # Add a placeholder in the script
                if prompt_data.get("position"):
                    # Create a descriptive placeholder that will be replaced in the final output
                    image_path = image_result.get("local_path", "")
                    relative_path = os.path.relpath(image_path, os.getcwd()) if image_path else ""
                    
                    placeholder = f"\n\n[VISUAL: {visual_id} - {prompt_data['concept']}]"
                    if relative_path:
                        placeholder += f"\n[Image: {relative_path}]\n\n"
                    else:
                        placeholder += "\n\n"
                    
                    results["visualized_script"] = results["visualized_script"].replace(
                        prompt_data["position"], 
                        f"{prompt_data['position']}{placeholder}"
                    )
                
                results["generated_visuals"].append(visual_metadata)
        
        return results
    
    def _quality_control(self, visualized_script: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the generated visuals and provide refinement suggestions.
        
        Args:
            visualized_script: The script with integrated visuals
            
        Returns:
            The final output with quality assessment and refinement suggestions
        """
        system_message = """
        You are an AI assistant specialized in educational content quality assessment.
        Review the visualized educational content and provide:
        1. An assessment of how well the visuals support the learning objectives
        2. Suggestions for refinements or improvements
        3. Any missing concepts that should be visualized
        
        Return your response as a JSON object with these keys:
        - assessment: string with your overall assessment
        - refinement_suggestions: array of strings with suggestions
        - missing_concepts: array of strings with concepts that should be visualized
        
        Make sure your response can be parsed as valid JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": json.dumps(visualized_script)}
                ]
            )
            
            try:
                quality_assessment = json.loads(response.choices[0].message.content)
                visualized_script["quality_assessment"] = quality_assessment
                visualized_script["refinement_suggestions"] = quality_assessment.get("refinement_suggestions", [])
                return visualized_script
            except json.JSONDecodeError:
                print("Warning: Quality control response was not valid JSON.")
                content = response.choices[0].message.content
                # Fallback to basic text analysis
                visualized_script["quality_assessment"] = {"assessment": content}
                visualized_script["refinement_suggestions"] = []
                return visualized_script
        except Exception as e:
            print(f"Error during quality control: {e}")
            visualized_script["quality_assessment"] = {"error": str(e)}
            visualized_script["refinement_suggestions"] = []
            return visualized_script

def main():
    parser = argparse.ArgumentParser(description="Educational Content Visualizer")
    parser.add_argument("--script", required=True, help="Path to the educational script file")
    parser.add_argument("--output", required=True, help="Path to save the output JSON")
    parser.add_argument("--images", help="Directory to save generated images to")
    parser.add_argument("--api-key", help="OpenAI API key")
    
    args = parser.parse_args()
    
    # Read the script file
    with open(args.script, 'r', encoding='utf-8') as f:
        script_content = f.read()
    
    # Process the script
    visualizer = EducationalVisualizer(api_key=args.api_key)
    result = visualizer.process_script(script_content, output_dir=args.images)
    
    # Save the output
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    
    print(f"Visualization completed. Output saved to {args.output}")
    if args.images:
        print(f"Generated images saved to {args.images}")

if __name__ == "__main__":
    main() 