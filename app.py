from src.langraphagenticai.main import load_langraphagenticai_ui
if __name__ == "__main__":
    user_input = load_langraphagenticai_ui()

    if not user_input:
        print("Please select an LLM and a Use Case to continue.")
        

    
