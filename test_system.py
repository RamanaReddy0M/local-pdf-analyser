"""Test script for the PDF Resume Analyzer system."""

import subprocess
import sys
from pathlib import Path


def run_test_command(command: str, description: str) -> bool:
    """Run a test command and return success status."""
    print(f"\n🧪 Testing: {description}")
    print(f"Command: {command}")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=120
        )
        
        if result.returncode == 0:
            print("✅ SUCCESS")
            if result.stdout:
                print("Output:")
                print(result.stdout[-500:])  # Show last 500 chars
            return True
        else:
            print("❌ FAILED")
            print("Error:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT - Command took too long")
        return False
    except Exception as e:
        print(f"💥 EXCEPTION: {e}")
        return False


def main():
    """Run comprehensive system tests."""
    print("🚀 PDF Resume Analyzer - System Test Suite")
    print("=" * 60)
    
    # Check if resume.pdf exists
    if not Path("resume.pdf").exists():
        print("❌ resume.pdf not found. Please ensure the sample resume is in the current directory.")
        return False
    
    # Test cases
    test_cases = [
        {
            "command": "source venv/bin/activate && python3 main.py --help",
            "description": "Help command functionality"
        },
        {
            "command": "source venv/bin/activate && python3 main.py --pdf resume.pdf",
            "description": "Basic PDF analysis without questions"
        },
        {
            "command": "source venv/bin/activate && python3 main.py --pdf resume.pdf --question 'What is this person\\'s name?'",
            "description": "Simple name extraction question"
        },
        {
            "command": "source venv/bin/activate && python3 main.py --pdf resume.pdf --question 'What programming languages does this person know?'",
            "description": "Technical skills question"
        },
        {
            "command": "source venv/bin/activate && python3 main.py --pdf resume.pdf --question 'What is this person\\'s educational background?'",
            "description": "Education background question"
        },
        {
            "command": "source venv/bin/activate && python3 main.py --pdf resume.pdf --question 'What projects has this person worked on?'",
            "description": "Project experience question"
        }
    ]
    
    # Run tests
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        if run_test_command(test_case["command"], test_case["description"]):
            passed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 TEST SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready for use.")
        print("\n📖 Usage Examples:")
        print("  python3 main.py --pdf resume.pdf --interactive")
        print("  python3 main.py --pdf resume.pdf --question 'What are their skills?'")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
