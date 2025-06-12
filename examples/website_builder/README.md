# Website builder

This example shows a simple multi-agent workflow exposed via a FastAPI web page.
The user submits a short description of the desired website and a Project Manager
agent coordinates a Developer, Designer and Copywriter to produce the final
code.

Run the server with:

```bash
uvicorn examples.website_builder.main:app --reload
```

Then open `http://localhost:8000` in your browser.
