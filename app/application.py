from flask import Flask, render_template, request, session, redirect, url_for
from app.components.retriever import create_qa_chain
from app.components.pdf_loader import load_pdf_files, create_text_chunks
from app.components.vector_store import save_vector_store
from app.config.config import DB_FAISS_PATH
from app.common.logger import get_logger
from dotenv import load_dotenv
from markupsafe import Markup
import os

load_dotenv()

logger = get_logger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# nl2br filter
def nl2br(value):
    return Markup(value.replace("\n", "<br>\n"))

app.jinja_env.filters['nl2br'] = nl2br

# ✅ Auto-generate vectorstore if not exists
def initialize_vectorstore():
    if not os.path.exists(DB_FAISS_PATH):
        logger.info("Vectorstore not found — generating from PDFs...")
        try:
            documents = load_pdf_files()
            if documents:
                chunks = create_text_chunks(documents)
                save_vector_store(chunks)
                logger.info("Vectorstore generated successfully!")
            else:
                logger.warning("No PDFs found in data folder!")
        except Exception as e:
            logger.error(f"Failed to generate vectorstore: {str(e)}")
    else:
        logger.info("Vectorstore already exists — skipping generation!")

@app.route("/", methods=["GET", "POST"])
def index():
    if "messages" not in session:
        session["messages"] = []

    if request.method == "POST":
        user_input = request.form.get("prompt")

        if user_input:
            messages = session["messages"]
            messages.append({"role": "user", "content": user_input})
            session["messages"] = messages

            try:
                qa_chain = create_qa_chain()

                if qa_chain is None:
                    raise Exception("QA chain could not be created")

                # ✅ LCEL style - returns plain string directly
                result = qa_chain.invoke(user_input)

                messages.append({"role": "assistant", "content": result})
                session["messages"] = messages

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                return render_template(
                    "index.html",
                    messages=session["messages"],
                    error=error_msg
                )

        return redirect(url_for("index"))

    return render_template(
        "index.html",
        messages=session.get("messages", [])
    )

@app.route("/clear")
def clear():
    session.pop("messages", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    initialize_vectorstore()  # ✅ Auto-generate vectorstore on startup
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)