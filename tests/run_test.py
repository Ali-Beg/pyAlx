# tests/run_tests.py
import pytest
import os
import sys

def main():
    # Add project root to path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    
    # Run tests with coverage
    pytest.main([
        '--verbose',
        '--cov=src',
        '--cov-report=term-missing',
        'tests/'
    ])

if __name__ == '__main__':
    main()