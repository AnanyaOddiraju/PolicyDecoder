from src.generation.llm import LLM

def test_llm():
    llm = LLM()

    response = llm.generate(
        "Explain what a vector database is in one sentence."
    )

    print("\nLLM response:")
    print(response)

    assert response