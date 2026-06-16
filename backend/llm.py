from .config import Config


def get_llm():
    """
    Factory function - returns LangChain chat model based on config.
    Add new providers here.
    """
    provider = Config.LLM_PROVIDER.lower()

    providers = {
        "groq": _get_groq_llm,
        "openai": _get_openai_llm,
        "anthropic": _get_anthropic_llm,
        "google": _get_google_llm,
    }

    if provider not in providers:
        raise ValueError(
            f"Unknown provider: {provider}. "
            f"Available: {list(providers.keys())}"
        )

    return providers[provider]()


# --------------- Provider Functions ---------------
# Add new providers as separate functions below

def _get_groq_llm():
    from langchain_groq import ChatGroq
    return ChatGroq(
        model=Config.LLM_MODEL,
        api_key=Config.GROQ_API_KEY,
        temperature=Config.LLM_TEMPERATURE,
    )


def _get_openai_llm():
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model=Config.LLM_MODEL,
        api_key=Config.OPENAI_API_KEY,
        temperature=Config.LLM_TEMPERATURE,
    )


def _get_anthropic_llm():
    from langchain_anthropic import ChatAnthropic
    return ChatAnthropic(
        model=Config.LLM_MODEL,
        api_key=Config.ANTHROPIC_API_KEY,
        temperature=Config.LLM_TEMPERATURE,
    )


def _get_google_llm():
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(
        model=Config.LLM_MODEL,
        google_api_key=Config.GOOGLE_API_KEY,
        temperature=Config.LLM_TEMPERATURE,
    )