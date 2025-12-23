"""
formatter.py - Format test results for display
"""
from datetime import datetime

def format_results(results):
    """Format test results for display"""
    if not results:
        return "No results found."
    
    sorted_results = sorted(
        results,
        key=lambda x: datetime.strptime(x['Date'], "%m/%d/%Y"),
        reverse=True
    )
    
    # Check what type of record this is
    record_type = results[0].get('Type', 'Lab Test')
    
    lines = [f"Total entries: {len(sorted_results)}"]
    lines.append(f"Record type: {record_type}")
    lines.append("")
    lines.append("All Results (newest to oldest):")
    
    for i, r in enumerate(sorted_results, 1):
        if record_type in ['Vital Sign', 'Lab Test']:
            lines.append(
                f"  {i}. {r['Date']}: {r['Value']} {r['Unit']} "
                f"(Ref: {r['Reference Range']}, Status: {r['Status']})"
            )
        elif record_type == 'Immunization':
            lines.append(f"  {i}. {r['Date']}: {r['Value']}")
        elif record_type == 'Medication':
            lines.append(f"  {i}. {r['Date']}: {r['Value']} (Status: {r['Status']})")
        elif record_type == 'Problem':
            lines.append(f"  {i}. {r['Date']}: {r['Value']} (Status: {r['Status']})")
        elif record_type == 'Procedure':
            lines.append(f"  {i}. {r['Date']}: {r['Value']}")
            if r['Status'] and r['Status'] != 'See full report':
                lines.append(f"      Finding: {r['Status']}")
        else:
            lines.append(f"  {i}. {r['Date']}: {r['Value']}")
    
    # Calculate statistics for numeric values
    if record_type in ['Vital Sign', 'Lab Test']:
        try:
            values = [float(r['Value']) for r in sorted_results]
            if len(values) > 1:
                lines.append("")
                lines.append("Statistics:")
                lines.append(f"  Min: {min(values)}")
                lines.append(f"  Max: {max(values)}")
                lines.append(f"  Avg: {sum(values)/len(values):.2f}")
        except:
            pass
    
    return "\n".join(lines)


def format_abnormal_tests(all_tests):
    """Format all tests with abnormal values"""
    abnormal_tests = {}
    
    # Find all tests with abnormal values
    for test_name, results in all_tests.items():
        abnormal_entries = [
            r for r in results 
            if r['Status'] in ['Low', 'High', 'Critical']
        ]
        if abnormal_entries:
            abnormal_tests[test_name] = abnormal_entries
    
    if not abnormal_tests:
        return "No abnormal tests found. All results are within normal range!"
    
    lines = [f"Found {len(abnormal_tests)} tests with abnormal values:\n"]
    
    for test_name in sorted(abnormal_tests.keys()):
        abnormal_entries = abnormal_tests[test_name]
        sorted_entries = sorted(
            abnormal_entries,
            key=lambda x: datetime.strptime(x['Date'], "%m/%d/%Y"),
            reverse=True
        )
        
        lines.append(f"=== {test_name} ===")
        lines.append(f"Abnormal entries: {len(abnormal_entries)}")
        
        for i, r in enumerate(sorted_entries, 1):
            lines.append(
                f"  {i}. {r['Date']}: {r['Value']} {r['Unit']} "
                f"(Ref: {r['Reference Range']}, Status: {r['Status']})"
            )
        lines.append("")
    
    return "\n".join(lines)