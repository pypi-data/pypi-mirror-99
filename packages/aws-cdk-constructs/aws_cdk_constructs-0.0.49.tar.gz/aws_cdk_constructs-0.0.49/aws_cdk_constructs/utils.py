def normalize_environment_parameter (environment):
    environment_lower = environment.lower()
    
    if environment_lower == "qa":
        return "QA"

    if environment_lower == "production":
        return "Production"

    return "Development"