"""
Import questions from CSV or text file

CSV Format:
subject_code,level,question_text,option_a,option_b,option_c,option_d,correct_answer,explanation

Text Format Example:
---
SUBJECT: CSW351-AI
LEVEL: easy
QUESTION: What is AI?
A: Artificial Intelligence
B: Automatic Integration
C: Advanced Innovation
D: Analog Input
CORRECT: A
EXPLANATION: AI stands for Artificial Intelligence
---

Usage:
    python scripts/import_questions.py questions.csv
    or
    python scripts/import_questions.py questions.txt
"""

import os
import sys
import django
import csv

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_quiz_project.settings')
django.setup()

from apps.quiz_app.models import Subject, Question


def import_from_csv(filepath):
    """Import questions from CSV file"""
    print(f"\nImporting from CSV: {filepath}")
    
    imported = 0
    errors = 0
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    subject = Subject.objects.get(code=row['subject_code'])
                    
                    Question.objects.create(
                        subject=subject,
                        question_text=row['question_text'],
                        option_a=row['option_a'],
                        option_b=row['option_b'],
                        option_c=row['option_c'],
                        option_d=row['option_d'],
                        correct_answer=row['correct_answer'].upper(),
                        level=row['level'].lower(),
                        explanation=row.get('explanation', '')
                    )
                    imported += 1
                    print(f"✓ Imported: {row['question_text'][:60]}...")
                    
                except Exception as e:
                    errors += 1
                    print(f"✗ Error: {e}")
        
        print(f"\n✅ Imported {imported} questions, {errors} errors")
        
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
    except Exception as e:
        print(f"❌ Error: {e}")


def import_from_text(filepath):
    """Import questions from text file"""
    print(f"\nImporting from text file: {filepath}")
    
    imported = 0
    errors = 0
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by separator
        questions = content.split('---')
        
        for q_block in questions:
            if not q_block.strip():
                continue
            
            try:
                lines = [line.strip() for line in q_block.strip().split('\n') if line.strip()]
                
                data = {}
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().upper()
                        value = value.strip()
                        
                        if key == 'SUBJECT':
                            data['subject_code'] = value
                        elif key == 'LEVEL':
                            data['level'] = value.lower()
                        elif key == 'QUESTION':
                            data['question_text'] = value
                        elif key == 'A':
                            data['option_a'] = value
                        elif key == 'B':
                            data['option_b'] = value
                        elif key == 'C':
                            data['option_c'] = value
                        elif key == 'D':
                            data['option_d'] = value
                        elif key == 'CORRECT':
                            data['correct_answer'] = value.upper()
                        elif key == 'EXPLANATION':
                            data['explanation'] = value
                
                # Create question
                subject = Subject.objects.get(code=data['subject_code'])
                
                Question.objects.create(
                    subject=subject,
                    question_text=data['question_text'],
                    option_a=data['option_a'],
                    option_b=data['option_b'],
                    option_c=data['option_c'],
                    option_d=data['option_d'],
                    correct_answer=data['correct_answer'],
                    level=data['level'],
                    explanation=data.get('explanation', '')
                )
                imported += 1
                print(f"✓ Imported: {data['question_text'][:60]}...")
                
            except Exception as e:
                errors += 1
                print(f"✗ Error: {e}")
        
        print(f"\n✅ Imported {imported} questions, {errors} errors")
        
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
    except Exception as e:
        print(f"❌ Error: {e}")


def create_sample_csv():
    """Create a sample CSV file"""
    filename = 'sample_questions.csv'
    
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['subject_code', 'level', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'explanation'])
        writer.writerow(['CSW351-AI', 'easy', 'What is AI?', 'Artificial Intelligence', 'Automatic Integration', 'Advanced Innovation', 'Analog Input', 'A', 'AI stands for Artificial Intelligence'])
        writer.writerow(['INT353-MULTIMEDIA', 'medium', 'What is RGB?', 'Color model', 'Video format', 'Audio codec', 'File system', 'A', 'RGB is a color model'])
    
    print(f"✅ Created sample file: {filename}")


def create_sample_text():
    """Create a sample text file"""
    filename = 'sample_questions.txt'
    
    content = """---
SUBJECT: CSW351-AI
LEVEL: easy
QUESTION: What is AI?
A: Artificial Intelligence
B: Automatic Integration
C: Advanced Innovation
D: Analog Input
CORRECT: A
EXPLANATION: AI stands for Artificial Intelligence
---
SUBJECT: INT353-MULTIMEDIA
LEVEL: medium
QUESTION: What is RGB?
A: Color model
B: Video format
C: Audio codec
D: File system
CORRECT: A
EXPLANATION: RGB is a color model
---
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created sample file: {filename}")


def main():
    """Main function"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       📁 QUESTION IMPORTER                                   ║
║                                                                              ║
║  Import questions from CSV or text files                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python scripts/import_questions.py <filename.csv>")
        print("  python scripts/import_questions.py <filename.txt>")
        print("\nOr choose an option:")
        print("1. Create sample CSV file")
        print("2. Create sample text file")
        print("3. Import from file")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            create_sample_csv()
        elif choice == '2':
            create_sample_text()
        elif choice == '3':
            filepath = input("Enter file path: ").strip()
            if filepath.endswith('.csv'):
                import_from_csv(filepath)
            elif filepath.endswith('.txt'):
                import_from_text(filepath)
            else:
                print("❌ Unsupported file format! Use .csv or .txt")
    else:
        filepath = sys.argv[1]
        
        if filepath.endswith('.csv'):
            import_from_csv(filepath)
        elif filepath.endswith('.txt'):
            import_from_text(filepath)
        else:
            print("❌ Unsupported file format! Use .csv or .txt")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

