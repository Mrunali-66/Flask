import PyPDF2
import pyttsx3
from pathlib import Path

class PDFtoAudioConverter:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.setup_voice()
        
    def setup_voice(self):
        """Configure voice settings"""
        voices = self.engine.getProperty('voices')
        
        # Set voice (0 = male, 1 = female on most systems)
        self.engine.setProperty('voice', voices[1].id)
        
        # Set speech rate (default is 200)
        self.engine.setProperty('rate', 150)
        
        # Set volume (0.0 to 1.0)
        self.engine.setProperty('volume', 0.9)
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        try:
            print(f"📄 Opening PDF: {pdf_path}")
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                print(f"📖 Total pages: {total_pages}")
                
                text = ""
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    text += page_text + "\n"
                    print(f"✓ Extracted page {page_num + 1}/{total_pages}")
                
                return text.strip()
                
        except FileNotFoundError:
            print("❌ Error: PDF file not found!")
            return None
        except Exception as e:
            print(f"❌ Error extracting text: {str(e)}")
            return None
    
    def text_to_speech(self, text, output_filename):
        """Convert text to speech and save as audio file"""
        try:
            if not text:
                print("❌ No text to convert!")
                return False
            
            print(f"🎙️ Converting text to speech...")
            print(f"📝 Text length: {len(text)} characters")
            
            # Save to file
            self.engine.save_to_file(text, output_filename)
            self.engine.runAndWait()
            
            print(f"✅ Audio saved: {output_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error converting to speech: {str(e)}")
            return False
    
    def convert_pdf_to_audio(self, pdf_path, output_path=None):
        """Main conversion function"""
        print("=" * 50)
        print("PDF to Audiobook Converter (Offline)")
        print("=" * 50)
        
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        
        if not text:
            print("❌ Failed to extract text from PDF")
            return False
        
        # Generate output filename if not provided
        if not output_path:
            pdf_name = Path(pdf_path).stem
            output_path = f"{pdf_name}_audiobook.wav"
        
        # Convert to speech
        success = self.text_to_speech(text, output_path)
        
        if success:
            print(f"\n🎉 Success! Audiobook created: {output_path}")
        
        return success

def main():
    converter = PDFtoAudioConverter()
    
    # Example usage
    pdf_file = input("Enter PDF file path: ").strip()
    output_file = input("Enter output audio file name (press Enter for default): ").strip()
    
    if not output_file:
        output_file = None
    
    converter.convert_pdf_to_audio(pdf_file, output_file)

if __name__ == "__main__":
    main()