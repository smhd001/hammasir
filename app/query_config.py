query_config = {
    "function_score": {
        "user-score": {
            "field_value_factor": {
                "field": "star",
                "factor": 5,
                "modifier": "none",
                "missing": 0,
            }
        },
        "moral": {
            "field_value_factor": {
                "field": "doctor-encounter",
                "factor": 5,
                "modifier": "none",
                "missing": 0,
            }
        },
        "experience": {
            "field_value_factor": {
                "field": "experience",
                "factor": 5,
                "modifier": "none",
                "missing": 0,
            }
        },
        "amount-of-delay": {
            "gauss": {
                "waiting-time": {
                    "origin": 0,
                    "scale": 1,
                    "offset": 0.5,
                    "decay": 0.5,
                }
            }
        },
        "first-available-appointment": {
            "gauss": {
                "presence_freeturn": {
                    "origin": "now",
                    "scale": "1d",
                    "offset": "0d",
                    "decay": 0.5,
                }
            }
        },
    },
    "gender_map": {
        "F": ["خانم", "زن", "مونث", "دختر"],
        "M": ["آقا", "مرد", "مذکر", "پسر"],
    },
}
