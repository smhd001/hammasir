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
                "factor": 0.5,
                "modifier": "log1p",
                "missing": 1,
            },
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
}
