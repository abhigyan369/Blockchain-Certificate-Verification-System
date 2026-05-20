import hashlib

def generate_data_hash(certificate):
    """
    Generates a deterministic SHA256 hash based on the core certificate data.
    """
    # Create a deterministic string representation of the data
    data_string = f"{certificate.certificate_id}|{certificate.student_name}|{certificate.course_name}|{certificate.issue_date.isoformat()}"
    
    # Generate SHA256 hash
    hash_obj = hashlib.sha256(data_string.encode('utf-8'))
    return hash_obj.hexdigest()

def verify_data_hash(certificate, provided_hash):
    """
    Recalculates the hash and compares it with the provided hash.
    Returns True if they match, False otherwise.
    """
    expected_hash = generate_data_hash(certificate)
    return expected_hash == provided_hash
