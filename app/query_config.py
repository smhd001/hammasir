query_config = {
    "function_score": {
        "user-score": {
            "field_value_factor": {
                "field": "star",
                "modifier": "none",
                "missing": 0,
            }
        },
        "moral": {
            "field_value_factor": {
                "field": "doctor_encounter",
                "modifier": "none",
                "missing": 0,
            }
        },
        "experience": {
            "field_value_factor": {
                "field": "experience",
                "factor": 0.6,
                "modifier": "log1p",
                "missing": 0,
            }
        },
        "popularity": {
            "field_value_factor": {
                # maximum amount of views is about 300k which is about 5
                "field": "number_of_visits",
                "modifier": "log1p",
                "missing": 1,
            },
            "weight": 0.5,
        },
        "amount-of-delay": {
            "gauss": {
                "waiting_time": {
                    "origin": 0,
                    "scale": 1,
                    "offset": 0.5,
                    "decay": 0.5,
                }
            },
            "weight": 5,
        },
        "first-available-appointment": {
            "gauss": {
                "presence_freeturn": {  # TODO filter old ones
                    "origin": "1724617800",  # crawl time
                    "scale": "1d",
                    "offset": "0d",
                    "decay": 0.5,
                },
            },
            "weight": 5,
        },
    },
    "gender_map": {
        "F": ["خانم", "زن", "مونث", "دختر"],
        "M": ["آقا", "مرد", "مذکر", "پسر"],
    },
    "boosts": {
        "expertise": 1.5,
        "problem": 1,
        ("problem", "symptomes"): 0.5,
        ("problem", "about"): 0.1,
        ("expertise", "about"): 0.2,
        ("expertise", "symptomes"): 0.1,
    },
}
