import re

def load_termination_rules():
    """
    Load a set of predefined termination-related rules.
    
    Each rule is a dictionary with:
    - 'pattern': A regex string to match
    - 'description': A human-readable explanation of what the rule captures
    """
    return [
        {
            "pattern": r"(14|fourteen)\s+days\s+notice",
            "description": "Requires 14 days notice for termination"
        },
        {
            "pattern": r"(terminate|end)\s+the\s+lease",
            "description": "Mentions termination of lease"
        },
        {
            "pattern": r"early\s+termination",
            "description": "Clause about early lease termination"
        },
        {
            "pattern": r"breach\s+of\s+agreement",
            "description": "Mentions breach as a cause for termination"
        }
    ]


def apply_rules(text, rules):
    """
    Apply termination rules to a given text and return matches.

    Args:
        text (str): The contract text to scan.
        rules (list): List of rules to apply (from `load_termination_rules`).

    Returns:
        list: A list of dictionaries, each representing a rule match with:
            - 'match': the actual matched text
            - 'description': the description of the rule matched
            - 'start': start index of match in text
            - 'end': end index of match in text
    """
    results = []

    for rule in rules:
        pattern = rule["pattern"]
        description = rule["description"]

        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            results.append({
                "match": match.group(0),
                "description": description,
                "start": match.start(),
                "end": match.end()
            })

    return results