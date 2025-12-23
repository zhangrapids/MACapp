"""
Medical RAG App - Main Application
Simplified modular structure for easy maintenance
"""
import sys
import os
#from trial_manager import check_trial_and_start_app, TrialManager

# Add current directory to path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from loader import load_all_tests
    from matcher import find_test
    from formatter import format_results, format_abnormal_tests
    from config import RESULTS_FOLDER, DEBUG_MODE
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("\nMake sure all these files are in the same directory:")
    print("  - medical_rag_app.py (this file)")
    print("  - loader.py")
    print("  - matcher.py")
    print("  - formatter.py")
    print("  - parsers.py")
    print("  - normalizer.py")
    print("  - config.py")
    sys.exit(1)

def main():
    """Main application entry point"""
    print("="*60)
    print("MEDICAL TEST QUERY SYSTEM")
    print("="*60)
    
    # Load all test data
    all_tests = load_all_tests(RESULTS_FOLDER, DEBUG_MODE)
    test_names = sorted(all_tests.keys())
    
    print(f"\nLoaded {len(test_names)} unique test types")
    print(f"Total entries: {sum(len(v) for v in all_tests.values())}")
    print("="*60)
    
    if not test_names:
        print("\nNo test data loaded. Exiting.")
        return
    
    print("\nCommands:")
    print("  - Type test/record name (e.g., 'glucose', 'blood pressure', 'immunizations')")
    print("  - 'list tests' - Show all available records")
    print("  - 'abnormal' or 'abnormal tests' - Show tests with abnormal values")
    print("  - 'vital signs' - Show all vital sign measurements")
    print("  - 'procedures' - Show all procedures and imaging")
    print("  - 'clinical notes' - Show doctor's notes and summaries")
    print("  - 'problems' - Show active and resolved problems")
    print("  - 'exit' - Quit")
    print("="*60 + "\n")
    
    # Query loop
    while True:
        query = input("Question: ").strip()
        
        if not query:
            continue
        
        if query.lower() in ['exit', 'quit']:
            print("\nExiting. Stay healthy!")
            break
        
        # List all tests
        if 'list tests' in query.lower():
            print(f"\nAvailable tests ({len(test_names)}):")
            for i, name in enumerate(test_names, 1):
                count = len(all_tests[name])
                print(f"  {i}. {name} ({count} entries)")
            print()
            continue
        
        # Show abnormal tests
        if 'abnormal' in query.lower():
            print("\n--- Abnormal Tests ---")
            print(format_abnormal_tests(all_tests))
            print()
            continue
        
        # Find and display test(s)
        matches = find_test(query, test_names)
        
        if matches:
            if len(matches) == 1:
                # Single match
                test_name = matches[0]
                print(f"\n--- {test_name} ---")
                print(format_results(all_tests[test_name]))
                print()
            else:
                # Multiple matches
                print(f"\n--- Found {len(matches)} matching tests ---\n")
                for test_name in sorted(matches):
                    print(f"=== {test_name} ===")
                    print(format_results(all_tests[test_name]))
                    print()
        else:
            print("\n✗ Test not found. Try 'list tests' to see all available tests.\n")

if __name__ == "__main__":
    main()