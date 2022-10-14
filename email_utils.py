import re

EMAIL_REGEX = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                          "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                          "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))


def extract_emails(filename):
    """Returns the contents of filename as a string."""
    with open(filename) as f:
        s = f.read().lower()  # Case is lowered to prevent regex mismatches.

    """Returns an iterator of matched emails found in string s."""
    # Removing lines that start with '//' because the regular expression
    # mistakenly matches patterns like 'http://foo@bar.com' as '//foo@bar.com'.
    return (email[0] for email in re.findall(EMAIL_REGEX, s) if not email[0].startswith('//'))
