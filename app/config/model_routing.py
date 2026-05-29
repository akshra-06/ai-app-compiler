
MODEL_ROUTING = {

    "intent_extraction": {

        "primary": {

            "provider": "groq",

            "model":
                "llama3-8b-8192"
        },

        "fallback": {

            "provider":
                "openrouter",

            "model":
                "deepseek/deepseek-chat"
        },

        "max_cost":
            0.001
    },

    "schema_generation": {

        "primary": {

            "provider":
                "deepseek",

            "model":
                "deepseek-chat"
        },

        "fallback": {

            "provider":
                "openrouter",

            "model":
                "gpt-4o-mini"
        },

        "max_cost":
            0.01
    },

    "appspec_generation": {

        "primary": {

            "provider":
                "openai",

            "model":
                "gpt-4o-mini"
        },

        "fallback": {

            "provider":
                "openrouter",

            "model":
                "claude-3-haiku"
        },

        "max_cost":
            0.02
    },

    "repair": {

        "primary": {

            "provider":
                "openrouter",

            "model":
                "deepseek/deepseek-chat"
        },

        "fallback": {

            "provider":
                "openrouter",

            "model":
                "gpt-4o-mini"
        },

        "max_cost":
            0.005
    }
}

